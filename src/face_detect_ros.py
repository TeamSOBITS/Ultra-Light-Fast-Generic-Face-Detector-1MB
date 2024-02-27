#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import rospy
from std_msgs.msg import UInt8, Bool
from sensor_msgs.msg import Image
# from ulfg_face_detector.msg import BoundingBox, BoundingBoxes, BoundingBoxesStamp
from sobits_msgs.msg import BoundingBox, BoundingBoxes

ulfg_path = rospy.get_param("ulfg_path")
import sys
sys.path.append(ulfg_path)  # 親ディレクトリのファイルをインポートするための設定
import cv2
from cv_bridge import CvBridge

from vision.ssd.config.fd_config import define_img_size
input_img_size = rospy.get_param("ulfg_camera_width_size")
test_device = rospy.get_param("test_device")
if input_img_size > 640 and test_device == "cpu":
    input_img_size = 640
define_img_size(input_img_size)  # must put define_img_size() before 'import create_mb_tiny_fd, create_mb_tiny_fd_predictor'
from vision.ssd.mb_tiny_fd import create_mb_tiny_fd, create_mb_tiny_fd_predictor
from vision.ssd.mb_tiny_RFB_fd import create_Mb_Tiny_RFB_fd, create_Mb_Tiny_RFB_fd_predictor
from vision.utils.misc import Timer

class UlfgFaceDetector():
    def __init__(self):
        # Bool
        self.img_show_flag = rospy.get_param("ulfg_img_show_flag")
        self.execute_flag = rospy.get_param("ulfg_execute_default")
        self.pub_result_flag = rospy.get_param("ulfg_pub_result_image")
        self.needs_time_stamp = rospy.get_param("needs_time_stamp")
        self.unique_class_flag = rospy.get_param("unique_class_flag")
        
        # str
        self.sub_img_topic_name = rospy.get_param("ulfg_image_topic_name")
        self.net_type = rospy.get_param("net_type")
        self.label_path = rospy.get_param("ulfg_label_file_path")
        self.class_names = [name.strip() for name in open(self.label_path).readlines()]

        # int and double
        self.in_scale_factor = rospy.get_param("ulfg_inScaleFactor")
        self.confidence_threshold = rospy.get_param("ulfg_confidenceThreshold")
        self.input_img_size = input_img_size
        self.candidate_size = rospy.get_param("ulfg_candidate_size")
        self.class_num = len(self.class_names)
        self.sum = 0
        self.counter = 0

        # pub and sub
        self.pub_faces_num = rospy.Publisher("faces_num", UInt8, queue_size=10)
        self.pub_faces_rect = rospy.Publisher("faces_rect", BoundingBoxes, queue_size=10)
        self.pub_result_img = rospy.Publisher("detect_result", Image, queue_size=10)
        self.sub_img = rospy.Subscriber(self.sub_img_topic_name, Image, self.img_cb)
        self.sub_ctrl = rospy.Subscriber("detect_ctrl", Bool, self.ctrl_cb)
        
        self.timer = Timer()
        self.read_files()

    def read_files(self):
        if self.net_type == 'mb_tiny_fd':
            self.model_path = "{}/models/pretrained/Mb_Tiny_FD_train_input_{}.pth".format(ulfg_path, self.input_img_size)
            self.net = create_mb_tiny_fd(len(self.class_names), is_test=True, device=test_device)
            self.predictor = create_mb_tiny_fd_predictor(self.net, candidate_size=self.candidate_size, device=test_device)
            # print("read_if")
        elif self.net_type == 'mb_tiny_RFB_fd':
            self.model_path = "{}/models/pretrained/Mb_Tiny_RFB_FD_train_input_{}.pth".format(ulfg_path, self.input_img_size)
            self.net = create_Mb_Tiny_RFB_fd(len(self.class_names), is_test=True, device=test_device)
            self.predictor = create_Mb_Tiny_RFB_fd_predictor(self.net, candidate_size=self.candidate_size, device=test_device)
            print("read_elif")
        else:
            print("The net type is wrong!")
            return -1
        self.net.load(self.model_path)
        return 0

    def ctrl_cb(self, msg):
        self.execute_flag = msg.data
        if self.execute_flag:
            rospy.loginfo("ULFG_Face_Detection -> Start")
            print("ctrl_if")
        else:
            rospy.loginfo("ULFG_Face_Detection -> Stopped")
            print("ctrl_elif")
            try:
                cv2.destroyAllWindows()
            except Exception as err:
                rospy.logerr(err)

    def img_cb(self, msg):
        if not self.execute_flag:   return

        orig_image = image = CvBridge().imgmsg_to_cv2(msg, "bgr8")
        if orig_image is None:
            rospy.logerr("ULFG_Face_Detection -> input_image error")
            return 0

        image = cv2.cvtColor(orig_image, cv2.COLOR_BGR2RGB)
        face_bbox_array = BoundingBoxes()
        self.timer.start()
        # image = cv2.resize(image, (640, 480))
        boxes, labels, probs = self.predictor.predict(image, self.candidate_size / 2, self.confidence_threshold)
        interval = self.timer.end()
        # print('Time: {:.6f}s, Detect faces: {:d}.'.format(interval, labels.size(0)))
        for i in range(boxes.size(0)):
            box = boxes[i, :]

            face_bbox = BoundingBox()
            face_bbox.xmin = int(box[0])
            face_bbox.ymin = int(box[1])
            face_bbox.xmax = int(box[2])
            face_bbox.ymax = int(box[3])
            face_bbox.probability = probs[i]
            if self.unique_class_flag:
                face_bbox.Class = "face_{}".format(i)
            else:
                face_bbox.Class = "face"

            label = f"{face_bbox.Class} {probs[i]:.2f}"
            cv2.rectangle(orig_image, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), (0, 255, 0), 4)

            cv2.putText(orig_image, label,
                        (int(box[0]), int(box[1]) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,  # font scale
                        (0, 0, 255),
                        2)  # line type
        orig_image = cv2.resize(orig_image, None, None, fx=0.8, fy=0.8)
        self.sum += boxes.size(0)

        if labels.size(0) > 0:
            faces_num = UInt8()
            faces_num.data = labels.size(0)
            self.pub_faces_num.publish(faces_num)
            
        if self.pub_result_flag:
            result_img_msg = CvBridge().cv2_to_imgmsg(orig_image, "bgr8")
            result_img_msg.header.seq = self.counter
            result_img_msg.header.stamp = rospy.Time.now()
            self.pub_result_img.publish(result_img_msg)
            self.counter+=1


        if self.img_show_flag:
            cv2.imshow('ULFG_Face_Detection Result', orig_image)
            cv2.waitKey(1)



if __name__ == '__main__':
    rospy.init_node('ulfg_face_detector')
    ulfg_face_detector = UlfgFaceDetector()
    try:
        rospy.spin()
    finally:
        cv2.destroyAllWindows()    
