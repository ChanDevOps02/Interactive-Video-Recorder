import os
import cv2 as cv
import argparse

def VideoOpen(target_param, target_name, target_format, fourcc, fps, img):
    target_file = 'result/'+target_name + '.'+target_format
    target_fps = fps
    target_fourcc = fourcc
    h,w,*_ = img.shape
    is_color = (img.ndim > 2) and (img.shape[2] > 1)
    
    target_param.open(target_file, cv.VideoWriter_fourcc(*target_fourcc), target_fps, (w,h), is_color)

parser = argparse.ArgumentParser()
parser.add_argument("--camera", type = int, required=True)
parser.add_argument("--name", type=str, required=True)
parser.add_argument("--format", type=str, default='avi')
parser.add_argument("--fourcc", type=str, default='XVID')
parser.add_argument("--negative", action="store_true")
parser.add_argument("--flip", action="store_true")
parser.add_argument("--Grayscale", action="store_true")
parser.add_argument("--Blur", action="store_true")
parser.add_argument("--contbri", action="store_true")

args = parser.parse_args()

os.makedirs("result", exist_ok=True)

#1 : Iphone 16 pro max
#2 : Macbook Pro
video = cv.VideoCapture(args.camera, cv.CAP_AVFOUNDATION)
if not video.isOpened():
    print("Video open failed")
    raise SystemExit
else:
    target = cv.VideoWriter()
    record = False
    negative = False
    flip = False
    Grayscale = False
    Blur = False
    contbri = False
    contrast = 1.0
    contrast_step = 0.1
    brightness = 0
    brightness_step = 5

    while True:
        valid, img = video.read()
        if not valid:
            print("Frame read failed")
            break
        processed = img.copy()
        if negative == True:
            processed = 255 - processed

        if flip == True:
            processed = processed[::-1, :, :]
        
        if contbri == True:
            processed = contrast * processed + brightness
            processed[processed < 0] = 0
            processed[processed > 255] = 255
            processed = processed.astype("uint8")
        
        if Grayscale == True:
            gray = cv.cvtColor(processed, cv.COLOR_BGR2GRAY)
            processed = cv.cvtColor(gray, cv.COLOR_GRAY2BGR)

        if Blur == True:
            processed = cv.GaussianBlur(processed, (21,21), 0)
        
        display = processed.copy()
        if record:
            cv.circle(display, (30,30), 10, (0,0,255), -1)
        if contbri:
            info = f"contrast: {contrast:.1f} brightness: {brightness}"
            cv.putText(display, info, (50, 35), cv.FONT_HERSHEY_DUPLEX, 0.7, (0, 0, 0), thickness=2)
            cv.putText(display, info, (50, 35), cv.FONT_HERSHEY_DUPLEX, 0.7, (255, 255, 255), thickness=1)
        
        cv.imshow("MyCam", display)
      
        fps = video.get(cv.CAP_PROP_FPS)

        if record and target.isOpened():
            target.write(processed)
        key = cv.waitKey(1)

        if key == 27:
            print("Program terminated")
            break
        elif key == ord(' '):
            if not record:
                record = True
                if not target.isOpened():
                    VideoOpen(target, args.name, args.format, args.fourcc, fps, processed)
                print("Recording Started")
            else:
                record = False
                if target.isOpened():
                    target.release()
                print("Recording stopped")
        elif (args.contbri == True) and (key == ord('c')):
            contbri = not contbri
        elif (args.flip == True) and (key == ord('f')):
            flip = not flip
        elif (args.negative == True) and (key== ord('n')):
            negative = not negative
        elif (args.Grayscale == True) and (key == ord('g')):
            Grayscale = not Grayscale
        elif (args.Blur == True) and (key == ord('b')):
            Blur = not Blur
        elif (args.contbri == True) and (key == ord('+') or key == ord('=')):
            contrast += contrast_step
        elif (args.contbri == True) and (key == ord('-') or key == ord('_')):
            contrast = max(0.1, contrast - contrast_step)
        elif (args.contbri == True) and (key == ord('>') or key == ord('.')):
            brightness += brightness_step
        elif (args.contbri == True) and (key == ord('<') or key == ord(',')):
            brightness -= brightness_step

    video.release()
    if target.isOpened():
        target.release()
    cv.destroyAllWindows()
        
