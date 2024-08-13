from collections import namedtuple

import numpy as np
from matplotlib import pyplot as plt

TAU = np.pi * 2
PLOT_DPI = 110

FreqResult = namedtuple("FreqResult", ["freq", "amp", "phase", "centroid"]) 

def generate_random_signal(dur, sample_rate, freq_count, max_freq, max_amp, print_summary = False):
    if max_freq < freq_count:
        raise ValueError("Number of frequencies required is higher than maximum allowed range.")
    
    x = np.linspace(0, dur, dur * sample_rate) * TAU
    y = np.zeros(x.shape)
    freqs, amps, phases = [], [], []

    for i in range(freq_count):
        freq = np.random.randint(max_freq)

        while freq in freqs:
            freq = np.random.randint(max_freq)

        amp = np.random.random() * max_amp
        phase = (np.random.random() * TAU) - (TAU / 2)

        y += amp * np.cos((x * freq) + phase)

        freqs.append(freq)
        amps.append(amp)
        phases.append(phase)

        if print_summary:
            print(f"Freq #{i + 1}:")
            print(f"\tFrequency: {freq} Hz")
            print(f"\tAmplitude: {amp:.2f}")
            print(f"\tPhase: {phase:.2f} radians")

    if print_summary:
        print(f"\nSamples generated: {len(x)}")

    return y, freqs, amps, phases

def plot_signal(sig):
    plt.figure(figsize = (9, 5), dpi = PLOT_DPI)
    plt.plot(sig)
    plt.xlabel("Samples")
    plt.ylabel("Amplitude")
    plt.show()

def get_freq_vectors(freq_to_check, samples):
    vec_x, vec_y = [], []
    num_samples = len(samples)

    for i, s_i in enumerate(samples):
        angle = (i / num_samples) * TAU * freq_to_check
        vec_x.append(np.cos(angle) * s_i)
        vec_y.append(np.sin(angle) * s_i)
    
    return vec_x, vec_y

def plot_freq(vec_x, vec_y, cen, plot_lim, title = ""):
    plot_lim += 0.02

    plt.figure(figsize = (5, 5), dpi = PLOT_DPI)
    plt.gca().add_patch(plt.Circle((0, 0), radius = 1, fill = None))
    plt.plot(vec_x, vec_y, linewidth = 1)
    plt.scatter(cen[0], cen[1], color = "red")
    plt.xlim((-plot_lim, plot_lim))
    plt.ylim((-plot_lim, plot_lim))
    plt.title(title)
    plt.axis(False)
    plt.show()

def centroid(vec_x: list, vec_y: list):
    x_mean = np.array(vec_x).mean()
    y_mean = np.array(vec_y).mean()
    return x_mean, y_mean

def magnitude(vec_x: list, vec_y: list):
    x, y = centroid(vec_x, vec_y)
    return np.sqrt((x ** 2) + (y ** 2))

def phase_radians(cen_x, cen_y):
    return -np.arctan2(cen_y, cen_x)

def check_freq(freq_to_check, samples, dur = 1.0, plot = False):
    vec_x, vec_y = get_freq_vectors(freq_to_check, samples)
    cen =  centroid(vec_x, vec_y)
    freq = freq_to_check / dur
    amp = magnitude(vec_x, vec_y)
    phase = phase_radians(*cen)

    if plot:
        plot_freq(
            vec_x, 
            vec_y, 
            cen, 
            max(1, samples.max()),
            f"Checked Freq: {freq_to_check} Hz | Actual Freq: {freq} Hz"
        )

    if (freq_to_check == 0) | (freq_to_check == len(samples)):
        FreqResult(freq, amp, phase, cen)
    return FreqResult(freq, amp * 2, phase, cen)

def check_freq_range(freq_arr, samples, dur = 1.0):
    freq_results: list[FreqResult] = []

    for freq_to_check in freq_arr:
        freq_results.append(check_freq(freq_to_check, samples, dur))
    
    return freq_results

def plot_amp_comparison(orig_freqs, orig_amps, freq_results):
    plt.figure(figsize = (9, 5), dpi = PLOT_DPI)
    plt.scatter(orig_freqs, orig_amps, color = "red", label = "Original")
    plt.plot(
        [fr.freq for fr in freq_results],
        [fr.amp for fr in freq_results],
        label = "DFT"
    )
    plt.legend()
    plt.xlabel("Frequency")
    plt.ylabel("Amplitude")
    plt.show()