#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 12:34:39 2020

@author: sama
"""
import math
import numpy as np
import matplotlib.pylab as plt
from matplotlib.widgets import Slider, TextBox
#import scipy.signal as signal
from matplotlib.ticker import FormatStrFormatter

plt.rcParams.update({'font.size': 10})
#%%
plt.close("all")

signal_freq_color = 'powderblue'
super_freq_color = 'cornflowerblue'
cutOff_freq_color = 'gold'
filter_taps_color = 'thistle'
title_color = 'goldenrod'
safe_color = 'yellowgreen'
warning_color = 'lightcoral'

num_samples = 5000

cutOff1_freq = 3.8 # initial value
cutOff2_freq = 2.4 # initial value
signal1_freq = 4.1
signal2_freq = 2.0
sampling_freq = 10 # initial value
nyquist_freq = sampling_freq/2

nTaps = 11


def doTheMath(sampling_freq, cutOff1_freq, cutOff2_freq, signal1_freq, signal2_freq, nTaps):
    bandWidth = 0
    nyquist_freq = sampling_freq/2
    
    endTime = 1 # plot only 1 second of signals
    time = np.linspace(0, endTime , num_samples)
    cutOff1Wave = np.sin(cutOff1_freq * 2 * np.pi * time)
    cutOff2Wave = np.sin(cutOff2_freq * 2 * np.pi * time)
    signal1 = np.sin(signal1_freq  * 2 * np.pi * time)
    signal2 = np.sin(signal2_freq  * 2 * np.pi * time)
    
    taps = np.arange(0, nTaps ,1, dtype = np.int)
    
    cutOff2_tap = ((cutOff2_freq/sampling_freq) * (nTaps-1))
    cutOff2_tap_mirror = (nTaps - cutOff2_tap)
    cutOff1_tap = ((cutOff1_freq/sampling_freq) * (nTaps-1))
    cutOff1_tap_mirror = (nTaps - cutOff1_tap)
    
    signal2_tap = ((signal2_freq/sampling_freq) * (nTaps-1))
    signal2_tap_mirror = (nTaps - signal2_tap)
    signal1_tap = ((signal1_freq/sampling_freq) * (nTaps-1))
    signal1_tap_mirror = (nTaps - signal1_tap)
    
    freq_axis = np.linspace(0, sampling_freq , nTaps, endpoint = False)
    freq_resolution = freq_axis[1]-freq_axis[0]
    
    freqs = np.array([cutOff1_freq, cutOff2_freq, signal1_freq, signal2_freq])
    freq_diffs = np.zeros(6)
    
    freq_diffs[0] = np.abs(freqs[0] - freqs[1])
    freq_diffs[1] = np.abs(freqs[0] - freqs[2])
    freq_diffs[2] = np.abs(freqs[0] - freqs[3])
    freq_diffs[3] = np.abs(freqs[1] - freqs[2])
    freq_diffs[4] = np.abs(freqs[1] - freqs[3])
    freq_diffs[5] = np.abs(freqs[2] - freqs[3])
    
    min_diff = min(freq_diffs)
    #print(freq_resolution)
    
    ideal_spect_X = np.arange(0, nTaps, 1, dtype = np.int)
    
    idea_spect_Y = np.ones(len(ideal_spect_X))
    min_cutoff = min(int(round(cutOff1_tap)), int(round(cutOff2_tap)))
    max_cutoff = max(int(round(cutOff1_tap)), int(round(cutOff2_tap)))
    min_cutoff_mirror = min(int(round(cutOff1_tap_mirror)), int(round(cutOff2_tap_mirror)))
    max_cutoff_mirror = max(int(round(cutOff1_tap_mirror)), int(round(cutOff2_tap_mirror)))
    idea_spect_Y[min_cutoff : max_cutoff+1] = 0.05
    idea_spect_Y[min_cutoff_mirror : max_cutoff_mirror+1] = 0.05
        #      0                1               2         3      4             5       6        7               8                9             10                   11         12             13           14          15         16       17         18              19               20             21                  22          23
    return sampling_freq, cutOff1_freq, cutOff2_freq, time, cutOff1Wave, cutOff2Wave, taps, cutOff2_tap, cutOff2_tap_mirror, cutOff1_tap, cutOff1_tap_mirror, freq_axis, ideal_spect_X, idea_spect_Y, nyquist_freq, bandWidth, signal1, signal2, signal2_tap, signal2_tap_mirror, signal1_tap, signal1_tap_mirror, freq_resolution,min_diff                                

allData = doTheMath(sampling_freq, cutOff1_freq, cutOff2_freq, signal1_freq, signal2_freq, nTaps)

sampling_freq = allData[0]
cutOff1_freq = allData[1]
cutOff2_freq = allData[2]
time = allData[3]
cutOff1Wave = allData[4]
cutOff2Wave = allData[5]
taps = allData[6]
cutOff2_tap = allData[7]
cutOff2_tap_mirror = allData[8]

cutOff1_tap = allData[9]
cutOff1_tap_mirror = allData[10]

freq_axis = allData[11]
idea_spect_X = allData[12]
idea_spect_Y = allData[13]

nyquist_freq = allData[14]
nyquist_freq_tap = (nTaps)/2
bandWidth = allData[15]

signal1 = allData[16]
signal2 = allData[17]
superWave = cutOff1Wave + cutOff2Wave + signal1 + signal2

signal2_tap= allData[18]
signal2_tap_mirror= allData[19]
signal1_tap= allData[20]
signal1_tap_mirror = allData[21]


freq_resolution = allData[22]
min_diff = allData[23]

fig = plt.figure('Interactive filter demonstration')
fig.subplots_adjust(bottom=0.35)

sliders_left = 0.125
sliders_bottom = 0.15
sliders_width = 0.03
sliders_length = 0.25


cutOff_left_freq_axesslider = fig.add_axes([sliders_left, sliders_bottom - 1 * 0.05, sliders_length, sliders_width])
cutOff_left_freq_slider = Slider(cutOff_left_freq_axesslider, 'Noise1 Freq. [Hz]: ', 1.00, 10.00, 
                              valinit = cutOff2_freq, color = cutOff_freq_color)

cutOff_right_freq_axes = fig.add_axes([sliders_left + sliders_length + 0.25, sliders_bottom - 1 * 0.05, sliders_length, sliders_width])
cutOff_right_freq_slider = Slider(cutOff_right_freq_axes, 'Noise2 Freq. [Hz]: ', 1.00, 10.00, 
                              valinit = cutOff1_freq, color = cutOff_freq_color )

signal_left_freq_axes = fig.add_axes([sliders_left, sliders_bottom - 0 * 0.05, sliders_length, sliders_width])
signal_left_freq_slider = Slider(signal_left_freq_axes, 'Signal1 Freq. [Hz]: ', 1.00, 10.00, 
                              valinit = signal2_freq, color = signal_freq_color)

signal_right_freq_axes = fig.add_axes([sliders_left + sliders_length + 0.25, sliders_bottom - 0 * 0.05, sliders_length, sliders_width])
signal_right_freq_slider = Slider(signal_right_freq_axes, 'Signal2 Freq. [Hz]: ', 1.00, 10.00, 
                              valinit = signal1_freq, color = signal_freq_color )

taps_axes = fig.add_axes([sliders_left, sliders_bottom - 2 * 0.05, sliders_length, sliders_width])
taps_slider = Slider(taps_axes, 'Taps: ', 5, 60, 
                              valinit = nTaps, color = filter_taps_color)

sampling_freq_axes = fig.add_axes([sliders_left + sliders_length + 0.25, sliders_bottom - 2 * 0.05, sliders_length, sliders_width])
sampling_freq_slider = Slider(sampling_freq_axes, 'Sampling Freq [Hz]: ', 10, 30, 
                              valinit = sampling_freq, color = filter_taps_color)


AXIS_sig = fig.add_subplot(211)
AXIS_sig.set_title("Start moving the sliders and observe the filtering", fontweight="bold", color = filter_taps_color)

[cutOff1_line] = AXIS_sig.plot(time, cutOff1Wave, color = cutOff_freq_color, linestyle = '--', label = 'Noise')
[cutOff2_line] = AXIS_sig.plot(time, cutOff2Wave,  color = cutOff_freq_color, linestyle = '--', label = 'Noise')
[signal1_line] = AXIS_sig.plot(time, signal1,  color = signal_freq_color, linestyle = '--', label = 'Signal')
[signal2_line] = AXIS_sig.plot(time, signal2,  color = signal_freq_color, linestyle = '--', label = 'Signal')
[super_line] = AXIS_sig.plot(time, superWave, color = super_freq_color, linestyle = '-', label = 'Superimposed')
AXIS_sig.set_yticks([-2,0,2])
AXIS_sig.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
AXIS_sig.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
AXIS_sig.legend(loc = 'upper right')
AXIS_sig.set_ylabel('Amplitude')
AXIS_sig.set_xlabel('Time [s]')

AXIS_taps = fig.add_subplot(212)
AXIS_freq = AXIS_taps.twiny()

[ideal_spect_graph] = AXIS_taps.plot(idea_spect_X, idea_spect_Y, color = filter_taps_color , alpha = 1, marker = 'o',linestyle = '--') #, width = 0.9)
[ideal_spect_graph_TWIN] = AXIS_freq.plot(idea_spect_X, idea_spect_Y, linestyle = '')
[cutOff2_overlay] = AXIS_taps.plot([cutOff2_tap,cutOff2_tap], [0,1], marker = 'o', color = cutOff_freq_color , linestyle = '--' )
[cutOff2_overlay_mirror] = AXIS_taps.plot([cutOff2_tap_mirror,cutOff2_tap_mirror], [0,1], marker = 'o', color = cutOff_freq_color , linestyle = '--' )
[cutOff1_overlay] = AXIS_taps.plot([cutOff1_tap, cutOff1_tap], [0,1], marker = 'o', color = cutOff_freq_color , linestyle = '--' )
[cutOff1_overlay_mirror] = AXIS_taps.plot([cutOff1_tap_mirror, cutOff1_tap_mirror], [0,1], marker = 'o', color = cutOff_freq_color , linestyle = '--' )

[signal2_overlay] = AXIS_taps.plot([signal2_tap,signal2_tap], [0,1], marker = 'o', color = signal_freq_color , linestyle = '--' )
[signal2_overlay_mirror] = AXIS_taps.plot([signal2_tap_mirror,signal2_tap_mirror], [0,1], marker = 'o', color = signal_freq_color , linestyle = '--' )
[signal1_overlay] = AXIS_taps.plot([signal1_tap, signal1_tap], [0,1], marker = 'o', color = signal_freq_color , linestyle = '--' )
[signal1_overlay_mirror] = AXIS_taps.plot([signal1_tap_mirror, signal1_tap_mirror], [0,1], marker = 'o', color = signal_freq_color , linestyle = '--' )

[nyquist_freq_mark]= AXIS_taps.plot([nyquist_freq_tap, nyquist_freq_tap], [0, 1], color= filter_taps_color, linestyle=':')
nyquist_text = AXIS_taps.text(nyquist_freq_tap, 1/2,' Nyquist', color = filter_taps_color)

AXIS_taps.set_xticks(taps)
AXIS_taps.set_xlabel(r"Taps axis")
AXIS_taps.set_ylim([0,1.2])
AXIS_taps.set_yticks([0,1])

AXIS_freq.xaxis.set_ticks_position("bottom")
AXIS_freq.xaxis.set_label_position("bottom")
AXIS_freq.spines["bottom"].set_position(("axes", -0.35))

AXIS_freq.set_xticks(np.concatenate([taps,[cutOff2_tap],[cutOff1_tap],[signal1_tap],[signal2_tap]]))
AXIS_freq.set_xticklabels("%.1f" % z for z in np.concatenate([freq_axis,[cutOff2_freq],[cutOff1_freq],[signal1_freq],[signal2_freq]]))

AXIS_taps.relim()
AXIS_taps.autoscale_view()
AXIS_freq.relim()
AXIS_freq.autoscale_view()
    
AXIS_freq.set_xlabel(r"Freq axis")
#AXIS_freq.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))


def sliders_on_changed(val):
    sampling_freq = round(sampling_freq_slider.val,1)
    cutOff1_freq = round(cutOff_right_freq_slider.val,1)
    cutOff2_freq = round(cutOff_left_freq_slider.val,1)
    nTaps = int(taps_slider.val)
    signal1_freq = round(signal_right_freq_slider.val,1)
    signal2_freq = round(signal_left_freq_slider.val,1)
    
    allData = doTheMath(sampling_freq, cutOff1_freq, cutOff2_freq, signal1_freq, signal2_freq, nTaps)
    
    sampling_freq = allData[0]
    cutOff1_freq = allData[1]
    cutOff2_freq = allData[2]
    time = allData[3]
    cutOff1Wave = allData[4]
    cutOff2Wave = allData[5]
    taps = allData[6]
    cutOff2_tap = allData[7]
    cutOff2_tap_mirror = allData[8]
    cutOff1_tap = allData[9]
    cutOff1_tap_mirror = allData[10]
    freq_axis = allData[11]
    idea_spect_X = allData[12]
    idea_spect_Y = allData[13]
    superWave = cutOff1Wave + cutOff2Wave
    nyquist_freq = allData[14]
    nyquist_freq_tap = (nTaps)/2 #nyquist_freq * (nTaps -1)/ sampling_freq
    signal1 = allData[16]
    signal2 = allData[17]
    superWave = cutOff1Wave + cutOff2Wave + signal1 + signal2
    
    signal2_tap= allData[18]
    signal2_tap_mirror= allData[19]
    signal1_tap= allData[20]
    signal1_tap_mirror = allData[21]
    
    cutOff1_line.set_xdata(time)
    cutOff1_line.set_ydata(cutOff1Wave)
    cutOff2_line.set_ydata(cutOff2Wave)
    super_line.set_ydata(superWave)
    cutOff2_overlay.set_xdata([cutOff2_tap,cutOff2_tap])
    cutOff2_overlay_mirror.set_xdata([cutOff2_tap_mirror,cutOff2_tap_mirror])
    cutOff1_overlay.set_xdata([cutOff1_tap, cutOff1_tap])
    cutOff1_overlay_mirror.set_xdata([cutOff1_tap_mirror, cutOff1_tap_mirror])
    signal2_overlay.set_xdata([signal2_tap,signal2_tap])
    signal2_overlay_mirror.set_xdata([signal2_tap_mirror,signal2_tap_mirror])
    signal1_overlay.set_xdata([signal1_tap, signal1_tap])
    signal1_overlay_mirror.set_xdata([signal1_tap_mirror, signal1_tap_mirror])
    ideal_spect_graph.set_xdata(idea_spect_X)
    ideal_spect_graph.set_ydata(idea_spect_Y)
    ideal_spect_graph_TWIN.set_xdata(idea_spect_X)
    ideal_spect_graph_TWIN.set_ydata(idea_spect_Y)
    nyquist_freq_mark.set_xdata([nyquist_freq_tap, nyquist_freq_tap])
    nyquist_text.set_x(nyquist_freq_tap)
    
    #freq_resolution = sampling_freq/(nTaps-1)
    freq_resolution = round(allData[22],1)
    min_diff = round(allData[23],1)
    
    print(freq_resolution)
    print(min_diff)
    
    if min_diff > freq_resolution:
        print('safe')
        nyquist_text.set_color(safe_color)
        nyquist_freq_mark.set_color(safe_color)
        AXIS_sig.set_title("You have SUFFICIENT number of taps, the noise is removed and the signal is untouched", fontweight="bold", color = safe_color)
        
    else:
        nyquist_text.set_color(warning_color)
        nyquist_freq_mark.set_color(warning_color)    
        AXIS_sig.set_title("You have INSUFFICIENT number of taps, both the noise and signal are removed", fontweight="bold", color = warning_color)

    
    AXIS_taps.set_xticks(taps)
    AXIS_freq.set_xticks(np.concatenate([taps,[cutOff2_tap],[cutOff1_tap],[signal1_tap],[signal2_tap]]))
    AXIS_freq.set_xticklabels("%.1f" % z for z in np.concatenate([freq_axis,[cutOff2_freq],[cutOff1_freq],[signal1_freq],[signal2_freq]]))
    
    AXIS_taps.relim()
    AXIS_taps.autoscale_view()
    AXIS_freq.relim()
    AXIS_freq.autoscale_view()
    
    fig.canvas.draw_idle()

cutOff_left_freq_slider.on_changed(sliders_on_changed) # refresh the plots
cutOff_right_freq_slider.on_changed(sliders_on_changed) # refresh the plots
signal_left_freq_slider.on_changed(sliders_on_changed) # refresh the plots
signal_right_freq_slider.on_changed(sliders_on_changed) # refresh the plots
taps_slider.on_changed(sliders_on_changed) # refresh the plots
sampling_freq_slider.on_changed(sliders_on_changed) # refresh the plots


