import bpy
import sys
import os
sys.path.append('C:\\Users\\fujit\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\site-packages\\cv2')#cv2のパス
import cv2
import bmesh
import math
"""
レンダリングする
"""
# --- 設定（ここを変更） ---
output_folder = "J:\\suns3D_samples"    # 出力ファイル
engines = ["CYCLES","BLENDER_EEVEE","BLENDER_WORKBENCH"]
engen=2 #0:Cycles,1:EEVEE,2:Workbench
resolution_percentage = 100                    # 100 = フル解像度
samples = 128                                  # Cycles のサンプル数（EEVEEは別設定）
form="png"#komoji
frame_to_render = bpy.context.scene.frame_current  # レンダーするフレーム
camera_names=["Camera","Camera.002"]
resolution_xy=[(1608,1104),(3333,1104)]

for i in range(2):
    camera_name = camera_names[i]
    resolution_x = resolution_xy[i][0]
    resolution_y = resolution_xy[i][1]

    for obj in list(bpy.data.objects): 
        if obj.type == 'FONT': 
            if obj.name[-1] != "1":
                outfile=obj.name

    for obj in list(bpy.data.objects): 
        if obj.type == 'MESH':
            try:
                if (obj.name).split("\\")[-3]==outfile:
                    outfile=(obj.name).split("\\")[-3]+"_"+(obj.name).split("\\")[-2]+"_"+(obj.name).split("\\")[-1]
                    if i ==0:
                        outfile+="up"
                    elif i == 1:
                        outfile+="west"
            except:
                pass
                

    output_path=output_folder+"\\"+outfile+"."+form
    print(output_path)

    # --- 出力ディレクトリ作成 ---
    out_dir = os.path.dirname(output_path)
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    # --- カメラ取得とチェック ---
    cam = bpy.data.objects.get(camera_name)
    if cam is None or cam.type != 'CAMERA':
        raise ValueError(f"カメラが見つかりません: {camera_name}")

    engine=engines[engen]
    # --- レンダー設定 ---
    scene = bpy.context.scene
    scene.camera = cam
    scene.render.engine = engine
    scene.render.image_settings.file_format = 'PNG'  # PNGで保存
    scene.render.filepath = output_path
    scene.render.resolution_x = resolution_x
    scene.render.resolution_y = resolution_y
    scene.render.resolution_percentage = resolution_percentage

    form = form.upper()

    # --- 実行レンダー（単一フレーム） ---
    scene = bpy.context.scene
    scene.camera = cam
    scene.render.engine = engine
    scene.render.image_settings.file_format = form
    scene.render.filepath = output_path
    scene.render.resolution_x = resolution_x
    scene.render.resolution_y = resolution_y
    scene.render.resolution_percentage = resolution_percentage
    bpy.ops.render.render(write_still=True, use_viewport=False)



