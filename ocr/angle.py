import cv2
import numpy as np
from matplotlib import pyplot as plt

def compute_angle(image):
    #img_d = image

    xs = len(image[0])
    ys = len(image)

    if xs > ys:
        img_d = image[0:ys, int(xs/2 - ys/2):int(xs/2 + ys/2)]
    else:
        img_d = image[int(ys/2 - xs/2):int(ys/2 + xs/2), 0:xs]

    img_gr = cv2.cvtColor(img_d, cv2.COLOR_BGR2GRAY)
    # (thresh, img_bw) = cv2.threshold(img_gr, 170, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    img_bw = cv2.adaptiveThreshold(img_gr,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,15,7)

    # cv2.imshow("BW", img_bw)

    fft = np.fft.fft2(img_bw);
    ffts = np.fft.fftshift(fft)
    mag = np.log(np.abs(ffts) + 1);

    maximum = max(mag.max(axis = 1))
    mag_n = mag/maximum

    # print maximum

    h = len(mag_n)
    w = len(mag_n[0])

    max_dist = 0

    x_max_dist = 0
    y_max_dist = 0

    angle = 0

    mag_filt = mag_n

    for i in range(h):
        for j in range(w):
            hor_d = w/2 - j
            ver_d = h/2 - i
            dist = np.sqrt(ver_d*ver_d + hor_d*hor_d)
            if mag_filt[i][j] <= 0.7:
                mag_filt[i][j] = 0
            elif dist > max_dist:
                max_dist = dist
                angle = -np.arctan2(hor_d*h, ver_d*w)/3.1415*180 - 90

    # print angle

    # cv2.imshow("Original", img_d)
    # cv2.waitKey(0)

    # plt.subplot(121),plt.imshow(img_bw, cmap = 'gray')
    # plt.title('Input Image'), plt.xticks([]), plt.yticks([])
    # plt.subplot(122),plt.imshow(mag_filt, cmap = 'gray')
    # plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
    # plt.show()

    return angle
