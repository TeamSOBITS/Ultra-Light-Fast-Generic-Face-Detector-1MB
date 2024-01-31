#!/usr/bin/env python
#coding: utf-8      #エンコード宣言
import rospy
import rospkg
import sys
import os
import subprocess
import cv2
from sensor_msgs.msg import Image       #imegeの画像を読み込む
from cv_bridge import CvBridge          #OpenCVの画像メッセージとPythonの画像メッセージの変換
from skybiometry_ros.msg import FaceProperties
from skybiometry_ros.srv import *

cv_img = []

def sky_client(images):
	rospy.wait_for_service('/get_face_properties')
	try:
		print "Waiting for Service....."
		send_sky = rospy.ServiceProxy('/get_face_properties', GetFaceProperties)
		#print "Sending Message....."
		sky_ans = send_sky(images)
		#rospy.sleep(5)
		#print ".....Responce Returned"
		#print ans
		return sky_ans
	except rospy.ServiceException, e:
		print "Service call failed: %s"%e
		#rospy.logerr("Service call failed.")
		return -1

def run_ulfg_face_detector(path):
        rospack = rospkg.RosPack()
        cmd = rospack.get_path('ulfg_face_detector')
        os.chdir(cmd)
        #subprocess.call(cmd.split())
        cmd = "python3 detect_imgs_ros.py"
        subprocess.call(cmd.split())
        print("---ulfg_face_detector finished---")
        #save_path = rospack.get_path('') + "/voice/speech_word.mp3"

def img_cb(msg):
    global cv_img
    #rospy.loginfo("Subscribed Image Topic")
    cv_img = CvBridge().imgmsg_to_cv2(msg,"bgr8")       #msgをOpenCVの画像メッセージに変換
    cv2.imshow("window",cv_img)     #「window」というウィンドウで画像を出力
    cv2.waitKey(1)      #1ミリ秒入力を待つ
    rate = rospy.Rate(10)
    rate.sleep()

if __name__ == '__main__':
    rospy.init_node('person_recognition')
    topic_name = "/usb_cam/image_raw"
    sub1 = rospy.Subscriber(topic_name,Image,img_cb)       #rospy.Subscriber(トピック名,引数,関数)
    res = False
    #rospack = rospkg.RosPack()
    #save_path = rospack.get_path('ulfg_face_detector') + "/imgs"
    while not res:
        rospy.sleep(3)
        #cv2.imwrite("face.jpg", cv_img)
        rospack = rospkg.RosPack()
        save_path = rospack.get_path('ulfg_face_detector') + "/imgs"
        res = cv2.imwrite(save_path + "/face.jpg", cv_img)

    run_ulfg_face_detector(save_path)

    read_path = rospack.get_path('ulfg_face_detector') + "/detect_imgs_results"
    images = []
    for i in range(0,100):
        img = Image()
        img = cv2.imread(read_path + "/face_" + str(i) + ".jpg")
        if img is None:
            rospy.loginfo("EOF!!")
            break
        else:
            ros_img = CvBridge().cv2_to_imgmsg(img, "rgb8")
            images.append(ros_img)
    #print images
    rospy.loginfo("images_num = %d", len(images))
    print sky_client(images)


    #save_path = rospack.get_path('') + "/voice/speech_word.mp3"
