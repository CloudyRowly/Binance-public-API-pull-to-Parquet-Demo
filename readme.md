# Data storage (Binance to Parquet)
Language: Python

Source files: ``realtime.py``, ``restful.py``

Output folder: ``/data``

Utilizes [binance's api library](https://github.com/binance/binance-connector-python/tree/master)

A program that demonstate the use of Binance API and the operations on Parquet files.


| Design choices made | Reasons                |
|---------------------| --------------------- |
| Used "snappy" compression | Fastest query time for "selected column query" of all types of compression, even faster than uncompressed. (130% faster than the next compression method: GZIP)|
| Used "PyArrow" engine for writing and reading Parquet files | Is natively supported by Pandas, the library used for Data framing.|

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


## Dependencies
The following libraries are required:
```
pip install pandas 
pip install binance-connector
pip install pyarrow
```

## Results
![tables from reading the Parquet files](/resource/Screenshot%202024-03-12%20030955.png)