#!/usr/bin/python3

import cv2
import imutils
import numpy as np
from skimage.metrics import structural_similarity as compare_ssim




def display_windows(windows):
    MAX_WIDTH = 2000
    MAX_HEIGHT = 2000
    winWidth = 500
    winHeight = 500
    x = 0
    y = 0
    for window in windows:
        w = cv2.namedWindow(window['name'], cv2.WINDOW_NORMAL)
        cv2.resizeWindow(window['name'],winWidth,winHeight)
        cv2.imshow(window['name'],window['img'])
        cv2.moveWindow(window['name'],x*winWidth, y*winHeight)
        x += 1
        if(x*winWidth>MAX_WIDTH):
            x = 0
            y += 1
    cv2.waitKey()
    cv2.destroyAllWindows()


def find_outlines(original_file, modified_file):

    windows=[]

    ###Load images
    original_img = cv2.imread(original_file,cv2.IMREAD_COLOR)
    modified_img = cv2.imread(modified_file,cv2.IMREAD_COLOR)


    original_img_gray = cv2.cvtColor(original_img,cv2.COLOR_BGR2GRAY)
    modified_img_gray = cv2.cvtColor(modified_img,cv2.COLOR_BGR2GRAY)

    ###Calculate differences
    absdiff = 255-cv2.absdiff(original_img_gray, modified_img_gray)
    windows.append({"name":'absdiff',"img":absdiff.copy()})

    (simi,diff) = compare_ssim(original_img_gray,modified_img_gray, guassian_weights=True, full=True)
    diff = (diff * 255).astype("uint8") 
    simi_diff = diff.copy()
    simi_diff = 255-simi_diff
    windows.append({"name":'ssim_diff',"img":simi_diff})


    ###Find edges/contours

    #thresholhd
    thresh = cv2.threshold(diff, 253, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)[1]
    windows.append({'name': 'thresh', "img":thresh})

    #canny threshold
    # thresh = cv2.Canny(diff, 10, 200, apertureSize=3)

    #watershed segmentation
    #thresh = cv2.

    ###Noise removal
    opening_median_blur = cv2.medianBlur(thresh,3)
    windows.append({"name":'opening_median_blur',"img":opening_median_blur.copy()})

    opening_guassian_blur = cv2.GaussianBlur(thresh,(3,3),0)
    windows.append({"name":'opening_guassian_blur',"img":opening_guassian_blur.copy()})

    opening_bilateral_blur = cv2.bilateralFilter(thresh,9, 75,75)
    windows.append({"name":'opening_bilat_blur',"img":opening_bilateral_blur.copy()})

    opening_to_morph = opening_guassian_blur

    kernel = np.ones((15,15),np.uint8)
    opening_morph = cv2.morphologyEx(opening_to_morph,cv2.MORPH_CLOSE, kernel, iterations=3)
    windows.append({"name":'opening_morph',"img":opening_morph.copy()})
    opening=opening_morph



    found_contours= cv2.findContours(image=opening.copy(), mode=cv2.RETR_EXTERNAL,method=cv2.CHAIN_APPROX_SIMPLE)
    found_contours = imutils.grab_contours(found_contours)

    found_contour_img = original_img.copy()
    found_contour_img[found_contour_img !=255 ] = 255 
    found_contour_img=cv2.drawContours(image=found_contour_img,contours=found_contours,contourIdx=-1, color=(0,0,255),thickness=3)


    ###Simplify contours
    simplified_contours = []
    for contour in found_contours:
        simplified_contour = cv2.approxPolyDP(curve=contour,epsilon=10,closed=True)
        simplified_contour = cv2.approxPolyDP(curve=simplified_contour,epsilon=5,closed=True) 
        simplified_contours.append(simplified_contour)


    # for countour in outlines: 
    #     (x,y,w,h)=cv2.boundingRect(countour)
    #     cv2.rectangle(diff,(x,y),(x+w, y+h), (0,0,255), 5)

    print("We have " + str(len(found_contours)) + " found_countours")
    print("We have " + str(len(simplified_contours)) + " simplified_countours")

    simplified_contour_img = original_img.copy()
    simplified_contour_img[simplified_contour_img !=255 ] = 255 
    simplified_contour_img=cv2.drawContours(image=simplified_contour_img,contours=simplified_contours,contourIdx=-1, color=(0,0,255),thickness=3)

    modified_wContours_img=cv2.drawContours(image=modified_img,contours=simplified_contours,contourIdx=-1, color=(255,0,0),thickness=5)




    windows.append({'name':'opening', "img":opening})
    windows.append({'name':'found_contours', "img":found_contour_img})
    windows.append({'name':'simplified_contours', "img":simplified_contour_img})
    windows.append({'name':'modified_outline', "img":modified_wContours_img})

    display_windows(windows)
    return simplified_contours



def convert_contour_to_svg_path(contour):
    from svg.path import Path, Move, Close, Line
    

    contour = iter(contour)
    pt = next(contour)
    x,y = pt[0]
    x_start,y_start = x,y
    path = Path(Move(to=(complex(x,y))))
    
    for pt in contour:
        x_1,y_1 = pt[0]
        path.append(Line(start=(complex(x,y)),end=(complex(x_1,y_1))))
        x,y=x_1, y_1

    path.append(Close(complex(x,y),complex(x_start,y_start)))
    #print((path.d()))

    # path=0
    # svg_path = '"m '

    # for pt in contour:
    #     x,y = pt[0]
    #     #print("x,y: "+ str(x)+" " + str(y))
    #     svg_path = svg_path + str(x) + ',' + str(y) + ' '
    # svg_path = svg_path + 'z"'
    return str(path.d())


def main():
    original_file="original.jpg"
    modified_file ="modified.png"
    outlines = find_outlines(original_file, modified_file)
    print(type(outlines))
    for path in outlines:
        svg_path = convert_contour_to_svg_path(path)
        #print((path.shape))
        #print((path.ndim))
        
        print('"'+svg_path+'",')




    
if __name__=="__main__":
    main()
