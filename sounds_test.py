# -*- coding: utf-8 -*-
"""
Created on Fri Nov 19 10:35:04 2021

@author: rober
"""

import os.path

import numpy as np
import wavio

import sine_wave
import sounds
    
DIR = 'C:\\Users\\rober\\.spyder-py3\\Robert_Python\\Sounds'

def times_test():
    config = sine_wave.Config(1, 20)
    times = sine_wave.get_time_array(config)
    print(times)

def sine_test():
    config = sine_wave.Config(1, 20)
    
    sine = sine_wave.get_sine_wave(config,
                                   frequency=2,
                                   amplitude=1,
                                   offset=0)
    
    for s in sine:
        print('{:.3f}'.format(s))

def sine_wav_test():
    width = 3
    rate = 44100
    
    config = sine_wave.Config(width, rate)
    
    freq = 220
    amplitude = 1.0
    
    sine1 = sine_wave.get_sine_wave(config,
                                    frequency=freq,
                                    amplitude=amplitude,
                                    offset=0)
    
    sine2 = sine_wave.get_sine_wave(config,
                                    frequency=freq*2,
                                    amplitude=amplitude,
                                    offset=0)
    
    sine = sine1 + sine2
    
    filename = os.path.join(DIR, 'sine.wav')
    wavio.write(filename, sine, rate, sampwidth=width)

def sum_of_sines_test():
    width = 3
    rate = 44100
    
    config = sine_wave.Config(width, rate)
    
    # The sine waves for a just-intoned major chord
    descs = ((220, 1, 0),
             (275, 1, 0),
             (330, 1, 0))
    
    sounds = sine_wave.get_sine_wave_superposition(config, descs)
    
    filename = os.path.join(DIR, 'chord.wav')
    wavio.write(filename, sounds, rate, sampwidth=width)

def harmonic_series_test():
    width = 0.2
    rate = 44100
    
    sample_width = 4
    
    config = sine_wave.Config(width, rate)
    
    # An A note
    base = 100
    
    # c = 5
    # s = 5
    # The amplitudes
    # amplitudes = list([max(0, 5-((x*x)/5)) for x in range(1, 20)])
    # amplitudes = list(range(1, 11))# + list(range(10, 0, -1))
    # amplitudes = list([max(np.exp(-(((n-c)/s)**2)) - 0.01, 0) for n in range(1, 101)])
    # for i, amplitude in enumerate(amplitudes, 1):
    #     print('{}: {:3f}'.format(i, amplitude))
    
    # amplitudes = [1] * 20
    
    # amplitudes = [0.1, 0.2, 0.3, 0.4, 0.4, 0.3, 0.2, 0.1]
    
    # amplitudes = [1, 2, 3, 4]
    amplitudes = [1, 2, 2.5, 3]
    
    sound1 = sine_wave.get_harmonic_series(config, base, amplitudes)
    sound2 = sound1 + sine_wave.get_harmonic_series(config, base*7/6, amplitudes)
    sound3 = sound1 + sine_wave.get_harmonic_series(config, base*6/5, amplitudes)
    sound4 = sound1 + sine_wave.get_harmonic_series(config, base*7/4, amplitudes)
    sound5 = sound1 + sine_wave.get_harmonic_series(config, base*9/5, amplitudes)
    # sound4 = sine_wave.get_harmonic_series(config, base*7/4, amplitudes)
    # sound5 = sine_wave.get_harmonic_series(config, base*2, amplitudes)
    
    # wave = [sound1, sound2, sound3, sound4, sound3, sound2]
    wave = [sound2, sound3, sound4, sound5]
    # end = [sound1] * 4
    
    sound = np.concatenate(wave * 20, axis=0)
    
    filename = os.path.join(DIR, 'series.wav')
    wavio.write(filename, sound, rate, sampwidth=sample_width)

def func_test():
    # wave = sounds.get_sine(440)
    # wave = sounds.get_triangle(440, num_harmonics=10)
    
    freq = 440
    # harmons = [1, 1/4, 1/9, 1/16, 1/25, 1/36]
    # harmons = [1, 4, 6, 4, 1]
    # harmons = list(range(4, 0, -1))
    
    harmons = list(range(10, 0, -1))
    
    sound = lambda freq: sounds.harmonic_series(freq, harmons)
    # sound = lambda freq: sounds.sine(freq)
    
    wave1 = sound(freq)
    
    # Make these start a bit later
    wave2 = sound(freq * (7/6))
    # wave2 = wave2 * sounds.interval_envelope(0, 3)
    # wave2 = sounds.delayed(wave2, 0.1)
    
    wave3 = sound(freq * (3/2))
    # wave3 = wave3 * sounds.interval_envelope(0, 3)
    # wave3 = sounds.delayed(wave3, 0.2)
    
    
    wave = wave1 + wave2 + wave3
    
    # env = sounds.get_normal_envelope(1, 0.05)
    hard_env = sounds.interval_envelope(0, 2)
    env = sounds.exponential_envelope(0, 15)
    sound = wave * env * hard_env
    
    filename = os.path.join(DIR, 'note.wav')
    sound.save(filename, 0, 2)

def main():
    # times_test()
    # sine_test()
    # sine_wav_test()
    # sum_of_sines_test()
    # harmonic_series_test()
    func_test()

if __name__ == '__main__':
    main()