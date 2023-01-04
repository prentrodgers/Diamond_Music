import numpy as np
import numpy.testing as npt

# import copy
# import mido
# import time
from importlib import reload
# from IPython.display import Audio, display
import os
# import muspy
# import pandas as pd
import sys
import logging
# import ctcsound 
# commented out 12/15/22 due to problems loading ctcsound in some environments
# sys.path.insert(0, '/home/prent/Dropbox/Tutorials/coconet-pytorch/coconet-pytorch-csound')
# import piano as p
# import selective_stretching_codes as stretch
# import samples_used as su
# import subprocess
from fractions import Fraction
from numpy.random import default_rng
rng = np.random.default_rng()

# build the chord structures for the different modes for the 16 keys
      # build the 16 tone scales in each of the keys in the diamond. otonal first, then utonal
      # nested dictionary keys[mode][ratio_name] 
def build_all_ratios():
      for limit in ([31]): # calculate the size of tonality diamond to the 31-limit and create the array all_ratios.
            end_denom = limit + 1
            start_denom = (end_denom) // 2
            o_numerator = np.arange(start_denom, end_denom, 1) # create a list of overtones
            u_denominator = np.arange(start_denom, end_denom, 1) # create a list of undertones
            all_ratios = []
            for oton_root in u_denominator:
                  # print()
                  for overtone in o_numerator:
                        if overtone < oton_root: oton = overtone * 2
                        else: oton = overtone
                        all_ratios.append(oton / oton_root)
      return all_ratios

def build_ratio_strings(all_ratios):
      ratio_strings = np.array([str(Fraction(ratio).limit_denominator(max_denominator = 100)) for ratio in all_ratios]).reshape(16,16)
      i = 0
      for ratio in ratio_strings:
            j = 0
            for r in ratio:
                  if ratio_strings[i,j] == '1': 
                        ratio_strings[i,j] = '1/1'
                  j += 1
            i += 1
      return ratio_strings


stored_gliss = np.empty((0,70), dtype = float)
current_gliss_table = 800
all_ratios = build_all_ratios()
ratio_strings = build_ratio_strings(all_ratios)
all_ratio_strings = ratio_strings.reshape(256,)

keys = {'oton': {ratio_strings[0, 0]: np.arange(0 * 16, 1 * 16, 1),
                  ratio_strings[1 ,0]: np.arange(1 * 16, 2 * 16, 1),
                  ratio_strings[2 ,0]: np.arange(2 * 16, 3 * 16, 1),
                  ratio_strings[3 ,0]: np.arange(3 * 16, 4 * 16, 1),
                  ratio_strings[4 ,0]: np.arange(4 * 16, 5 * 16, 1),
                  ratio_strings[5 ,0]: np.arange(5 * 16, 6 * 16, 1),
                  ratio_strings[6 ,0]: np.arange(6 * 16, 7 * 16, 1),
                  ratio_strings[7 ,0]: np.arange(7 * 16, 8 * 16, 1),
                  ratio_strings[8 ,0]: np.arange(8 * 16, 9 * 16, 1),
                  ratio_strings[9 ,0]: np.arange(9 * 16, 10 * 16, 1),
                  ratio_strings[10, 0]: np.arange(10 * 16, 11 * 16, 1),
                  ratio_strings[11, 0]: np.arange(11 * 16, 12 * 16, 1),
                  ratio_strings[12, 0]: np.arange(12 * 16, 13 * 16, 1),
                  ratio_strings[13, 0]: np.arange(13 * 16, 14 * 16, 1),
                  ratio_strings[14, 0]: np.arange(14 * 16, 15 * 16, 1),
                  ratio_strings[15, 0]: np.arange(15 * 16, 16 * 16, 1)
                  },
            'uton': {ratio_strings[0, 0]: np.arange(0, 256, 16),
                  ratio_strings[0, 1]: np.arange(1, 256, 16),
                  ratio_strings[0, 2]: np.arange(2, 256, 16),
                  ratio_strings[0, 3]: np.arange(3, 256, 16),
                  ratio_strings[0, 4]: np.arange(4, 256, 16),
                  ratio_strings[0, 5]: np.arange(5, 256, 16),
                  ratio_strings[0, 6]: np.arange(6, 256, 16),
                  ratio_strings[0, 7]: np.arange(7, 256, 16),
                  ratio_strings[0, 8]: np.arange(8, 256, 16),
                  ratio_strings[0, 9]: np.arange(9, 256, 16),
                  ratio_strings[0, 10]: np.arange(10, 256, 16),
                  ratio_strings[0, 11]: np.arange(11, 256, 16),
                  ratio_strings[0, 12]: np.arange(12, 256, 16),
                  ratio_strings[0, 13]: np.arange(13, 256, 16),
                  ratio_strings[0, 14]: np.arange(14, 256, 16),
                  ratio_strings[0, 15]: np.arange(15, 256, 16)                 
                  }
                  }
      # build the 8 note scales for each of the rank A, B, C, D otonal and utonal out of the 16 note scales
#                                                        start, end, step size
# make this dictionary nested: rank, mode
scales = {'A': {'oton': np.array([note % 16 for note in np.arange(0, 16, 2)]),
                      'uton': np.array([note % 16 for note in np.arange(8, -8, -2)])}, # utonal goes down, so that the scale will go up.
                'B': {'oton': np.array([note % 16 for note in np.arange(2, 18, 2)]),
                      'uton': np.array([note % 16 for note in np.arange(14, -2, -2)])},
                'C': {'oton': np.array([note % 16 for note in np.arange(1, 17, 2)]),
                      'uton': np.array([note % 16 for note in np.arange(13, -2, -2)])},
                'D': {'oton': np.array([note % 16 for note in np.arange(3, 19, 2)]),
                      'uton': np.array([note % 16 for note in np.arange(15, 0, -2)])},
          # the next 8 are additional 8 note scales that have good 3:2, and interesting thirds
                'E': {'oton': np.array([ 2,  4,  6,  8, 11, 13, 15,  0]), # 3rd: 11:9 neutral
                      'uton': np.array([ 8,  6,  4,  2,  0, 15, 13, 11])}, # 3rd: 6:5 minor
                'F': {'oton': np.array([ 8, 10, 12, 14,  0,  2,  4,  6]), # 3rd: 7:6 subminor
                      'uton': np.array([ 0, 14, 12, 10,  8,  6,  4,  2])}, # 3rd: 8:7 subminor
                'G': {'oton': np.array([ 4,  6,  8, 10, 14, 15,  0,  2]), # 3rd: 6:5 minor
                      'uton': np.array([14, 10,  8,  6,  4,  2,  0, 15])}, # 3rd: 5:4 major
                'H': {'oton': np.array([12, 14,  0,  2,  5,  7,  9, 11]), # 3rd: 8:7 sub-subminor
                      'uton': np.array([5,  3,   1, 15, 12, 10,  8,  6])} # 3rd: 21/17 neutral
               }
      # this dictionary is helpful in doing a lookup of different inversions of a chord
# choose the notes in scale for each rank (A, B, C, D), mode (oton, uton), & inversion (1, 2, 3, 4)
# access the four note chords by specifying inversions[rank][mode][inv]
# where rank is in (A, B, C, D) mode is in (oton, uton), and inv is in (1, 2, 3, 4)
# use the resulting array as the index into a keys[mode][ratio]

inversions = {'A': {'oton': {1: np.array([0, 4, 8, 12]),
                             2: np.array([4, 8, 12, 0]),
                             3: np.array([8, 12, 0, 4]),
                             4: np.array([12, 0, 4, 8])},
                    'uton': {1: np.flip(np.array([0, 4, 8, 12])),
                             2: np.flip(np.array([4, 8, 12, 0])),
                             3: np.flip(np.array([8, 12, 0, 4])),
                             4: np.flip(np.array([12, 0, 4, 8]))}}, 
              'B': {'oton': {1: np.array([2, 6, 10, 14]),
                             2: np.array([6, 10, 14, 2]),
                             3: np.array([10, 14, 2, 6]),
                             4: np.array([14, 2, 6, 10])},
                    'uton': {1: np.flip(np.array([2, 6, 10, 14])),
                             2: np.flip(np.array([6, 10, 14, 2])),
                             3: np.flip(np.array([10, 14, 2, 6])),
                             4: np.flip(np.array([14, 2, 6, 10]))}}, 
              'C': {'oton': {1: np.array([1, 5, 9, 13]),
                             2: np.array([5, 9, 13, 1]),
                             3: np.array([9, 13, 1, 5]),
                             4: np.array([13, 1, 5, 9])},
                    'uton': {1: np.flip(np.array([2, 6, 10, 14])),
                             2: np.flip(np.array([6, 10, 14, 2])),
                             3: np.flip(np.array([10, 14, 2, 6])),
                             4: np.flip(np.array([14, 2, 6, 10]))}}, 
              'D': {'oton': {1: np.array([3, 7, 11, 15]),
                             2: np.array([7, 11, 15, 3]),
                             3: np.array([11, 15, 3, 7]),
                             4: np.array([15, 3, 7, 11])},
                    'uton': {1: np.flip(np.array([3, 7, 11, 15])),
                             2: np.flip(np.array([7, 11, 15, 3])),
                             3: np.flip(np.array([11, 15, 3, 7])),
                             4: np.flip(np.array([15, 3, 7, 11]))}},
              'E': {'oton': {1: np.array([ 2,  6, 11, 15]),
                             2: np.array([ 6, 11, 15,  2]),
                             3: np.array([11, 15,  2,  6]),
                             4: np.array([15,  2,  6, 11])},
                    'uton': {1: np.array([8,  4,  0, 13]),
                             2: np.array([4,  0, 13,  8]),
                             3: np.array([0, 13,  8,  4]),
                             4: np.array([8,  4,  0, 13])}},
              'F': {'oton': {1: np.array([ 8, 12,  0,  4]),
                             2: np.array([12, 0,  4, 8]),
                             3: np.array([ 0, 4, 8, 12]),
                             4: np.array([ 4, 8, 12,  0])},
                    'uton': {1: np.array([ 0, 12,  8,  2]),
                             2: np.array([12,  8,  2,  0]),
                             3: np.array([ 8,  2,  0, 12]),
                             4: np.array([ 2,  0, 12,  8])}},
              'G': {'oton': {1: np.array([ 4,  8, 14,  0]),
                             2: np.array([ 8, 14,  0,  4]),
                             3: np.array([14,  0,  4,  8]),
                             4: np.array([ 0,  4,  8, 14])},
                    'uton': {1: np.array([14,  8,  4,  0]),
                             2: np.array([ 8,  4,  0, 14]),
                             3: np.array([ 4,  0, 14,  8]),
                             4: np.array([ 0, 14,  8,  4])}},
              'H': {'oton': {1: np.array([12,  0,  5,  9]),
                             2: np.array([ 0,  5,  9, 12]),
                             3: np.array([ 5,  9, 12,  0]),
                             4: np.array([ 9, 12,  0,  5])},
                    'uton': {1: np.array([ 5,  1, 12,  8]),
                             2: np.array([ 1, 12,  8,  5]),
                             3: np.array([12,  8,  5,  1]),
                             4: np.array([ 8,  5,  1, 12])}}}

def build_scales(mode, ratio, rank):
      # print(f'{mode = }, {ratio = }, {rank = }')
      # if rank in (['A', 'B', 'C', 'D']):
      if ratio in keys[mode]: 
            scale = np.array([keys[mode][ratio][note] for note in (scales[rank][mode])])
      else: 
            print(f'in build_scales. Could not find {ratio = } with {mode} in {keys[mode] = } with {rank = }')
            scale = None
      return scale

def ratio_string_to_float(ratio):
      n, d = ratio.split('/')
      return float(float(n) / float(d))

def ratio_to_cents(ratio):
    return round(1200 * np.log(ratio)/np.log(2),1)

def cents_to_ratio(cents):
    return str(Fraction(np.power(2, cents/1200)).limit_denominator(max_denominator = 100))


def show_keys():
      return(keys)

def show_scales():
      return(scales)

def show_inversions():
      return(inversions)      
      
# note that this function tries to find the closest end note to the start note.
# It might be up or down, it might cross an octave boundary.
# for example, from 15:8 to 1:1 would ordinarily return 15:8 distance between the two notes, 
# but the closest one is from 15:8 to 2:1, moving up an octave, multiplying the second value by 2
# to accomodate that, the function tests the size of the ratio returned from the normal calculation,
# and multiplies either the start or the end note by 2 before recalculating the ratio.
# this can cause problems if you are looking for that large leap.
# You can override the default behavior by setting find_closest = False
def ratio_distance(start, end, find_closest = True):
      start_ratio = ratio_string_to_float(start)
      end_ratio = ratio_string_to_float(end)
      ratio = end_ratio / start_ratio 
      # print(f'calculated ratio is {ratio = }')
      if not find_closest: return (ratio)
      min_ratio = 0.75
      max_ratio = 1.50
      if min_ratio <= ratio <= max_ratio:
            return ratio
      else:
            # print(f'out of range: {round(ratio,2) = }')
            if ratio >= max_ratio: 
                  ratio = end_ratio / (start_ratio * 2)
            elif ratio <= min_ratio: 
                  ratio = end_ratio * 2 / start_ratio
            # print(f'new {round(ratio,2) = }')
      return ratio

# for each of the keys, build the chords from the scales created above.
# key is a string index into the keys dictionary: e.g. mode, ratio
# inversion is the string index into the inversions dictionary e.g. 'A_oton_1'
# the inversion includes the rank is which of the four tetrachords in each scale, A, B, C, or D
# And it specifies which note is on top

def build_chords(mode, root, rank, inversion):
      if type(inversion) != int: inversion = int(inversion)
      if (root in keys[mode]) and (inversion in inversions[rank][mode]): 
            chord = np.array([keys[mode][root][note] for note in (inversions[rank][mode][inversion])]) 
      else:
            print(f'in build_chords. Could not find {root = } with {mode = }, in {inversion = } ')
            chord = None
      return chord

# this function transform a note sequence dictionary into an array.
def array_from_dict(time_step_dict):
    
      time_step_array = np.empty((len(time_step_dict), len(time_step_dict["instrument"])), dtype = float) 
      # make sure you have the same number of values in each dictionary entry
      assert all([len(time_step_dict[time_step]) == len(time_step_dict["instrument"]) for time_step in time_step_dict.keys()]), "not all items in the note dictionary have the same quantity of notes"
    
      inx = 0
      for column in time_step_dict:
            time_step_array[inx] = time_step_dict[column]
            inx += 1
            

      return (time_step_array.T)      

# This function takes a table number, glissando type, and ratio and returns an array that can be passed to csound to bend a note
def make_ftable_glissando(t_num, gliss_type, ratio):
#                               +-- table number
#                               |       +-- start at time zero
#                               |       |    +-- size of the table
#                               |       |   |   +-- GEN07 type table, negative = don't normalize
#                               |       |   |   |   +-- start at 1:1, which is the current note
#                               |       |   |   |   |  +-- take this amount of time at 1:1 some portion of the note duration
#                               |       |   |   |   |  |   +-- stay at 1:1
#                               |       |   |   |   |  |   |  +-- take this long to reach the next 
#                               |       |   |   |   |  |   |  |   +-- target ratio, you want to go up or down this amount
#                               |       |   |   |   |  |   |  |   |      +-- stay at 2nd note this long
#                               |       |   |   |   |  |   |  |   |      |    +-- end at the target ratio, or 1 
#                               |       |   |   |   |  |   |  |   |      |    |
      if gliss_type == 'slide':
            fn_array = np.array([t_num, 0, 256, -7, 1, 64, 1, 64, ratio, 128, ratio])
      elif gliss_type == 'cubic16_16_224':
            fn_array = np.array([t_num, 0, 256, -6, 1, 16, np.average((1, ratio)), 16, ratio, 224, ratio])
      elif gliss_type == 'cubic32_32_192':
            fn_array = np.array([t_num, 0, 256, -6, 1, 32, np.average((1, ratio)), 32, ratio, 192, ratio])
      elif gliss_type == 'cubic64_64_128':
            fn_array = np.array([t_num, 0, 256, -6, 1, 64, np.average((1, ratio)), 64, ratio, 128, ratio])
      elif gliss_type == 'cubic96_96_64':
            fn_array = np.array([t_num, 0, 256, -6, 1, 96, np.average((1, ratio)), 96, ratio, 64, ratio])
      elif gliss_type == 'cubic112_112_32':
            fn_array = np.array([t_num, 0, 256, -6, 1, 112, np.average((1, ratio)), 112, ratio, 32, ratio])
      elif gliss_type == 'trill_1_step':
            fn_array = np.array([t_num, 0, 32, -7, 1, 16, 1, 0, ratio, 16, ratio])
      elif gliss_type == 'trill_2_step':
            fn_array = np.array([t_num, 0, 64, -7, 1, 16, 1, 0, ratio, 16, ratio, 0, 1, 16, 1, 0, ratio, 16, ratio])
      elif gliss_type == 'trill_3_step':
            fn_array = np.array([t_num, 0, 64, -7, 1, 13, 1, 0, ratio, 13, ratio, 0, 1, 13, 1, 0, ratio, 13, ratio, 0, 1, 12, 1])
      elif gliss_type == 'trill_4_step':
            fn_array = np.array([t_num, 0, 128, -7, 1, 16, 1, 0, ratio, 16, ratio, 0, 1, 16, 1, 0, ratio, 16, ratio, 0, 1, 16, 1, 0, ratio, 16, ratio, 0, 1, 16, 1, 0, ratio, 16, ratio])
      elif gliss_type == 'trill_6_step':
            fn_array = np.array([t_num, 0, 256, -7, 1, 21, 1, 0, ratio, 21, ratio, 0, 1, 22, 1, 0, ratio, 21, ratio, 0, 1, 21, 1, 0, ratio, 22, ratio, 0, 1, 21, 1, 0, ratio, 21, ratio, 0, 1, 22, 1, 0, ratio, 21, ratio, 0, 1, 21, 1, 0, ratio, 22, ratio]) 
      elif gliss_type == 'trill_8_step':
            fn_array = np.array([t_num, 0, 256, -7, 1, 16, 1, 0, ratio, 16, ratio, 0, 1, 16, 1, 0, ratio, 16, ratio, 0, 1, 16, 1, 0, ratio, 16, ratio, 0, 1, 16, 1, 0, ratio, 16, ratio, 0, 1, 16, 1, 0, ratio, 16, ratio, 0, 1, 16, 1, 0, ratio, 16, ratio, 0, 1, 16, 1, 0, ratio, 16, ratio, 0, 1, 16, 1, 0, ratio, 16, ratio])
      elif gliss_type == 'flat':
            fn_array = np.array([t_num, 0, 256, -7, 1, 256, 1]) # f799 0 256 -7 1 256 1 ; 799 = no change; 
      else: print(f'invalid gliss type: {gliss_type}')
            
      return fn_array    

# take a scale as indexes and return the ratios as strings
def show_scale_ratios(scale):
      for note in scale:
            return(all_ratio_strings[scale])

def start_logger(LOGNAME):
      if os.path.exists(LOGNAME):
            os.remove(LOGNAME) # make sure the log starts over with a fresh log file. Next line starts the logger.
      logger = logging.getLogger()
      fhandler = logging.FileHandler(filename=LOGNAME, mode='w')
      formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
      fhandler.setFormatter(formatter)
      logger.addHandler(fhandler)
      logger.setLevel(logging.DEBUG)      

def flushMessages(cs, delay=0):
      s = ""
      if delay > 0:
            time.sleep(delay)
      for i in range(cs.messageCnt()):
            s += cs.firstMessage()
            cs.popFirstMessage()
      return s

def printMessages(cs, delay=0):
    s = flushMessages(cs, delay)
    this_many = 0
    if len(s)>0:
        logging.info(s)            

# load the orchestra .csd file in to a long string that can be passed to csound
def load_csd(csd_file, strip_f0 = False):
      csd_content = ""
      lines = 0
      empty = False
      with open(csd_file,'r') as csd:
            while not empty:
                  skip = False
                  read_str = csd.readline()
                  empty = not read_str
                  lines += 1
                  if strip_f0:
                        if read_str.startswith('f0') or read_str.startswith('</CsScore') or read_str.startswith('</CsoundS'):
                              skip = True
                  if read_str.startswith('i') or read_str.startswith('t'):
                        skip = True
                  if not skip: csd_content += read_str
      csd.close()        
      return(csd_content, lines)

# start up an instance of csound so that you can pass commands to the started orchestra
# commented out 12/15/22 due to problems loading ctcsound in some environments
# def load_csound(csd_content):
#       cs = ctcsound.Csound()    # create an instance of Csound
#       cs.createMessageBuffer(0)    
#       cs.setOption('-odac') # live performance is the default
#       cs.setOption("-G")  # Postscript output
#       cs.setOption("-W")  # create a WAV format output soundfile
#       printMessages(cs)
#       cs.compileCsdText(csd_content)  # Compile Orchestra from String - already read in from a file 
      
#       # logging.info(csd_content)    
#       printMessages(cs)
#       cs.start()         # When compiling from strings, this call is necessary before doing any performing
#       flushMessages(cs)

#       pt = ctcsound.CsoundPerformanceThread(cs.csound()) # Create a new CsoundPerformanceThread, passing in the Csound object
#       pt.play()          # starts the thread, which is now running separately from the main thread. This 
#                         # call is asynchronous and will immediately return back here to continue code
#                         # execution.
#       return (cs, pt)

# send in two arrays of note indeciiss and it will build a set of gliss indeciis to move from one to the other
# for example, chord_1 = np.array([36, 40, 44, 32]), chord_2 = np.array([34, 38, 42, 46]), slide='slide'
# will return four slides for the four notes.
# meanwhile it will increment current_gliss_table with the last table number, and concatenate the gliss tables to stored_gliss

def build_slides(chord_1, chord_2, gliss_type = 'slide'):
      global current_gliss_table # what the next table number created should be
      global stored_gliss # collection of all the slides asked for so far
      assert chord_1.shape == chord_2.shape, print(f'{chord_1.shape = } is not equal to {chord_1.shape = }. Halting.')
      # print(f'\nIn build_slides. {stored_gliss.shape = }, {current_gliss_table = }')
      # make a glissando table for all the notes in the two chords (should be 4 per chord for a typical usage)
      new_gliss_tables = np.array([make_ftable_glissando(current_gliss_table + i, gliss_type, ratio_distance(all_ratio_strings[a],all_ratio_strings[b])) for i, (a, b) in enumerate(zip(chord_1, chord_2))])
      # print(f'after making gliss tables. {new_gliss_tables.shape = }, {[gliss[0] for gliss in new_gliss_tables]}') 
      return_table_nums = np.zeros(new_gliss_tables.shape[0]) # array of table numbers for the incoming chords. returned to caller. 
      inx = 0
      for gliss in new_gliss_tables: # for each of the most recently created slides
            found_one = False
            for stored_fn_array in stored_gliss: # check it against all the ones created previously
                  if np.allclose(stored_fn_array[1:gliss.shape[0]], gliss[1:gliss.shape[0]], rtol=1e-4): # pretty close
                        # print(f'found a match between this new gliss {gliss[0]} and the stored one {stored_fn_array[0]}')
                        found_one = True
                        gliss[0] = stored_fn_array[0] # save the number in the table array of the old table so you can use it later
                        return_table_nums[inx] = gliss[0] # save the position of the old table so you can return it to the caller
                  else: 
                        pass
                        # print(f'no match between incoming {gliss[0]} and old one {stored_fn_array[0]}')
            if not found_one:
                  return_table_nums[inx] = gliss[0] # if it's a new one, save its number
                  # print(f'no match found for incoming {gliss[0] = }.')
            # print(f'{return_table_nums[inx] = }')
            inx += 1
      # print(f'all the {return_table_nums = }')      
      # only store the tables that are new. If the table number is small, you don't need to store it because it's already stored
      new_gliss_tables = np.array([gliss for gliss in new_gliss_tables if gliss[0] >= current_gliss_table]) # trim to the new ones
      # already_stored = np.array([gliss for gliss in new_gliss_tables if gliss[0] < current_gliss_table]) # point to old ones
      # print(f'{new_gliss_tables.size = }') # 
      if new_gliss_tables.size > 0: # we have some to store
            new_tables = new_gliss_tables[:,0] # new tables that need to be stored
            # print(f'new glissandi to be stored: {new_tables.shape = }, {new_tables = }')
            this_call_tables = np.min((chord_1.shape[0], new_tables.shape[0])) # how many new slides are needed to be saved
            # print(f'storing {this_call_tables = } new tables')
            # we only want to increment this_call_tables by the new tables, not the ones that were found in older gliss tables.
            current_gliss_table += this_call_tables # add the lesser of the number of notes in chord_1 or chord_2
            pad_size = 70 - new_gliss_tables.shape[1] # subtract the length of the array of values in this table
            pad_gliss = np.ones((this_call_tables, pad_size), dtype = float) # padded with ones, not zeros. Zeros cause it to go to 0 Hz.
            new_gliss_tables = np.concatenate((new_gliss_tables, pad_gliss), axis = 1)
            # print(f'About to store this set of gliss tables in the stored gliss table.')
            # print(f'before adding new f tables: {stored_gliss.shape = }') 
            stored_gliss = np.concatenate((stored_gliss, new_gliss_tables))
            
            # print(f'{stored_gliss.shape = }')
            # print(f'after adding new f tables: {stored_gliss.shape = }')    
      else: # no new tables. All were found in existing f tables collection
            this_call_tables = 0 
      return return_table_nums 

# this is a function call to build an octave boost mask that can be applied to keep scales always moving up.
# scale is an array of (note,) 
# return a mask that indicates by a 1 that the note should be increased an octave, or a zero that it should not.
# this only works for scales going up. 
def build_scale_mask(scale):
      
      boost_octave = 1
      mask = np.zeros(scale.shape, dtype=int) # assume no increase
      prev_note = ratio_string_to_float(all_ratio_strings[scale[0]]) # this assumes shape in (note,) dangerous
      inx = 0
      boost_remaining = False
      
      for note in scale:
            current_note_ratio = ratio_string_to_float(all_ratio_strings[note])
            if current_note_ratio < prev_note or boost_remaining:
                  if current_note_ratio < prev_note and boost_remaining:
                        boost_octave += 1
                  mask[inx] = boost_octave
                  boost_remaining = True
            prev_note = current_note_ratio
            
            inx += 1
      return (mask)

def retrieve_gliss_tables():
      global stored_gliss 
      global current_gliss_table 
      return stored_gliss, current_gliss_table
  
def init_stored_gliss():
      global stored_gliss
      global current_gliss_table 
      stored_gliss = np.empty((0,70), dtype = float) # each slide is made of 11 values
      # #     - size type start         end
      # [800. 0. 256. -7. 1. 16. 1. 128. 1.125 112. 1.125]
      current_gliss_table = 800
      return stored_gliss

def update_gliss_table(gliss_table, current_gl):
      global stored_gliss
      global current_gliss_table 
      stored_gliss = gliss_table 
      current_gliss_table = current_gl     
      # print(f'{stored_gliss.shape = }, {current_gliss_table = }')
      return current_gliss_table