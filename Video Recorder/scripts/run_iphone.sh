#!/bin/zsh
/opt/anaconda3/bin/python "Video Recorder/My_Video_Recorder.py" \
  --camera 1 \
  --name iphone_record \
  --format avi \
  --fourcc XVID \
  --negative \
  --flip \
  --Grayscale \
  --Blur \
  --contbri
