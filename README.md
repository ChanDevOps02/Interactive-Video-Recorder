# Interactive Video Recorder

An interactive OpenCV video recorder with real-time image editing effects.

## Overview

Interactive Video Recorder is a Python-based camera recording program built with OpenCV.  
It supports real-time camera preview, video recording, and several image editing effects that can be toggled during execution.

## Features

- Real-time camera preview using `cv.VideoCapture`
- Video recording using `cv.VideoWriter`
- Preview mode and record mode
- Record mode indicator shown as a red circle on the screen
- Start and stop recording with the `Space` key
- Exit the program with the `ESC` key
- Real-time image editing options:
  - Negative image
  - Flip
  - Grayscale conversion
  - Gaussian blur
  - Contrast and brightness adjustment

## Project Structure

```text
.
├── My_Video_Recorder.py
├── README.md
├── result/
└── scripts/
    ├── run_macbook.sh
    └── run_iphone.sh
```

## Requirements

- Python 3
- OpenCV (`cv2`)

Example installation:

```bash
pip install opencv-python
```

## How to Run

### MacBook camera

```bash
zsh "scripts/run_macbook.sh"
```

### iPhone camera

```bash
zsh "scripts/run_iphone.sh"
```

## Command-line Arguments

The program supports the following arguments:

- `--camera`: camera index
- `--name`: output video file name
- `--format`: output file format
- `--fourcc`: codec for video saving
- `--negative`: enable negative mode toggle
- `--flip`: enable flip mode toggle
- `--Grayscale`: enable grayscale mode toggle
- `--Blur`: enable blur mode toggle
- `--contbri`: enable contrast and brightness mode toggle

## Keyboard Controls

### Recording Control

- `Space`: start or stop recording
- `ESC`: terminate the program

### Image Editing Control

- `n`: toggle negative effect
- `f`: toggle flip effect
- `g`: toggle grayscale effect
- `b`: toggle Gaussian blur effect
- `c`: toggle contrast and brightness mode

### Contrast and Brightness Adjustment

When contrast and brightness mode is enabled:

- `+` or `=`: increase contrast
- `-` or `_`: decrease contrast
- `>` or `.`: increase brightness
- `<` or `,`: decrease brightness

## Output

Recorded video files are automatically saved in:

```text
result/
```

## Example Workflow

1. Run the program with one of the shell scripts.
2. Check the live camera preview.
3. Press `n`, `f`, `g`, `b`, or `c` to apply image editing effects.
4. Press `Space` to start recording.
5. Press `Space` again to stop recording.
6. Press `ESC` to exit the program.

## Implementation Summary

This project was implemented using:

- `cv.VideoCapture` for camera input
- `cv.VideoWriter` for video file output
- OpenCV image processing functions for real-time editing
- `argparse` for execution-time option control
- Shell scripts for convenient preset execution

## Author

Minchan Kang (SEOULTECH CSE)
