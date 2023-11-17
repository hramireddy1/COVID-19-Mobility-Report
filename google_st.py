import streamlit as st
import numpy as np
import pandas as pd

st.image("mobility_report.png")
st.title("An interactive App to visualize Google\'s Mobility Report")
st.write("This Web Application aims to help visualize Google's Community Mobility Reports that can be found here:")
st.write("google.com/covid19/mobility/")
st.write("The purpose of the report is to see the changes that have occured with the policies being implemented to combat COVID-19. The movement trends across multiple geographies in multiple sectors such as workplaces, groceries and pharmacies etc. can be found.")
st.write("The changes for each day as compared to a baseline value for that day of the week is plotted on the y-axis.")
df = pd.read_csv("data.csv",encoding = "utf-8",dtype={"country_region_code":str,"country_region":str,"sub_region_1":str,"sub_region_2":str})
df.drop(['country_region_code'],axis=1,inplace=True)
df['date']=pd.to_datetime(df['date'])
df.fillna('none',inplace=True)
#df.set_index("geo_type",inplace=True)



country_region = st.sidebar.selectbox("Please select the country you would like to explore?", list(df["country_region"].unique()))
if not country_region:
	st.error("Please select one option")
st.subheader("You selected: "+ country_region)


df_interest = df.loc[df["country_region"] == country_region]
df_interest.set_index("date",inplace=True)
#st.write(df_interest)

if(df_interest.sub_region_1.any() == 'none'):
	st.header('Countrywide')
	final_df = df_interest.loc[df_interest.sub_region_1=='none']
	final_df.drop(['sub_region_1','sub_region_2'], axis=1, inplace=True)
	sectors = st.multiselect('Please select the categories of places',['retail_and_recreation','grocery_and_pharmacy','parks','transit_stations','workplaces','residential'])
	st.line_chart(final_df[sectors])
	if(st.checkbox('Show raw data',key=1)):
		st.subheader('Raw data')
		st.write(final_df)



if(df_interest.sub_region_1.all() != 'none'):
	st.header('State/Sub-region1 wide')
	sub_reg_df = df_interest.loc[(df_interest.sub_region_1!='none') & (df_interest.sub_region_2=='none')]
	sub_region = st.sidebar.selectbox('Please select a State',list(df_interest["sub_region_1"].unique()))
	final_df = sub_reg_df.loc[sub_reg_df["sub_region_1"] == sub_region]
	final_df.drop(['sub_region_2'], axis=1, inplace=True)
	sectors = st.multiselect('Please select the categories of places',['retail_and_recreation','grocery_and_pharmacy','parks','transit_stations','workplaces','residential'],key=2)
	st.line_chart(final_df[sectors])
	if(st.checkbox('Show raw data',key=3)):
		st.subheader('Raw data')
		st.write(final_df)



if(df_interest.sub_region_2.all() != 'none'):
	st.header('County/City/Sub-region2 wide')
	sub_reg2_df = df_interest.loc[(df_interest.sub_region_1!='none') & (df_interest.sub_region_2!='none')]
	sub_region1 = st.selectbox('Please select a State to see the County/City list',list(df_interest["sub_region_1"].unique()))
	sub_region1_df = sub_reg2_df.loc[(sub_reg2_df["sub_region_1"] == sub_region1)]
	sub_region2 = st.selectbox('Please select a County',list(sub_region1_df["sub_region_2"].unique()))
	final_df = sub_region1_df.loc[(sub_region1_df["sub_region_2"] == sub_region2)]
	sectors2 = st.multiselect('Please select the categories of places',['retail_and_recreation','grocery_and_pharmacy','parks','transit_stations','workplaces','residential'],key=4)
	st.line_chart(final_df[sectors2])
	if(st.checkbox('Show raw data',key=5)):
		st.subheader('Raw data')
		st.write(final_df)













