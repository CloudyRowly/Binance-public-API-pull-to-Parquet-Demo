# Data storage (Binance to Parquet)
Language: Python

Source files: ``realtime.py``, ``restful.py``, ``utils.py``

Output folder: ``/data``

Utilizes [binance's api library](https://github.com/binance/binance-connector-python/tree/master)

A program that demonstate the use of Binance API and the operations on Parquet files.

Resources:
- [Intro to Parquet](https://www.jumpingrivers.com/blog/parquet-file-format-big-data-r/)
- [fast parquet](https://fastparquet.readthedocs.io/en/latest/api.html#fastparquet.write)
- [Pandas' Data frame](https://pandas.pydata.org/pandas-docs/version/1.1/reference/api/pandas.DataFrame.html)



| Design choices made | Reasons                |
|---------------------| --------------------- |
| Used "snappy" compression | Fastest query time for "selected column query" of all types of compression, even faster than uncompressed. (130% faster than the next compression method: GZIP) (Source: [Riz Ang: What is Apache Parquet file](https://www.youtube.com/watch?v=PaDUxrI6ThA))|
| Used "PyArrow" engine for writing and reading Parquet files | Is natively supported by Pandas, the library used for Data framing. Is faster than other engines at writing files.|
| Used Fast Parquet engine for appending to Parquet file | PyArrow does not support Parquet file appending.|

---

### Restful API Test

Module used: ``Spot`` from ``binance.spot`` 

reference: [rest-api.md](https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md)

implementation: ``restful.py``

Uses Binance restful API, easy interface to pull historical data.

Test for independent read and write off Parquet files.

Test for column selective querying.

---

### Websocket stream Test (Real-time data pulling)

Module used: ``SpotWebsocketStreamClient`` from ``binance.websocket.spot.websocket_stream``

Reference document: [web-socket-streams.md](https://github.com/binance/binance-spot-api-docs/blob/master/web-socket-streams.md)

implementation: ``realtime.py``

Uses websocket, useful for listening to real time data.

Py Arrow does not support Parquet file appending => Use Fast Parquet for appending instead

**Observation:** first interval in the stream returns exception => Implemented exception handling to not write this interval into the data files. 

### CSV to Parquet

Utilizing [binance public data](https://github.com/binance/binance-public-data/tree/master), download monthly data using the command:

``` python download-kline.py -t spot -s BTCUSDT -i 15m -folder D:\Learning\y2s2\comp3500\Binance-public-API-pull-to-Parquet-Demo\public_kline ```

Binance will then return a folder of zip files:

![CMD showing download process](<resource/Screenshot 2024-03-27 121433.png>)

Using `unzip` in `csv_to_parquet.py`, unzip all file in the given folder, result:

![extracted csv files](<resource/Screenshot 2024-03-27 124803.png>)

---

### Week 7 research progress: Focus on converting and storing tick data csv files

Focused on the tick data aka trades.

**Goal:** 
- Investigate the resource need for tick data files, and the writing speed
- Start investigating on the integration of data storage module into the system:
    - Write node: [using Python for easy data processing, calculation of indicators (pre-processing)](https://automaticaddison.com/how-to-add-a-python-ros2-node-to-a-c-ros-2-package/)
    - Reading node: use CPP for spped and efficiency, todo: investigate in [Apache Drill](https://drill.apache.org/docs/querying-parquet-files/) for SQL query


#### Analysis

Sampled data from 6 days (17th - 22nd April 2024):

**CSV:**
| Total | Per day |
|-----------------------------|------------------------|
| 12 012 572 entries          | ~2 002 095 entries |
| 888 357 908 bytes           | ~148 059 651 bytes |

**Parquet control test (only convert data on the 19th - the peak day):**
| Properties                                           | value              |          note         |
|------------------------------------------------------|--------------------|-----------------------|
| Number of entries                                    | 2828283            |
| CSV file size                                        | 209 333 843 bytes  |
| Parquet file size                                    | 54 456 020 bytes   | ~74% size compression |
| Time taken to convert and write to Parquet from csv  | ~1.44 seconds      |
| Time taken to write each entry                       | ~0.50 micro-seconds|

**Parquet:**
| Total                                     | Per file                               | Per entry          |
|-------------------------------------------|----------------------------------------|--------------------|
| 220 309 998 bytes                         | ~36 718 333 bytes = 36.7 MB            | 18.339 bytes       |
| 5.9533 seconds to convert csv to parquet  | ~0.99 seconds to convert csv to parquet| ~0.5 micro-seconds |

- 75.2% size compression
- 1GB of HDD can store ~27 days of tick data
- Relatively affordable 256GB of space can store ~6971 days of tick data (19.1 years)
- Takes ~362 seconds (~6 minutes) to convert and store a year worth of tick data
- Can compress to a zip file => Further 55% size compressed => 85.5% in total compression ratio


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

**Note**: Binance has a limit of 1000 intervals per request.

![tables from reading the Parquet files](/resource/Screenshot%202024-03-12%20030955.png)

### Real-time data pulling appending

![tables showing data progression](/resource/Screenshot%202024-03-14%20112909.png)

### Selective reading

Two tables showing column selected query and column + row_filtered query respectively.

**Note**: index column is pandas' format for data Framing, is not modifiable. Index of filtered row does not match with its original order from full table.

![table showing filtered data](/resource/Screenshot%202024-03-14%20120003.png)

### CSV to Parquet

![a view of the written Parquet file](/resource/Screenshot%202024-04-24%20134353.png)