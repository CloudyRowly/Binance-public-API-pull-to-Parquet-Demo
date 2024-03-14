# Data storage (Binance to Parquet)
Language: Python

Source files: ``realtime.py``, ``restful.py``

Output folder: ``/data``

Utilizes [binance's api library](https://github.com/binance/binance-connector-python/tree/master)

A program that demonstate the use of Binance API and the operations on Parquet files.


| Design choices made | Reasons                |
|---------------------| --------------------- |
| Used "snappy" compression | Fastest query time for "selected column query" of all types of compression, even faster than uncompressed. (130% faster than the next compression method: GZIP) (Source: [Riz Ang: What is Apache Parquet file](https://www.youtube.com/watch?v=PaDUxrI6ThA))|
| Used "PyArrow" engine for writing and reading Parquet files | Is natively supported by Pandas, the library used for Data framing. Is faster than other engines at writing files.|
| Used Fast Parquet engine for appending to Parquet file | PyArrow does not support Parquet file appending.|

### Restful API Test

Module used: ``Spot`` from ``binance.spot`` 

reference: [rest-api.md](https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md)

implementation: ``restful.py``

Uses Binance restful API, easy interface to pull historical data.

Test for independent read and write off Parquet files.

Test for column selective querying.

### Websocket stream Test (Real-time data pulling)

Module used: ``SpotWebsocketStreamClient`` from ``binance.websocket.spot.websocket_stream``

Reference document: [web-socket-streams.md](https://github.com/binance/binance-spot-api-docs/blob/master/web-socket-streams.md)

implementation: ``realtime.py``

Uses websocket, useful for listening to real time data.

Py Arrow does not support Parquet file appending => Use Fast Parquet for appending instead

**Observation:** first interval in the stream returns exception => Implemented exception handling to not write this interval into the data files. 


## Dependencies
The following libraries are required:
```
pip install pandas 
pip install binance-connector
pip install pyarrow
pip install fastparquet
```

## Results

### Rest api testing result

![tables from reading the Parquet files](/resource/Screenshot%202024-03-12%20030955.png)

### Real-time data pulling appending

![tables showing data progression](/resource/Screenshot%202024-03-14%20112909.png)