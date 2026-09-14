import streamlit as st
import pandas as pd
import plotly.express as px

st.title('Visualizations and Interactivity')

# Read data file
df = pd.read_csv('assets/penguins.csv')
st.dataframe(df)

# Scatter plot
fig = px.scatter(
    data_frame=df,
    x='bill_length_mm',
    y='bill_depth_mm', 
    color='species',
    hover_data=['species', 'island'],
    marginal_y='violin',
    marginal_x='violin'
)
st.plotly_chart(fig)

# Bar chart
df_g = df.groupby(['island'])[['body_mass_g']].mean().reset_index()
st.dataframe(df_g)

fig = px.bar(
    data_frame=df_g,
    x='island',
    y='body_mass_g',
    color = {'Biscoe': 'green', 'Dream': 'blue', 'Torgersen': 'red'},
    labels={'body_mass_g': 'Average Body Mass (g)', 'island': 'Island'}
)
st.plotly_chart(fig)

# Histogram
df_dropna = df.dropna(subset=['sex'])
fig = px.histogram(
    data_frame=df_dropna,
    x='body_mass_g',
    facet_col='sex',
    color='sex',
    nbins=10
)
st.plotly_chart(fig)

# Line chart
df_g = df.groupby(['flipper_length_mm'])[['bill_length_mm']].mean().reset_index()
fig = px.line(
    data_frame=df_g, 
    x='flipper_length_mm',
    y='bill_length_mm',
    labels={'flipper_length_mm': 'Flipper Length', 'bill_length_mm': 'Average Bill Length'}
)
st.plotly_chart(fig)

df_g = df.groupby(['flipper_length_mm', 'sex'])[['bill_length_mm']].mean().reset_index()
fig = px.line(
    data_frame=df_g, 
    x='flipper_length_mm',
    y='bill_length_mm',
    color='sex',
    labels={'flipper_length_mm': 'Flipper Length', 'bill_length_mm': 'Average Bill Length'}
)
st.plotly_chart(fig)

# Iteractivities
numerical_cols = ['bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g']
col1, col2 = st.columns(2)
with col1:
    option_x = st.selectbox(label='Select X from:', index=0, options=numerical_cols, key='option1')
    st.write(f'This is the selected column: {option_x}')
with col2:
    option_y = st.selectbox(label='Select Y from:', index=1, options=numerical_cols, key='option2')

if option_x != option_y:
    interactive_fig = px.scatter(
        data_frame = df,
        x=option_x,
        y=option_y, 
        color='species'
    )
    st.plotly_chart(interactive_fig)
else:
    st.markdown(f'You selected the same X and Y columns: X={option_x}, Y={option_y}. A scatter plot should have different X and Y.')


# Interactive bar chart
df_g = df.groupby(['island'])[['body_mass_g']].mean().reset_index()
col1, col2 = st.columns(2, border=True)

with col1:
    fig = px.bar(
        data_frame=df_g,
        x='island',
        y='body_mass_g',
        color = 'island',
        color_discrete_map= {'Biscoe': 'green', 'Dream': 'blue', 'Torgersen': 'red'},
        labels = {'body_mass_g': 'Average Body Mass (g)', 'island': 'Island'}
    )

    event = st.plotly_chart(fig, key='bar2', on_select='rerun', selection_mode='points')
with col2:
    #st.markdown('Text placeholder.')
    #st.write(event)
    selected_pt = event['selection']['points']
    #st.write(selected_pt)
    if len(selected_pt) == 0:
        selected_island = 'Biscoe'
    else:
        selected_island = selected_pt[0]['x']

    st.write(selected_island)

    df_selected = df.loc[df['island']==selected_island]
    #st.dataframe(df_selected)

    n_penguins = df_selected.shape[0]
    body_mass_075 = df_selected['body_mass_g'].quantile(0.75)
    body_mass_025 = df_selected['body_mass_g'].quantile(0.25)
    body_mass_avg = df_selected['body_mass_g'].mean()
    body_mass_max = df_selected['body_mass_g'].max()
    body_mass_min = df_selected['body_mass_g'].min()


    md_txt = f"""
    There are **{n_penguins}** penguins living on the **{selected_island}** Island. 
    Their average body mass is **{body_mass_avg:.1f}** grams. 
    The penguins’ weights range from **{body_mass_max}** g to **{body_mass_min}** g, 
    with an interquartile range (IQR) of **{body_mass_025}** - **{body_mass_075}** g.
    """
    st.markdown(md_txt)

# Exercise
# Create two columns:
# - In the left column, display a bar chart showing the average body mass of each penguin species.
# - In the right column, display a scatter plot with bill length on the x-axis
#   and bill depth on the y-axis for Adelie penguins.
# - When the user clicks a bar in the left chart, update the scatter plot to show only penguins from the selected species.
col1, col2 = st.columns(2)

with col1:
    df_g = df.groupby(['species'])[['body_mass_g']].mean().reset_index()
    fig = px.bar(
        data_frame=df_g,
        x='species',
        y='body_mass_g',
        color = 'species',
        #color_discrete_map= {'Biscoe': 'green', 'Dream': 'blue', 'Torgersen': 'red'},
        labels = {'body_mass_g': 'Average Body Mass (g)', 'species': 'Species'}
    )

    event = st.plotly_chart(fig, key='bar3', on_select='rerun', selection_mode='points')
with col2:
    selected_pt = event['selection']['points']
    if len(selected_pt) == 0:
        selected_species = 'Adelie'
    else:
        selected_species = selected_pt[0]['x']

    df_plt = df.loc[df['species']==selected_species]
    fig = px.scatter(
        data_frame=df_plt,
        x='bill_length_mm', 
        y='bill_depth_mm',
        title=f'{selected_species} penguins'
    )
    st.plotly_chart(fig, key='interactive_line')


st.header('Some other widgets')
all_cols = df.columns.tolist()
multi_seletions = st.multiselect(label='Select multiple items from:', options=all_cols)
st.write(f'Selected items: {multi_seletions}')

my_slider = st.slider(
    label='Select a range of body mass', 
    max_value=df['body_mass_g'].max(),
    min_value=df['body_mass_g'].min(),
    value = (df['body_mass_g'].min(), df['body_mass_g'].max())
)
st.write(f'Selected range: {my_slider}')

my_checkbox = st.checkbox(label='Show data')
st.write(my_checkbox)
if my_checkbox:
    st.dataframe(df)
else:
    pass