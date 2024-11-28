import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Function to generate a plot
def generate_plot(title):
    x = np.linspace(0, 10, 100)
    y = np.sin(x) * np.random.rand(100)  # Randomize sine wave amplitude
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set_title(title)
    return fig

st.title("Page 1: Random Graphs")

# Display 4 random graphs
for i in range(1, 5):
    st.subheader(f"Graph {i}")
    st.pyplot(generate_plot(f"Graph {i}: Randomized Sine Wave"))
