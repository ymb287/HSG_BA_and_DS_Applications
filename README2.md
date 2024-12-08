# Pedestrian Forecast Melbourne Center

This project was conducted during the course "Business Analytics and Data Science Applications". 
Our goal is to provide Restaurant and SMEs with information, so they can make informed decisions for marketing in the city center of Melbourne (SMEs) as well as match staffing of their restaurants and Pedestrian predictions around the latter, adapting for before unexpected peaks or lows. 

Our approach uses historic weather and pedestrian counts of five sensors in the city center of Melbourne, ranging from April 2022 until October 2024, for concentrating of post-covid trends, and reduce the noise of the pandemic from our predictions. 

---

## Repo Structure

0 - Data
  1.  `raw` - Data structures created by various python scripts for inital exploratory data analysis and modeling.
  2.  `processed` - Final data sets both 6 locations and the five final chosen ones


01 - shared
  1.  `data_check.ipynb` - Exploring the data, cleaning it, pre-processing it
  2.  `data_check_2.ipynb` - ??
  3.  `data_loader.py` - Selenium Web Driver

02 - Models used for Prediction and Benchmarking
  1. First layer, folders for each models used, Exponential smoothing, Sarima, Prophet, XGB, as well as the Plots for each streets and each model
  2. Within every model's folders, the ipynb file for the model preiction, a csv with the model prediction as well as the pkl files for streamlit application

03 - streamlit
  1. ???

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

