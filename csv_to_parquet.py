import pandas as pd
from fastparquet import write as pq_write
import os
from os.path import isfile, join
from utils import Database
import zipfile

from delta_parquet import delta_encode


def unzip(folder_path):
    folders = [f for f in os.listdir(folder_path) if isfile(join(folder_path, f))]
    for f in folders:
        if f.endswith(".zip"):
            with zipfile.ZipFile(join(folder_path, f), 'r') as zip_ref:
                zip_ref.extractall(folder_path)
                print(f"File {f} has been extracted.")
            os.remove(join(folder_path, f))
            print(f"File {f} has been deleted.")


def csv_to_parquet(csv_file, parquet_file, columns, ref_row):
    """Convert a CSV file to a parquet file.
    
    Args:
        csv_file (str): path to the CSV file.
        parquet_file (str): path to the parquet file.
    """
    df = pd.read_csv(csv_file)
    df.columns = columns

    if ref_row is not None:
        df = delta_encode(df, columns, ref_row)
    # pq_write(join("data", parquet_file), df, compression="snappy")

    if (not os.path.exists(parquet_file)):
        df.to_parquet(parquet_file, engine="fastparquet", compression="snappy")
        print(f"File {parquet_file} has been written.")
    else:
        pq_write(parquet_file, df, compression="SNAPPY", append=True)
        print(f"File {csv_file} has been appended to {parquet_file}.")


def merge_to_parquet(folder_path, parquet_file, delta_encoding=True):
    """Merge all CSV files in a folder to a parquet file.
    
    Args:
        folder_path (str): path to the folder containing CSV files.
        parquet_file (str): path to the parquet file.
    """
    csv_files = [f for f in os.listdir(folder_path) if isfile(join(folder_path, f))]
    print(csv_files)

    ref_row = None  # Reference row for delta encoding

    columns = []
    initialized = True
    for f in csv_files:
        # Create unified column names for all CSV files
        if(initialized):
            df = pd.read_csv(join(folder_path, f))
            column_count = len(df.columns)
            
            if delta_encoding:
                ref_row = df.iloc[0, :]
            
            for i in range(column_count):
                columns.append("column_" + str(i))
            initialized = False

        if f.endswith(".csv"):
            csv_to_parquet(join(folder_path, f), parquet_file, columns, ref_row)


if __name__ == "__main__":
    # unzip("public_kline/data/spot/monthly/klines/BTCUSDT/15m")
    merge_to_parquet("public_kline/data/spot/monthly/klines/BTCUSDT/15m", "btcusdt@kline_15m_all_time.parquet.snappy")
    print(Database.read("btcusdt@kline_15m_all_time.parquet.snappy"))