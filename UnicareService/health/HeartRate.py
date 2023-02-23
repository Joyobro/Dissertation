from scipy import signal
import numpy as np
from scipy.signal import find_peaks, peak_widths, butter, lfilter

class HeartRate():
    def reject_outliers(self,data, m=1):
        return data[abs(data - np.mean(data)) < m * np.std(data)]

    def butter_lowpass(self,cutoff, fs, order=5):
        return butter(order, cutoff, fs=fs, btype='low', analog=False)


    def butter_lowpass_filter(self,data, cutoff, fs, order=5):
        b, a = self.butter_lowpass(cutoff, fs, order=order)
        y = lfilter(b, a, data)
        return y

    def butter_highpass(self,cutoff, fs, order=5):
        return butter(order, cutoff, fs=fs, btype='high', analog=False)

    def butter_highpass_filter(self,data, cutoff, fs, order=5):
        b, a = self.butter_highpass(cutoff, fs, order=order)
        y = lfilter(b, a, data)
        return y

    def process_signal(self,raw_sig,sample_rate=400):
        try:
            # window_size= 50
            # raw_sig = np.convolve(sig, np.ones(window_size), 'valid') / window_size
            #
            pt_time = 1/sample_rate
            # cutoff_fre = 200
            # new_sig_low = self.butter_lowpass_filter(raw_sig, cutoff_fre*2/sample_rate,fs=sample_rate,order=5)
            # window_size= 200
            sig = (np.array(raw_sig))
            # print(len(sig))
            window_size= 50
            order = 6
            for i in range(0,order):
                sig = np.convolve(sig, np.ones(window_size), 'valid') / window_size
            new_sig_low = sig
            peaks, _ = find_peaks(new_sig_low, height=None)
            # peaks = peaks[1:-1]
            # new_sig_low = butter_lowpass_filter(new_sig_low, 40,fs=400,order=4)


            # print(peaks)
            scale = len(raw_sig)/len(new_sig_low)
            peak_diffs = np.array([(j-i)*scale*pt_time for i, j in zip(peaks[:-1], peaks[1:])])
            peak_diffs = peak_diffs[np.where(peak_diffs>0.3)]
            peak_diffs = peak_diffs[np.where(peak_diffs<1.5)]
            # peak_diffs = self.reject_outliers(peak_diffs,m=1)
            bpm = int(60/np.mean(peak_diffs))
            return bpm
        except Exception:
            return 0

    def process_rr_signal(self,raw_sig,sample_rate=400):
        try:
            # window_size= 50
            # raw_sig = np.convolve(sig, np.ones(window_size), 'valid') / window_size
            #
            pt_time = 1/sample_rate
            # cutoff_fre = 200
            # new_sig_low = self.butter_lowpass_filter(raw_sig, cutoff_fre*2/sample_rate,fs=sample_rate,order=5)
            # window_size= 200
            sig = (np.array(raw_sig))
            # print(len(sig))
            window_size= 50
            order = 50
            for i in range(0,order):
                sig = np.convolve(sig, np.ones(window_size), 'valid') / window_size
            new_sig_low = sig
            peaks, _ = find_peaks(new_sig_low, height=None)
            # # peaks = peaks[1:-1]
            # # new_sig_low = butter_lowpass_filter(new_sig_low, 40,fs=400,order=4)
            #
            #
            # # print(peaks)
            # scale = len(raw_sig)/len(new_sig_low)
            # peak_diffs = np.array([(j-i)*scale*pt_time for i, j in zip(peaks[:-1], peaks[1:])])
            # peak_diffs = peak_diffs[np.where(peak_diffs>0.3)]
            # peak_diffs = peak_diffs[np.where(peak_diffs<1.5)]
            # peak_diffs = self.reject_outliers(peak_diffs,m=1)
            # bpm = int(60/np.mean(peak_diffs))
            return len(peaks)*6
        except Exception:
            return 0
