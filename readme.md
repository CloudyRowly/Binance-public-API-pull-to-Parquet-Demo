# Data storage (Binance to Parquet)
Language: Python

Source files: ``main.py``, ``binance_api.py``

Output files: ``LTCUSDT_15m.parquet.snappy``, ``BTCUSDT_30m.parquet.snappy``

A program that demonstate the use of Binance API and the operations on Parquet files.

Test for independent read and write off Parquet files.

Test for column selective querying.

| Design choices made | Reasons                |
|---------------------| --------------------- |
| Used "snappy" compression | Fastest query time for "selected column query" of all types of compression, even faster than uncompressed. (130% faster than the next compression method: GZIP)|
| Used "PyArrow" engine for writing and reading Parquet files | Is natively supported by Pandas, the library used for Data framing.|

## Dependencies
The following libraries are required:
```
pip install pandas 
pip install binance-connector
pip install pyarrow
```

## Results
![tables from reading the Parquet files](/resource/Screenshot%202024-03-12%20030955.png)