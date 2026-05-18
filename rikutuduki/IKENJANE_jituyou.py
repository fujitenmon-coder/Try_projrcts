from calendar import c
from encodings.punycode import T
from unicodedata import digit
from PIL import Image ,ImageDraw
import numpy as np
import tqdm
import cv2
import matplotlib.pyplot as plt
import time

def fill_checker_pattern(img, coords, color1=(255, 0, 0, 255), color2=(0, 0, 255, 255), alpha=255):
    """
    img: PIL.Image または numpy.ndarray (H, W, 4)
    coords: [(x, y), ...]
    """
    print("img type:", type(img))
    if isinstance(img, np.ndarray):
        print("img shape:", img.shape, "dtype:", img.dtype)

    print("coords sample:", coords[:10])
    if isinstance(img, np.ndarray) and img.ndim == 3 and img.shape[2] == 3:
        alpha = np.full((img.shape[0], img.shape[1], 1), 255, dtype=np.uint8)
        img = np.concatenate([img, alpha], axis=2)
    img = Image.fromarray(img, mode="RGBA")

    # coords を安全に整数タプルへ変換
    clean_coords = []
    for xy in coords:
        x, y = xy

        # NumPy 配列 → スカラー
        if hasattr(x, "__len__"):
            x = x[0]
        if hasattr(y, "__len__"):
            y = y[0]

        clean_coords.append((int(x), int(y)))

    coords = clean_coords

    # --- NumPy 配列なら PIL Image に変換 ---
    if isinstance(img, np.ndarray):
        if img.dtype != np.uint8:
            raise ValueError("NumPy画像は dtype=uint8 である必要があります")
        if img.ndim == 3 and img.shape[2] == 3:
        # RGB → RGBA に変換
            alpha = np.full((img.shape[0], img.shape[1], 1), 255, dtype=np.uint8)
            img = np.concatenate([img, alpha], axis=2)
        if img.ndim == 2:
            img = np.stack([img, img, img, np.full_like(img, 255)], axis=2)
        if img.shape[0] < img.shape[1] and img.shape[2] == 4:
            img = np.transpose(img, (1, 0, 2))

        img = Image.fromarray(img, mode="RGBA")

    draw = ImageDraw.Draw(img, "RGBA")
    for (x, y) in coords: 
        x = int(x)
        y = int(y)
    for (x, y) in coords:
        # チェッカー判定
        base_color = color1 if (x + y) % 2 == 0 else color2

        # アルファ上書き
        r, g, b, _ = base_color
        color = (r, g, b, alpha)

        draw.point((x, y), fill=color)

    return img


"""
===プログラムの仕組み===
1. TIFF画像を読み込み、一定以上の明るさのピクセルの座標をyet_listに格納
2. yet_listから陸続きのピクセルを探索し、G_listに格納
 2-1. yet_listから空でない最もindexの小さいリストの最初の要素を取得
 2-2. そのピクセルの上下左右のピクセルがyet_list内にあるか調べ、あればその座標をリストで取得
 2-3. 2-2で取得したピクセルについて、再び2-2を繰り返す
3. G_list内のピクセルのグループについて最も大きいものを太陽とする。(そのほかはノイズとする)
"""




#===画像パスの指定===
impath=r"j:\img1.tiff" #画像パスを指定







#===画像読み込み===
# TIFF画像を読み込む
img = Image.open(impath) 

print("img_dtype:", img.mode)
arr = np.array(img)# 画像をNumPy配列に変換
threshold = 10542#明るさの閾値自動化または手動で設定
positions = np.argwhere(arr >= threshold)# 条件を満たすピクセルの位置を取得
#処理する一定以上の明るさのピクセルをリスト化=yet_list
yet_list=[]
for i in range(arr.shape[0]):
    yet_list.append([])
for y, x in positions:
    yet_list[y].append(x)





#===関数の定義===
#リストの長さのリストを返す
def llen(l):
    return range(len(l))
#すべてのサブリストの要素数の合計をカウント(2Dリスト用)
def count_elements(lis):
    count = 0
    for sublist in lis:
        count += len(sublist)
    return count
#2Dlist内の空ではない最もindexの小さいリストの最初の要素を返す。
# yet_listに対してしか使わない
def serch_first(lis):
    for li in llen(lis):
        if lis[li] == []:
            pass
        else:
            return (lis[li][0],li)
#上下左右のピクセルがyet_list内にあるか調べ、あればその座標をリストで返す
def research_four_direction(lis,Zaho):
    X=Zaho[0]
    Y=Zaho[1]
    re_list=[]
    if X+1 in lis[Y]:#右
        re_list.append((X+1,Y))
    if X-1 in lis[Y]:#左
        if X-1>=0:
            re_list.append((X-1,Y))
    if Y+1<len(lis):#下
        if X in lis[Y+1]:
            re_list.append((X,Y+1))
    if Y-1>=0:#上
        if X in lis[Y-1]:
            re_list.append((X,Y-1))
    return re_list
#いろぬり
def ironuri(img,coods,color):
    for x, y in coods:
        img[y, x] = color
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
    return img
#チェッカーボードマスクを適用する関数
import cv2
import numpy as np

def apply_checkerboard_points(img, points,
                              color1=(255, 255, 255),
                              color2=(0, 0, 0)):
    """
    img    : BGR画像 (H, W, 3)
    points : [(y, x), (y, x), ...] もしくは shape=(N, 2) の配列
    color1, color2 : チェッカーの2色 (B, G, R)
    """

    out = img.copy()
    h, w = out.shape[:2]

    points = np.asarray(points)  # (N, 2)
    ys = points[:, 0]
    xs = points[:, 1]

    # 画像外の座標を除外（安全対策）
    valid = (ys >= 0) & (ys < h) & (xs >= 0) & (xs < w)
    ys = ys[valid]
    xs = xs[valid]

    # チェッカー判定
    checker = (xs + ys) % 2 == 0

    c1 = np.array(color1, dtype=np.uint8)
    c2 = np.array(color2, dtype=np.uint8)

    out[ys[checker], xs[checker]] = c1
    out[ys[~checker], xs[~checker]] = c2

    return out





#===メイン処理===
ti0= time.time()#処理時間計測開始
G_list=[]#yet_listの陸続きのピクセルのリスト2D
whi=count_elements(yet_list)#yet_listの要素数
first_element=whi#処理前のyet_listの要素数を保存
digit=len(str(whi))#処理時間計測用
til=ti0#処理時間計測用
yetlast=whi#処理時間計測用
ave=1#処理時間計測用
while whi>0:
    #要素数が0なら終了
    whi=count_elements(yet_list)
    if whi==0:
        break
    #陸続きのピクセルを探索
    even=[]#偶数回目のresesrch_four_directionで発見したピクセル
    odd=[]#奇数回目のresesrch_four_directionで発見したピクセル
    together=[]#一つのグループに属するピクセルのリスト
    even.append(serch_first(yet_list))
    yet_list[even[0][1]].remove(even[0][0])
    together.append(even[0])
    #陸続きのピクセルを1グループ探索
    pbar=tqdm.tqdm(total=whi)
    while len(even)+len(odd)>0: 
        for ev in even: 
            app=research_four_direction(yet_list,ev)
            if app!=[]:
                for a in app:
                    odd.append(a)
                    yet_list[a[1]].remove(a[0])
                    together.append(a)
                    pbar.update(1)
        yetnow=count_elements(yet_list)
        tin= time.time()
        ave=((ave*(whi-yetlast)+tin-til)/(whi-yetnow))
        """if yetlast!=yetnow:
            print("  yet_list length:", str(yetnow).zfill(digit),"/",whi,",prossesingtime:", np.around(tin-ti0,4),"sec,Estimated time remaining:", np.around(ave,4),"sec")"""
        yetlast=yetnow
        til=tin
        even.clear()
        for od in odd:
            app=research_four_direction(yet_list,od)
            if app!=[]:
                for a in app:
                    even.append(a)
                    yet_list[a[1]].remove(a[0])
                    together.append(a)
                    pbar.update(1)
        yetnow=count_elements(yet_list)
        tin= time.time()
        ave=((ave*(whi-yetlast)+tin-til)/(whi-yetnow))
        """if yetlast!=yetnow:
            print("  yet_list length:", str(yetnow).zfill(digit),"/",whi,",prossesingtime:", np.around(tin-ti0,4),"sec,Estimated time remaining:", np.around(ave,4),"sec")"""
        yetlast=yetnow
        til=tin
        odd.clear()
    G_list.append(together)#グループを収穫





#===デバック情報===
print("lenG_list:", len(G_list))
Gds=[]
coods=[]
for g in G_list:#G_list内のピクセル群を1Dリストに変換
    for gg in g:
        Gds.append(gg[0]*100000+gg[1])
        ha=int(gg[0]),int(gg[1])
        coods.append(ha)
for g in llen(Gds):#重複確認
    if g !=0:
        if Gds[g]==Gds[g-1]:
            print("重複発見:", Gds[g])
print("firsst_element:", first_element)   
print("img.mode:", img.mode)         
#print("Gds",sorted(Gds))
#print("coods",coods)

gking=0
for G in llen(G_list):#各グループの要素数を表示
    if len(G_list[G])>len(G_list[gking]):
        gking=G



truelist=G_list[gking]


#===結果の可視化===
img = cv2.imread(impath)


# --- 使用例 ---


result = fill_checker_pattern(
    img,
    coods,
    color1=(255, 0, 0, 255),
    color2=(0, 0, 255, 255),
    alpha=150
)




plt.imshow(result) 
plt.axis("off") 
plt.show(block=True)


