# ---
# jupyter:
#   jupytext:
#     formats: py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.17.1
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# area_definition3.py で作成した
# ule_xy_points.csvを使い
# car.pngにプロットする
# 好き：青○
# 嫌い：赤○

# %%
import cv2
import pandas as pd

# ファイル名
img_path = "car.png"
csv_path = "rule_xy_points.csv"
output_path = "rule_likes_dislikes.png"

# 画像読み込み
img = cv2.imread(img_path)
if img is None:
    print(f"画像ファイル {img_path} が読み込めません。")
    exit()

# CSV読み込み
df = pd.read_csv(csv_path)

# 点を描く関数
def draw_points(img, points, color, radius=5, thickness=2):
    for (x, y) in points:
        cv2.circle(img, (int(x), int(y)), radius, color, thickness)

# likeとdislikeの座標を抽出
like_points = []
dislike_points = []

for idx, row in df.iterrows():
    # like座標はlike1_x, like1_y, like2_x, like2_y, ... 最大9まで対応
    for i in range(1, 10):
        x_col = f"like{i}_x"
        y_col = f"like{i}_y"
        if x_col in df.columns and y_col in df.columns:
            x, y = row[x_col], row[y_col]
            if pd.notnull(x) and pd.notnull(y):
                like_points.append((x, y))
    # dislike座標はDislike1_x, Dislike1_y, ... 同様に最大9まで
    for i in range(1, 10):
        x_col = f"Dislike{i}_x"
        y_col = f"Dislike{i}_y"
        if x_col in df.columns and y_col in df.columns:
            x, y = row[x_col], row[y_col]
            if pd.notnull(x) and pd.notnull(y):
                dislike_points.append((x, y))

# 描画（BGRカラー）
draw_points(img, like_points, (255, 0, 0))      # 青色（like）
draw_points(img, dislike_points, (0, 0, 255))   # 赤色（dislike）

# 画面に表示（ESCや任意キーで終了）
cv2.imshow("Likes (Blue) & Dislikes (Red)", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

# 画像ファイルとして保存
cv2.imwrite(output_path, img)
print(f"描画結果を {output_path} に保存しました。")
