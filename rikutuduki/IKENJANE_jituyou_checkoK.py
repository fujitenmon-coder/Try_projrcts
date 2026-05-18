from calendar import c
from encodings.punycode import T
from unicodedata import digit
from PIL import Image
import numpy as np
import tqdm
import cv2
import matplotlib.pyplot as plt
import time
import sys
from skimage import measure

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
impath=r"J:\img1.tiff" #画像パスを指定






#===画像読み込み===
# TIFF画像を読み込む
img = cv2.imread(impath)
print(img[1000,1000])#デバック用
img = Image.open(impath) 
print("img_dtype:", img.mode)
print(img  )#デバック用
arr = np.array(img)# 画像をNumPy配列に変換
threshold = 21000#明るさの閾値自動化または手動で設定
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
    pbar=tqdm.tqdm(total=whi)#進捗表示用(追加)
    while len(even)+len(odd)>0 : 
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
        """if yetlast!=yetnow:愛着がわいてしまったので残していいですか
            print("  yet_list length:", str(yetnow).zfill(digit),"/",whi,",prossesingtime:", np.around(tin-ti0,4),"sec,Estimated time remaining:", np.around(ave,8),"sec")
        """
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
        """ if yetlast!=yetnow:
            print("  yet_list length:", str(yetnow).zfill(digit),"/",whi,",prossesingtime:", np.around(tin-ti0,4),"sec,Estimated time remaining:", np.around(ave,8),"sec")
        """ 
        yetlast=yetnow
        til=tin
        odd.clear()
    G_list.append(together)#グループを収穫





#===デバック情報===
print("lenG_list:", len(G_list))
Gds=[]
coods=[]
lg=0
for g in llen(G_list):
    if len(G_list[g])>lg:
        lg=len(G_list[g])
        gking=g
for g in llen(G_list):#G_list内のピクセル群を1Dリストに変換
    for gg in G_list[g]:
        Gds.append(gg[0]*100000+gg[1])
        ha=int(gg[0]),int(gg[1])
        if g==gking:
            coods.append(ha)
for g in llen(Gds):#重複確認
    if g !=0:
        if Gds[g]==Gds[g-1]:
            print("重複発見:", Gds[g])

print("firsst_element:", first_element)   
print("img.mode:", img.mode)         
#print("Gds",sorted(Gds))
#print("coods",coods)

#plt.imshow(img) 
plt.axis("off") 

#plt.show(block=True)




#===結果の可視化===
img = cv2.imread(impath)
#cv2.imshow("Image with Points", img)

color1 = (0, 0, 100)  # 赤（BGR）
color2 = (20, 20, 100)  # うす赤（BGR）
for x, y in coods:#いろぬり
    if (y+x)%2==0:
        img[y, x] = np.average([img[y, x], color2], axis=0).astype(np.uint8)
    else:
        img[y, x] = np.average([img[y, x], color1], axis=0).astype(np.uint8)
#cv2.imshow("Image with Points", img)
#plt.show(block=True)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
#plt.imsave(f"D:\\{impath.split('\\')[1]}_result_image.tiff", img)

plt.imshow(img) 
plt.axis("off") 

plt.show(block=True)



# -----------------------------
# 1. 画像と領域ピクセルのリスト
# -----------------------------
img = np.array(Image.open(impath))
#img = np.array(img)
# 例：領域に属するピクセル座標のリスト
# [(x, y), (x, y), ...] という形式を想定
region_pixels = coods

# -----------------------------
# 2. マスク画像を作成
# -----------------------------
# 画像サイズに合わせた 2D マスクを作る
h, w = img.shape[0], img.shape[1]
mask = np.zeros((h, w), dtype=np.uint8)

for x, y in region_pixels:
    mask[y, x] = 1   # (x, y) → mask[y, x]

# -----------------------------
# 3. 輪郭抽出
# -----------------------------
contours = measure.find_contours(mask, 0)

# -----------------------------
# 4. 画像上に輪郭を描画
# -----------------------------
fig, ax = plt.subplots()
ax.imshow(img)

for contour in contours:
    ax.plot(contour[:, 1], contour[:, 0], color='gray', linewidth=2)

plt.show()
