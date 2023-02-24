from scipy import signal
import numpy as np
from scipy import signal,stats
from scipy.signal import find_peaks,peak_widths,filtfilt,lfilter,butter
class HeartRate():
    def reject_outliers(self,data, m=1):
        return data[abs(data - np.mean(data)) < m * np.std(data)]

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
        nyq = fs
        normal_cutoff = cutoff / nyq
        b, a = signal.butter(order, normal_cutoff, btype = "high", analog = False)
        return b, a

    def butter_highpass_filter(self,data, cutoff, fs, order=5):
        b, a = self.butter_highpass(cutoff, fs, order=order)
        y = signal.filtfilt(b, a, data)
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
            cutoff_fre_low = 200/60.0
            cutoff_fre_high = 40/60.0

            # smt_sig = butter_highpass_filter(sig,cutoff_fre_high,sample_rate)
            # smt_sig = butter_highpass_filter(sig,cutoff_fre_high,sample_rate)

            smt_sig = self.butter_lowpass_filter(raw_sig,cutoff_fre_low,sample_rate)
            smt_sig = self.butter_highpass_filter(smt_sig,cutoff_fre_high,sample_rate)

            peaks, _ = find_peaks(smt_sig, height=None)
            peak_diffs = np.array([(j-i)*pt_time for i, j in zip(peaks[:-1], peaks[1:])])
            peak_diffs = peak_diffs[np.where(peak_diffs>0.3)]
            peak_diffs = peak_diffs[np.where(peak_diffs<1.5)]
            # peak_diffs = self.reject_outliers(peak_diffs,m=1)
            bpm = int(60/np.mean(peak_diffs))
            return bpm
        except Exception:
            return 0

    def process_rr_signal(self,raw_sig,sample_rate=400):
        try:
            cutoff_fre_low = 60/60.0
            cutoff_fre_high = 30/60.0
            pt_time = 1/sample_rate
            smt_sig = self.butter_highpass_filter(raw_sig,cutoff_fre_high,sample_rate)
            smt_sig = self.butter_lowpass_filter(smt_sig,cutoff_fre_low,sample_rate)
            peaks, _ = find_peaks(smt_sig, height=None)
            peak_diffs = np.array([(j-i)*pt_time for i, j in zip(peaks[:-1], peaks[1:])])
            rr = int(60/np.mean(peak_diffs))
            return rr
        except Exception:
            return 0
