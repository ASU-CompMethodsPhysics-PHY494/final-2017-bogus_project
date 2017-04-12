####################################################################################
### visualization.py
### Created by Brian Pickens, Nathan Chrisman, and Andrew Shurman
###
### Imports processed simulation dataset and animates it with matplotlib
### using frames created by the yt volume render package  
####################################################################################

import numpy as np
import yt


################################################################################
# Testing area - will be deleted later
resolution = 32
bboxSize = 1.5

testArray = np.zeros([resolution, resolution, resolution])
testArray[1:-1, 1:-1, 1:-1] = 0.1
testArray[6:-6, 6:-6, 6:-6] = 0
testArray[12:-12, 12:-12, 12:-12] = 0.5
testArray[14:-14, 14:-14, 14:-14] = 0.9

#testArray[:, :, :] = 
#testArray[:, :, :] = testArray[:, :, :] * np.cos(

testData = dict(density = (testArray, "g/cm**3"))
testbbox = np.array([[-bboxSize, bboxSize], [-bboxSize, bboxSize], [-bboxSize, bboxSize]])
ds = yt.load_uniform_grid(testData, testArray.shape, length_unit = "dimensionless", bbox = testbbox, nprocs = resolution)

sc = yt.create_scene(ds)
#im, sc = yt.volume_render(ds, 'density', fname='test_frame')

# From yt tutorial:
# Get a reference to the VolumeSource associated with this scene
# It is the first source associated with the scene, so we can refer to it
# using index 0.
source = sc[0]

# Colormap boundaries (min, max) (don't set any part to 0, it hates 0)
bounds = (0.01,1)
tf = yt.ColorTransferFunction(np.log10(bounds))
tf.add_layers(10, colormap='arbre')

source.tfh.tf = tf
source.tfh.bounds = bounds

#Our probability data is going to be low resolution, so this will prevent artifacts created as a consequence of that 
source.set_use_ghost_zones(True)

cam = sc.camera

#cam.zoom(0.4)
#sc.camera.set_lens('plane-parallel')
cam.set_lens('perspective')
cam.set_position([1, 1, 1])
#sc.camera.set_position(ds.domain_left_edge - 1.5)

# The width determines the opening angle
#cam.set_width(ds.domain_width)
frame = 0

for _ in cam.iter_rotate(2 * np.pi, 30, rot_vector = [1, 0, 0], rot_center = ds.domain_center):
    #sc.render()
    sc.save('Frames/test_frame{}'.format(frame), sigma_clip = 4)
    frame += 1

#sc.save('test_frame', sigma_clip = 4)
################################################################################



################################
### Begin createFrame2D()
################################
def createFrame2D():
    '''
    description
    '''
    return None
################################

    

################################
### Begin createFrame3D()
################################
def createFrame3D():
    '''
    description
    '''
    return None
################################



################################
### Begin animateFrames()
################################
def animateFrames():
    '''
    description
    '''
    return None
################################
