#include <iostream>
#include <cstdlib>
#include <fstream>
#include <time.h>
#include <sstream>
#include <stdlib.h>
#include <unistd.h>
#include <limits>
#include <ros/ros.h>
#include <ros/package.h>

//for image input
#include <cv_bridge/cv_bridge.h>
#include <std_msgs/Bool.h>
#include <ros/package.h>
#include <geometry_msgs/PointStamped.h>
#include <std_msgs/Header.h>
#include <geometry_msgs/Point.h>
#include <sensor_msgs/PointCloud2.h>
#include <tf/transform_broadcaster.h>

// PCL specific includes
#include <pcl_ros/transforms.h>
#include <pcl_conversions/pcl_conversions.h>
#include <pcl/point_cloud.h>
#include <pcl/point_types.h>
#include <pcl/ModelCoefficients.h>

#include <ulfg_face_detector/BoundingBox.h>
#include <ulfg_face_detector/BoundingBoxesStamp.h>
#include <sobit_common_msg/RunCtrl.h>

#include <message_filters/subscriber.h>
#include <message_filters/sync_policies/approximate_time.h>
#include <message_filters/time_synchronizer.h>

typedef message_filters::sync_policies::ApproximateTime<ulfg_face_detector::BoundingBoxesStamp, sensor_msgs::PointCloud2>
    BBoxesCloudSyncPolicy;


class tf_broadcaster
{
	ros::NodeHandle nh;
	ros::ServiceServer srv_ctrl;

	tf::TransformBroadcaster br;

	std::string cloud_topic_name;
	std::string target_frame;
	bool execute_flag;
	bool get_cloud_flag;

	int cloud_width;

	std::unique_ptr<message_filters::Subscriber<ulfg_face_detector::BoundingBoxesStamp>> sub_bboxes;
  	std::unique_ptr<message_filters::Subscriber<sensor_msgs::PointCloud2>>        sub_cloud;
  	std::shared_ptr<message_filters::Synchronizer<BBoxesCloudSyncPolicy>>         sync;

private :
	/* tf */
	tf::TransformListener tf_listener_;

public:
	tf_broadcaster(){
		
		this->get_cloud_flag = false;
		ros::param::get("ulfg_execute_default", execute_flag);
		ros::param::get("ulfg_cloud_topic_name", cloud_topic_name);
		ros::param::get("ulfg_target_frame_name", target_frame);
		ros::param::get("ulfg_camera_width_size", cloud_width);
		srv_ctrl = nh.advertiseService ("/ulfg_face_detect/detect_ctrl", &tf_broadcaster::detect_ctrl_server, this);

		sub_bboxes.reset(new message_filters::Subscriber<ulfg_face_detector::BoundingBoxesStamp>(nh, "faces_rect_stamp", 5));
		sub_cloud.reset(new message_filters::Subscriber<sensor_msgs::PointCloud2>(nh, cloud_topic_name, 5));
		sync.reset(new message_filters::Synchronizer<BBoxesCloudSyncPolicy>(
			BBoxesCloudSyncPolicy(200), *sub_bboxes, *sub_cloud));
		sync->registerCallback(boost::bind(&tf_broadcaster::callback_BBoxCloud, this, _1, _2));

		ROS_INFO("tf_broadcaster initialize ok");
	}//tf_broadcaster

	~tf_broadcaster(){}


	bool detect_ctrl_server(sobit_common_msg::RunCtrl::Request &req,
							sobit_common_msg::RunCtrl::Response &res){
		execute_flag = req.request;
		if(execute_flag == true){
			ROS_INFO("ulfg_tf_broadcaster -> Start");
		}
		else{
			ROS_INFO("ulfg_tf_broadcaster -> Stopped");
		}
		res.response = execute_flag;
		return true;
	}//detect_ctrl_server


	void callback_BBoxCloud(const ulfg_face_detector::BoundingBoxesStampConstPtr &bbox_msg,
							const sensor_msgs::PointCloud2ConstPtr &input){
		
		pcl::PointCloud<pcl::PointXYZ> cloud_local;
		pcl::PointCloud<pcl::PointXYZ>::Ptr output_cloud (new pcl::PointCloud<pcl::PointXYZ>);

		if(execute_flag == false){	return;	}

		pcl::fromROSMsg(*input, cloud_local);

		if(cloud_local.points.size() == 0){
			ROS_ERROR("NO point cloud");
			this->get_cloud_flag = false;
			return;
		}
		this->get_cloud_flag = true;
		
		if (target_frame.empty() ) {
                ROS_ERROR("Please set the target frame.");
                return;
            }
            try {
                // transform frame :
                tf_listener_.waitForTransform(target_frame, cloud_local.header.frame_id, ros::Time(0), ros::Duration(1.0));
                pcl_ros::transformPointCloud(target_frame, ros::Time(0), cloud_local, cloud_local.header.frame_id, *output_cloud, tf_listener_);
                output_cloud->header.frame_id = target_frame;
            } catch ( const tf::TransformException& ex) {
                ROS_ERROR("%s", ex.what());
                return;
            }

		if(this->get_cloud_flag == false){
			ROS_ERROR("tf_broadcaster -> waiting cloud");
			return;
		}

        for ( const auto& face : bbox_msg->boundingBoxes ) {
			int face_x = face.x + (face.width * 0.5);
			int face_y = face.y + (face.height * 0.5);

			pcl::PointXYZ face_pt;
			face_pt.x = output_cloud->points[cloud_width * face_y + face_x].x;
			face_pt.y = output_cloud->points[cloud_width * face_y + face_x].y;
			face_pt.z = output_cloud->points[cloud_width * face_y + face_x].z;

			if(std::isnan( face_pt.x ) || std::isnan( face_pt.y ) || std::isnan( face_pt.z )){
				continue;
			}

			br.sendTransform(tf::StampedTransform(tf::Transform(tf::Quaternion(0, 0, 0, 1), tf::Vector3(face_pt.x, face_pt.y, face_pt.z)),
			ros::Time::now(), target_frame, face.Class));
		}//for
	}

};



int main(int argc, char** argv)
{
	ros::init(argc, argv, "tf_broadcaster");
	tf_broadcaster tf_class;
	ros::spin();
	return 0;
}
