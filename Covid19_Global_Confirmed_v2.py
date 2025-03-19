import pandas as pd
import numpy as np
import streamlit as st
from PIL import Image

st.set_page_config(layout="wide")   
st.text("""
This was my first Python app. It's purpose is to pivot the data from wide format to long format, with some data cleanup along the way.
""")
def app():
    #st.subheader('Using python melt function to change from wide to long format.')
    
    with st.container():

        col1, col2 = st.columns([2.5, 1.5])

        with col1:
            st.markdown('Wide Format (before)')
            image = Image.open('wide_format_cvs_view.png')
            st.image(image, caption='')

        with col2:
            # a subheader for the format change
            st.markdown('Long Format (after)')

            # this line reads a data file from an external source
            url = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')

            #  this line creates a dataframe with the variable df from the url
            df = pd.DataFrame(url)

            # this line drops any unnecessary columns
            df = df.drop(['Lat', 'Long'], axis=1)

            #  these 3 lines replace the cruise line names and any other non country values as a 'nan' (i.e. N/A) and then dropna removes any nan's
            df=df.replace('Diamond Princess', np.nan).dropna(axis=0, how='any')
            df=df.replace('Grand Princess', np.nan).dropna(axis=0, how='any')
            df=df.replace('Repatriated Travellers', np.nan).dropna(axis=0, how='any')

            #  this line renames a column(s)
            df.rename(columns={'Province/State': 'Province_State', 'Country/Region': 'Country_Region'}, inplace=True)

            #  this line removes the asterisk from the country name
            df['Country_Region'] = df['Country_Region'].replace(['Taiwan*'], 'Taiwan')


            #  this line pivots the dates (as headers for each column) and values from wide to long format; id_vars keeps the columns as they are,
            #  value_vars is the column that is the pivot point, var_name is the new columnS for dates and value_name is for the date values
            df_melted = pd.melt(df, id_vars = ['Province_State', 'Country_Region'], value_vars=df.columns[2:], var_name='Date', value_name='Confirmed')


            #  this line removes any rows with values of 0
            df_melted = df_melted[df_melted['Confirmed'] != 0]


            #df_melted.to_csv ('./time_series_covid19_confirmed_global_mod.csv')
            #st.bar_chart(data=df_melted, x="Country_Region", y="Confirmed",)
            #print (df_melted)
            st.dataframe(df_melted)

app()
