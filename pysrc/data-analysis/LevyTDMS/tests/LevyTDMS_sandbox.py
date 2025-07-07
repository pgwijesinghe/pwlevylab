import nptdms
import os
import logging
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from itertools import zip_longest
from tqdm import tqdm

class LevyTDMS:
    def __init__(self, path):
        """
        Initialize the LevyTDMS class with a file or directory path.
        If a directory is provided, it will search for TDMS files within it.
        If a file is provided, it will use that file directly.
        :param path: str, file or directory path to TDMS files
        """
        self.file_paths = self._init_files(path)
        if self.file_paths is not None: print(self.info())
        self.data = None
        logging.basicConfig(
            filename='ledaan_operations.log', 
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def _init_files(self, path):
        """
        Initialize file paths based on the provided path.
        If a directory is provided, it will search for TDMS files within it.
        If a file is provided, it will use that file directly.
        :param path: str, file or directory path to TDMS files
        :return: list of TDMS file paths or None if not found
        """
        try:
            if os.path.isfile(path):
                logging.info(f"Found valid file path: {path}")
                return os.path.abspath(path)
            elif os.path.isdir(path):
                tdms_files = [os.path.join(os.path.abspath(path), f) 
                            for f in os.listdir(path) if f.endswith('.tdms')]
                logging.info(f"Found {len(tdms_files)} TDMS files in directory: {path}")
                return tdms_files
            else:
                logging.error(f"Path not found: {path}")
                return None
        except Exception as e:
            logging.error(f"Error checking path: {e}")
            return None

    def info(self):
        """
        Load the TDMS file and return a summary of its contents.
        This includes the file name and available channels.
        :return: str, summary of the TDMS file contents
        """
        try:
            if isinstance(self.file_paths, list) and self.file_paths:
                file_to_read = self.file_paths[0]
            elif isinstance(self.file_paths, str):
                file_to_read = self.file_paths
            else:
                return "No valid TDMS file path found."

            self.data = nptdms.TdmsFile.read(file_to_read)

            group_channels = {}
            for group in self.data.groups():
                group_channels[group.name] = [channel.name for channel in group.channels()]
            
            self.clear_data()  # Clear data after loading to save memory

            summary_lines = [f"Loaded file: {os.path.basename(file_to_read)}", "Available Channels:"]

            for group, channels in group_channels.items():
                summary_lines.append(f"{group}:")
                ch_list = [f"  {ch}" for ch in channels]
                summary_lines.append("".join(ch_list))
                summary_lines.append("")  # empty line between groups

            return "\n".join(summary_lines)

        except Exception as e:
            logging.error(f"Error loading data in info(): {e}")
            return f"Error loading data: {e}"
        
    def extract_channels(self, filepath=None, channels=None, group='Data.000000', cache_file=None):
        """
        Extract specified channels from TDMS files and return as list of dictionaries.
        Each dictionary contains channel data from one TDMS file.
        
        :param filepath: Optional single file path override. If not provided, uses self.file_paths.
        :param channels: dict, keys are group names and values are list of channels to extract.
                        If None, extract all channels from the specified group.
        :param group: str, group name to extract from (default is 'Data.000000')
        :param cache_file: str, path to the cache file to load/save data in .npz format.
        :return: List[Dict[str, np.ndarray]]
        """
        # If cache file exists, load the data from it
        if cache_file and os.path.exists(cache_file):
            logging.info(f"Loading cached data from {cache_file}")
            return np.load(cache_file, allow_pickle=True)["data"].tolist()

        file_list = [filepath] if filepath else self.file_paths
        if isinstance(file_list, str):  # Single file path
            file_list = [file_list]

        results = []

        for file in tqdm(file_list, desc="Extracting channels", unit="file"):
            try:
                tdms_data = nptdms.TdmsFile.read(file)
                tdms_group = tdms_data[group]

                if channels is None:
                    channel_names = [channel.name for channel in tdms_group.channels()]
                elif isinstance(channels, dict) and group in channels:
                    channel_names = channels[group]
                else:
                    logging.warning(f"No matching channels specified for group '{group}' in file {file}. Skipping.")
                    continue

                data_dict = {}
                for ch_name in channel_names:
                    data_dict[ch_name] = tdms_group[ch_name][:]
                
                results.append(data_dict)

            except Exception as e:
                logging.error(f"Error extracting from {file}: {e}")
                continue

        # Save the extracted data to cache file if needed
        if cache_file:
            np.savez_compressed(cache_file, data=np.array(results, dtype=object))
            logging.info(f"Saved extracted data to cache at {cache_file}")

        return results

    
    def clear_data(self):
        """
        Clear the loaded TDMS data to free up memory.
        """
        try:
            if self.data is not None:
                self.data = None
                logging.info("Data cleared successfully.")
            else:
                logging.warning("No data to clear.")
        except Exception as e:
            logging.error(f"Error clearing data: {e}")
            return None
        
    def plot_heatmap(self, extracted_data, sig_channel, x_channel, y_channel=None, title='Heatmap', xlabel='X-axis', ylabel='Y-axis'):
        """
        Plot a heatmap from a list of extracted TDMS data dictionaries.
        
        :param extracted_data: List of dicts, each containing channel data from one file
        :param sig_channel: str, name of the signal channel (values form the heatmap)
        :param x_channel: str, name of the X-axis channel (assumed to be same across files)
        :param y_channel: str or None, name of the Y-axis channel, or None to use file index
        :param title: str, title of the plot
        :param xlabel: str, label for x-axis
        :param ylabel: str, label for y-axis
        """
        l = len(extracted_data[0][sig_channel])
        try:
            sig = [np.abs((d[sig_channel]-np.mean(d[sig_channel]))/np.std(d[sig_channel])) for d in extracted_data if len(d[sig_channel]) == l]  # z-score with abs
            sig = [(d[sig_channel]-np.mean(d[sig_channel]))/np.std(d[sig_channel]) for d in extracted_data if len(d[sig_channel]) == l]  # z-score without abs
            # sig = [np.abs(d[sig_channel]-np.mean(d[sig_channel])) for d in extracted_data if len(d[sig_channel]) == l]

            # Validate and convert to 2D array
            if not all(len(s) == len(sig[0]) for s in sig):
                raise ValueError("Signal arrays are not the same length. Cannot create 2D heatmap.")

            sig = np.array(sig)
            x = [d[x_channel] for d in extracted_data][0]  # assume same x in all

            if y_channel is not None:
                y = [d[y_channel] for d in extracted_data]
                y = np.concatenate(y) 
            else:
                y = np.arange(len(sig))  # Use file index as Y-axis
            plt.figure(figsize=(10, 6))
            extent = [x[0], x[-1], y[0], y[-1]]
            plt.imshow(sig, aspect='auto', cmap='plasma', origin='lower', extent=extent, vmin=-2, vmax=2)
            plt.colorbar(label="Normalized Photocurrent [A]")
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.title(title)
            plt.tight_layout()
            plt.show()

        except Exception as e:
            logging.error(f"Error plotting heatmap: {e}")
            return None


if __name__ == "__main__":
    files = LevyTDMS(r"G:\.shortcut-targets-by-id\0B8-gGFa6hkR4XzJJMDlqZXVKRk0\ansom\Data\THz 1\SA40653C.20250526\10 - 20250604_CtrlExp")
    data = files.extract_channels(
        channels={'Data.000000': ['Delay', 'Ch3_y', 'Insertion']}
    )
    files.plot_heatmap(extracted_data=data, sig_channel='Ch3_y', x_channel='Delay', y_channel='Insertion', title='TD vs GDD', xlabel='Delay [ps]', ylabel='Insertion [mm]')

