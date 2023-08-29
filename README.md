# SDS4GDSP

Spatial Data Science for the Globe Data Science Program is the dedicated workshop material for the incoming batch of Globe DSP Cadets aimed to equip them with the basic skills to process and unravel insights using geospatial data.

## 1. Setup

Please execute the following steps in your local machine.

1. Clone the **sds4gdsp** github repository from this link. <br>
```git clone https://github.com/jpacil0/sds4gdsp.git```

2. Create (then activate) a virtual environment named **gdsenv** with **python=3.8.16**. <br>
```conda create --name gdsenv python=3.8.16```

3. Install **jupyterlab** and **leafmap** separately in that environment, we will use this for the workshop. <br>
```pip install jupyterlab``` <br>
```conda install leafmap -c conda-forge```

5. Install the packages from the **requirements.txt**, follow the **README.md**. <br>
```pip install -r requirements.txt```

6. Setup jupyter and the widgets to be used. <br>
```conda install -c conda-forge ipyleaflet``` <br>
```jupyter labextension install @jupyter-widgets/jupyterlab-manager jupyter-leaflet```

## 2. Data

Create a local copy of the fake telco datasets. This might take a while. <br>
The scripts are designed to be [configurable](https://hydra.cc/). See **scripts/** and **config/** for more details.

1. Create a fake set of telco subscribers. <br>
```python -m scripts.make_fake_subscribers```

2. Create a fake set of telco cellsites. <br>
```python -m scripts.make_fake_cellsites```

3. Create a fake set of telco transactions. <br>
```python -m scripts.make_fake_transactions```

After you've completed the steps above, you should be able to see something like this.

```
sds4gdsp/data/
│   fake_subscribers.csv
│   fake_cellsites.csv
│   fake_transactions.csv
```

## 3. Lecture

This workshop is a two-way street. Pay attention to the lecture, follow-along with the given code, ask questions, and give feedback!

1. Introduction: Grammar of Spatial Data Science
2. Application: Calculating Telco Mobility Index
3. Take Home: Mobility Index Calculation and Profiling
