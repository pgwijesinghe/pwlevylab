import os
import logging
import numpy as np
import matplotlib.pyplot as plt
import nptdms
from tqdm import tqdm
import matplotlib.animation as animation

class LevyTDMS:
    def __init__(self, path):
        self.file_paths = self._init_files(path)
        self.logger = self._setup_logger()
        if self.file_paths: print(self.info())
        self.data = None

    def _setup_logger(self):
        logger = logging.getLogger("LevyTDMSLogger")
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            handler = logging.FileHandler("ledaan_operations.log")
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        return logger

    def _init_files(self, path):
        if os.path.isfile(path):
            return os.path.abspath(path)
        elif os.path.isdir(path):
            tdms_files = [os.path.join(os.path.abspath(path), f) for f in os.listdir(path) if f.endswith('.tdms')]
            return tdms_files
        else:
            return None

    def info(self):
        try:
            file_to_read = self.file_paths[0] if isinstance(self.file_paths, list) else self.file_paths
            self.data = nptdms.TdmsFile.read(file_to_read)

            group_channels = {
                group.name: [channel.name for channel in group.channels()]
                for group in self.data.groups()
            }
            self.clear_data()
            summary_lines = [f"Loaded file: {os.path.basename(file_to_read)}", "Available Channels:"]
            for group, channels in group_channels.items():
                summary_lines.append(f"{group}:")
                summary_lines.extend([f"  {ch}" for ch in channels])
                summary_lines.append("")
            return "\n".join(summary_lines)
        except Exception as e:
            self.logger.error(f"Error loading data in info(): {e}")
            return f"Error loading data: {e}"

    def extract_channels(self, filepath=None, channels=None, group='Data.000000', cache_file=None):
        if cache_file and os.path.exists(cache_file):
            self.logger.info(f"Loading cached data from {cache_file}")
            return np.load(cache_file, allow_pickle=True)["data"].tolist()

        file_list = [filepath] if filepath else self.file_paths
        if isinstance(file_list, str):
            file_list = [file_list]
        file_list.sort()
        results = []
        for file in tqdm(file_list, desc="Extracting channels", unit="file"):
            try:
                tdms_data = nptdms.TdmsFile.read(file)
                tdms_group = tdms_data[group]
                channel_names = [channel.name for channel in tdms_group.channels()] if channels is None else channels.get(group, [])
                if not channel_names:
                    self.logger.warning(f"No channels specified for {file}")
                    continue
                data_dict = {ch: tdms_group[ch][:] for ch in channel_names}
                results.append(data_dict)
            except Exception as e:
                self.logger.error(f"Error extracting from {file}: {e}")
                continue

        if cache_file:
            np.savez_compressed(cache_file, data=np.array(results, dtype=object))
            self.logger.info(f"Saved extracted data to cache at {cache_file}")

        return results

    def apply_frequency_filter(self, data, signal_key, delay_key, bands_THz):
        filtered_data = []
        for entry in tqdm(data, desc="Filtering data"):
            try:
                delay_ps = entry[delay_key]
                signal = entry[signal_key]

                delay_s = delay_ps * 1e-12
                dt = np.mean(np.diff(delay_s))
                freq = np.fft.fftfreq(len(signal), d=dt) / 1e12  # in THz
                spectrum = np.fft.fft(signal)

                mask = np.zeros_like(freq, dtype=bool)
                for fmin, fmax in bands_THz:
                    mask |= (np.abs(freq) >= fmin) & (np.abs(freq) <= fmax)

                filtered = np.fft.ifft(spectrum * mask).real
                entry[signal_key + '_filtered'] = filtered
                filtered_data.append(entry)
            except Exception as e:
                self.logger.error(f"Error filtering data entry: {e}")
        return filtered_data

    def plot_heatmap(self, extracted_data, sig_channel, x_channel, y_channel=None, title='Heatmap', xlabel='X-axis', ylabel='Y-axis'):
        l = len(extracted_data[0][sig_channel])
        print(l)
        try:
            sig = [np.abs(d[sig_channel] - np.mean(d[sig_channel])) for d in extracted_data if len(d[sig_channel]) == l]
            if not all(len(s) == len(sig[0]) for s in sig):
                raise ValueError("Signal arrays are not the same length.")
            sig = np.array(sig)
            x = extracted_data[0][x_channel]
            y = np.concatenate([d[y_channel] for d in extracted_data]) if y_channel else np.arange(len(sig))
            print(len(sig), len(x), len(y))
            extent = [x[0], x[-1], y[0], y[-1]]
            plt.figure(figsize=(10, 6))
            plt.imshow(sig + 1e-12, aspect='auto', cmap='plasma', origin='lower', extent=extent)
            plt.colorbar(label="Photocurrent [A]")
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.title(title)
            plt.tight_layout()
            plt.show()
        except Exception as e:
            self.logger.error(f"Error plotting heatmap: {e}")

    def plot_heatmap_1(self, extracted_data, sig_channel, x_channel, y_channel=None, title='Heatmap', xlabel='X-axis', ylabel='Y-axis'):
        import numpy as np
        import matplotlib.pyplot as plt
        from scipy.signal import savgol_filter
        from scipy.fft import rfft, irfft, rfftfreq
        from scipy.ndimage import median_filter

        def fft_despike(signal, fs, threshold=8.0, window_size=9):
            signal = np.asarray(signal, dtype=float)
            n = len(signal)
            spectrum = rfft(signal)
            mag = np.abs(spectrum)

            mag_med = median_filter(mag, size=window_size, mode='reflect')
            mad = median_filter(np.abs(mag - mag_med), size=window_size, mode='reflect')
            spike_mask = np.abs(mag - mag_med) > threshold * mad

            cleaned_mag = np.copy(mag)
            cleaned_mag[spike_mask] = mag_med[spike_mask]
            spectrum_cleaned = cleaned_mag * np.exp(1j * np.angle(spectrum))
            return irfft(spectrum_cleaned, n=n)

        try:
            l = len(extracted_data[0][sig_channel])
            print(l)

            # Get x and compute fs assuming x is delay in ps → convert to seconds
            x = np.array(extracted_data[0][x_channel]) * 1e-12
            fs = 1 / np.mean(np.diff(x))

            # Process each line: FFT-despike + SG smooth
            sig = []
            for d in extracted_data:
                if len(d[sig_channel]) == l:
                    raw = np.array(d[sig_channel])
                    cleaned = fft_despike(raw, fs=fs, threshold=8.0, window_size=9)
                    smoothed = savgol_filter(cleaned, window_length=21, polyorder=3)
                    sig.append(smoothed - np.mean(smoothed))  # Centered

            sig = np.array(sig)
            if not all(len(s) == len(sig[0]) for s in sig):
                raise ValueError("Signal arrays are not the same length.")

            y = np.concatenate([d[y_channel] for d in extracted_data]) if y_channel else np.arange(len(sig))
            print(len(sig), len(x), len(y))
            extent = [x[0]*1e12, x[-1]*1e12, y[0], y[-1]]  # convert x back to ps

            plt.figure(figsize=(10, 6))
            plt.imshow(np.abs(sig + 1e-12), aspect='auto', cmap='plasma', origin='lower', extent=extent, vmax=0.5e-6)
            plt.colorbar(label="Photocurrent [A]")
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.title(title)
            plt.tight_layout()
            plt.show()

        except Exception as e:
            self.logger.error(f"Error plotting heatmap: {e}")

    def plot_PS(self, extracted_data, sig_channel, x_channel, y_channel=None, title='Heatmap', xlabel='X-axis', ylabel='Y-axis'):
        l = len(extracted_data[0][sig_channel])
        try:
            sig = [d[sig_channel] for d in extracted_data if len(d[sig_channel]) == l]
            if not all(len(s) == len(sig[0]) for s in sig):
                raise ValueError("Signal arrays are not the same length.")
            sig = np.array(sig)
            x = extracted_data[0][x_channel]
            y = np.concatenate([d[y_channel] for d in extracted_data]) if y_channel else np.arange(len(sig))
            extent = [x[0], x[-1], y[0], y[-1]]
            plt.figure(figsize=(10, 6))
            plt.imshow(np.log(sig), aspect='auto', cmap='plasma', origin='lower', extent=extent)
            plt.colorbar(label="Photocurrent [A]")
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.title(title)
            plt.tight_layout()
            plt.show()
        except Exception as e:
            self.logger.error(f"Error plotting heatmap: {e}")


    def clear_data(self):
        self.data = None

if __name__ == "__main__":
    # files = LevyTDMS(r"G:\.shortcut-targets-by-id\0B8-gGFa6hkR4XzJJMDlqZXVKRk0\ansom\Data\THz 1\SA40663G.20250429\20250430_HighRes_2")
    # files = LevyTDMS(r"G:\.shortcut-targets-by-id\0B8-gGFa6hkR4XzJJMDlqZXVKRk0\ansom\Data\THz 1\SA40653C.20250526\10 - 20250604_CtrlExp")
    # files = LevyTDMS(r"G:\.shortcut-targets-by-id\0B8-gGFa6hkR4XzJJMDlqZXVKRk0\ansom\Data\THz 1\SA40653C.20250526\12 - 20250606_TDvBackgate_45mmInsertion")
    files = LevyTDMS(r"G:\.shortcut-targets-by-id\0B8-gGFa6hkR4XzJJMDlqZXVKRk0\ansom\Data\THz 1\SA40653C.20250526\27 - 20250704_TDvSDBias_45mmInsertion_6K_Fine_-100m to 100m Bias_5mSteps")


    data = files.extract_channels(
        channels={'Data.000000': ['Delay', 'Ch3_PS_y', 'Ch3_PS_x', 'Ch3_y', 'SD']},
        # cache_file="extracted_data__no_nanorod-bg20.npz"
    )

    filtered_data = files.apply_frequency_filter(
        data,
        signal_key='Ch3_y',
        delay_key='Delay',
        bands_THz=[(350, 450), (700, 900)]
    )

    files.plot_heatmap(
        extracted_data=data,
        sig_channel='Ch3_y',
        x_channel='Delay',
        y_channel='SD',
        title='TD vs SD Bias (Filtered)',
        xlabel='Delay [ps]',
        ylabel='SD Bias (V)'
    )

    files.plot_heatmap(
    extracted_data=filtered_data,
    sig_channel='Ch3_y_filtered',
    x_channel='Delay',
    y_channel='SD',
    title='TD vs SD Bias (Filtered)',
    xlabel='Delay [ps]',
    ylabel='SD Bias (V)'
)

    files.plot_PS(
        extracted_data=data,
        sig_channel='Ch3_PS_y',
        x_channel='Ch3_PS_x',
        y_channel='SD',
        title='Power Spectrum (log) vs SD',
        xlabel='Frequency [THz]',
        ylabel='SD Bias (V)'
)