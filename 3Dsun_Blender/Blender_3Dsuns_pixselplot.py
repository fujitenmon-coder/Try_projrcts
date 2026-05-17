import bpy
import sys

sys.path.append("C:\\Users\\fujit\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\site-packages\\cv2")#popencvnopathwodecide
import cv2
import bmesh

inp_file="C:\\Users\\fujit\\OneDrive\\画像\\img00000001.tif"

#既存のメッシュオブジェクトをすべて削除
for mesh in bpy.data.meshes:
    bpy.data.meshes.remove(mesh)

    
# 画像をグレースケールで読み込む
img = cv2.imread(inp_file, cv2.IMREAD_GRAYSCALE)

# 明るさを2次元リストに変換
data = img.tolist()

vertex_coords=[]
for dd in range(len(data)):
    for d in range(len(data[dd])):
        ap=(dd,d,data[dd][d])
        
        vertex_coords.append(ap)
        
        
# 新しいメッシュとオブジェクトを作成
mesh = bpy.data.meshes.new("CustomMesh")
obj = bpy.data.objects.new("CustomObject", mesh)
bpy.context.collection.objects.link(obj)
bpy.context.view_layer.objects.active = obj

# BMeshを作成
bm = bmesh.new()

# 四角形の頂点座標（XY平面上の矩形）


# 頂点を追加してリストに保持
verts = [bm.verts.new(coord) for coord in vertex_coords]
bm.verts.ensure_lookup_table()

# 四角形の面を作成
#m.faces.new(verts)

# メッシュに反映
bm.to_mesh(mesh)
bm.free()

# 編集モードに切り替え
bpy.ops.object.mode_set(mode='EDIT')

# すべての面を選択（変換対象にする）
bpy.ops.mesh.select_all(action='SELECT')

# 面を三角面に変換
bpy.ops.mesh.quads_convert_to_tris()

# オブジェクトモードに戻す
bpy.ops.object.mode_set(mode='OBJECT')
