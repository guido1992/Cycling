# In[45]:


# Import Libraries
import glob, os
import numpy as np
import pandas as pd

# Set Max Rows
pd.set_option("display.max_rows", None)

# Set Max columns
pd.set_option("display.max_columns", None)


# In[72]:


# Read in GPX files - wildcard union
GPX = pd.concat(map(pd.read_excel, glob.glob(os.path.join(r'C:\Users\Alex\Desktop\Strava\GPX files', '*_2021.xlsx'))))
GPX.head()


# In[73]:


# Keep specific columns - Only value filled columns
GPX = GPX[['version', 'creator', 'ns1:name43', 'ns1:type51', 'lat52', 'lon53', 'ns1:ele54', 'ns1:time55']]
GPX.head()


# In[74]:


# Rename columns
GPX.rename(columns={'version':'Version',
                    'creator':'Creator',
                    'ns1:name43':'Ride_Name', 
                    'ns1:type51':'XXX', 
                    'lat52':'Latitude',
                    'lon53':'Longitude',
                    'ns1:ele54':'Elevation',
                    'ns1:time55':'DateTime'},
                 inplace=True)
GPX.head()


# In[75]:


# Split DateTime column
GPX[['Date', 'Time']] = GPX.DateTime.str.split("T", expand=True,)
GPX.head()


# In[76]:


GPX[['Time1', 'Other']] = GPX.Time.str.split("Z", expand=True,)
GPX.head()


# In[77]:


# Select only columns we need
GPX = GPX[['Version', 'Creator', 'Ride_Name', 'XXX', 'Latitude', 'Longitude', 'Elevation', 'DateTime', 'Date', 'Time1']]
GPX.head()


# In[78]:


# Rename Time1 column to Time
GPX.rename(columns={'Time1':'Time'},
                 inplace=True)
GPX.head()


# In[79]:


# Remove NA rows
GPX = GPX.dropna()
GPX.head()


# In[80]:


GPX.Ride_Name.unique()


# In[81]:


# Write to csv file - Df.to_csv('Filename.csv') - additions remove index
GPX.to_csv(r'C:\Users\Alex\Desktop\Strava\2021_cycle_XY.csv', 
              index=False, encoding='utf8')


# In[ ]:




