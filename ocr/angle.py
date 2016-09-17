import cv2
import numpy as np
from matplotlib import pyplot as plt

def compute_angle(image):
    img_d = image
    img_gr = cv2.cvtColor(img_d, cv2.COLOR_BGR2GRAY)
    (thresh, img_bw) = cv2.threshold(img_gr, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    # cv2.imshow("BW", img_bw)

    fft = np.fft.fft2(img_bw);
    ffts = np.fft.fftshift(fft)
    mag = np.log(np.abs(ffts) + 1);

    maximum = max(mag.max(axis = 1))
    mag_n = mag/maximum

    # print maximum

    w = len(mag_n)
    h = len(mag_n[0])

    max_dist = 0
    angle = 0

    mag_filt = mag

    for i in range(w):
        for j in range(h):
            hor_d = h/2 - j
            ver_d = w/2 - i
            dist = np.sqrt(ver_d*ver_d + hor_d*hor_d)
            if mag_filt[i][j] <= 0.65*maximum:
                mag_filt[i][j] = 0
            elif dist > max_dist:
                max_dist = dist
                angle = np.arctan2(ver_d*h, hor_d*w)/3.1415*180

    # print angle

    # cv2.imshow("Original", img_d)
    # cv2.waitKey(0)

    plt.subplot(121),plt.imshow(img_bw, cmap = 'gray')
    plt.title('Input Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(122),plt.imshow(mag)
    plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
    plt.show()

    return angle
