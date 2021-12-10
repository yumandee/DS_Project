#!/usr/bin/env python
# coding: utf-8

# # Data Science Project: Ethnic Bias of Standardized Testing
# ### By: Mandy Yu, Fall 2021
# ### Github: <a href="https://github.com/yumandee" target="_new">https://github.com/yumandee</a>
# ### LinkedIn: <a href="https://www.linkedin.com/in/mandy-yu-378a49162/" target="_new">https://www.linkedin.com/in/mandy-yu-378a49162/</a>
# 
# The institutionalized Standardized Testing of New York State has inaccurately reflected students’ mental capacities. This project explores whether or not there is a correlation between the New York Statewide English Language Arts and Math Exam results and student ethnicity across all school districts. In this project, the ethnic composition of test results will be explored to expose the inaccuracy and unfairness of standardized testing. 
# 
# I examined the top scoring schools in NYC and took a closer look at their ethnic compositions. A correlation ranker revealed that as the population of certain ethnicities (typically non-minority groups such as White or Asian students) increased, so too did the mean scale score. The opposite also applies where as the population of certain ethnicities (typically minority groups such as Black or Hispanic students) decreased, so too did the mean scale score.
# 

# In[102]:


# score_map


# ## Datasets
# 
# This project uses data from OpenData NYC on New York State Standardized Testing results from 2013-2018. 
# - **ELA Test Results From 2013-18 by District:** 
# - **Math Test Results From 2013-18 by District:** 
# 
# The ELA and Math statewide tests evaluate a student beginning from 3rd grade until 8th grade on their ability to solve Common Core questions. Students are evaluated on a scale from 1-4, 1 being the lowest and 4 being the highest. These datasets provide information on schools in New York City and their reported test scores. The information includes the percentage and number of students who received a certain exam score. Information is provided for every grade at the listed school.  
#   
# - **Ethnic Demographics of NYC Public Schools from 2013-2018:** 
# 
# This dataset provides information on the demographic snapshot of the same schools listed in the statewide exam result datasets. The information provided includes the total number of students in each grade, gender composition, ethnic composition and economic composition of students. Only the ethnic composition data is utilized in this project as the ratio of female to male remained around an even split of 50% and the timespan of the project would not allow for an in-depth exploration of the economic composition in relation to the exam scores.
# 
# - **School Locations 2017-2018**:
# 
# This dataset was used to create a map of the school locations.
# 
# 
# ## Techniques
# 
# To explore the datasets and test if there existed an ethnic bias in standardized testing, I utilized my knowledge of pandas to effectively clean and gather data. With my previous experience in json files, I was able to get data from the OpenData NYC website without downloading csv files. I used a correlation ranker and scatter plots to explore if there existed a correlation between ethnicity and exam scores.
# 
# ## Resources
# 
# - https://towardsdatascience.com/choropleth-maps-with-folium-1a5b8bcdd392
# 
# - https://pandas.pydata.org/docs/reference/index.html
# 
# - https://python-visualization.github.io/folium/
# 
# - https://sakshumkulshrestha.github.io/
# 
# - https://opendata.cityofnewyork.us/projects/introduction-to-choropleth-maps/
# 
# - https://www.kaggle.com/daveianhickey/how-to-folium-for-maps-heatmaps-time-data/notebook
# 
# - https://github.com/randyzwitch/streamlit-folium/blob/bd61709e91724fc53994259df897f15c93927aac/streamlit_folium/__init__.py#L79
# 
# Datasets: 
# - https://data.cityofnewyork.us/Education/2013-2019-English-Language-Arts-ELA-Test-Results-S/gu76-8i7h 
# 
# - https://data.cityofnewyork.us/Education/2013-2019-Math-Test-Results-School-SWD-Ethnicity-G/74ah-8ukf
# 
# - https://data.cityofnewyork.us/Education/2013-2018-Demographic-Snapshot-School/s52a-8aq6
# 
# - https://data.cityofnewyork.us/Education/2017-2018-School-Locations/p6h4-mpyy 
# 

# # Code

# In[86]:


import pandas as pd
import pandasql as psql
import requests
import json
import folium
from folium import plugins
import matplotlib.pyplot as plt

# get_ipython().run_line_magic('matplotlib', 'inline')


# <h2> Gathering and Cleaning Data </h2>
# 
# This project explores data on New York Statewide English Language Arts and Math exams from the 2012-13 to 2017-18 school years. 
# In the 2018-19 school year, the statewide exam was changed from three days of testing to two. Thus, data from the 2018-19 school year was omitted. The project also utilizes geographical data to create a mapped visualization of the correlation between exam results and ethnicity. 
# 
# The NY Statewide ELA and Math Exams are graded on a scale of 1-4 where:
# <ul>
#     <li> 1: Little or No Mastery </li>
#     <li> 2: Partial Mastery of Target </li>
#     <li> 3: Meets Expectations </li>
#     <li> 4: Advanced </li>
# </ul>
# 
# ### **ELA Test Results from 2013-2018 by District**

# In[3]:


res = requests.get('https://data.cityofnewyork.us/resource/gu76-8i7h.json?$limit=32826')
cols = {'dbn': 'DBN', 'school_name':'School Name', 'grade': 'Grade', 'year':'Year',         'number_tested':'Number Tested', 'mean_scale_score':'Mean Scale Score','level_1':'# Level 1', 'level_1_1':'% Level 1',         'level_2':'# Level 2', 'level_2_1':'% Level 2', 'level_3':'# Level 3', 'level_3_1':'% Level 3',         'level_4':'# Level 4', 'level_4_1':'% Level 4', 'level_3_4': '# Level 3+4', 'level_3_4_1':'% Level 3+4'}
# Extract columns from json and rename the columns 
ela_df = pd.DataFrame(res.json(), columns = cols).rename(columns = cols)
ela_df = ela_df.loc[ela_df['Mean Scale Score'] != 's'] # there exists rows without number values
ela_df = ela_df.loc[ela_df['Grade'] != 'All Grades']
ela_df


# *Data obtained from OpenData NYC: https://data.cityofnewyork.us/Education/2013-2019-English-Language-Arts-ELA-Test-Results-S/gu76-8i7h*
# 
# ### **Math Test Results from 2013-2018 by District**

# In[4]:


res = requests.get('https://data.cityofnewyork.us/resource/74ah-8ukf.json?$limit=32826')

# Extract columns from json and rename the columns (same columns as ela_df)
math_df = pd.DataFrame(res.json(), columns = cols).rename(columns = cols)
math_df = math_df.loc[math_df['Mean Scale Score'] != 's'] # there exists rows without number values
math_df = math_df.loc[math_df['Grade'] != 'All Grades']

math_df


# *Data obtained from OpenData NYC: https://data.cityofnewyork.us/Education/2013-2019-Math-Test-Results-School-SWD-Ethnicity-G/74ah-8ukf*
# 
# To effectively work with these number values, we need to convert columns to the appropriate datatypes. This applies to both math and ela dataframes.

# In[5]:


ela_df.dtypes


# In[6]:


ela_df['Grade'] = ela_df['Grade'].astype(int)
math_df['Grade'] = math_df['Grade'].astype(int)
cols = ['Number Tested', 'Mean Scale Score', '# Level 1','% Level 1', '# Level 2','% Level 2',        '# Level 3','% Level 3', '# Level 4','% Level 4', '# Level 3+4', '% Level 3+4']
for col in cols:
    ela_df[col] = ela_df[col].astype(float)
    math_df[col] = math_df[col].astype(float)


# In[7]:


ela_df.dtypes


# ### **Ethnic Demographics of NYC Public Schools from 2013-2018**

# In[8]:


res = requests.get('https://data.cityofnewyork.us/resource/s52a-8aq6.json?$limit=8972')
cols = {'dbn':'DBN', 'school_name':'School Name', 'year':'Year', 'total_enrollment':'Total Enrollment',         'grade_3':'Grade 3', 'grade_4':'Grade 4','grade_5':'Grade 5','grade_6':'Grade 6','grade_7':'Grade 7',         'grade_8':'Grade 8','asian_1':'# Asian', 'asian_2':'% Asian', 'black_1':'# Black', 'black_2':'% Black',         'hispanic_1':'# Hispanic', 'hispanic_2':'% Hispanic', 'multiple_race_categories_not_represented_1':'# Other',        'multiple_race_categories_not_represented_2':'% Other', 'white_1':'# White', 'white_2':'% White'}

#Extract columns from json and rename the columns to easily distinguish # and % 
demographics_df = pd.DataFrame(res.json(), columns = cols).rename(columns=cols)

demographics_df


# *Data obtained from OpenData NYC: https://data.cityofnewyork.us/Education/2013-2018-Demographic-Snapshot-School/s52a-8aq6*
# 
# I utilized apply() to extract the district for all schools for the ELA, Math, and Demographic dataframes. This will be used to visualize by district.

# In[9]:


"""
@param name: string of public school code formatted as "01M015" 
@return: district extracted from public school code
"""
def extractDistrict(name):
    return  int(name[:2])


# In[10]:


ela_df.insert(0, 'District', ela_df['DBN'].apply(extractDistrict))

ela_df.head()


# In[11]:


math_df.insert(0, 'District', math_df['DBN'].apply(extractDistrict))

math_df.head()


# In[12]:


demographics_df.insert(0, 'District', demographics_df['DBN'].apply(extractDistrict))

demographics_df


# ### **NYC Public School Location Data from 2017-18**

# In[13]:


res = requests.get('https://data.cityofnewyork.us/resource/p6h4-mpyy.json?$limit=1823')
cols = {"geographical_district_code":"District", "ats_system_code":"DBN", "location_name":"School Name", "location_1":"Location"}

location_df = pd.DataFrame(res.json(), columns=cols).rename(columns=cols)
location_df.head()


# *Data obtained from OpenData NYC: https://data.cityofnewyork.us/Education/2017-2018-School-Locations/p6h4-mpyy*
# 
# After cleaning the data to extract only the necessary columns and renaming them to consist with the other dataframes, the location column contains coordinates that need to be extracted.
# 
# 
# If we take a look closer at one of the entries, it appears to be a Python dictionary. With this, indexing and extracting the columns needed can be done easily.
# 

# In[14]:


location_df["Location"][0]


# In[15]:


lat = []
lon = []
for idx, row in location_df.iterrows():
    location = row['Location']
    if type(location) is float:
        lat.append(0)
        lon.append(0)
    else:
        lat.append(location['latitude'])
        lon.append(location['longitude'])
location_df['Latitude']  = lat
location_df['Longitude'] = lon


location_df = location_df.loc[location_df['Latitude'] != 0]
location_df


# # Analysis 
# 
# 
# The average mean scale score and average count/percentages of students were calculated for each grade in each district.
# 
# ### **ELA Average Test Scores by District and Grade**

# In[16]:


def groupByDistrictGrade(df, columns):
    d = df.groupby('District')
    data = {key: [] for key in columns}

    for i in range(1, 33): # loop for districts 1-32
        district = d.get_group(i)
        grades = district['Grade'].unique()
        grade = district.groupby('Grade')
        for g in range(grades[0], grades[-1] + 1): # loop for grades 3-8
            data['District'].append(i)
            data['Grade'].append(g)
            data['Number Tested'].append(grade.get_group(g)['Number Tested'].sum().astype(int))
         
        for col in columns[3:]: # ignore District, Grade, and Number Tested columns
            for g in range(grades[0], grades[-1] + 1): # loop for possible grades in district (not all districts are gr3-8)
                data[col].append(float("{:.2f}".format(grade.get_group(g)[col].mean())))
    df = pd.DataFrame.from_dict(data)
    return df


# In[17]:


columns = ['District', 'Grade', 'Number Tested', 'Mean Scale Score', '# Level 1', '% Level 1', '# Level 2',
           '% Level 2', '# Level 3', '% Level 3', '# Level 4', '% Level 4', '# Level 3+4', '% Level 3+4']
ela_averages = groupByDistrictGrade(ela_df, columns)

ela_averages


# ### **Math Average Test Scores by District and Grade**

# In[18]:


math_averages = groupByDistrictGrade(math_df, columns)
math_averages


# The percentage of students who received a satisfactory score (3 or 4) on the statewide exam is reflected in % Level 3+4 column. Let's take a look at the range of values for every grade in all districts.

# In[19]:


def calculateRangeByGrade(df, col):
    df = df.groupby('Grade')
    data = {'Grade': [], 'Lowest': [], 'Highest': [], 'Range':  []}
    for i in range(3, 9):
        highest = df.get_group(i)[col].max()
        lowest = df.get_group(i)[col].min()
        rnge = float("{:.2f}".format(highest-lowest))
        data['Grade'].append(i)
        data['Lowest'].append(lowest)
        data['Highest'].append(highest)
        data['Range'].append(rnge)
    return pd.DataFrame.from_dict(data)


# In[20]:


ela_ranges_bygrade = calculateRangeByGrade(ela_averages, '% Level 3+4')
ela_ranges_bygrade


# In[21]:


math_ranges_bygrade = calculateRangeByGrade(math_averages, '% Level 3+4')
math_ranges_bygrade


# In both the ELA and math averages, there is a high difference between districts. In the ELA data, one district had 20.78% of their third grade students from 2013-18 receive a satisfactory score of 3 or 4. Another district had 67.36% of their third grade students from 2013-18 receive a 3 or 4. This is nearly a 50% difference. In the math data, one district had 15.15% of their 5th grade students from 2013-18 receive of 3 or 4 and another had 73.85%. That is nearly a 60% difference.
# 
# With this information, it is evident there is a difference between districts. In this project, I explore how ethnicity possibly 
# influences the averages. So, let's take a look at each districts' ethnic composition.

# In[22]:


demographics_df.head()


# First, let's convert the datatypes of the appropriate columns to floats.

# In[23]:


columns = list(demographics_df.columns)
demographics_df[columns[4:]] = demographics_df[columns[4:]].astype(float)
demographics_df.dtypes


# Now, let's average the demographics from 2013-18 for each district.

# In[24]:


def avgDemographics(df):
    districts = df.groupby('District')
    columns = list(df.columns)
    columns.remove('DBN')
    columns.remove('School Name')
    columns.remove('Year')
    data = {key: [] for key in columns}
    for i in range(1, 33): #Districts 1-32 (To match ELA and Math datasets)
        district = districts.get_group(i)
        data['District'].append(i)
        data['Total Enrollment'].append(int(district['Total Enrollment'].sum()))
        for col in columns[2:]:
            data[col].append(float("{:.2f}".format(district[col].mean())))
    return pd.DataFrame.from_dict(data)
        
    
avg_demographics = avgDemographics(demographics_df)
avg_demographics


# ### **Bottom 5 Districts and Ethnicity**
# 
# Let's observe the bottom 5 districts based on their mean scale score for 5th graders and explore if there exists a potential correlation between ethnicity and score. In the dataframe below, the lowest 5 scoring schools are shown. In four of the lowest scoring districts, the majority of the student population was greater than **65%** Hispanic. In District 5, **50.71%** of the student population was Black.

# In[25]:


data = pd.merge(ela_averages, avg_demographics, on="District", how='left') # merge ela averages and demographics
data.groupby('Grade').get_group(5).sort_values(by='Mean Scale Score')[:5] # group by 5th grade and sort to get 5 lowest districts


# ### **Top 5 Districts and Ethnicity**
# 
# Let's observe the top 5 districts based on their mean scale score for 5th graders and again explore if there exists a potential correlation between ethnicity and score. In the dataframe below, the highest 5 scoring schools are shown. District 26, 20, and 25 have majority Asian students (nearly 50%). District 2 shows a somewhat even distribution between all ethnicities. District 3 shows an even distribution between Black, Hispanic, and White students. 
# 
# With the bottom and top 5 scoring districts, there is a correlation between mean scale score and ethnicity. However, the correlation is not strong as minority groups are capable of scoring high on the statewide tests.

# In[26]:


# group by 5th grade and sort to get 5 lowest districts
data.groupby('Grade').get_group(5).sort_values(by='Mean Scale Score', ascending=False)[:5] 


# <h2> Visualizations </h2>
# 

# Let's confirm if there exists a correlation between ethnicity and score using the Pearson correlation ranker.

# In[27]:


indexes = [2,3,5,7,9,11,13,22,24,26,28,30] #limit the columns (remove district and grade and # values)
corrdf = data[data.columns[indexes]]
corrdf.corr().style.background_gradient(cmap="Blues")


# Let's take a close look at the correlation between ethnicity and percentage of students in the district who received a satisfactory grade of 3 or 4.
# 
# **% Asian vs % Level 3+4**
# 
# There is a strong positive correlation of **0.751451** between the percentage of Asian students and students with 3 or 4. This indicates that as the percentage of Asian students increases, the percentage of students who receive 3 or 4 also increases. This means the population of Asian students possibly influences the percentage of students who receive a satisfactory score. This correlation suggests that a higher percenteage of Asian students results in more students who receive a 3 or 4.
# 
# **% Black vs % Level 3+4**
# 
# There is a weak negative correlation of **-0.448200** between the percentage of Black students and students with 3 or 4. This indicates that as the percentage of Black students increases, the percentage of students who receive 3 or 4 decreases. This indicates a possible influence of ethnicity on the percentage of students who receive a satisfactory score. This correlation suggests that a higher percentage of Black students results in less students who receive 3 or 4.
# 
# 
# ## Scatter Plots
# 
# **% Asian vs % Level 3+4**

# In[28]:


def scatterPlot(col1, col2):
    plt.scatter(corrdf[col1], corrdf[col2])
    plt.xlabel(col1)
    plt.ylabel(col2)


# In[29]:


scatterPlot('% Asian', '% Level 3+4')


# **% Black vs % Level 3+4**

# In[30]:


scatterPlot('% Black', '% Level 3+4')


# **% White vs % Level 3+4**

# In[31]:


scatterPlot('% White', '% Level 3+4')


# **% Hispanic vs % Level 3+4**

# In[32]:


scatterPlot('% Hispanic', '% Level 3+4')


# These scatter plots suggest that for minority groups, the schools with higher populations of minority students, the lower the average statewide test score. While this may not be directly influenced by the ethnicity, there is a suggestion that there exists this influence.

# ## **School District Zones**

# In[103]:


# school_map = folium.Map(location=[40.69022469799167, -73.9871222729115], zoom_start=10)

# folium.Choropleth(
#     geo_data='School Districts.geojson',
#     name='School Districts',
#     fill_opacity=0.3,
#     line_opacity=1
# ).add_to(school_map)


# school_map


# In[82]:


# data['District'] = data['District'].astype(str)


# In[101]:


# score_map = folium.Map(location=[40.69022469799167, -73.9871222729115], zoom_start=10)

# folium.Choropleth(
#     geo_data='School Districts.geojson',
#     fill_opacity=0.75, 
#     line_opacity=1,
#     threshold_scale = list(range(100, 500, 50)),
#     data = data,
#     key_on='feature.properties.school_dist',
#     columns = ['District', 'Mean Scale Score']
# ).add_to(score_map)

