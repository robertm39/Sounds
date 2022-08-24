# -*- coding: utf-8 -*-
"""
Created on Tue Aug 23 20:38:39 2022

@author: rober
"""

import wave

# The wave module seems to work fine
def main():
    filename = 'recordings/deg_2.wav'
    
    sound = wave.open(filename, 'rb')
    params = sound.getparams()
    print(params)
    print(sound.readframes(1))
    
    out_filename = 'recordings/deg_2_copy.wav'
    out_sound = wave.open(out_filename, 'wb')
    out_sound.setparams(params)
    out_sound.writeframes(sound.readframes(params.nframes))
    
    sound.close()
    out_sound.close()
    
if __name__ == '__main__':
    main()