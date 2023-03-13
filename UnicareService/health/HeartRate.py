from scipy import signal
import numpy as np
from scipy import signal,stats
from scipy.signal import find_peaks,peak_widths,filtfilt,lfilter,butter,freqz

class HeartRate():
    def reject_outliers(self,data, m=1):
        return np.where(abs(data - np.mean(data)) > m * np.std(data)), data[abs(data - np.mean(data)) < m * np.std(data)]

    def butter_lowpass(self,cutoff, fs, order=5):
        nyq = fs
        normal_cutoff = cutoff / nyq
        b, a = signal.butter(order, normal_cutoff, btype = "low", analog = False)
        return b, a


    def butter_lowpass_filter(self,data, cutoff, fs, order=5):
        b, a = self.butter_lowpass(cutoff, fs, order=order)
        y = filtfilt(b, a, data)
        return y


    def butter_highpass(self,cutoff, fs, order=5):
        nyq = 0.5*fs
        normal_cutoff = cutoff / nyq
        b, a = signal.butter(order, normal_cutoff, btype = "high", analog = False)
        return b, a

    def butter_highpass_filter(self,data, cutoff, fs, order=5):
        b, a = self.butter_highpass(cutoff, fs, order=order)
        y = signal.filtfilt(b, a, data)
        return y

    def butter_bandpass(self,lowcut, highcut, fs, order=5):
        return butter(order, [lowcut, highcut], fs=fs, btype='bandpass')

    def butter_bandpass_filter(self,data, lowcut, highcut, fs, order=5):
        b, a = self.butter_bandpass(lowcut, highcut, fs, order=order)
        y = lfilter(b, a, data)
        return y

    def process_hr_signal(self,raw_sig,f_low,f_high, order=3, sample_rate=400):
        try:
            # fs = sample_rate
            # b, a = signal.butter(order, [f_low, f_high], btype='bandpass', analog=False, fs=fs)
            peaks_dx = 0

            cutoff_fre_high = 40/60
            window_size= 80
            smth_order = 8
            smt_sig = raw_sig
            for i in range(0,smth_order):
                smt_sig = np.convolve(smt_sig, np.ones(window_size), 'valid') / window_size
            # smt_sig = self.butter_highpass_filter(smt_sig,cutoff_fre_high,sample_rate)
            # smt_sig = signal.filtfilt(b, a, smt_sig)

            peaks, _ = find_peaks(smt_sig, height=None)
            # new_sample_rate = sample_rate*(len(raw_sig)/len(smt_sig))
            pt_time = 1/sample_rate
            peak_diffs = np.array([(j-i)*pt_time for i, j in zip(peaks[:-1], peaks[1:])])
            peak_diffs = peak_diffs[np.where(peak_diffs>0.3)]
            peak_diffs = peak_diffs[np.where(peak_diffs<1.5)]
            peak_diffs = (self.reject_outliers(peak_diffs,m=1))[1]
            if (len(peak_diffs)>0):
                dy = smt_sig[peaks]
                dy = (dy-np.min(dy))/(np.max(dy)-np.min(dy))
                dy = abs(np.diff(dy))
                dx = np.diff(peaks)
                peaks_dx = np.mean(dy/dx)
                bpm = int(60/np.mean(peak_diffs))
            else:
                bpm = 0
            # value = bpm
            return bpm,peaks_dx
        except Exception as e:
            print(e)
            return 0,0

    def process_rr_signal(self,raw_sig,f_low,f_high, order=3, sample_rate=400):
        try:
            pt_time = 1/sample_rate

            y = self.butter_bandpass_filter(raw_sig, f_low, f_high, sample_rate, order=3)
            peaks, _ = find_peaks(y, height=None)
            peak_diffs = np.array([(j-i)*pt_time for i, j in zip(peaks[:-1], peaks[1:])])
            rr = int(60/np.mean(peak_diffs))
            return rr
        except Exception as e:
            print(e)
            return 0