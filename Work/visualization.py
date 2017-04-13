####################################################################################
### visualization.py
### Created by Brian Pickens, Nathan Chrisman, and Andrew Shurman
###
### Imports processed simulation dataset and animates it with matplotlib
### using frames created by the yt volume render package  
####################################################################################

import numpy as np
import yt



################################
### Begin createFrames2D()
################################
def createFrames2D():
    '''
    description
    '''
    return None
################################

    

################################
### Begin createFrames3D()
################################
def createFrames3D(dataSet, totalFrames = 10, rotation = 0):
    '''
    Generates animation frames for a 3D pi/2 rotation based on the data set inputted.
    
    ----- Arguments -----
    dataSet: 3D cubic numpy array.
    totalFrames: Number of frames. More frames means smoother animation. Recommend 24 per second.
    rotation: gradual rotation occurs around the data set across all frames up until this point.
    
    ----- Returns -----
    Returns nothing. Frames generated are stored in local Frames/3D directory.
    '''
    
    # 
    resolution = int(len(dataSet[0, 0, 0]))
    bboxSize = 1.5
    boundingBox = np.array([[-bboxSize, bboxSize], [-bboxSize, bboxSize], [-bboxSize, bboxSize]])
    bounds = (0.01,1)
    
    for index in range(totalFrames):
        frameData = dict(density = (dataSet[index], "g/cm**3"))
        ds = yt.load_uniform_grid(frameData, dataSet[index].shape, length_unit = "dimensionless", bbox = boundingBox, nprocs = resolution)
        sc = yt.create_scene(ds)

        # These values don't need to be calculated each step
        if index == 0:
            dataSetOrigin = ds.domain_center
            # Throws a log error, ignore it
            tf = yt.ColorTransferFunction(np.log10(bounds))
            tf.add_layers(10, colormap='Blues')    

        source = sc[0]
        source.tfh.tf = tf
        source.tfh.bounds = bounds
        # Our probability data might be low resolution, so this will prevent artifacts created as a consequence of that 
        source.set_use_ghost_zones(True)

        cam = sc.camera
        #cam.resolution = 1024
        cam.set_lens('perspective')
        cam.north_vector = [0, 0, 1]
        cam.set_position([1.5, 1.5, 0.75])
        
        cam.rotate((index / totalFrames) * rotation, rot_vector = [0, 0, 1], rot_center = dataSetOrigin)
        #cam.yaw((index / totalFrames) * rotation, [0, 0, 1])
        
        sc.save('Frames/3D/test_frame{}'.format(index), sigma_clip = 4)
        print('-------')
        
    return
################################



################################
### Begin animateFrames()
################################
def animateFrames(targetDirectory, render3D = True):
    '''
    description
    '''
    return None
################################



################################################################################
# Testing area - will be deleted later
resolution = 32
bboxSize = 1.5

testArray = np.zeros([25, resolution, resolution, resolution])
testArray[:, 1:-1, 1:-1, 1:-1] = 0.1
testArray[:, 6:-6, 6:-6, 6:-6] = 0
testArray[:, 12:-12, 12:-12, 12:-12] = 0.5
testArray[:, 14:-14, 14:-14, 14:-14] = 0.9

#testArray[1, 12:-12, 12:-12, 12:-12] = 0

createFrames3D(testArray, 7, (0.5 * np.pi))
################################################################################
