import cv2
import numpy as np

def find_right_point(y, binary_otsu, img):
    h, w = img.shape[: 2]
    for x in range(w // 2, w - 1, +1):
        if(binary_otsu[y, x -1] == 255) and (binary_otsu[y, x] == 255 ) and (binary_otsu[y, x + 1] == 0):
            img[y, x] = [0, 255, 0]
            return x


def find_left_point(y, binary_otsu, img):
    h, w = img.shape[: 2]
    for x in range(w // 2, -1, -1):
        if (binary_otsu[y, x - 1] == 0) and (binary_otsu[y, x] == 255) and (binary_otsu[y, x + 1] == 255):
            img[y, x] = [0, 0, 255]
            return x


def main():
    #1.图片预处理
    img = cv2.imread("test.png")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    ret1, binary_otsu = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)#大津阈值算法

    #2.扫线
    h, w = img.shape[: 2]
    for y in range(h - 1, -1, -1):
        left_x = find_right_point(y, binary_otsu, img)
        right_x = find_left_point(y, binary_otsu, img)
        if left_x is not None and right_x is not None:
            mid_x = (left_x + right_x) // 2
            img[y, mid_x] = [255, 0, 255]


    #3.显示图像
    cv2.imshow("otsu", binary_otsu)
    cv2.imshow("img", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()