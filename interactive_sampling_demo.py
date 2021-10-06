#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 12:34:39 2020

@author: sama
"""

import numpy as np
import matplotlib.pylab as plt
from matplotlib.widgets import Slider, TextBox
import scipy.signal as signal
from matplotlib.ticker import FormatStrFormatter

plt.rcParams.update({'font.size': 10})
#%%
plt.close("all")
original_freq = 6 # initial value
sampling_freq = 12 # initial value 
original_freq_color = 'powderblue'
aliased_freq_color = 'cornflowerblue'
sampling_freq_color = 'gold'
fold_down_color = 'thistle'
title_color = 'goldenrod'
safe_color = 'yellowgreen'
warning_color = 'lightcoral'

num_samples = 5000

def doTheMath(original_freq, sampling_freq):
    nyquist_freq = sampling_freq/2
    ## determine the aliased frequency:
    quotient, remainder = divmod(original_freq,nyquist_freq)
    aliased_freq = 0
    startSample = 0
    checkSample = 1
    if remainder == 0: # DC, no need to bother with else
        if divmod(quotient,2)[1] == 0: # quotient is even
            aliased_freq = 0
        else:
            aliased_freq = nyquist_freq # given the phase is pi/4
            startSample = 1/(4*original_freq) # phase is pi/4
            checkSample = 0
    else:
        if divmod(quotient,2)[1] == 0: # quotient is even
            aliased_freq = remainder
        else: # quotient is odd
            aliased_freq = nyquist_freq - remainder
    endTime = 1 # plot only 1 second of signals
    time = np.linspace(0, endTime , num_samples)
    original_sig = np.sin(original_freq * 2 * np.pi * time)
    sampled_X_values = np.arange(startSample, endTime , 1/sampling_freq)
    sampled_Y_values = np.sin(original_freq * sampled_X_values * 2 * np.pi) 
    aliased_sig = np.sin(aliased_freq * 2 * np.pi * time)
    if sampled_Y_values[checkSample] < 0: # if the sin wave is reflected over the x_axis
        aliased_sig = - aliased_sig
        #      0           1         2             3             4                 5                6             7
    return aliased_freq, time, original_sig, aliased_sig, sampled_X_values, sampled_Y_values, original_freq, sampling_freq

allData = doTheMath(original_freq, sampling_freq)
aliased_freq = allData[0] # re-evaluate aliased freq
original_freq = allData[6] # re-evaluate original freq
sampling_freq = allData[7] # re-evaluate sampling freq
nyquist_freq = sampling_freq/2 

fig = plt.figure('Interactive sampling demonstration')
fig.subplots_adjust(bottom=0.25)

sliders_left = 0.125
sliders_bottom = 0.15
sliders_width = 0.03
sliders_length = 0.775

original_freq_axes = fig.add_axes([sliders_left, sliders_bottom, sliders_length, sliders_width])
original_freq_slider = Slider(original_freq_axes, 'Original Freq. [Hz]: ', 1, 31, 
                              valinit = original_freq, color = original_freq_color)

sampling_freq_axes = fig.add_axes([sliders_left, sliders_bottom - 1 * 0.05, sliders_length, sliders_width])
sampling_freq_slider = Slider(sampling_freq_axes, 'Sampling Freq. [Hz]: ', 1, 31, 
                              valinit = sampling_freq, color = sampling_freq_color )

aliased_freq_axes = fig.add_axes([sliders_left, sliders_bottom - 2 * 0.05, sliders_width * 2, sliders_width])
aliased_freq_box = TextBox(aliased_freq_axes, 'Detected Freq. [Hz]:    ', 
                           color = aliased_freq_color)

ax_sig = fig.add_subplot(211)
ax_sig.set_title("Start moving the sliders for the original and sampling frequencies and observe the detected frequency"
                 .format(original_freq,sampling_freq,aliased_freq), fontweight="bold", color = fold_down_color)

[original_freq_line] = ax_sig.plot(allData[1], allData[2], color = original_freq_color , linestyle = '-', label = 'Original sig.')
[sampling_freq_line] = ax_sig.plot(allData[4], allData[5], color = sampling_freq_color, marker = 'o', linestyle = '', label = 'Samples')
[aliased_freq_line] = ax_sig.plot(allData[1], allData[3], color = aliased_freq_color, linestyle = '--', label = 'Detected sig.')
ax_sig.set_xticks(np.concatenate([allData[4],[1]]))
ax_sig.set_yticks([-1,0,1])
ax_sig.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
ax_sig.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
ax_sig.legend(loc = 'upper right')
ax_sig.set_ylabel('Amplitude')
ax_sig.set_xlabel('Time [s]')


def doMoreMath(original_freq, sampling_freq):
    all_freq= np.linspace(0, (int(original_freq / sampling_freq) + 1.5) * sampling_freq, num_samples)
    actual_freq= np.linspace(0, original_freq, num_samples)
    
    sawtooth_graph =  (signal.sawtooth(2 / sampling_freq * np.pi * all_freq, width = 0.5) + 1 ) * sampling_freq/4
    fold_down_graph = (signal.sawtooth(2 / sampling_freq * np.pi * actual_freq, width = 0.5) + 1 ) * sampling_freq/4
    ticks = np.arange(0, original_freq + sampling_freq/2 , sampling_freq/2)
    #          0               1           2          3       
    return actual_freq, fold_down_graph, ticks, sawtooth_graph, all_freq

moreData = doMoreMath(original_freq,sampling_freq)
ax_fd = fig.add_subplot(212)
[sawtooth_graph] = ax_fd.plot(moreData[4], moreData[3], color = fold_down_color , alpha = 0.5, linestyle = ':' )
[fold_down_line] = ax_fd.plot(moreData[0], moreData[1], color = fold_down_color , linestyle = '-' )
plt.xticks(np.concatenate([moreData[2],[original_freq]]))
ax_fd.set_xticks(np.concatenate([moreData[2],[original_freq],[sampling_freq]]))
ax_fd.set_yticks([0,allData[0],sampling_freq/2])
ax_fd.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
ax_fd.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
ax_fd.set_aspect(aspect = 'equal')
[original_freq_mark] = ax_fd.plot(np.ones(20) * original_freq , np.linspace(0, aliased_freq,20), color= original_freq_color, linestyle='-')
[aliased_freq_mark]= ax_fd.plot(np.linspace(0, original_freq, 20), np.ones(20) * aliased_freq, color= aliased_freq_color, linestyle='--')
[nyquist_freq_mark]= ax_fd.plot(np.ones(20) * nyquist_freq , np.linspace(0, nyquist_freq ,20), color= fold_down_color, linestyle=':')
[sampling_freq_mark] = ax_fd.plot(sampling_freq, 0, color = sampling_freq_color, marker = 'o', linestyle = '')
nyquist_text = ax_fd.text(nyquist_freq, nyquist_freq/2,'Nyquist\nFreq.', color = fold_down_color)
sampling_text = ax_fd.text(sampling_freq, 0 ,'Sampling\nFreq.', color = sampling_freq_color)
#sampling_text = ax_fd.text(original_freq , nyquist_freq/2 ,'Original freq.')
ax_fd.set_ylabel('Detected Freq. [Hz]')
ax_fd.set_xlabel('Original Freq. [Hz]')

def sliders_on_changed(val):
    original_freq = original_freq_slider.val
    sampling_freq = sampling_freq_slider.val
    nyquist_freq = sampling_freq/2
    allData = doTheMath(original_freq,sampling_freq)
    aliased_freq = allData[0] # re-evaluate aliased freq
    original_freq = allData[6] # re-evaluate original freq
    sampling_freq = allData[7] # re-evaluate sampling freq
    ax_sig.set_xticks(np.concatenate([allData[4],[1]]))
    original_freq_line.set_ydata(allData[2])
    original_freq_line.set_xdata(allData[1])
    aliased_freq_line.set_ydata(allData[3])
    aliased_freq_line.set_xdata(allData[1])
    sampling_freq_line.set_ydata(allData[5])
    sampling_freq_line.set_xdata(allData[4])
    nyquist_text.set_x(nyquist_freq)
    nyquist_text.set_y(nyquist_freq/2)
    if aliased_freq == original_freq:
        nyquist_text.set_color(safe_color)
        nyquist_freq_mark.set_color(safe_color)
    else:
        nyquist_text.set_color(warning_color)
        nyquist_freq_mark.set_color(warning_color)        
    sampling_text.set_x(sampling_freq)
    sampling_text.set_y(0)
    if aliased_freq < original_freq:
        ax_sig.set_title("You have DOWN-SAMPLED the {} Hz original signal with a sampling frequency of {} Hz.\n You have detected an aliased frequency at {} Hz "
                         .format(round(original_freq,2),round(sampling_freq,2),round(aliased_freq,2)), fontweight="bold", color = warning_color)
    else:
        ax_sig.set_title("You have CORRECTLY sampled and detected the {} Hz original signal with a sampling frequency of {} Hz "
                         .format(round(original_freq,2),round(sampling_freq,2),round(aliased_freq,2)), fontweight="bold", color = safe_color)
    moreData = doMoreMath(original_freq,sampling_freq)
    ax_fd.set_xticks(np.concatenate([moreData[2],[original_freq],[sampling_freq]]))
    ax_fd.set_yticks([0,allData[0],sampling_freq/2])
    ax_fd.set_aspect(aspect = 'equal')
    original_freq_mark.set_xdata(np.ones(20) * original_freq)
    original_freq_mark.set_ydata(np.linspace(0,aliased_freq,20))
    aliased_freq_mark.set_ydata(np.ones(20) * aliased_freq)
    aliased_freq_mark.set_xdata(np.linspace(0,original_freq,20))
    nyquist_freq_mark.set_ydata(np.linspace(0, sampling_freq/2 ,20))
    nyquist_freq_mark.set_xdata(np.ones(20) * sampling_freq/2)
    sampling_freq_mark.set_xdata(sampling_freq)
    fold_down_line.set_ydata(moreData[1])
    fold_down_line.set_xdata(moreData[0])
    sawtooth_graph.set_ydata(moreData[3])
    sawtooth_graph.set_xdata(moreData[4])
    aliased_freq_box.set_val(round(doTheMath(original_freq,sampling_freq)[0],2))
    fig.canvas.draw_idle()

original_freq_slider.on_changed(sliders_on_changed) # refresh the plots
sampling_freq_slider.on_changed(sliders_on_changed) # refresh the plots


