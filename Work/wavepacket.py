import numpy as np
import matplotlib.pyplot as plt

mass_electron = 9.109383e-31 #kg
hbar = 6.58212e-16 #eV-s

#initial conditions

def Gaussian(x, sigma, t):
    return np.exp(-(x-t)**2/(2*sigma**2))

def schrodinger_1D(x, t, v):
    """
    Solves the time-dependent Schrodinger equation in 1D

    Arguments
    _________

    x : array
        one-dimensional array for position of the Particle

    t : array
        one-dimensional array of time-steps for calculation

    v : float
        potential step

    """
    return None
