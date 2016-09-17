import cv2
import numpy as np
from matplotlib import pyplot as plt

def compute_angle(image):
    img_d = image
    img_gr = cv2.cvtColor(img_d, cv2.COLOR_BGR2GRAY)
    (thresh, img_bw) = cv2.threshold(img_gr, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    cv2.imshow("BW", img_bw)

    fft = np.fft.fft2(img_bw);
    ffts = np.fft.fftshift(fft)
    mag = np.log(np.abs(ffts) + 1);

    maximum = max(mag.max(axis = 1))
    mag_n = mag/maximum

    print maximum

    w = len(mag_n)
    h = len(mag_n[0])

    max_hor_d = 0
    angle = 0

    mag_filt = mag

    for i in range(w):
        for j in range(h):
            hor_d = h/2 - j
            ver_d = w/2 - i
            if mag_filt[i][j] <= 0.7*maximum:
                mag_filt[i][j] = 0
            elif abs(hor_d) > max_hor_d:
                max_hor_d = abs(hor_d)
                angle = np.arctan2(ver_d*h, hor_d*w)

    print angle

    cv2.imshow("Original", img_d)
    cv2.waitKey(0)

    #mag_grey = cv2.cvtColor(mag, cv2.COLOR_BGR2GRAY)
    #(_, mag_thresh) = cv2.threshold(mag_grey, 128, 255, cv2.THRESH_BINARY)

    plt.subplot(121),plt.imshow(img_bw, cmap = 'gray')
    plt.title('Input Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(122),plt.imshow(mag)
    plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
    plt.show()

    return angle
