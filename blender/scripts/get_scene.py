import bpy
import os
import json
import numpy as np
from scipy.spatial.transform import Rotation

def set_camera(camera_name, xyz, rpy):
    #Set camera position
    bpy.data.objects[camera_name].location = xyz
    bpy.data.objects[camera_name].rotation_euler = rpy

# Set light
light_name = 'Ceiling'
bpy.data.objects[light_name].location = (0,0,40)
bpy.data.objects[light_name].rotation_euler = (0,0,0)

# Set data path
FILE_PATH = os.path.realpath(__file__)
FILE_PATH = FILE_PATH.split('/')
FILE_PATH = '/'.join(FILE_PATH[:-3])

DATA_PATH = os.path.join(FILE_PATH, 'data/one_spin')
print(DATA_PATH)

# Get transform
with open(os.path.join(DATA_PATH, 'transforms.json'), 'r') as f:
    transforms = json.load(f)


# Set render resolution
bpy.context.scene.render.resolution_x = transforms['w']
bpy.context.scene.render.resolution_y = transforms['h']
bpy.context.scene.render.image_settings.file_format = 'PNG'

# Set camera paramerters

camera_name = 'Camera'
bpy.data.objects[camera_name].data.angle_x = transforms['fl_x']
bpy.data.objects[camera_name].data.angle_y = transforms['fl_y']


for frame in transforms['frames']:
    file_path = os.path.join(DATA_PATH, frame['file_path'])
    transform_matrix = np.asarray(frame['transform_matrix'])
    xyz = transform_matrix[:3, 3]
    rpy = transform_matrix[:3, :3]
    rpy = Rotation.from_matrix(rpy).as_euler('xyz', degrees=False)

    set_camera(camera_name, xyz, rpy)

    # Render Path
    bpy.context.scene.render.filepath = os.path.join(DATA_PATH,file_path)

    # Render scene
    bpy.ops.render.render(write_still=True)
