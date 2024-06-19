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
  <summary>目次</summary>
  <ol>
    <li>
      <a href="#概要">概要</a>
    </li>
    <li>
      <a href="#セットアップ">セットアップ</a>
      <ul>
        <li><a href="#環境条件">環境条件</a></li>
        <li><a href="#インストール方法">インストール方法</a></li>
      </ul>
    </li>
    <li><a href="#実行方法">実行方法</a></li>
    <!-- <li><a href="#マイルストーン">マイルストーン</a></li> -->
    <!-- <li><a href="#変更履歴">変更履歴</a></li> -->
    <!-- <li><a href="#contributing">Contributing</a></li> -->
    <!-- <li><a href="#license">License</a></li> -->
    <li><a href="#参考文献">参考文献</a></li>
  </ol>
</details>



<!-- レポジトリの概要 -->
## 概要

<!-- [![Product Name Screen Shot][product-screenshot]](https://example.com) -->

CPUでもサクサク動く顔検出パッケージです．

<p align="right">(<a href="#readme-top">上に戻る</a>)</p>



<!-- セットアップ -->
## セットアップ
本レポジトリのセットアップ方法について説明します．

### 環境条件
| System  | Version |
| ------------- | ------------- |
| Ubuntu | 20.04 (Focal Fossa) |
| ROS | Noetic Ninjemys |
| Python | 3.0~ |

### インストール方法

1. ROSの`src`フォルダに移動します．
   ```sh
   $ cd　~/catkin_ws/src/
   ```
2. 本レポジトリをcloneします．
   ```sh
   $ git clone https://github.com/TeamSOBITS/Ultra-Light-Fast-Generic-Face-Detector-1MB.git
   ```
3. レポジトリの中へ移動します．
   ```sh
   $ cd Ultra-Light-Fast-Generic-Face-Detector-1MB
   ```
4. 依存パッケージをインストールします．
    ```sh
    $ bash install.sh
    ```
5. パッケージをコンパイルします．
   ```sh
   $ cd ~/catkin_ws/
   $ catkin_make
   ```

<p align="right">(<a href="#readme-top">上に戻る</a>)</p>



<!-- 実行・操作方法 -->
## 実行方法
実行方法は，tfを使用しないNormal Modeとtfを使用するTF Modeの２種類あります．
Normal ModeはPCのカメラでも使用することが出来ます．TF Modeは点群の取れるカメラ（例：Azure kinect）を接続して使用してください．


### Normal Mode（tfを使用しない場合）
1. カメラを起動する. 
2. face_detect.launchをたてる．
    ```sh
    $ roslaunch ulfg_face_detector face_detect.launch
    ```
    これで顔検出ができるようになります．これでエラーが発生する場合はface_detect.launchの13行目
    ```sh
    <param name="ulfg_image_topic_name" type="str" value="/camera/rgb/image_raw"/> 
    ```
    このvalueを変更してもう一度試しましょう．\

3. 検出した顔を識別したいとき
    face_detect.launchの11行目
    ```sh
    <param name="unique_class_flag" type="bool" value="false"/> 
    ```
    このvalueを"true"にすると検出した顔をナンバリングします．


### TF Mode（tfを使用する場合）
ここではRGB-Dカメラが必要になります．
1. RGB-Dカメラを起動する．
2. face_detect_with_tf.launchをたてる．
    ```sh
    $ roslaunch ulfg_face_detector face_detect_with_tf.launch
    ```
    違うカメラを使用する場合はface_detect_with_tf.launchの5,35,37行目
    ```sh
    $ <arg name="img_topic_name"           default="/camera/rgb/image_raw"/>

    $ <arg name="base_frame_name" value="camera_depth_frame"/> 

    $ <arg name="cloud_topic_name" value="/camera/depth_registered/points"/>
    ```
    このdefaltとvalueを適切なものに変更しましょう．


<p align="right">(<a href="#readme-top">上に戻る</a>)</p>



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
## 参考文献

<!-- * [ROS Navigationスタックソフトウェア設計仕様](https://robo-marc.github.io/navigation_documents/)
* [explore_lite](http://wiki.ros.org/explore_lite) -->

<p align="right">(<a href="#readme-top">上に戻る</a>)</p>

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



