# Aliya Tyshkanbayeva
# Project 2
# Visualization and Analysis on Zillow Economics Data

import numpy as np # linear algebra
import pandas as pd # to read csv file
from matplotlib import pyplot as plt
plt.style.use('dark_background')
import seaborn as sns
from IPython.display import Image, display
from matplotlib.ticker import MaxNLocator
#from fbprophet import Prophet
import squarify


import plotly
import plotly.offline as py
py.init_notebook_mode(connected=True)
import plotly.tools as tls
import plotly.graph_objs as go
import plotly.tools as tls
import plotly.figure_factory as fig_fact
plotly.tools.set_config_file(world_readable=True, sharing='public')


from IPython.display import HTML
from subprocess import check_output

#Loading Data
# let's read the 'City_time_series.csv' 
StateTimeSeries=pd.read_csv("/Users/aliyatyshkanbayeva/Downloads/State_time_series.csv",parse_dates=True)
StateTimeSeries.Date=pd.to_datetime(StateTimeSeries.Date)
StateTimeSeries['year'] = StateTimeSeries.Date.dt.year
print(StateTimeSeries.head())

cityTimeSeries = pd.read_csv('/Users/aliyatyshkanbayeva/Downloads/City_time_series.csv')
cityTimeSeries.Date=pd.to_datetime(cityTimeSeries.Date)
cityTimeSeries['year'] = cityTimeSeries.Date.dt.year

states = set(StateTimeSeries[~StateTimeSeries['ZHVI_AllHomes'].isnull() &
    ~StateTimeSeries['Sale_Prices'].isnull()]['RegionName'].values)

# 1 Here we are plotting a bar chart with values of all houses per square. The numbers are calculated through
# dividing  the estimated home values for each house in given state by house's square footage 
stateTimeSeries.Date = pd.to_datetime(stateTimeSeries.Date)
stateTimeSeries.groupby(stateTimeSeries.Date.dt.year)['ZHVIPerSqft_AllHomes'].mean().plot(kind='bar', figsize=(10, 6))
plt.suptitle('Median of the value of all homes per square foot in different year', fontsize=14)
plt.ylabel('ZHVI per square feet')
plt.xlabel('Year')

# 2. Here I am plotting a bar chart of median of list prices per square foot in different years. It is calculated by dividing the median of list prices by the square footage of the house. 

stateTimeSeries = stateTimeSeries.dropna(subset=['MedianListingPricePerSqft_AllHomes'], how='any')
stateTimeSeries.groupby(stateTimeSeries.Date.dt.year)['MedianListingPricePerSqft_AllHomes'].mean().plot(kind='bar', figsize=(10, 6))
plt.suptitle('Median of list prices per square foot in different year', fontsize=24)
plt.ylabel('Median Listing Price Per Square foot')
plt.xlabel('Year')

#  3 Here I have plotted a bar chart with three variables: Zillow Home Value for 1 bedroom, 3 bedroom and 4 bedroom. This is a data visualization of zillow’s home values in different years by type of the house. 

stateTimeSeries.groupby(stateTimeSeries.Date.dt.year)[['ZHVI_1bedroom','ZHVI_3bedroom','ZHVI_4bedroom']].mean().plot(kind='bar', figsize=(10, 6))
plt.suptitle("Zillow's different home value in different year", fontsize=24)
plt.ylabel('Zillow home value in 1bd,3bd,4bd apartments')
plt.xlabel('Year')


#  4 Here our plot shows how top 5 states by costs behave in past 20 years based on the house sold prices using fte - fivethirtyeight style
StateTimeSeriesYear = StateTimeSeries[StateTimeSeries['RegionName'].isin(states)].copy()
HighestCostStates = StateTimeSeriesYear[['RegionName', 'ZHVI_AllHomes']].groupby('RegionName').max().sort_values(by=['ZHVI_AllHomes'], ascending=False)[:5].index.values.tolist()
StateTimeSeriesYear=StateTimeSeriesYear[StateTimeSeriesYear.RegionName.isin(HighestCostStates)]
StateTimeSeriesYear.year = StateTimeSeriesYear.Date.dt.year


# colorblind friendly colors
colors = [[0,0,0], [230/255,159/255,0], [86/255,180/255,233/255], [0,158/255,115/255], 
          [213/255,94/255,0], [0,114/255,178/255]]

StatesyearSalePrices=StateTimeSeriesYear.groupby([StateTimeSeriesYear.year,StateTimeSeriesYear.RegionName])['ZHVI_AllHomes'].mean().dropna().reset_index(name='SoldPrice')
fte_graph=StatesyearSalePrices.pivot(index='year', columns='RegionName', values='SoldPrice').plot(figsize=(14,7), color=colors, legend=False)
fte_graph.figure.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
fte_graph.tick_params(axis = 'both', which = 'major', labelsize = 16)
plt.xlabel("")
fte_graph.set_yticklabels(labels = [-10, '100000   ', '200000   ',  '300000   ', '400000   ',  '500000 $'])
# Generate a bolded horizontal line at y = 0 
fte_graph.axhline(y = 100000, color = 'black', linewidth = 1.3, alpha = .7)
# Add an extra vertical line by tweaking the range of the x-axis
fte_graph.set_xlim(left = 1995, right = 2018)
# The signature bar

fte_graph.text(x = 1994, y = 30000,
    s = '  @Aliya Tyshkanbayeva                                                                                                                                                                        Source: Zillow   ',
    fontsize = 14, color = 'white', backgroundcolor = 'black')


# Adding a title and a subtitle
fte_graph.text(x = 1994, y = 570000, s = "Visual representation of situation in Real Estate Sector in US",
               fontsize = 25, weight = 'bold', alpha = .75)
fte_graph.text(x = 1994, y = 550000, 
               s = 'Noticed Increase in house sales prices in past 20 years in US states',
              fontsize = 18, alpha = .85)

# Adding colored labels in order to see the states 
fte_graph.text(x = 2002, y = 390000, s = 'California', color = 'white', weight = 'bold', rotation = 55,
              backgroundcolor = 'yellow')
fte_graph.text(x = 2012, y = 530000, s = 'District of Columbia', color = 'orange', weight = 'bold', rotation = 30,
              backgroundcolor = 'yellow')
fte_graph.text(x = 2015, y = 370000, s = 'Hawaii', color = 'blue', weight = 'bold', rotation = 0, 
               backgroundcolor = 'yellow')
fte_graph.text(x = 2004, y = 310000, s = 'Massachusetts', color = 'green', weight = 'bold', rotation = 30,
              backgroundcolor = 'yellow')
fte_graph.text(x = 2013, y = 220000, s = 'New Jersey', color = 'red', weight = 'bold',  rotation = 15,
              backgroundcolor = 'yellow');


#  5 plotting the comparison of percentage of homes in decreasing in values vs increasing in values in the US states over different range of years
plt.figure(figsize=(15,8))

cityTimeSeries.groupby(cityTimeSeries['year'])['PctOfHomesDecreasingInValues_AllHomes'].median().plot(linewidth=4,c='pink', legend=False)
cityTimeSeries.groupby(cityTimeSeries['year'])['PctOfHomesIncreasingInValues_AllHomes'].median().plot(linewidth=4,c='yellow')

# creating a  horizontal line at y = 0 
plt.axhline(y = 9, color = 'black', linewidth = 1.3, alpha = .7)
# Add an extra vertical line by tweaking the range of the x-axis
plt.xlim(left = 1996, right = 2017)
# The signature bar
plt.legend()
plt.text(x = 1996, y = 0,
    s = '   Aliya Tyshkanbayeva                                                                                                                                                      Source: Zillow   ',
    fontsize = 14, color = 'white', backgroundcolor = 'black')

# Adding a title and a subtitle
plt.text(x = 1996, y = 95, s = "Comparing Real Estate Properties that are increasing and decreasing in US",
               fontsize = 25, weight = 'bold', alpha = .75)
plt.text(x = 1996, y = 90, 
               s = 'Perentage Of Homes Increasing and Decreasing In Values from 1997 to 2017 in the US states',
              fontsize = 18, alpha = .85)


# 6 Plotting a tree map to see how states differentiate based on their house sale counts based on Zillow Data
# Treemap of listing counts for different states in US 
figr = plt.figure(figsize=(10, 10))
regions=stateTimeSeries.RegionName.value_counts().to_frame()
fd = figr.add_subplot(111, aspect="equal")
fd = squarify.plot(sizes=regions['RegionName'].values,label=regions.index,
              color=sns.color_palette('viridis', 52), alpha=1)
fd.set_xticks([])
fd.set_yticks([])
figr=plt.gcf()
figr.set_size_inches(41,23)
plt.title("Treemap that shows listing counts of different states in US", fontsize=18)
plt.show()