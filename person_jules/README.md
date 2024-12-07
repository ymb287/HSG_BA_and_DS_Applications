# Pedestrian Forecast Melbourne Center

This project was conducted during the course "Business Analytics and Data Science Applications". 
Our goal is to provide Restaurant and SMEs with information, so they can make informed decisions for marketing in the city center of Melbourne (SMEs) as well as match staffing of their restaurants and Pedestrian predictions around the latter, adapting for before unexpected peaks or lows. 

Our approach uses historic weather and pedestrian counts of five sensors in the city center of Melbourne, ranging from April 2022 until October 2024, for concentrating of post-covid trends, and reduce the noise of the pandemic from our predictions. 

---

## Repo Structure

00 - Data
  1.  `custom` - Data structures created by various python scripts for inital exploratory data analysis and modeling.
  2.  `external` - Historical data that is not fetched live and was retrieved from various outside sources. 


01 - Data Fetching
  1.  `011_Live_Weather_Data.ipynb` - Monthly fetching of the pedestrian counts live fetching of weather data for our streamlit app.
  2.  `012_Historic_Energy_Demand.ipynb` - Fetching of historic pedestrian movements for model training. 
  3.  `secret_weather.py` - secret file for weather API-key.
  5.  `weather_data_pull.py` - Script to pull weather data from the OpenWeatherMap API. (initial version)
  6.  `weather_data_process.py` - Script for processing the raw weather data. (initial version)

02 - Data Pre-processing
  1. `022_Merge_Weather_and_PedestrianForecasts.ipynb` - Merging our key historical data for training and benchmarking.
  2. `data_handling.ipynb` - Primary notebook for initial data processing and handling. For initial Modelling purpose, not used further in our benchmarking and App.

03 - Data exploration
  1. `030_Data_exploration.ipynb` - Data exploration and time series analytics, to gain understanding of the data structure.

04 - Model Benchmarking

`040_benchmarking_setup.ipynb` - Definition of our setup for benchmarking different ML models. 
  1. `041_bm_exponential_smoothing.ipynb` - Exponentential smoothing model (univariate) benchmark.
  2. `042_bm_XGB.ipynb` - XGB model (multivariate) benchmark. 
  3. `044_bm_SARIMAX.ipynb` - SARIMAX model (multivariate) benchmark.
  4. `048_bm_prophet_multi.ipynb` - Prophet model (multivariate) benchmark.

05 - App development

  see `README.md` in `05_Streamlit_App`

---

## Installation
To set up this project, clone the repository and install the required dependencies:
```bash
git clone <repository-url>
cd <repository-name>
pip install [dependencies]
```

---

## Miscellaneous 

App link:
- put the actual link

Data sources:
- Historic Pedestrian Forecasts - put the actual link
- Historic Weather Data - https://openweathermap.org/history-bulk
- Real-time Weather Data - https://openweathermap.org/api

