# -*- coding: utf-8 -*-
"""
Created on Fri Nov 19 10:54:58 2021

@author: rober
"""

import numpy as np

class Config:
    def __init__(self, duration, sample_rate):
        self.duration = duration
        self.sample_rate = sample_rate

# Seems to work
def get_time_array(config, start=0):
    """
    Return an array containing the time at each sample.
    
    Parameters:
        config:
            The configuration of the audio.
        
        start:
            What time to start at.
    
    Return:
        an array containing the time at each sampling point.
    """
    num_samples = round(config.duration * config.sample_rate)
    
    # This will have the time value at each sample position 
    times = np.zeros([num_samples], dtype=np.float64)
    
    # How much time passes in each sample
    delta_t = 1 / config.sample_rate
    
    for i in range(num_samples):
        time = start + i * delta_t
        times[i] = time
    
    return times

# Seems to work
def get_sine_wave(config,
                   frequency,
                   amplitude=1,
                   offset=0):
    """
    Return an array containing a sine wave.
    
    Parameters:
        config:
            The configuration of the audio.
        
        frequency:
            The frequency of the sine wave, in hertz.
        
        amplitude:
            The amplitude of the sine wave.
        
        offset:
            What time the sine wave starts at, in periods.
    
    Return:
        A sine wave with the specified characteristics.
    """
    # Get a times array
    times = get_time_array(config)
    
    # Scale it so that you get the right sine wave after applying
    # the sine function
    scaled_times = times * 2 * np.pi * frequency
    
    # Add the offset
    scaled_times += offset * 2 * np.pi
    
    return np.sin(scaled_times) * amplitude

def get_sine_wave_superposition(config,
                                   wave_descs):
    """
    Return a sum of sine waves.
    
    Parameters:
        config:
            The configuration of the audio.
        
        wave_descs:
            The descriptions of each wave.
    
    Return:
        A sum of the given sine waves.
    """
    waves = list()
    for frequency, amplitude, offset in wave_descs:
        wave = get_sine_wave(config, frequency, amplitude, offset)
        waves.append(wave)
    
    return sum(waves)

def get_harmonic_series(config, base, amplitudes):
    """
    Return a harmonic series with the given amplitudes.
    
    Parameters:
        config:
            The configuration of the audio.
        
        base:
            The base frequency of the series.
        
        amplitudes:
            The amplitudes of each harmonic, starting with the base.
    
    Return:
        A superposition of the specified elements of the harmonic series.
    """
    
    # The wave descriptions
    descs = list()
    
    for i, amplitude in enumerate(amplitudes, 1):
        freq = i * base
        # print('{}: {:3f}'.format(freq, amplitude))
        descs.append([freq, amplitude, 0])
    
    return get_sine_wave_superposition(config, descs)

def blur(sound, blur_width):
    """
    Return a blurred version of the given sound. Suppresses very high frequencies.
    """