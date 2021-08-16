from scipy import signal

def butter_lowpass_filtfilt(data, cutoff, fs, order=4):
    wn = 2*cutoff/fs
    b, a = signal.butter(order, wn, 'lowpass', analog = False)
    output = signal.filtfilt(b, a, data, axis=0)
    return output 
