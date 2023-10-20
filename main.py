import cv2
import numpy as np

sourcefile = '/Users/mac/Desktop/Programming/Python/intermediate/Image_Processing/image.jpg'
img = cv2.imread(sourcefile)
gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY) 
_, thresh = cv2.threshold(gray, 230, 255, cv2.THRESH_BINARY_INV) # threshodl = 门槛 = 230

canny = cv2.Canny(thresh, 254, 255) #thresh 是黑白，所以 its binary, and takes ones to make it green
# cv2.imshow('canny', canny) #test to understand
# cv2.waitKey(0)  #test to understand

contours, hierarchy = cv2.findContours(canny.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # external = 外轮廓
cv2.drawContours(img, contours, -1, (0,255,0), 2) # -1 indicates all contours, 2 pixels
# cv2.imshow('img', img)
# cv2.waitKey(0)
# for c in contours:
#     print('c: ',c)  #test to understand

# cv2.imshow('img', img) #test to understand
# cv2.waitKey(0) #test to understand

sortedCon = sorted(contours, key = cv2.contourArea) # sort the contours according to their areas 
# print("sortedCon[0]: ", sortedCon[0]) 
# print("sortedCon[1]: ", sortedCon[1]) #test to understand



# largest area number1: 
x,y,w,h = cv2.boundingRect(sortedCon[0])
cv2.rectangle(img, (x,y), (x+w, y+h), (255, 0, 0), 3)
roi = img.copy()[y:y+h, x:x+w]

# largest area number2:
x2, y2, w2, h2 = cv2.boundingRect(sortedCon[1])
cv2.rectangle(img, (x2,y2), (x2+w2, y2+h2), (0,255,0), 3)
roi2 = img.copy()[y2: y2+h2, x2:x2+w2 ]


roi_h = roi.shape[0]
roi_w = roi.shape[1]
roi2_h = roi2.shape[0]
roi2_w = roi2.shape[1]

# print("shapes: ")
# print(roi_h)
# print(roi_w)
# print(roi2_h)
# print(roi2_w)  #test to understand

# reduce the size of the pictures according to smallest higth and width because they has to be same size
if roi_h >= roi2_h:
    if roi_w >= roi2_w:
        roi = roi[0:roi2_h, 0:roi2_w] # they are same shape 
    else:
        roi = roi[0:roi2_h, 0:roi_w] # they are same shape 
else:
        if roi_w >= roi2_w:
            roi = roi[0:roi_h, 0:roi2_w] # they are same shape 
        else:
            roi = roi[0:roi_h, 0:roi_w] # they are same shape 
# we made the roi according to the smallest contour
# now we will make roi2 same size with roi

roi2 = roi2[0:roi_h, 0:roi_w] # they are same shape 

# print('roi[0] = ', roi.shape[0], '.  roi[1] = ',roi.shape[1])
# print('roi', roi.shape)
# print('roi2', roi2.shape)  # check if they are same sizse


diff = 255 - cv2.absdiff(roi, roi2) # absolute difference between two arrays (thats why we made them same size above)
# diff = cv2.absdiff(roi, roi2) # run this if you want to know why we subtracked it from 255

lower = np.array([0,0,0])  # bounderies
upper = np.array([180,255,255]) # 360红， 240蓝， 120绿

imgHSV = cv2.cvtColor(diff, cv2.COLOR_BGR2HSV) # hsv representation to make the differrence more clear
mask = cv2.inRange(imgHSV, lower, upper)

result = cv2.bitwise_and(diff, diff, mask=mask) 
# cv2.imshow("result", result)  # test to understand
# cv2.waitKey(0)  # test to understand


blur = cv2.GaussianBlur(result, (11,11),0)
canny = cv2.Canny(blur, 50, 150) # make it black and white (binary form) 
edges = cv2.dilate(canny, None)  # make the white pixels thicker (255)

# cv2.imshow("edges", edges)  # test to understand
# cv2.waitKey(0)   # test to understand

contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # detect the contours (thats why we made it black and white)

for cn in contours:  # put each contours (which are the difference between the two images) in a rectangle
    
    #  print("contors", cn) # test
     x, y, w, h = cv2.boundingRect(cn)
     
     cv2.rectangle(result, (x,y), (x+w, y+h), (0,0,255, 2))
     cv2.rectangle(roi, (x,y), (x+w, y+h), (0,255,0, 2))
     cv2.rectangle(roi2, (x,y), (x+w, y+h), (255,0,0, 2))

cv2.imshow('result', result)
cv2.imshow('roi', roi)
cv2.imshow('roi2', roi2)

# cv2.imshow('blurry', blur)
# cv2.imshow('edgs', edges)
# cv2.imshow('diff', diff)
# cv2.imshow("canny", canny)

cv2.waitKey(0)
cv2.destroyAllWindows()