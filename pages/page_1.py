# Import packages
import streamlit as st
import pandas as pd
from assets.styling import hide_toolbar

# Add a title
st.title('Text formatting and working with CSV file')

# Markdown for text formatting
md_heading = """
# Heading level 1
## Heading level 2
### Heading level 3
###### Heading level 6
"""
st.markdown(md_heading)

md_list = """
- item 1
- item 2

1. numbered item 1
2. numbered item 2
4. numbered item 3
"""
st.markdown(md_list)

md_txt = """
This is a sentence.   
**This sentence is in bold text.** *This sentence is in italic text.*
"""
st.markdown(md_txt)

my_height = 172
md_txt_height = f"""
My height is {my_height} cm.
"""
st.markdown(md_txt_height)

# insert an image
# st.image('assets/pikachu.jpg', width=300)

# columns
col1, col2 = st.columns(2, border=False)
with col1:
    st.image('assets/pikachu.jpg', width=300)
with col2:
    with st.container(border=True, height=300):
        md_txt = 'A suprised Pikachu'
        st.markdown(md_txt)

# Metrics
st.metric('Score:', 97, border=True)

# CSV

# Read data
df = pd.read_csv('assets/penguins.csv')

with st.container(key='no_download'):
    hide_toolbar(container_key='no_download')
    st.dataframe(df)

df_g = df.groupby(['species'])[['species']].count()
st.dataframe(df_g)

for i, row in df_g.iterrows():
    st.write(row.name, row['species'])

# Exercise
# Create 3 columns. 
# First column display total number of peguins using metric
# Second column display a dataframe showing the nunmbers of MALE and FEMALE penguins.
# Third column display a list showing the numbers of MALE and FEMALE penguise.

df_g2 = df.groupby(['sex'])[['sex']].count()
total_penguine =df.shape[0]
col1, col2, col3 = st.columns(3)
with col1:
    st.metric('Total number of penguins:', total_penguine)
with col2:
    st.dataframe(df_g2)
with col3:
    for i, row in df_g2.iterrows():
        sex = row.name
        sex_count = row['sex']
        md_txt = f'- {sex}: {sex_count}'
        st.markdown(md_txt)


