import cv2
import time

from numpy.ma.core import right_shift


def find_left_point(y, binary_otsu, img):
    h, w = img.shape[: 2]
    for x in range(1, w - 2, +1):
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


def find_born_left(y, left,py, px, binary_otsu):
    # 定义八邻域的偏移量 (dy, dx)
    neighbors = [
        (1, 1),  # 右下
        (0, 1),  # 右
        (-1, 1),  # 右上
        (-1, 0),  # 上
        (-1, -1),  # 左上
        (0, -1),  # 左
        (1, -1)  # 左下
    ]

    # 按顺序检查每个邻域点
    for dy, dx in neighbors:
        ny, nx = y + dy, left + dx
        # 检查边界
        if 0 <= ny < binary_otsu.shape[0] and 0 <= nx < binary_otsu.shape[1]:
            if binary_otsu[ny, nx] == 0:
                return ny, nx

    # 如果没有找到合适的点，返回原始位置
    return y, left


def find_born_right(y, right,py, px, binary_otsu):
    # 定义八邻域的偏移量 (dy, dx)
    neighbors = [
        (1, -1),  # 左下
        (0, -1),  # 左
        (-1, -1),  # 左上
        (-1, 0),  # 上
        (-1, 1),  # 右上
        (0, 1),  # 右
        (1, 1),  # 右下
        (1, 0)  # 下
    ]
    neighbors_n = [
        (-1, -1),  # 左上
        (-1, 0),  # 上
        (-1, 1),  # 右上
        (0, 1),  # 右
        (1, 1),  # 右下
        (1, 0), # 下
        (1, -1),  # 左下
        (0, -1),  # 左

    ]
    if py == y and px == right:
        # 按顺序检查每个邻域点
        for dy, dx in neighbors_n:
            ny, nx = y + dy, right + dx
            # 检查边界
            if 0 <= ny < binary_otsu.shape[0] and 0 <= nx < binary_otsu.shape[1]:
                if binary_otsu[ny, nx] == 0:
                    return ny, nx

        # 如果没有找到合适的点，返回原始位置
        return y, right
    else:
        # 按顺序检查每个邻域点
        for dy, dx in neighbors:
            ny, nx = y + dy, right + dx
            # 检查边界
            if 0 <= ny < binary_otsu.shape[0] and 0 <= nx < binary_otsu.shape[1]:
                if binary_otsu[ny, nx] == 0:
                    return ny, nx

        # 如果没有找到合适的点，返回原始位置
        return y, right



def main():
    start = time.time()

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

    # (2)延伸
    left_y = h // 2
    right_y = h // 2

    for _ in range(90):  # 限制步数
        p_left_y, p_left_x = left_y, left_x
        left_y, left_x = find_born_left(left_y, left_x, p_left_y, p_left_x, binary_otsu)
        p_right_y, p_right_x = right_y, right_x
        right_y, right_x = find_born_right(right_y, right_x, p_right_y, p_right_x,  binary_otsu)

        img[left_y, left_x] = [0, 0, 255]
        img[right_y, right_x] = [0, 255, 0]
        left.append([left_y, left_x])
        right.append([right_y, right_x])
        mid.append([(left_y + right_y) // 2, (left_x + right_x) // 2])
        img[(left_y + right_y) // 2, (left_x + right_x) // 2] = [255, 0, 255]


    # for _ in range(200):#限制范围
    #     n_left_y, left_x = find_born_left(n_left_y, left_x, binary_otsu)
    #     n_right_y, right_x = find_born_right(n_right_y, right_x, binary_otsu)
    #     img[n_left_y, left_x] = [0, 0, 255]
    #     img[n_right_y, right_x] = [0, 255, 0]
    #     left.append([n_left_y, left_x])
    #     right.append([n_right_y, right_x])
    #     mid.append([(n_left_y + n_right_y) // 2, (left_x + right_x) // 2])
    #     img[(n_left_y + n_right_y) // 2, (left_x + right_x) // 2] = [255, 0, 255]

    #3.打印坐标
    print(left)
    print(right)
    print(mid)

    end = time.time()
    execution_time = end - start
    print(f"代码执行时间: {execution_time:.4f} 秒")

    #4.显示图像
    cv2.imshow("otsu", binary_otsu)
    cv2.imshow("img", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    cv2.imwrite("new1.png", img)

if __name__ == '__main__':
    main()
