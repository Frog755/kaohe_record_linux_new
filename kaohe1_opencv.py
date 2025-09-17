import cv2
import numpy as np

def cv_show(name, img):
    cv2.imshow(name, img)
    cv2.waitKey()
    cv2.destroyAllWindows()

img = cv2.imread("test.png")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
v = cv2.Canny(blurred, 50, 150)
_, thresh = cv2.threshold(v, 85, 255, cv2.THRESH_BINARY)

contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
draw_img = img.copy()
#画两条边线
res = cv2.drawContours(draw_img, contours, 0, (0, 255, 0), 1)
res = cv2.drawContours(draw_img, contours, 1, (0, 0, 255), 1)
left_contour, right_contour = contours[1], contours[0]
#两条边线坐标数据
left_contour = left_contour.reshape(-1, 2)  # 重塑为 (N, 2)
right_contour = right_contour.reshape(-1, 2)

x_left_contour = left_contour[left_contour[:, 1] > 46]#仅保留大于43的y值
x_right_contour = right_contour[right_contour[:, 1] > 46]

# 步骤1：将坐标按y值排序，并转为字典（y值为键，x值为值，便于查找）
def coords_to_dict_y(coords):
    # 按y值排序
    sorted_coords = coords[coords[:, 1].argsort()]
    # 转为字典 {y: x}，若有相同y值则取最后一个
    coord_dict = {y: x for x, y in sorted_coords}
    return coord_dict

#转换为字典
x_left_dict = coords_to_dict_y(x_left_contour)
x_right_dict = coords_to_dict_y(x_right_contour)
#步骤2：找到两组坐标中共同的y值（交集）
common_ys = set(x_right_dict.keys()) & set(x_left_dict.keys())
common_ys = sorted(common_ys)  # 按y值从小到大排序
#计算共同Y值点对应的X中点
x_mid_points = []
for y in common_ys:
    x_left = x_left_dict[y]    # 左坐标在该y值的x
    x_right = x_right_dict[y]  # 右坐标在该y值的x
    mid_x = (x_left + x_right) // 2  # x中点
    x_mid_points.append([mid_x, y])    # 中点坐标

# 转换为numpy数组，便于OpenCV绘制
mid_points = np.array(x_mid_points, dtype=np.int32)
# 绘制中点（并连接成线）
cv2.polylines(draw_img, [mid_points], False, (255, 0, 255), 1)  # 中线：紫色

#处理后半段-------------------------
n_left_contour = left_contour[left_contour[:, 0] > 131]  # 左轮廓只保留x>131的点
n_right_contour = right_contour[right_contour[:, 0] > 131]  # 右轮廓只保留x>131的点
n_right_contour = right_contour[right_contour[:, 1] < 47]  # 右轮廓只保留y<45的点
def coords_to_dict_x(coords):
    # 按x值排序
    sorted_coords = coords[coords[:, 0].argsort()]
    # 转为字典 {x: y}，若有相同x值则取最后一个
    coord_dict = {x: y for x, y in sorted_coords}
    return coord_dict

n_left_dict = coords_to_dict_x(n_left_contour)
n_right_dict = coords_to_dict_x(n_right_contour)
#步骤2：找到两组坐标中共同的x值（交集）
common_xs = set(n_left_dict.keys()) & set(n_right_dict.keys())
common_xs = sorted(common_xs)  # 按x值从小到大排序
#计算共同x值点对应的y中点
n_mid_points = []
for x in common_xs:
    y_left = n_left_dict[x]    # 左坐标在该x值的y
    y_right = n_right_dict[x]  # 右坐标在该x值的y
    mid_y = (y_left + y_right) // 2  # y中点
    n_mid_points.append([x, mid_y])    # 中点坐标

# 转换为numpy数组，便于OpenCV绘制
n_mid_points = np.array(n_mid_points, dtype=np.int32)
# 绘制中点（并连接成线）
cv2.polylines(draw_img, [n_mid_points], False, (255, 0, 255), 1)  # 中线：紫色

mid_points = np.concatenate([n_mid_points, x_mid_points], axis=0)  # axis=0表示纵向拼接

#手动补点
cv2.line(draw_img, (137, 40), (105, 43), (255, 0, 255), 1)
cv2.line(draw_img, (105, 43), (102, 47), (255, 0, 255), 1)
cv2.line(draw_img, (97, 109), (97, 120), (255, 0, 255), 1)

print(mid_points)
print("------------------------------------------------------------------------------------------")
print(left_contour)
print("------------------------------------------------------------------------------------------")
print(right_contour)
#cv2.namedWindow("img", cv2.WINDOW_NORMAL)
cv_show("img", draw_img)


cv2.imwrite("new_opencv.png", draw_img)