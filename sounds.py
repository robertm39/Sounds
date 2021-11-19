# -*- coding: utf-8 -*-
"""
Created on Fri Nov 19 13:06:08 2021

@author: rober
"""

import numpy as np

import wavio

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

class Sound:
    """
    Base class for sound.
    """
    def save(self, start, stop, filename, sample_rate=44100):
        num_samples = np.ceil((stop - start) * sample_rate)
        
        sampled = np.zeros(num_samples)
        
        for i in range(num_samples):
            time = start + i / sample_rate
            pressure = self.sample(time)
            sampled[i] = pressure
        
        wavio.write(filename, sampled, sample_rate, sampwidth=4)
    
    def __add__(self, other):
        return SumSound(self, other)
    
    def __mul__(self, other):
        if isinstance(other, Sound):
            return ProductSound(self, other)
        
        other_sound = FuncSound(lambda time: other)
        return ProductSound(self, other_sound)
    
    def __rmul__(self, other):
        return self * other

class SumSound(Sound):
    """
    The sum of multiple sounds.
    """
    def __init__(self, sound1, sound2):
        self.sounds = list()
        
        # Add these sounds to sounds,
        # unless they themselves are sums, then add their sounds to sounds
        if type(sound1) is SumSound:
            self.sounds.extend(sound1.sounds)
        else:
            self.sounds.append(sound1)
        
        if type(sound2) is SumSound:
            self.sounds.extend(sound2.sounds)
        else:
            self.sounds.append(sound2)
    
    def sample(self, time):
        return sum([s.sample(time) for s in self.sounds])

class ProductSound(Sound):
    """
    The product of multiple sounds.
    To be used for volume envelopes.
    """
    def __init__(self, sound1, sound2):
        self.sounds = list()
        
        # Add these sounds to sounds,
        # unless they themselves are sums, then add their sounds to sounds
        if type(sound1) is SumSound:
            self.sounds.extend(sound1.sounds)
        else:
            self.sounds.append(sound1)
        
        if type(sound2) is SumSound:
            self.sounds.extend(sound2.sounds)
        else:
            self.sounds.append(sound2)
    
    def sample(self, time):
        pressures = [s.sample(time) for s in self.sounds]
        pressure = 1
        for p in pressures:
            pressure *= p
        
        return pressure

class FuncSound(Sound):
    """
    A sound defined by a function.
    """
    def __init__(self, func):
        self.func = func
    
    def sample(self, time):
        return self.func(time)

##################################
#                                #
#   Functions that give sounds   #
#                                #
##################################

def delay(sound, t):
    """
    Return the given sound, delayed by the given time.
    
    Parameters:
        sound:
            The sound to delay.
        
        time:
            The amount of time the sound will be delayed by.
    
    Return:
        The given sound, delayed by the given time.
    """
    return FuncSound(lambda time: sound.sample(time-t))

def get_sine(frequency):
    """
    Return a sine wave.
    
    Parameters:
        frequency:
            The frequency of the wave, in hertz.
    
    Return:
        A sine wave with the given frequency.
    """
    return FuncSound(lambda time: np.sin(time * 2 * np.pi * frequency))

def get_normal_envelope(center, spread):
    """
    Return a volume envelope with a normal curve.
    
    Parameters:
        center:
            The center of the normal curve.
        
        spread:
            How spread out the curve is.
    
    Return:
        A volume envelope with a normal curve.
    """
    return FuncSound(lambda time: np.exp(- (time - center) / spread) ** 2)