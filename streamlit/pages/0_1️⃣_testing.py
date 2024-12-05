import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import altair as alt

st.set_page_config(
    page_title="Pedestrian Forecast",
    page_icon="👣",
    layout="wide",
    initial_sidebar_state="expanded")
alt.themes.enable("dark")

import matplotlib.pyplot as plt
# Plot the pedestrian counts

