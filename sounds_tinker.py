# -*- coding: utf-8 -*-
"""
Created on Tue Aug 23 19:00:05 2022

@author: rober
"""

import os.path

# import numpy as np
# import wavio

# import sine_wave
import sounds

#DIR = 'C:\\Users\\rober\\.spyder-py3\\Robert_Python\\Sounds'
DIR = os.path.dirname(__file__)

def make_sound_1():
    # width = 1
    # rate = 44100
    # sample_width = 4
    
    # config = sine_wave.Config(width, rate)
    
    # A note
    # base = 620
    # base = 27
    
    # The relative amplitudes of the harmonics
    # harmons = [1, 1/2, 1/3, 1/4, 1/5]
    # harmons = [1, 1, 1, 1, 1, 1, 1/2, 1/3, 1/4, 1/5]
    # harmons = [1, .25, 0, 0, 0, .0015, .0015, .0015, 0.0015]
    
    # sound = sine_wave.get_harmonic_series(config, base, amplitudes)
    # sound = sounds.harmonic_series(base, harmons)
    
    # amps = {base:   1,
    #         base*2: .25,
    #         base*6: .0015,
    #         base*6.67: .001,
    #         base*7: .0015,
    #         base*7.5: .001,
    #         base*8: .0015,
    #         base*9: .0015,}
    
    # base = 2700
    base = 2000
    
    amps = {#base*7/9: .001,
            base: 1,
            # 2500: .05,
            5000: .2,
            }
    
    sound = sounds.sum_of_sines(amps)
    
    exp_env = sounds.exponential_envelope(.1, 30, before_decay=1)
    hard_env = sounds.interval_envelope(0, 1)
    
    sound = sound * hard_env * exp_env
    
    # sound = np.concatenate([sound] * 5, axis=0)
    
    num = 48
    
    filename = os.path.join(DIR, 'samples', 'sound_{}.wav'.format(num))
    if os.path.exists(filename):
        raise RuntimeError('File already exists: {}'.format(filename))
    
    with open(os.path.join(DIR,
                          'tries',
                          'harmons_{}.txt'.format(num)), 'w') as file:
        for freq, amp in amps.items():
            file.write('{}: {}\n'.format(freq, amp))
    
    sound.save(filename, 0, 2)
    # wavio.write(filename, sound, rate, sampwidth=sample_width)
    
def main():
    make_sound_1()

if __name__ == '__main__':
    main()