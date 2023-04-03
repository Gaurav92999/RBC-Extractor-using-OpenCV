import cv2
import numpy as np
import os

if not os.path.exists('RBC_IMAGES'):
    os.makedirs('RBC_IMAGES')

for i in range(1, 120):  
    filename = f'image-{i}.png'
    if not os.path.exists(filename):
        continue
    
    img = cv2.imread(filename)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    
    a = 0
    b = 255
    c = np.min(gray)
    d = np.max(gray)
    stretched = np.round((gray - c) * ((b - a) / (d - c)) + a).astype(np.uint8)

    equ = cv2.equalizeHist(stretched)

    blurred = cv2.GaussianBlur(equ, (5,5), 0)
    unsharp_mask = cv2.addWeighted(equ, 1.5, blurred, -0.5, 0)

    f = np.fft.fft2(unsharp_mask)
    fshift = np.fft.fftshift(f)

    rows, cols = unsharp_mask.shape
    crow, ccol = int(rows/2), int(cols/2)
    mask = np.zeros((rows,cols), np.uint8)
    r = 50
    center = [crow,ccol]
    x, y = np.ogrid[:rows, :cols]
    mask_area = (x - center[0])*2 + (y - center[1])*2 <= r*r
    mask[mask_area] = 1

    fshift_filtered = fshift * mask

    f_ishift = np.fft.ifftshift(fshift_filtered)
    filtered = np.fft.ifft2(f_ishift)
    filtered = np.abs(filtered)

    thresh_val, thresh = cv2.threshold(np.uint8(filtered), 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel, iterations=1)

    contours, hierarchy = cv2.findContours(closing.astype(np.uint8), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    rbc_images = []

    for i, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if area > 1000:
            x,y,w,h = cv2.boundingRect(contour)
            cell = img[y:y+h, x:x+w]
            cell = cv2.resize(cell, (100, 100), interpolation=cv2.INTER_AREA)
            avg_color_per_row = np.average(cell, axis=0)
            avg_color = np.average(avg_color_per_row, axis=0)

            if avg_color[2] > avg_color[0] + 30 and avg_color[2] > avg_color[1] + 30:
                rbc_images.append(cell)

    for i, rbc_image in enumerate(rbc_images):
        cv2.imwrite(f'RBC_IMAGES/{filename[:-4]}_rbc{i+1}.png', rbc_image)
