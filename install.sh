#!/bin/bash

read -p $'pytorch のCPU版をインストールします。
        \e[33m＊既にpytorchをインストールしている,
        　あるいはGPU版を入れたい人は実行しないで下さい。\e[0m
実行しますか? (y/N): ' yn
case "$yn" in
  [yY]*) sudo apt install python3-pip
         python3 -m pip install -U pip
         python3 -m pip install torch==1.9.0+cpu torchvision==0.10.0+cpu torchaudio==0.9.0 -f https://download.pytorch.org/whl/torch_stable.html;;
  *) echo "終了します。
pytorchのGPU版を入れたい方はこちら
https://pytorch.org/";;
esac

cd ~/catkin_ws/src/
git clone https://github.com/TeamSOBITS/bbox_to_tf.git