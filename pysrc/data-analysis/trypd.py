import pandas as pd
from nptdms import TdmsFile

tdms_file_path = "./datafile_XY.tdms"

with TdmsFile.open(tdms_file_path) as tdms_file:
    df = tdms_file['Data.000000'].as_dataframe()
    print(df.head())
    print(df.keys())
    print(df.shape)

