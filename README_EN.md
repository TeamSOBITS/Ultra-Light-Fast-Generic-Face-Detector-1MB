<a name="readme-top"></a>

[JP](README.md) | [EN](README_EN.md) | [FORK](README_FORK.md)

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![License][license-shield]][license-url]

# light_face_detector

<!-- 目次 -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#Introduction">Introduction</a>
    </li>
    <li>
      <a href="#Setup">Setup</a>
      <ul>
        <li><a href="#Prerequisites">Prerequisites</a></li>
        <li><a href="#Installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#Launch and Usage">Launch and Usage</a></li>
    <!-- <li><a href="#マイルストーン">マイルストーン</a></li> -->
    <!-- <li><a href="#変更履歴">変更履歴</a></li> -->
    <!-- <li><a href="#contributing">Contributing</a></li> -->
    <!-- <li><a href="#license">License</a></li> -->
    <li><a href="#References">References</a></li>
  </ol>
</details>



<!-- レポジトリの概要 -->
## Introduction

<!-- [![Product Name Screen Shot][product-screenshot]](https://example.com) -->

This is a face detection package that runs smoothly on CPU.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- セットアップ -->
## Setup
Here, we will explain the setup process for this repository.

### Prerequisites
| System  | Version |
| ------------- | ------------- |
| Ubuntu | 20.04 (Focal Fossa) |
| ROS | Noetic Ninjemys |
| Python | 3.0~ |

### Installation

1. Move to the 'src' folder.
   ```sh
   $ cd　~/catkin_ws/src/
   ```
2. Clone this repository.
   ```sh
   $ git clone https://github.com/TeamSOBITS/Ultra-Light-Fast-Generic-Face-Detector-1MB.git
   ```
3. Navigate tp the repository.
   ```sh
   $ cd Ultra-Light-Fast-Generic-Face-Detector-1MB
   ```
4. Install dependencies.
    ```sh
    $ bash install.sh
    ```
5. Compile the package.
   ```sh
   $ cd ~/catkin_ws/
   $ catkin_make
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- 実行・操作方法 -->
## Launch and Usage
There are two modes of execution: Normal Mode, which does not use tf, and TF Mode, which uses tf.
Normal Mode can be also used with PC cameras.TF Mode should be used by connecting a camera (e.g. Azure kinect) that can take point clouds.


### Normal Mode（tf not used）
Here we will show you how to use the camera built into the PC.
1. Run the camera.
2. Run face_detect.launch．
    ```sh
    $ roslaunch ulfg_face_detector face_detect.launch
    ```
    This will enable face detection.If this causes an error, line 13 of face_detect.launch
    ```sh
    <param name="ulfg_image_topic_name" type="str" value="/camera/rgb/image_raw"/> 
    ```
    Change this value and try again.\

3. When you want to identify the detected face
    Line 11 of face_detect.launch
    ```sh
    <param name="unique_class_flag" type="bool" value="false"/> 
    ```
    Changing this value to "true" will number the detected faces.


### TF Mode（tf use）
Here we show you how to use RGB-D camera.
1. Start RGB-D camera.
2. Run face_detect_with_tf.launch.
    ```sh
    $ roslaunch ulfg_face_detector face_detect_with_tf.launch
    ```
    If a different camera is used, line 5,35,37 of face_detect_with_tf.launch
    ```sh
    $ <arg name="img_topic_name"           default="/camera/rgb/image_raw"/>

    $ <arg name="base_frame_name" value="camera_depth_frame"/> 

    $ <arg name="cloud_topic_name" value="/camera/depth_registered/points"/>
    ```
    Change this default and value to something appropriate.


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- マイルストーン -->
<!-- ## マイルストーン

- [x] 目標 1
- [ ] 目標 2
- [ ] 目標 3
    - [ ] サブ目標

現時点のバッグや新規機能の依頼を確認するために[Issueページ](https://github.com/github_username/repo_name/issues) をご覧ください．

<p align="right">(<a href="#readme-top">上に</a>)</p> -->



<!-- 変更履歴 -->
<!-- ## 変更履歴

- 2.0: 代表的なタイトル
  - 詳細 1
  - 詳細 2
  - 詳細 3
- 1.1: 代表的なタイトル
  - 詳細 1
  - 詳細 2
  - 詳細 3
- 1.0: 代表的なタイトル
  - 詳細 1
  - 詳細 2
  - 詳細 3 -->

<!-- CONTRIBUTING -->
<!-- ## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">上に戻る</a>)</p> -->



<!-- LICENSE -->
<!-- ## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">上に戻る</a>)</p> -->



<!-- 参考文献 -->
## References

<!-- * [ROS Navigationスタックソフトウェア設計仕様](https://robo-marc.github.io/navigation_documents/)
* [explore_lite](http://wiki.ros.org/explore_lite) -->

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/TeamSOBITS/Ultra-Light-Fast-Generic-Face-Detector-1MB.svg?style=for-the-badge
[contributors-url]: https://github.com/TeamSOBITS/Ultra-Light-Fast-Generic-Face-Detector-1MB/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/TeamSOBITS/Ultra-Light-Fast-Generic-Face-Detector-1MB.svg?style=for-the-badge
[forks-url]: https://github.com/TeamSOBITS/Ultra-Light-Fast-Generic-Face-Detector-1MB/network/members
[stars-shield]: https://img.shields.io/github/stars/TeamSOBITS/Ultra-Light-Fast-Generic-Face-Detector-1MB.svg?style=for-the-badge
[stars-url]: https://github.com/TeamSOBITS/Ultra-Light-Fast-Generic-Face-Detector-1MB/stargazers
[issues-shield]: https://img.shields.io/github/issues/TeamSOBITS/Ultra-Light-Fast-Generic-Face-Detector-1MB.svg?style=for-the-badge
[issues-url]: https://github.com/TeamSOBITS/Ultra-Light-Fast-Generic-Face-Detector-1MB/issues
[license-shield]: https://img.shields.io/github/license/TeamSOBITS/Ultra-Light-Fast-Generic-Face-Detector-1MB.svg?style=for-the-badge
[license-url]: https://github.com/TeamSOBITS/Ultra-Light-Fast-Generic-Face-Detector-1MB/blob/master/LICENSE.txt




