# -*- coding: utf-8 -*-
"""
Created on Fri Nov 19 13:06:08 2021

@author: rober
"""

import numpy as np

# Instead of being numpy arrays,
# sounds will be functions from time to pressure
# unbounded both ways
# sounds will be sampled only at the end
# and the sampling rate can be adapted

# there will be transformations that take a sound or multiple sounds
# and return a new sound
# due to how sounds are represented, these are lazily evaluated

# the sound interface:
# sound.sample(float) -> float
# sounds support addition with other sounds
# and multiplication by numbers and other sounds

def get_sine(frequency):
    """
    Return a sine wave.
    
    Parameters:
        frequency:
            The frequency of the wave, in hertz.
    """
    return Sound(lambda time: np.sin(time * 2 * np.pi * frequency))

class SumSound:
    def __init__(self, sound1, sound2):
        self.sounds = list()

class Sound:
    def __init__(self, func):
        self.func = func
    
    def sample(self, time):
        return self.func(time)
    
    def __add__(self, other):
        return SumSound(self, other)