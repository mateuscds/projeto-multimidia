import matplotlib.pyplot as plt
import numpy as np
import wave, sys
import threading
import os
from pydub import AudioSegment
from scipy.interpolate import make_interp_spline, BSpline
from scipy.signal import find_peaks

from scipy.fft import fft, fftfreq

def time_graph(path):
    raw = wave.open(path)
     
    sample_freq = raw.getframerate()
    n_samples = raw.getnframes()
    t_audio = n_samples/sample_freq
    n_channels = raw.getnchannels()
    signal_wave = raw.readframes(n_samples)

    signal_array = np.frombuffer(signal_wave, dtype=np.int16)
    l_channel = signal_array[0::2]
    r_channel = signal_array[1::2]
    times = np.linspace(0, n_samples/sample_freq, num=2*n_samples)

    x_new_t = np.linspace(times.min(), times.max(), 1000) 

    spl = make_interp_spline(times, signal_array, k=3)  # type: BSpline
    power_smooth = spl(x_new_t)

    # power_smooth = power_smooth / np.max(power_smooth)

    # for index in range(len(power_smooth)):
    #     if power_smooth[index] < 0:
    #         power_smooth[index] = -1*power_smooth[index]
        
    #     if power_smooth[index] < 12000:
    #         power_smooth[index] = 0

    for index in range(len(power_smooth)):
        if power_smooth[index] < 0:
            power_smooth[index] = 0
        if power_smooth[index] < 5000:
            power_smooth[index] = 0


    plt.figure(2)
    plt.plot(x_new_t, power_smooth)
    plt.title('Channel')
    plt.ylabel('Signal Value')
    plt.xlabel('Time (s)')
    plt.xlim(0, t_audio)

    peaks, _ = find_peaks(power_smooth, height=0)
    plt.plot(x_new_t[peaks], power_smooth[peaks], "x")
    plt.plot(np.zeros_like(power_smooth), "--", color="gray")


    plt.show()
    # plt.savefig('data/test.png')
 

if __name__ == "__main__":
   
    # gets the command line Value
    path = sys.argv[1]

    if path.endswith('.mp3'):
        sound = AudioSegment.from_mp3(path)
        sound.export(os.path.splitext(path)[0]+'.wav', format="wav")
        time_graph(os.path.splitext(path)[0]+'.wav')
    else:
        time_graph(path)
    # visualize(path)