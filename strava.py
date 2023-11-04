# -*- coding: utf-8 -*-
"""Strava.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1kzp6sixl5ZxyjY6G6WmEmKDaW09cS4F8
"""

### ----- IMPORT LIBRARIES -----

from google.colab import auth
import gspread
from google.auth import default
import glob, os
import numpy as np
import pandas as pd

import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.font_manager import FontProperties

!pip install highlight-text
from highlight_text import fig_text

### ----- AUTHENTICATE TO GOOGLE DRIVE -----

auth.authenticate_user()
creds, _ = default()
gc = gspread.authorize(creds)

# Set Max Rows
pd.set_option("display.max_rows", None)

# Set Max columns
pd.set_option("display.max_columns", None)

### ----- CONNECT TO FILE -----

# Define the worksheet
worksheet = gc.open('Strava').sheet1
# Get all values gives a list of rows
rows = worksheet.get_all_values()
# Convert to a DataFrame
df = pd.DataFrame(rows)

### ----- DATA PREP -----

# Creating columns name
df.columns = df.iloc[0]
df = df.iloc[1:]

# Remove blank rows
df = df.replace('', np.nan).dropna()

# Remove value 'Sport' from Sport column header
df = df[df['Sport'] != 'Sport']

# Replace 'Ride' value in Sport column to 'Cycle
df['Sport'] = df['Sport'].replace({'Ride': 'Cycle'})

# Replace values in Title column
df['Title'] = df['Title'].replace({'Morning Ride': 'Morning', 'Morning Cycle': 'Morning', 'Evening Ride':'Evening', 'Lunch Ride':'Afternoon',
                                   'Evening Cycle':'Evening', 'Cycle for Pints':'Evening', 'Post Pints Cycle':'Night', 'Lunch Cycle':'Afternoon',
                                   'Post Cycle Pints':'Night', 'Afternoon Cycle':'Evening', 'Night Cycle':'Night', 'Post Swim Cycle':'Night',
                                   'Pre Swim Cycle':'Evening', 'Morning Spin':'Morning', 'Evening Spin':'Evening', 'Pre Football Cycle':'Night',
                                   'Post Football Cycle':'Night', 'Evebing Cycle':'Evening', 'Night Spin':'Night', 'Morning Sprint':'Morning',
                                   'Afternoon Spin':'Afternoon', 'Evening Sprint':'Evening', 'Lunch Spin':'Afternoon', 'Night Ride':'Night',
                                   'Quick Morning Spin':'Morning'})


# Split Distance column into two new columns to separate the distance and km value
df[['Distance', 'Measurement (km)']] = df.Distance.str.split(" ", expand = True)
# Change value from object to float
df['Distance'] = df['Distance'].astype(float)

# Split Distance column into two new columns to separate the distance and km value
df[['Elevation', 'Measurement (m)']] = df.Elevation.str.split(" ", expand = True)
# Change value from object to float
df['Elevation'] = df['Elevation'].astype(int)

# Split Date column into two new columns to separate Day and Date
df[['Day', 'Date']] = df.Date.str.split(",", expand = True)

# Replace values in Day column
df['Day'] = df['Day'].replace({'Mon': 'Monday', 'Tue':'Tuesday', 'Wed':'Wednesday', 'Thurs':'Thursday', 'Fri':'Friday', 'Sat':'Saturday',
                               'Sun':'Sunday'})

# Convert Date to Date time
df['Date'] = pd.to_datetime(df['Date'])
# Sort for data in chronological order
df = df.sort_values(by='Date')

# Extract the month value and create a new column 'Month' as a string
df['Month'] = df['Date'].dt.strftime('%B')

# Assuming your DataFrame is named 'df'
df['RunningTotal'] = df['Distance'].cumsum()

df.head()

# Last 5 records
df.tail()

### ----- SET VARIABLES -----
text_color = 'black'
background = '#E5E4E2'

### ----- CREATE FIGURE -----

# Create the figure and GridSpec
#fig = plt.figure()
fig, ax = plt.subplots(figsize=(12,8))

# Remove the outline
for spine in ax.spines.values():
    spine.set_linewidth(0)

# Remove the axis ticks
ax.set_xticks([])
ax.set_yticks([])

# Set Gridspec
gs = GridSpec(3, 4)

### ----- CREATE SUBPLOTS -----

# Create axes for the rest of the subplots
#for i in range(1, 4):
#    ax = fig.add_subplot(gs[0, i])

# Create SubplotSpec for the first row of 5 columns
gs_first_row = GridSpec(nrows=1, ncols=5)
ax_first_row = []
for i in range(5):
    ax_first_row.append(fig.add_subplot(gs_first_row[0, i]))
    ax_first_row[-1].axis('off')  # Remove axis

### ----- FIRST SUBPLOT -----

# Calculate total km cycled
Totalkm = df['Distance'].sum()
Totalkm = round(Totalkm)
total_km_text = "Distance\n\n{:,} km".format(Totalkm)

# Add the total km cycled text to the first grid box
ax0 = fig.add_subplot(gs[0, 0])
ax0.text(0.5, 0.5, total_km_text, fontsize=15, ha='center', va='center', fontproperties=FontProperties(weight='bold'))

# Remove axis
ax0.axis('off')

### ----- SECOND SUBPLOT -----

# Total Elevation
Elevation = df['Elevation'].sum()
Elevation = round(Elevation)
elevation = "Elevation\n\n{:,} m".format(Elevation)

# Add total elevation cycled text to the second subplot
ax1 = fig.add_subplot(gs[0, 1])
ax1.text(0.5, 0.5, elevation, fontsize=15, ha='center', va='center', fontproperties=FontProperties(weight='bold'))

# Remove axis
ax1.axis('off')

### ----- THIRD SUBPLOT -----

# Count the number of rides in each week
weekly_rides = df.groupby(df['Date'].dt.week)['Title'].count()
# Calculate the average rides per week
average_rides_per_week = weekly_rides.mean()
average_rides_per_week = round(average_rides_per_week)
ridesweek = "Weekly cycles\n\n{:}".format(average_rides_per_week)

# Add total elevation cycled text to the third subplot
ax2 = fig.add_subplot(gs[0, 2])
ax2.text(0.5, 0.5, ridesweek, fontsize=15, ha='center', va='center', fontproperties=FontProperties(weight='bold'))

# Remove axis
ax2.axis('off')

### ----- FOURTH SUBPLOT -----

# Day most common cycled
most_common_day = df['Day'].mode()[0]
day = f"Cycling day\n\n{most_common_day}"#.format(most_common_day)

# Add total elevation cycled text to the fourth subplot
ax3 = fig.add_subplot(gs[0, 3])
ax3.text(0.5, 0.5, day, fontsize=15, ha='center', va='center', fontproperties=FontProperties(weight='bold'))

# Remove axis
ax3.axis('off')

### ----- 2ND ROW 1ST SUBPLOT -----

ax4 = fig.add_subplot(gs[1:5, 0:2])

# Define the correct order of the months
month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
               'August', 'September', 'October', 'November', 'December']

# Convert the 'Month' column to a categorical data type with the correct order
df['Month'] = pd.Categorical(df['Month'], categories=month_order, ordered=True)

# Group by month and calculate the total distance cycled for each month
monthly_distance = df.groupby('Month')['Distance'].sum()

# Plotting the bar plot
monthly_distance.plot(kind='bar', ax=ax4)

# Setting labels and title
ax4.set_xlabel('Month')
#ax4.set_ylabel('Distance Cycled (km)')
ax4.set_title('Distance Cycled by Month')

# Remove axis
ax4.spines['top'].set_visible(False)  # Remove top border
#ax4.spines['bottom'].set_visible(False)  # Remove bottom border
#ax4.spines['left'].set_visible(False)  # Remove left border
ax4.spines['right'].set_visible(False)  # Remove right border
ax4.tick_params(axis='both', which='both', length=0)  # Remove tick marks

### ----- 2ND SUBPLOT 2ND SUBPLOT -----

ax5 = fig.add_subplot(gs[1:5, 2:5])  # Use colspan to fill up the width
# Line plot
sns.lineplot(data=df, x='Date', y='RunningTotal', ax=ax5)
# Add plot labels
ax5.set_title('Running Total of kilometres cycled')
plt.xlabel('\nDate', fontsize=10) #x-axis label
#plt.ylabel('\nRunning total of kilometres cycled', fontsize=12) #y-axis label
plt.ylabel('\n')

# Title
#fig_text(
#    x = 0.125, y = 0.63,
#    s = f'Running total of kilometres cycled',
#    color = text_color,
#    weight = "bold",
#    va = 'center',
#    ha = 'left',
#    size = 15
#    )

# Remove axis
ax5.spines['top'].set_visible(False)  # Remove top border
#ax4[-1].spines['bottom'].set_visible(False)  # Remove bottom border
#ax4[-1].spines['left'].set_visible(False)  # Remove left border
ax5.spines['right'].set_visible(False)  # Remove right border
ax5.tick_params(axis='both', which='both', length=0)  # Remove tick marks

### ----- TEXT & DESCRIPTION -----

# Title
fig_text(
    x = 0.125, y = 1.08,
    s = f'Cycling Dashboard',
    color = text_color,
    weight = "bold",
    va = 'center',
    ha = 'left',
    size = 15
    )

# Description
fig_text(
    x = 0.125, y = 0.95,
    s = f"In 2023, I decided to approach goal setting differently compared to previous years. As part of this new approach, I set myself a\n"
         "demanding target of cycling 2,500km from January 1st to June 30th. Although it may not seem overly difficult when broken down\n"
         "on a daily basis, incorporating this goal into my already busy schedule of daily activities, career commitments, hobbies, family time,\n"
         "socialising, and part-time work proved to be quite challenging.\n\n"

         "Despite the challenges, I diligently tracked and analysed my daily progress, capturing essential details such as distance, elevation,\n"
         "and duration. By maintaining a running total calculation, I was able to monitor my cumulative progress over time, which proved\n"
         "instrumental in setting and monitoring my overall achievement towards the goal.\n\n",
    color = text_color,
    va = 'center',
    ha = 'left',
    size = 10
    )

# Adjust the spacing between subplots
plt.subplots_adjust(wspace=0.1, hspace=0.1)

plt.setp(ax5.get_xticklabels(), rotation = 45)

# Show the figure
plt.show()

### ----- GRAPH ADDITIONS -----