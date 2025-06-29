# retico-screen

A retico module for showing video streams and detected objects on a screen.

## Overview

The `retico-screen` module provides functionality to display video streams from a camera module or by passing the detected objects from other modules like [YoloV11](https://github.com/retico-team/retico-yolov11.git) or [SAM](https://github.com/retico-team/retico-sam.git) to the provided converter and then to the screen module. 

## Installation

### Step 1: Install the package

```bash
pip install git+https://github.com/retico-team/retico-screen.git
```

### Step 2: Install retico-vision dependency
Since this module depends on `retico-vision`, you need to install it and add it to your Python path:
```bash
git clone https://github.com/retico-team/retico-vision.git
```
**Important**: Make sure to add the path to the `retico-vision` library to your `PYTHONPATH` environment variable. This is required for the module to properly import the vision components.

## Usage
For a basic example of how to use the `retico-screen` module, refer to the `example.py` file in the repository. Note that you will also need to install and add to the environment the `retico-yolov11` module to provide the object detection capabilities.

## Project Structure

```
retico-screen/
├── retico_screen/
│   ├── __init__.py
│   ├── converter.py          # Converter module to convert DetectedObjectsIU to ImageIU for display
│   ├── screen.py            # Main screen module for displaying video streams and detected objects
│   └── version.py              # Version information
├── setup.py                    # Package setup
├── example.py                  # Example usage script
├── README.md                   # This file
└── LICENSE                     # License file
```

## Related Projects

- [ReTiCo Core](https://github.com/retico-team/retico-core) - The core ReTiCo framework
- [ReTiCo Vision](https://github.com/retico-team/retico-vision) - Vision components for ReTiCo
