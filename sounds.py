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

DIR = 'C:\\Users\\rober\\.spyder-py3\\Robert_Python\\Sounds'

class Sound:
    """
    Base class for sound.
    """
    def save(self, filename, start, stop, sample_rate=44100):
        num_samples = np.ceil((stop - start) * sample_rate)
        
        # convert to an integer
        num_samples = np.int64(num_samples)
        
        sampled = np.zeros(num_samples)
        
        for i in range(num_samples):
            time = start + i / sample_rate
            pressure = self.sample(time)
            sampled[i] = pressure
        
        wavio.write(filename, sampled, sample_rate, sampwidth=4)
    
    def __add__(self, other):
        if isinstance(other, Sound):
            return SumSound(self, other)
        
        other_sound = FuncSound(lambda time: other)
        return SumSound(self, other_sound)
    
    __radd__ = __add__
    
    def __mul__(self, other):
        if isinstance(other, Sound):
            return ProductSound(self, other)
        
        other_sound = FuncSound(lambda time: other)
        return ProductSound(self, other_sound)
    
    __rmul__ = __mul__
    
    # def __rmul__(self, other):
    #     return self * other

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
        if type(sound1) is ProductSound:
            self.sounds.extend(sound1.sounds)
        else:
            self.sounds.append(sound1)
        
        if type(sound2) is ProductSound:
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
def sine(frequency):
    """
    Return a sine wave.
    
    Parameters:
        frequency:
            The frequency of the wave, in hertz.
    
    Return:
        A sine wave with the given frequency.
    """
    return FuncSound(lambda time: np.sin(time * 2 * np.pi * frequency))

def triangle(frequency, num_harmonics=10):
    """
    Return a triangle wave, up to the given number of harmonics.
    
    Parameters:
        frequency:
            The frequency of the triangle wave.
        
        num_harmonics:
            How many harmonics to include.
    
    Return:
        A triangle wave with the given frequency and number of harmonics.
    """
    waves = list()
    for i in range(1, num_harmonics + 1):
        freq = i * frequency
        
        # I haven't implemented dividing sounds yet
        wave = sine(freq) * (1 / i)
        
        waves.append(wave)
    
    return sum(waves)

def harmonic_series(frequency, amplitudes):
    """
    Return a superposition of the harmonics of the given frequency.
    
    Parameters:
        frequency:
            The base frequency of the harmonic series.
        
        amplitudes:
            The amplitudes of the different harmonics.
    
    Return:
        A superposition of the harmonics of the given frequency.
    """
    waves = list()
    for i, amplitude in enumerate(amplitudes, 1):
        # Don't bother if the amplitude is zero
        if amplitude == 0:
            continue
        
        freq = i * frequency
        
        wave = sine(freq) * amplitude
        
        waves.append(wave)
    
    return sum(waves)

#################
#               #
#   Envelopes   #
#               #
#################

# this sounded interesting
# although it isn't actually a normal distribution

# return FuncSound(lambda time: np.exp(- (time - center) / spread) ** 2)

def normal_envelope(center, spread):
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
    return FuncSound(lambda time: np.exp(- ((time - center) / spread) ** 2))

def interval_envelope(start, stop):
    """
    Return an envelope that's one within an interval and zero elsewhere.
    
    Parameters:
        start:
            The start of the interval, in seconds.
        
        stop:
            The end of the interval, in seconds.
    
    Return:
        An envelope equal to one on the given interval and zero elsewhere.
    """
    return FuncSound(lambda time: 1 if start <= time <= stop else 0)

def exponential_envelope(start, decay):
    """
    Return an exponential decay envelope.
    
    Parameters:
        start:
            The start of the envelope.
        
        decay:
            The decay rate of the envelope.
    
    Return:
        An exponential decay envelope with the given start and decay rate.
    """
    return FuncSound(lambda time: 0 if time < start else\
                     np.exp((time - start) * -decay))


#######################
#                     #
#   Transformations   #
#                     #
#######################

def delay(t):
    """
    Return a delay of t seconds.
    
    Parameters:
        t:
            The amount of time to delay by, in seconds.
    
    Return:
        A delay of t seconds
    """
    return lambda sound: delayed(sound, t)

def delayed(sound, t):
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

# Some utilities
def to_cents(ratio):
    return 100 * np.log(ratio) / np.log(2 ** (1/12))

def from_cents(cents):
    return (2 ** (1/12)) ** (cents / 100)