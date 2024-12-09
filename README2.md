# Pedestrian Forecast Melbourne Center

This project was conducted during the course "Business Analytics and Data Science Applications". 
Our goal is to provide Restaurants and SMEs (including Marketing Agencies) with information, so they can make informed decisions for: for the SMEs, choosing the right time and right place for digital billboards marketing actions in the city center of Melbourne, as well as, for the restaurants in the location of our sensors, to match their staffing to the related Pedestrian predictions close to them, anticipating the lwos and peaks in predicted demand.

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
- Put the link here

Data sources:
- Historic Pedestrian Forecasts - https://www.pedestrian.melbourne.vic.gov.au/#date=09-12-2024&time=8
- Historic Weather Data - https://openweathermap.org/history-bulk
- Real-time Weather Data - https://openweathermap.org/api

