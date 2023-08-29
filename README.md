# SDS4GDSP

Spatial Data Science for the Globe Data Science Program is the dedicated workshop material for the incoming batch of Globe DSP Cadets aimed to equip them with the basic skills to process and unravel insights using geospatial data.

1. Introduction: Grammar of Spatial Data Science
2. Application: Calculating Telco Mobility Index
3. Take Home: Mobility Index Calculation and Profiling

## 1. Setup

Please execute the following steps in your local machine.

1. Clone the **sds4gdsp** github repository from this link <br>
```git clone https://github.com/jpacil0/sds4gdsp.git```

2. Create (then activate) a virtual environment named **gdsenv** with **python=3.8.16** <br>
```conda create --name gdsenv python=3.8.16```

3. Install **jupyterlab** and **leafmap** separately in that environment, we will use this for the workshop <br>
```pip install jupyterlab``` <br>
```conda install leafmap -c conda-forge```

5. Install the packages from the **requirements.txt**, follow the **README.md** <br>
```pip install -r requirements.txt```

6. Setup jupyter and the widgets to be used <br>
```conda install -c conda-forge ipyleaflet``` <br>
```jupyter labextension install @jupyter-widgets/jupyterlab-manager jupyter-leaflet```