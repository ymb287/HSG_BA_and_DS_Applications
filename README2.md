# Pedestrian Forecast Melbourne Center

This project was conducted during the course "Business Analytics and Data Science Applications". 
Our goal is to provide Restaurants and Marketing Agencies (MA) and their clients with pedestrian movements information, so they can make informed decisions for: for the SMEs, choosing the right time and right place for digital billboards marketing actions in the city center of Melbourne, as well as, for the restaurants in the location of our sensors, to match their staffing to the related Pedestrian predictions close to their location, anticipating the lwos and peaks of movement in the city center.

Our approach uses historic weather and pedestrian counts of five sensors in the city center of Melbourne, ranging from April 2022 until October 2024, for concentrating of post-covid trends, and reduce the noise of the pandemic from our predictions. 

---

## Repo Structure

0 - Data
  1.  `raw` - Data structures created by various python scripts for inital exploratory data analysis and modeling.
  2.  `processed` - Final data sets both 6 locations and the five final chosen ones

01 - shared
  1.  `data_check.ipynb` - Exploring the data, cleaning it, pre-processing it
  2.  `data_loader.py` - Scraping tool for pedestrian count data

02 - Models used for Prediction and Benchmarking
  1. First layer, folders for each models used, Exponential smoothing, Sarima, Prophet, XGB, as well as the Plots for each streets and each model
  2. Within every model's folders, the ipynb file for the model preiction, a csv with the model prediction as well as the pkl files for streamlit application

03 - streamlit
  1. `Home.py`- The Home page of the Web App dashboard
  2. Folder `pages` including all the streets subpages python files for the dashboard on streamlit
  3. `__init__.py`Empty Python file
  4. Folder `__pycache__` Created to store the compiled versions of Pythons scripts for the Streamlit Web Application. Helps to execute the code faster by skipping the steps of rec-compiling the source code if it has not changed (which is the case now)
  5. `forecast.py`The actual forecasts of the XGB Model (best performing one from the benchmark) python file
  6. `layout.py` Layout of the web app visualisations within the different dashboard pages
  7. Folder Models in which the model for each street is saved in pkl format for the streamlit application, as well as the scaler for the latter
  8. `requirement.txt`All the Python packages dependencies needed for running the code of the streamlit Web App application 
  9. `pedestrian_data_filtered_2.csv` Data Set of the Historical data from Melbourne pedestrian movement on the 5 selcted streets including the external variables of weather, structured the same way as the API calls will bring it into the modeling of the predictions.
  10. `test_api.ipynb`Jupyter notebook for testing the Openweather API for the streamlit model integration

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
- https://hsgbaanddsapplications-umjzpjndrfvquxiwaku9g9.streamlit.app/

Data sources:
- Historic Pedestrian Forecasts - https://www.pedestrian.melbourne.vic.gov.au/#date=09-12-2024&time=8
- Historic Weather Data - https://openweathermap.org/history-bulk
- Real-time Weather Data - https://openweathermap.org/api

