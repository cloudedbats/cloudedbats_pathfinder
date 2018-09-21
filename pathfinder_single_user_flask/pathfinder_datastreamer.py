#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://cloudedbats.org
# Copyright (c) 2018 Arnold Andreasson 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import math
import time
import pathlib
import datetime
import numpy as np
import pandas as pd

from pathfinder_single_user_flask.dsp4bats import wave_file_utils
from pathfinder_single_user_flask.dsp4bats import time_domain_utils
from pathfinder_single_user_flask.dsp4bats import frequency_domain_utils
from pathfinder_single_user_flask.dsp4bats import sound_stream_manager

class PathfinderDataStreamer():
    """ """
    def __init__(self):
        """ """
        self.x_max = 0
        self.ix_max = 0
        #
        self.source = None
        self.process = None
        self.target = None
        self.stream_manager = None
                        
    def start_streaming(self):
        """ """
        self.source = SoundSourceReadFiles()
        self.process = SoundProcessFindPeaks()
        self.target = SoundTargetPeakBuffer()
        self.stream_manager = sound_stream_manager.SoundStreamManager(
                            self.source, 
                            self.process, 
                            self.target,
                            source_queue_max=200, # 20 = 10 sec.
                            target_queue_max=10000)
        #
        self.stream_manager.start_streaming()
    
    def stop_streaming(self):
        """ """
        if self.stream_managerself:
            self.stream_manager.stop_streaming()    
    
    def get_target_data(self):
        """ """
        return self.target.get_data()


class SoundSourceReadFiles(sound_stream_manager.SoundSourceBase):
    """ Base class for sound sources. Mainly files or streams. """
    
    def __init__(self):
        """ """
        super().__init__()
        
        self.sound_file_name = '../data/WURB-2_20160908T220024+0200_N57.6627E12.6393_TE384_part.wav'
        
        self.wave_reader = None
        
    def read_file(self):
        """ """
        if self.wave_reader is not None:
            self.wave_reader.close()
        #
        self.wave_reader = wave_file_utils.WaveFileReader(self.sound_file_name)
        self.samp_width = self.wave_reader.samp_width
        self.frame_rate = self.wave_reader.frame_rate
        self.sampling_freq = self.wave_reader.sampling_freq
        
    def source_exec(self):
        """ Called from base class. """        
        self._active = True
        self.read_file()
        #
        while self._active:
            buffer = self.wave_reader.read_buffer(buffer_size=int(self.sampling_freq/2)) # 0.5 sec.
            if len(buffer) > 0:
                self.push_item(buffer) #, skip_if_full=False)
#                 print('--- Source queue length: ', self.source_queue.qsize())
                
                time_to_sleep = len(buffer) / self.sampling_freq
#                 print('--- Time_to_sleep: ', time_to_sleep)
                time.sleep(time_to_sleep)
            else:
                # Read the file again.
                self.read_file()
#                 print('--- New file')
#                 self.push_item(None)
#                 self._active = False
        #
        self.push_item(None)


class SoundProcessFindPeaks(sound_stream_manager.SoundProcessBase):
    """ Base class for sound processing algorithms. """
    def __init__(self):
        """ """
        super().__init__()
        
        self.test = True
        self.test = False
    
    def process_exec(self):
        """ Called from base class. """
        # Settings.
        sampling_freq = 384000
        factor = 8000 # Factor is number of steps per sec.
        dbfs_limit = -55
        freq_window_size = 256
        kaiser_beta = 10 # 14
        #
        self._active = True
        x = 0.0
        y = 0.0
        ix = 0.0
        time_start = 0.0
        ix_space_counter = 0
        #
        spectrum_util = frequency_domain_utils.DbfsSpectrumUtil(window_size=freq_window_size,
                                                  window_function='kaiser',
                                                  kaiser_beta=kaiser_beta,
                                                  sampling_freq=sampling_freq)
        #
        while self._active:
            item = self.pull_item()
            if item is None:
                print('Process terminated.')
                self.push_item(None) # Terminate.
                self._active = False
            else:
                try:
                    signal = item
                    size = int(len(signal) / sampling_freq * factor) # 
                    jump = int(sampling_freq/factor)
                    matrix = spectrum_util.calc_dbfs_matrix(signal, matrix_size=size, jump=jump)
                    #
                    for index, spectrum_db in enumerate(matrix):
                        freq, amp = spectrum_util.interpolate_spectral_peak(spectrum_db)
                        if amp > dbfs_limit:
                            ix_space_counter = 20
                            x = time_start + index / factor
                            ix += 1.0/factor
                            amp = (amp + dbfs_limit) * 0.1
                            #
                            self.push_item((x,freq/1000.0, ix, amp)) #, skip_if_full=False)
                        else:
                            ix_space_counter -= 1
                            if ix_space_counter > 0:
                                ix += 1.0/factor
                    
                    # Calculate start time for next buffer.
                    time_start += len(signal) / sampling_freq
                    # Timebeat to enable scrolling when silent.
                    self.push_item((time_start,5, ix, 1)) 
                #
                except Exception as e:
                    print('Exception: ', e)
                        


class SoundTargetPeakBuffer(sound_stream_manager.SoundTargetBase):
    """ Base class for sound targets. Mainly files or streams. """
    def __init__(self):
        """ """
        super().__init__()
        
        self.target_list = []

    def get_data(self):
        """ """    
        x_list = [] 
        y_list = []
        ix_list = [] 
        amp_list = []
        
        # Copy
        list_copy = self.target_list[:]
        # Clear the old one.
        self.target_list = []
        #
        for x,y, ix, amp in list_copy:
            x_list.append(x)
            y_list.append(y)
            ix_list.append(ix)
            amp_list.append(amp)
        #
        return x_list, y_list, ix_list, amp_list
    
    def target_exec(self):
        """ Called from base class. """
        self._active = True
        #
        while self._active:
#             time.sleep(0.01)
            item = self.pull_item()
            if item is None:
                print('Target terminated.')                 
                self._active = False # Terminated.
            else:
                self.target_list.append(item)
                if len(self.target_list) > 10000:
                    self.target_list = []
                    print('----- CLEAR TARGET LIST -----')

