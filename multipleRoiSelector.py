import numpy as np
import argparse
import glob
import json
import sys
import cv2


def parseArgs():
    parser = argparse.ArgumentParser(description='Roi Selector with OpenCV')
    parser.add_argument( # Path to image Files
        '--path',
        dest='imagePath',
        help='path to image files',
        default='images',
        type=str
    )
    parser.add_argument( # Image extensions
        '--ext',
        dest='imageExt',
        help='image extension',
        default='jpg',
        type=str
    )
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    return parser.parse_args()

def printInfos():
    print('[INFO] This is a ROI selector script for multiple images')
    print('[INFO] Click the left button: select the point, right click: delete the last selected point')
    print('[INFO] Press ‘S’ to determine the selection area and save it')
    print('[INFO] Press ‘D’ to delete the selection area')
    print('[INFO] Press ESC to quit')
    
def getImagesFromFile(args):    
    images = glob.glob(args.imagePath + '/*.' + args.imageExt)
    return images

def plotSegmentedRois(imTemp, imMask, rois, colors):
    for qq, rs in enumerate(rois):
        roiPoints = rs['Points']
        roiPoints = np.array(roiPoints, np.int32)
        roiPoints = roiPoints.reshape((-1, 1, 2))
        imMask = cv2.fillPoly(imMask, [roiPoints], colors[qq])
        imTemp = cv2.addWeighted(imTemp, 0.5, imMask, 0.5, 0)
    return imTemp, imMask

def checkRoiClosed(pts,distTh=5):
    points = np.array(pts, np.int32)
    dist = np.linalg.norm(points[0] - points[-1])
    if dist < distTh:
        return True
    return False

def drawRoi(event, x, y,  flags, param):
    global pts, id
    colors = [(255,0,0),(0,255,0), (0,0,255), (204,78,1), (79,0,128), (255,255,85), (79,186,218), (229,152,230), (88,0,144)]
    imTemp = im.copy()
    imMask = im.copy()

    if event == cv2.EVENT_LBUTTONDOWN:  
        pts.append((x, y))  

    if event == cv2.EVENT_RBUTTONDOWN:  
        if len(pts)>0:
            pts.pop()  
    
    imTemp, imMask = plotSegmentedRois(imTemp, imMask, rois, colors)

    if len(pts) > 0:
        cv2.circle(imTemp, pts[-1], 1, (0, 0, 255), -1)

    if len(pts) > 1:

        if checkRoiClosed(pts,distTh=5):
            rois.append({'Id': id, 'Points': pts})
            id += 1
            print(rois, end='\n\n')
            pts = []
    
        for i in range(len(pts) - 1):
            cv2.circle(imTemp, pts[i], 1, (0, 0, 255), -1)
            cv2.line(imTemp, pt1=pts[i], pt2=pts[i + 1], color=(255, 0, 0), thickness=1)
    
    
    cv2.imshow('image', imTemp)

def roiSelector(image):
    global im, key, pts, rois, id

    id = 1
    pts = []
    rois = []

    im = cv2.imread(image)
    cv2.namedWindow('image',cv2.WINDOW_FREERATIO)
    cv2.imshow('image', im)
    cv2.setMouseCallback('image', drawRoi)    
    
    while True:
        key = cv2.waitKey(1) & 0xFF   

        if key == 27:
            break

        if chr(key).lower() == 'd':
            if len(rois) < 1: continue
            rois.pop()
            pts = []
            id -= 1
            
        if chr(key).lower() == 's':
            jsonName = image.split('.')[0] + '.json'
            with open(jsonName,'w') as jsonRoi:
                json.dump(rois, jsonRoi)
            break
    cv2.destroyAllWindows()


if __name__ == '__main__':

    printInfos()
    args = parseArgs()                      # Parse input parameters
    imageFiles = getImagesFromFile(args)    # Get image names from given path and extension

    for image in imageFiles:                # Loop all images and run roi selector
        roiSelector(image)                  # Function to select and save rois

    