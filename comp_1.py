# -*- coding: utf-8 -*-
"""
Created on Fri Nov 19 14:39:33 2021

@author: rober
"""

import os.path

import sounds

def bite_note(frequency, intervals):
    harmons = list(range(10, 0, -1))
    
    sound = lambda freq: sounds.harmonic_series(freq, harmons)
    # sound = lambda freq: sounds.sine(freq)
    
    waves = list()
    for interval in intervals:
        freq = frequency * interval
        wave = sound(freq)
        waves.append(wave)
    
    wave = sum(waves)
    hard_env = sounds.interval_envelope(0, 2)
    env = sounds.exponential_envelope(0, 14)
    sound = wave * env * hard_env
    
    return sound

def comp():
    notes = list()
    
    base = 440
    half_down = sounds.from_cents(-200)
    
    flat_minor = [1, 7/6, 3/2]
    
    notes.append(bite_note(base, flat_minor))
    notes.append(sounds.delayed(bite_note(base * half_down, flat_minor), 2))
    notes.append(sounds.delayed(bite_note(base, flat_minor), 2.5))
    
    sound = sum(notes)
    
    
    filename = os.path.join(sounds.DIR, 'comp_1.wav')
    sound.save(filename, 0, 3)

def main():
    comp()

if __name__ == '__main__':
    main()