import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv('assets/penguins.csv')
st.dataframe(df)