#!/bin/zsh
/opt/anaconda3/bin/python "My_Video_Recorder.py" \
  --camera 2 \
  --name macbook_record \
  --format avi \
  --fourcc XVID \
  --negative \
  --flip \
  --Grayscale \
  --Blur \
  --contbri
