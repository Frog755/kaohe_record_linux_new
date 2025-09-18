import cv2
import numpy as np

def find_left_point(y, binary_otsu, img):
    h, w = img.shape[: 2]
    for x in range(0, w - 2, +1):
        if binary_otsu[y, x - 1] == 0 and binary_otsu[y, x] == 255 :
            img[y, x] = [0, 0, 255]
            return x
    return 0



def find_right_point(y, binary_otsu, img):
    h, w = img.shape[: 2]
    for x in range(1, w - 1, +1):
        if binary_otsu[y, x] == 255 and binary_otsu[y, x + 1] == 0:
            img[y, x] = [0, 255, 0]
            return x
    return 0

def find_born_left(y, left, binary_otsu):
    if binary_otsu[y+1, left+1] == 0:
        return y+1,left+1
    elif binary_otsu[y, left+1] == 0:
        return y,left+1
    elif binary_otsu[y-1, left+1] == 0:
        return y-1,left+1
    elif binary_otsu[y-1, left] == 0:
        return y-1, left
    elif binary_otsu[y-1, left-1] == 0:
        return y-1, left-1
    elif binary_otsu[y, left-1] == 0:
        return y, left-1
    elif binary_otsu[y+1, left-1] == 0:
        return y+1, left+1
    else:
        return y, left
def find_born_right(y, right, binary_otsu):
    # if binary_otsu[y+1, right-1] == 0:
    #     return y+1,right-1
    if binary_otsu[y, right-1] == 0:
        return y,right-1
    if binary_otsu[y-1, right-1] == 0:
        return y-1,right-1
    elif binary_otsu[y-1, right] == 0:
        return y-1,right
    elif binary_otsu[y-1, right+1] == 0:
        return y-1,right+1
    elif binary_otsu[y, right+1] == 0:
        return y, right+1
    elif binary_otsu[y+1, right+1] == 0:
        return y+1, right+1
    else:
        return y, right


def main():

    #1.图片预处理
    img = cv2.imread("test.png")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    ret1, binary_otsu = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)#大津阈值算法
    h, w = img.shape[: 2]

    left = []
    right = []
    mid = []

    # 2.扫线
    #(1)找到初始生长线
    for y in range(h - 12, h//2, -1):#限制范围
        left_x = find_left_point(y, binary_otsu, img)
        right_x = find_right_point(y, binary_otsu, img)
        if left_x != 0 and right_x != 0:
            left.append([y, left_x])
            right.append([y, right_x])
            mid.append([y, (left_x + right_x) // 2])
            img[y, (left_x + right_x) // 2] = [255, 0, 255]

    #(2)往上延伸
    for y in range(h//2, 45, -1):#限制范围
        y, left_x = find_born_left(y, left_x, binary_otsu)
        y, right_x = find_born_right(y, right_x, binary_otsu)
        img[y, left_x] = [0, 0, 255]
        img[y, right_x] = [0, 255, 0]
        left.append([y, left_x])
        right.append([y, right_x])
        mid.append([y, (left_x + right_x) // 2])
        img[y, (left_x + right_x) // 2] = [255, 0, 255]

    #(3)延伸
    for i in range(0, 40, 1):#限制范围
        y, left_x = find_born_left(y, left_x, binary_otsu)
        y, right_x = find_born_right(y, right_x, binary_otsu)
        img[y, left_x] = [0, 0, 255]
        img[y, right_x] = [0, 255, 0]
        left.append([y, left_x])
        right.append([y, right_x])
        mid.append([y, (left_x + right_x) // 2])
        img[y, (left_x + right_x) // 2] = [255, 0, 255]

    #3.打印坐标
    print(left)
    print(right)
    print(mid)

    #4.显示图像
    cv2.imshow("otsu", binary_otsu)
    cv2.imshow("img", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    cv2.imwrite("new1.png", img)

if __name__ == '__main__':
    main()