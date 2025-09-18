import cv2
import time

def find_left_point(y, binary_otsu, img, start, end):
    h, w = img.shape[: 2]
    for x in range(start, end, +1):
        if(binary_otsu[y, x -1] == 0) and (binary_otsu[y, x] == 255 ):
            img[y, x] = [0, 0, 255]
            return x
    return 0



def find_right_point(y, binary_otsu, img, start, end):
    h, w = img.shape[: 2]
    for x in range(start, end, +1):
        if (binary_otsu[y, x] == 255) and (binary_otsu[y, x + 1] == 0):
            img[y, x] = [0, 255, 0]
            return x
    return 0



def main():
    start_time = time.time()

    #1.图片预处理
    img = cv2.imread("test.png")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    ret1, binary_otsu = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)#大津阈值算法
    h, w = img.shape[: 2]

    # 2.扫线
    start, end = 0, w-1

    for y in range(h - 12, 40, -1):
            left_x = find_left_point(y, binary_otsu, img, start, end)
            right_x = find_right_point(y, binary_otsu, img, start, end)

            mid_x = (left_x + right_x) // 2
            img[y, mid_x] = [255, 0, 255]

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"代码运行时间：{execution_time:.4f} 秒")

    #3.显示图像
    cv2.imshow("otsu", binary_otsu)
    cv2.imshow("img", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    cv2.imwrite("new1.png", img)

if __name__ == '__main__':
    main()
