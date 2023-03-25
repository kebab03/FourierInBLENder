# This demo and the **Coding Druid** series is open source here:
# https://github.com/avantcontra/coding-druid

# You can find more articles, patches, and source code at:
# https://www.floatbug.com
# https://www.patreon.com/avantcontra

# Cheers~
# Contra


import bpy
import math
import numpy as np
from math import sin, cos

def get_grease_pencil(gpencil_obj_name='GPencil') -> bpy.types.GreasePencil:
    """
    Return the grease-pencil object with the given name. Initialize one if not already present.
    :param gpencil_obj_name: name/key of the grease pencil object in the scene
    """

    # If not present already, create grease pencil object
    if gpencil_obj_name not in bpy.context.scene.objects:
        # bpy.ops.object.gpencil_add(radius=1.0, align='WORLD', location=(0.0, 0.0, 0.0), rotation=(0.0, 0.0, 0.0), type='EMPTY')
        bpy.ops.object.gpencil_add(location=(0, 0, 0), type='EMPTY')
        # rename grease pencil
        bpy.context.scene.objects[-1].name = gpencil_obj_name

    # Get grease pencil object
    gpencil = bpy.context.scene.objects[gpencil_obj_name]

    return gpencil


def get_grease_pencil_layer(gpencil: bpy.types.GreasePencil, gpencil_layer_name='GP_Layer',
                            clear_layer=False) -> bpy.types.GPencilLayer:
    """
    Return the grease-pencil layer with the given name. Create one if not already present.
    :param gpencil: grease-pencil object for the layer data
    :param gpencil_layer_name: name/key of the grease pencil layer
    :param clear_layer: whether to clear all previous layer data
    """

    # Get grease pencil layer or create one if none exists
    if gpencil.data.layers and gpencil_layer_name in gpencil.data.layers:
        gpencil_layer = gpencil.data.layers[gpencil_layer_name]
    else:
        gpencil_layer = gpencil.data.layers.new(gpencil_layer_name, set_active=True)

    if clear_layer:
        gpencil_layer.clear()  # clear all previous layer data

    # bpy.ops.gpencil.paintmode_toggle()  # need to trigger otherwise there is no frame

    return gpencil_layer


# Util for default behavior merging previous two methods
def init_grease_pencil(gpencil_obj_name='GPencil', gpencil_layer_name='GP_Layer',
                       clear_layer=True) -> bpy.types.GPencilLayer:
    gpencil = get_grease_pencil(gpencil_obj_name)
    gpencil_layer = get_grease_pencil_layer(gpencil, gpencil_layer_name, clear_layer=clear_layer)
    return gpencil_layer


def draw_line(gp_frame, p0: tuple, p1: tuple):
    # Init new stroke
    gp_stroke = gp_frame.strokes.new()
    gp_stroke.display_mode = '3DSPACE'  # allows for editing
    gp_stroke.line_width = 50
    gp_stroke.material_index = 1
    # Define stroke geometry
    gp_stroke.points.add(count=2)
    gp_stroke.points[0].co = p0
    gp_stroke.points[1].co = p1
    return gp_stroke

        
def draw_sine(gp_frame, frame_index:int):
    # Init new stroke
    gp_stroke = gp_frame.strokes.new()
    gp_stroke.display_mode = '3DSPACE'  # allows for editing
   #gp_stroke.draw_cyclic = True        # closes the stroke
    gp_stroke.line_width = 50
    gp_stroke.material_index = 2
    # Define stroke geometry
    gp_stroke.points.add(count=SEGMENTS)
    for i in range(SEGMENTS):
        x = angle*i
        
        sum = 0
        for n in range(1, N, 2):
            sum += (math.sin(x * n) * 4/(n * math.pi))
            
        y = sum
       
        gp_stroke.points[i].co = (x, y, 0)

    return gp_stroke

def draw_sine_dot(gp_frame, frame_index:int):
    # Init new stroke
    gp_stroke = gp_frame.strokes.new()
    gp_stroke.display_mode = '3DSPACE'  # allows for editing
    #gp_stroke.draw_cyclic = True        # closes the stroke
    gp_stroke.line_width = 200
    gp_stroke.material_index = 1
    # Define stroke geometry
    gp_stroke.points.add(count=SEGMENTS)
    x = angle*stepPerframe * frame_index
    
    sum = 0
    for i in range(1, N, 2):
        sum += (math.sin(x * i) * 4/(i * math.pi))
            
    y = sum
   
    gp_stroke.points[0].co = (x, y, 0)

    return gp_stroke

def draw_circle(gp_frame, center: tuple, radius: float):
    # Init new stroke
    gp_stroke = gp_frame.strokes.new()
    gp_stroke.display_mode = '3DSPACE'  # allows for editing
    #gp_stroke.draw_cyclic = True        # closes the stroke
    gp_stroke.line_width = 50
    gp_stroke.material_index = 2
    # Define stroke geometry
    gp_stroke.points.add(count=SEGMENTS)
    for i in range(SEGMENTS):
        x = center[0] + radius*math.cos(angle*i)
        y = center[1] + radius*math.sin(angle*i)
        z = center[2]
        gp_stroke.points[i].co = (x, y, z)

    return gp_stroke

def draw_circle_multi(gp_frame, frame_index:int):
 
    for n in range(1, N, 2):
        sum = 0
        for i in range(1, n, 2):
            sum += (math.cos(angle* i * frame_index*stepPerframe) * 4/(i * math.pi))
        x = sum - 2.5
        
        sum = 0
        for i in range(1, n, 2):
            sum += (math.sin(angle* i * frame_index*stepPerframe) * 4/(i * math.pi))
        y = sum
        
        r = 4/(n*math.pi)
        draw_circle(gp_frame, (x, y, 0), r)

    return

def draw_circle_dot(gp_frame, frame_index:int):
    # Init new stroke
    gp_stroke = gp_frame.strokes.new()
    gp_stroke.display_mode = '3DSPACE'  # allows for editing
    #gp_stroke.draw_cyclic = True        # closes the stroke
    gp_stroke.line_width = 200
    gp_stroke.material_index = 1
    # Define stroke geometry
  
    gp_stroke.points.add(count=SEGMENTS)
    
    sum = 0
    for i in range(1, N, 2):
        sum += (math.cos(angle*stepPerframe * frame_index * i) * 4/(i * math.pi))
        
    x = sum - 2.5 #offset
    
    sum = 0
    for i in range(1, N, 2):
        sum += (math.sin(angle*stepPerframe * frame_index * i) * 4/(i * math.pi))
        
    y = sum
    
    gp_stroke.points[0].co = (x, y, 0)
    
    return gp_stroke

def draw_conected_line(gp_frame, frame_index:int):
    
    # p0
    sum = 0
    for i in range(1, N, 2):
        sum += (math.cos(angle* i * frame_index*stepPerframe) * 4/(i * math.pi))
    x = sum - 2.5
    
    sum = 0
    for i in range(1, N, 2):
        sum += (math.sin(angle* i * frame_index*stepPerframe) * 4/(i * math.pi))
    y = sum
    
    p0 = (x, y, 0)
    
    # p1
    x = angle* stepPerframe * frame_index
    
    sum = 0
    for i in range(1, N, 2):
        sum += (math.sin(x * i) * 4/(i * math.pi))
        
    y = sum
    
    p1 = (x, y, 0)
    
    draw_line(gp_frame, p0, p1)
    return


NUM_FRAMES = 100
SEGMENTS = 100
FRAMES_SPACING = 1  # distance between frames
N = 11

stepPerframe = SEGMENTS/NUM_FRAMES
angle = 2*math.pi/SEGMENTS  # angle in radians
    
bpy.context.scene.frame_start = 0
bpy.context.scene.frame_end = NUM_FRAMES*FRAMES_SPACING

gp_layer = init_grease_pencil()


for frame_index in range(NUM_FRAMES):
    gp_frame = gp_layer.frames.new(frame_index*FRAMES_SPACING)
    # do something with your frame
    draw_sine(gp_frame, frame_index)
    draw_sine_dot(gp_frame, frame_index)
    draw_circle_multi(gp_frame, frame_index)
    draw_circle_dot(gp_frame, frame_index)
    draw_conected_line(gp_frame, frame_index)








