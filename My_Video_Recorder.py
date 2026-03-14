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
    last_key_text = "None"

    def draw_text_with_outline(image, text, org, scale=0.7, color=(255, 255, 255)):
        cv.putText(image, text, org, cv.FONT_HERSHEY_DUPLEX, scale, (0, 0, 0), thickness=2)
        cv.putText(image, text, org, cv.FONT_HERSHEY_DUPLEX, scale, color, thickness=1)

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
        
        output_frame = processed.copy()
        display = output_frame.copy()
        if record:
            cv.circle(display, (30,30), 10, (0,0,255), -1)
            cv.circle(output_frame, (30,30), 10, (0,0,255), -1)
        if contbri:
            info = f"contrast: {contrast:.1f} brightness: {brightness}"
            draw_text_with_outline(display, info, (50, 35))
            draw_text_with_outline(output_frame, info, (50, 35))
        key_info = f"Key: {last_key_text}"
        text_size, _ = cv.getTextSize(key_info, cv.FONT_HERSHEY_DUPLEX, 0.7, 1)
        key_org = (display.shape[1] - text_size[0] - 20, 35)
        draw_text_with_outline(display, key_info, key_org, color=(0, 255, 255))
        draw_text_with_outline(output_frame, key_info, key_org, color=(0, 255, 255))
        
        cv.imshow("MyCam", display)
      
        fps = video.get(cv.CAP_PROP_FPS)

        if record and target.isOpened():
            target.write(output_frame)
        key = cv.waitKey(1) & 0xFF

        if key == 27:
            last_key_text = "ESC"
            print("Program terminated")
            break
        elif key == ord(' '):
            last_key_text = "SPACE"
            if not record:
                record = True
                if not target.isOpened():
                    VideoOpen(target, args.name, args.format, args.fourcc, fps, output_frame)
                print("Recording Started")
            else:
                record = False
                if target.isOpened():
                    target.release()
                print("Recording stopped")
        elif (args.contbri == True) and (key == ord('c')):
            last_key_text = "C"
            contbri = not contbri
        elif (args.flip == True) and (key == ord('f')):
            last_key_text = "F"
            flip = not flip
        elif (args.negative == True) and (key== ord('n')):
            last_key_text = "N"
            negative = not negative
        elif (args.Grayscale == True) and (key == ord('g')):
            last_key_text = "G"
            Grayscale = not Grayscale
        elif (args.Blur == True) and (key == ord('b')):
            last_key_text = "B"
            Blur = not Blur
        elif (args.contbri == True) and (key == ord('+') or key == ord('=')):
            last_key_text = "+"
            contrast += contrast_step
        elif (args.contbri == True) and (key == ord('-') or key == ord('_')):
            last_key_text = "-"
            contrast = max(0.1, contrast - contrast_step)
        elif (args.contbri == True) and (key == ord('>') or key == ord('.')):
            last_key_text = ">"
            brightness += brightness_step
        elif (args.contbri == True) and (key == ord('<') or key == ord(',')):
            last_key_text = "<"
            brightness -= brightness_step

    video.release()
    if target.isOpened():
        target.release()
    cv.destroyAllWindows()
        
