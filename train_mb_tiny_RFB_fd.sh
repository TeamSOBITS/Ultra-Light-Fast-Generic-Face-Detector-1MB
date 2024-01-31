#!/usr/bin/env bash
model_root_path="./models/train_mb_tiny_RFB_fd"
log_dir="$model_root_path/logs"
log="$log_dir/log"
mkdir -p "$log_dir"

python3 -u src/train.py \
  --datasets \
  ./data/wider_face_add_lm_10_10 \
  --validation_dataset \
  ./data/wider_face_add_lm_10_10 \
  --net \
  mb_tiny_RFB_fd \
  --num_epochs \
  200 \
  --milestones \
  "95,150" \
  --lr \
  1e-2 \
  --batch_size \
  12 \
  --input_size \
  1280 \
  --checkpoint_folder \
  ${model_root_path} \
  --num_workers \
  1 \
  --log_dir \
  ${log_dir} \
  --cuda_index \
  0 \
  2>&1 | tee "$log"
