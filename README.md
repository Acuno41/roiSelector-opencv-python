# roiSelector-opencv-python

roiSelector-opencv-python is a Python script for selecting and segmentin ROI's in images and saves in a JSON File.
Currently working for only 1 segment per image.

## Download 

git clone https://github.com/Acuno41/roiSelector-opencv-python.git

## Installation

Use the [pip](https://pip.pypa.io/en/stable/) to install requirements.

```bash
pip3 install requirements.txt
```

## Usage

```bash
python roiSelector.py --path images --ext jpg
```

```python
print('[INFO] This is a ROI selector script for multiple images')
print('[INFO] Click the left button: select the point, right click: delete the last selected point')
print('[INFO] Press ‘S’ to determine the selection area and save it')
print('[INFO] Press ‘D’ to delete the selection area')
print('[INFO] Press ESC to quit')
```
![Alt text](https://github.com/Acuno41/roiSelector-opencv-python/blob/main/sources/selecting.jpg?raw=true "Optional Title")


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
