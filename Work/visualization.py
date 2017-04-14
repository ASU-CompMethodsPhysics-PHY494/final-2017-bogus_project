####################################################################################
### visualization.py
### Created by Brian Pickens, Nathan Chrisman, and Andrew Shurman
###
### Imports processed simulation dataset and animates it with matplotlib
### using frames created by the yt volume render package  
####################################################################################

import numpy as np
import yt
import imageio


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
def createFrames3D(dataSet, frameName = "default", rotation = 0):
    '''
    Called by animateDataSet()
    Generates animation frames for a 3D pi/2 rotation based on the data set inputted.
    dataSet needs to be passed in as a (total frames, box side length, box side length, box side length) shape array.
    
    ----- Arguments -----
    dataSet: numpy array of shape (frames, box side, box side, box side).
    frameName: Filename of the frames generated, without directories.
    rotation: gradual rotation occurs around the data set across all frames up until this point. BUG: only works for pi/2!
    
    ----- Returns -----
    Returns total frames rendered. Frames generated are stored in local Frames/3D directory.
    '''
    
    # Get relevant characteristics of the data set
    
    # The size of the box array does not change the size of the volume rendered. Bigger resolution = greater detail in volume
    resolution = int(len(dataSet[0, 0, 0]))
    totalFrames = int(len(dataSet[:]))
    
    # The bounding box of the volume rendered. This is arbitrary but used to position the camera around.
    bboxSize = 1.5
    boundingBox = np.array([[-bboxSize, bboxSize], [-bboxSize, bboxSize], [-bboxSize, bboxSize]])
    
    # What data values we care about rendering. Values outside (min, max) won't appear in rendering. 
    # Does not like 0! Don't do 0.
    bounds = (0.01,1)
    
    # Main rendering loop, each iteration will get us one frame.
    # BUGGED: Only works well when rotation = pi / 2
    for index in range(totalFrames):
    
        # ds is yt convention for dataset, sc is scene
        frameData = dict(density = (dataSet[index], "g/cm**3"))
        ds = yt.load_uniform_grid(frameData, dataSet[index].shape, length_unit = "dimensionless", bbox = boundingBox, nprocs = resolution)
        
        # 3D yt works in scenes. A scene is an infinite volume containing a dataSet ds to render, with a camera from which to render it from.
        sc = yt.create_scene(ds)

        # These values don't need to be calculated each step
        if index == 0:
            dataSetOrigin = ds.domain_center
            
            # tf = Transfer Function. This takes our 3D data and transcribes it to our 2D monitors. Reused for all frames.
            # Takes a long time to set up.. but we only need to do it once.
            # Prints a log error, ignore it
            tf = yt.ColorTransferFunction(np.log10(bounds))
            # A data point's final color is processed in layers of a colormap. We add the preset "Blues" colormap in 10 layers.
            tf.add_layers(10, colormap='Blues')    

        # tfh = transfer function helper. This is specific to our simple rendering needs. Speeds up rendering.
        source = sc[0]
        source.tfh.tf = tf
        source.tfh.bounds = bounds
        
        # Our probability data might be low resolution, so this will prevent artifacts created as a consequence of that 
        source.set_use_ghost_zones(True)

        # Camera manipulation
        cam = sc.camera
        #cam.resolution = 1024
        cam.set_lens('perspective')
        cam.north_vector = [0, 0, 1]
        cam.set_position([1.5, 1.5, 0.75])
        
        # Rotate method rotates the current data set by (progress towards last frame) * total rotation
        # This is the bugged portion of the loop. Adds a roll to the camera I can't find out how to fix.
        cam.rotate((index / totalFrames) * rotation, rot_vector = [0, 0, 1], rot_center = dataSetOrigin)
        #cam.yaw((index / totalFrames) * rotation, [0, 0, 1])
        # Sloppy correction to rotation roll.
        cam.roll(0.20 * (index / totalFrames) * rotation, dataSetOrigin)
        
        # Save away the frame.
        sc.save('Frames/3D/{0}{1}'.format(frameName, index), sigma_clip = 4)
        print('-------')
        
    return totalFrames
################################



################################
### Begin animateDataSet()
################################
def animateDataSet(animationName, dataSet, rotation, render3D = True):
    '''
    Generates an animated .mp4 of pre-rendered frames. Reads/writes in the local Frames directory.
    
    ----- Arguments -----
    animationName: Filename of the frames generated, without directories.
    dataSet: numpy array of shape (frames, box side, box side, box side).
    rotation: gradual rotation occurs around the data set across all frames up until this point. BUG: only works for pi/2!
    render3D: Works in Frames/3D if true, Frames/2D if false.
    
    ----- Returns -----
    Returns nothing. Animation is stored with its own frames.
    '''
    
    if render3D == True:
        totalFrames = createFrames3D(dataSet, animationName, rotation)
    else:
        createFrames2D()
    
    frameList = []
    for i in range(totalFrames):
        frameList.append('Frames/3D/{0}{1}.png'.format(animationName, i))
    
    with imageio.get_writer('Frames/3D/{}.gif'.format(animationName), mode='I', fps = 24) as writer:
        for frame in frameList:
            image = imageio.imread(frame)
            writer.append_data(image)
    
    return
################################



################################################################################
# Testing area - will be deleted later
resolution = 32
totalFrames = 68

testArray = np.zeros([totalFrames, resolution, resolution, resolution])
testArray[:, 1:-1, 1:-1, 1:-1] = 0.1
testArray[:, 6:-6, 6:-6, 6:-6] = 0
testArray[:, 12:-12, 12:-12, 12:-12] = 0.5
testArray[:, 14:-14, 14:-14, 14:-14] = 0.9

for i in range(totalFrames - 1):
    testArray[i] = testArray[i] * np.sin((i/totalFrames) * np.pi)

animateDataSet("test", testArray, (0.5 * np.pi), True)
################################################################################
