cmake_minimum_required(VERSION 3.10.2)
project(ulfg_face_detector)

add_compile_options(-std=c++14 -O3 -g -Wall)

find_package(OpenCV REQUIRED)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  sensor_msgs
  geometry_msgs
  cv_bridge
  pcl_conversions
  pcl_ros
  tf
  message_generation
  message_filters
)

# Generate added messages and services with any dependencies listed here
 generate_messages(
   DEPENDENCIES
   geometry_msgs
   sensor_msgs
   std_msgs
 )

catkin_package()

include_directories(
  include
  SYSTEM
  ${OpenCV_INCLUDE_DIRS}
  ${PCL_INCLUDE_DIRS}
  ${catkin_INCLUDE_DIRS}
)


#add_executable(${PROJECT_NAME}_node src/ulfg_face_detector_node.cpp)