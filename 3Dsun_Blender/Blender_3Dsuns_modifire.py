import bpy
import sys
import os
sys.path.append('C:\\Users\\fujit\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\site-packages\\cv2')#cv2のパス
import cv2
import bmesh
import math
""""
Blenderで画像を3D化して、テキストオブジェクトを追加し、指定したカメラからレンダリングして保存するスクリプトです。
-Displaceモディファイアを使用して、画像の明るさに基づいてメッシュを変形します。解像度は完ぺきではありません。
-すでに保存先に同名のファイルがある場合は保存されません。保存先のファイル名は、画像ファイル名をベースにして、カメラの位置（up,west）を付加したものになります。
"""
inp_file=r"J:\2025-07-19Z\2025-07-19-PL\2025-07-19-PL1\img00000010.tiff"#3D化する画像のパス
obj_name=inp_file
#既存のメッシュオブジェクトをすべて削除
for mesh in bpy.data.meshes:
    bpy.data.meshes.remove(mesh)
#既存のテキストオブジェクトをすべて削除
removed = [] 
for obj in list(bpy.data.objects): 
    if obj.type == 'FONT': 
        removed.append(obj.name) # オブジェクトをデータブロックから削除（シーンからも自動で外れる） 
        bpy.data.objects.remove(obj, do_unlink=True)

# 画像をグレースケールで読み込む
img = cv2.imread(inp_file, cv2.IMREAD_GRAYSCALE)
image = bpy.data.images.load(inp_file)
width, height = image.size
# 明るさを2次元リストに変換
data = img.tolist()
# グリッドを作成して、サイズを画像のアスペクト比に合わせる
Y,X=len(data),len(data[0])
obj=bpy.ops.mesh.primitive_grid_add(x_subdivisions=X, y_subdivisions=Y,size=2, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, X/Y, 1))
bpy.context.object.scale[0]=width/height
bpy.context.object.color = (0.677398, 0.252542, 0, 1)
bpy.context.object.show_name = True
obj = bpy.data.objects.get('Grid')#グリッドオブジェクトの名前を画像ファイル名にset
obj.name=inp_file

# オブジェクト取得
obj = bpy.data.objects.get(obj_name)
if obj is None:
    raise ValueError(f"オブジェクトが見つかりません: {obj_name}")

# 画像存在チェックと読み込み
if not os.path.exists(inp_file):
    raise FileNotFoundError(f"画像が見つかりません: {inp_file}")
img = bpy.data.images.load(inp_file)

# IMAGEタイプのテクスチャを作成して画像を割り当て
tex_name = "DisplaceImageTex"
tex = bpy.data.textures.get(tex_name) or bpy.data.textures.new(tex_name, type='IMAGE')
tex.image = img

# UVが無ければ自動でUV展開（Edit ModeでSmart UV Project）
mesh = obj.data
if not mesh.uv_layers:
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.uv.smart_project(angle_limit=66.0, island_margin=0.02)
    bpy.ops.object.mode_set(mode='OBJECT')

# Displaceモディファイアを追加してテクスチャを割り当て
mod = obj.modifiers.new(name="MyDisplace", type='DISPLACE')
mod.texture = tex
mod.texture_coords = 'UV'
mod.direction = 'NORMAL'
mod.strength = 0.5
mod.mid_level = 0.0

back=bpy.ops.mesh.primitive_plane_add(enter_editmode=False, align='WORLD', location=(-2, 0, 0), rotation=(0, 1.5708, 0), scale=(1, 1, 1))

locationas=[(-2, 0, 0.5),(0,0.8,1.5)]
rotations=[(90,0,90),(0,0,0)]
for i in range(2):
    # --- 設定 ---
    text_string = inp_file.split("\\")[-3]       # 表示する文字列
    location = locationas[i]           # オブジェクトの座標 (x, y, z)
    rotation_euler = (math.radians(rotations[i][0]), 0.0, math.radians(rotations[i][2]))  # 回転（ラジアン）
    object_scale = (0.15,0.15,0.15)       # オブジェクトのスケール
    font_size = .5                     # テキストのフォントサイズ（obj.data.size）
    extrude = 0.05                       # 立体化の厚み（obj.data.extrude）

    # --- 既存の選択をクリアしてテキストを追加 ---
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.text_add(location=location, rotation=rotation_euler)
    txt_obj = bpy.context.active_object

    # --- テキスト内容とプロパティを設定 ---
    txt_obj.data.body = text_string
    txt_obj.scale = object_scale
    txt_obj.data.size = font_size
    txt_obj.data.extrude = extrude

    # --- オブジェクト名を変更（任意） ---
    txt_obj.name = text_string



