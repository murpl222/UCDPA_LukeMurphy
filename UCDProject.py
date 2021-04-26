import pandas as pd
import numpy as np
url='https://pkgstore.datahub.io/core/global-temp/annual_csv/data/a26b154688b061cdd04f1df36e4408be/annual_csv.csv'
df = pd.read_csv(url)
print(df.head())
print(df.columns)
print(df['Source'].unique())
annual_temp = df[df['Source'] == 'GISTEMP']
annual_temp = annual_temp.loc[:, ['Year', 'Mean']]
annual_temp = annual_temp.sort_values('Year')
print(annual_temp.head())

import requests
url2 = 'https://pkgstore.datahub.io/core/co2-ppm/co2-annmean-mlo_json/data/5168771a128447a2d4c8a77e40844134/co2-annmean-mlo_json.json'
request = requests.get(url2)
data = request.json()
print(data)
print(type(data))
Co2 = pd.DataFrame(data)
print(Co2.columns)
Co2 = Co2.loc[:, ['Mean', 'Year']]
Co2['Year'] = pd.DatetimeIndex(Co2['Year']).year
print(Co2.head())

Co2_temp = pd.merge(annual_temp, Co2, how='inner', on='Year', suffixes=['_temp', '_Co2'])
Co2_temp = Co2_temp.set_index('Year')
print(Co2_temp.head())
# checking for any duplicate rows (none found)
print(Co2_temp.shape, Co2_temp.drop_duplicates().shape)
# checking for any na values to be filled (none found)
print(Co2_temp.isna().sum())

import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.plot(Co2_temp.index, Co2_temp['Mean_temp'], color='b', marker='v', linestyle=':', label='Temperature')
plt.xticks(rotation=45)
ax.set_xlabel('Year')
ax.set_ylabel('Temperture', color='b')
ax.set_title('Annual temperature and Co2 emissions fluctuations')
ax2 = ax.twinx()
ax2.plot(Co2_temp.index, Co2_temp['Mean_Co2'], color='r', marker='o', linestyle=':', label='Co2')
ax2.set_ylabel('Co2 in atmosphere (ppm)', color='r')
ax.legend()
ax2.legend(loc=1)
plt.show()

fig, ax3 = plt.subplots()
ax3.scatter(Co2_temp['Mean_temp'], Co2_temp['Mean_Co2'], c=Co2_temp.index)
ax3.set_xlabel('Temperature')
ax3.set_ylabel('Co2 in atmosphere (ppm)')
plt.show()

correlation = np.corrcoef(Co2_temp['Mean_temp'], Co2_temp['Mean_Co2'])
print(correlation)
# Confirms a very strong correlation between temperature and Co2 levels as seen in the graphs

Mean_temp = Co2_temp['Mean_temp'].tolist()
Mean_Co2 = Co2_temp['Mean_Co2'].tolist()
print(type(Mean_temp), type(Mean_Co2))

# defining a function to extrapolate future data based on previous decade
def extrapolation(list):
     future = (list[-1] + (list[-1] - list[-11])/10)
     list = list.append(future)
     return future


for i in range(25):
    extrapolation(Mean_temp)
    extrapolation(Mean_Co2)

Year = range(1959, 2042, 1)
Co2_temp_extra = pd.DataFrame({'Year': Year, 'Mean_temp': Mean_temp, 'Mean_Co2': Mean_Co2})
Co2_temp_extra = Co2_temp_extra.set_index('Year')
print(Co2_temp_extra.head())

#plot data with future estimates
fig, ax4 = plt.subplots()
ax4.plot(Co2_temp_extra.index, Co2_temp_extra['Mean_temp'], color= 'limegreen', linestyle= '--', label='Temp')
ax5 = ax4.twinx()
ax5.plot(Co2_temp_extra.index, Co2_temp_extra['Mean_Co2'], color= 'b', linestyle= ':', label='Co2')
ax4.set_xlabel('Year')
ax4.set_ylabel('Temperature', color= 'limegreen')
ax5.set_ylabel('Co2 in atmosphere (ppm)', color='b')
ax4.set_title('Temperature and Co2 emissions(ppm) present and forecast data')
ax4.legend()
ax5.legend(loc=1)
plt.show()
