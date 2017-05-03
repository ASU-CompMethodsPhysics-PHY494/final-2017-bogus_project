For 2D Simulations:

-Leave boolean 'sim3D = False' as it is
-Create wavePacket object, insert arguments for latticeSize, simulation time, initial conditions (only accepts Gaussian), and whether or not you would like a "Harmonic" or "Infinite Box" potential.
-Change arguments in view.animateDataSet to reflect the file name (for the simulation gif), the dataset you want to run, and make sure sim3D is the last argument and correct boolean value



For 3D Simulations:

-Change boolean 'sim3D = False' to 'sim3D = True'
-Create wavePacket object, insert arguments for latticeSize, simulation time, initial conditions (only accepts Gaussian), and whether or not you would like a "Harmonic" or "Infinite Box" potential.
-Change arguments in view.animateDataSet to reflect the file name (for the simulation gif), the dataset you want to run, and make sure that sim3D is the last argument