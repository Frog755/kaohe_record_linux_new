import cv2
import numpy as np


def find_left_point(y, binary_otsu, img, start_x=1, end_x=None):
    h, w = img.shape[:2]
    if end_x is None:
        end_x = w - 1

    for x in range(start_x, end_x, +1):
        if (binary_otsu[y, x - 1] == 0) and (binary_otsu[y, x] == 255):
            img[y, x] = [0, 0, 255]
            return x
    return 0


def find_right_point(y, binary_otsu, img, start_x=0, end_x=None):
    h, w = img.shape[:2]
    if end_x is None:
        end_x = w - 2

    for x in range(start_x, end_x, +1):
        if (binary_otsu[y, x] == 255) and (binary_otsu[y, x + 1] == 0):
            img[y, x] = [0, 255, 0]
            return x
    return 0


def find_born_left(y, prev_x, binary_otsu, img, search_range=5):
    """
    在当前行附近小范围搜索左边缘点，保持y坐标相近
    """
    h, w = binary_otsu.shape

    # 优先在当前行搜索
    start_x = max(1, prev_x - search_range)
    end_x = min(w - 1, prev_x + search_range)

    left_x = find_left_point(y, binary_otsu, img, start_x, end_x)
    if left_x != 0:
        return y, left_x

    # 如果当前行没找到，在相邻的上下行搜索
    for dy in [-1, 1, -2, 2]:  # 先搜索相邻行，再搜索稍远的行
        new_y = y + dy
        if 0 <= new_y < h:
            left_x = find_left_point(new_y, binary_otsu, img, start_x, end_x)
            if left_x != 0:
                return new_y, left_x

    # 如果都没找到，返回原始点
    return y, prev_x


def find_born_right(y, prev_x, binary_otsu, img, search_range=5):
    """
    在当前行附近小范围搜索右边缘点，保持y坐标相近
    """
    h, w = binary_otsu.shape

    # 优先在当前行搜索
    start_x = max(0, prev_x - search_range)
    end_x = min(w - 2, prev_x + search_range)

    right_x = find_right_point(y, binary_otsu, img, start_x, end_x)
    if right_x != 0:
        return y, right_x

    # 如果当前行没找到，在相邻的上下行搜索
    for dy in [-1, 1, -2, 2]:
        new_y = y + dy
        if 0 <= new_y < h:
            right_x = find_right_point(new_y, binary_otsu, img, start_x, end_x)
            if right_x != 0:
                return new_y, right_x

    return y, prev_x


def main():
    # 1. 图片预处理
    img = cv2.imread("test.png")
    if img is None:
        print("Error: Could not load image")
        return

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    ret1, binary_otsu = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    h, w = img.shape[:2]

    left_points = []
    right_points = []

    # 2. 扫线
    # (1) 底部区域：直接逐行查找边缘点
    print("Processing bottom area...")
    for y in range(h - 12, h // 2, -1):
        left_x = find_left_point(y, binary_otsu, img)
        right_x = find_right_point(y, binary_otsu, img)

        if left_x != 0 and right_x != 0:
            left_points.append([y, left_x])
            right_points.append([y, right_x])
            img[y, (left_x + right_x) // 2] = [255, 0, 255]
            print(f"Bottom - y:{y}, left:{left_x}, right:{right_x}")

    # (2) 顶部区域：基于前一行的位置进行小范围搜索
    print("Processing top area...")
    if left_points and right_points:
        # 获取最后一个有效的点
        last_left_y, last_left_x = left_points[-1]
        last_right_y, last_right_x = right_points[-1]

        # 从底部向上逐行处理
        for y in range(h // 2 - 1, 30, -1):
            # 处理左边缘 - 保持在同一行或相邻行
            new_left_y, new_left_x = find_born_left(y, last_left_x, binary_otsu, img, search_range=10)

            # 处理右边缘
            new_right_y, new_right_x = find_born_right(y, last_right_x, binary_otsu, img, search_range=10)

            # 确保点在同一行或相邻行，防止跳跃太大
            if abs(new_left_y - y) > 2:  # 如果跳跃太大，使用当前行和前一行的x坐标
                new_left_y = y
                new_left_x = last_left_x

            if abs(new_right_y - y) > 2:
                new_right_y = y
                new_right_x = last_right_x

            # 更新为当前找到的点
            last_left_y, last_left_x = new_left_y, new_left_x
            last_right_y, last_right_x = new_right_y, new_right_x

            # 添加到列表并标记
            left_points.append([new_left_y, new_left_x])
            right_points.append([new_right_y, new_right_x])

            img[new_left_y, new_left_x] = [0, 0, 255]
            img[new_right_y, new_right_x] = [0, 255, 0]

            print(
                f"Top - y:{y}, left_y:{new_left_y}, left_x:{new_left_x}, right_y:{new_right_y}, right_x:{new_right_x}")

    print(f"Found {len(left_points)} left points and {len(right_points)} right points")

    # 3. 显示图像
    cv2.imshow("otsu", binary_otsu)
    cv2.imshow("img", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.imwrite("new1.png", img)


if __name__ == '__main__':
    main()