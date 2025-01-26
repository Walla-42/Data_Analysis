import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# import seaborn as sns
""" This program uses the 'NCHS_-_Leading_Cause_of_Death__United_States.csv' for its analysis which can be found along side this code file. 
You can also view the graphs in this code under the seaborn styling if the seaborn package is installed. This can be installed with 'pip install seaborn' and 
removing the hashed commands. """
# sns.set()
df = pd.read_csv('NCHS_-_Leading_Causes_of_Death__United_States.csv')
print(df.shape)

df_UT_2017 = df[(df['Year'] == 2017) & (df['State'] == 'Utah')].sort_values(by='Deaths', ascending=False, ignore_index=True)

"""This section of code prints out some values I found helpful in determining what I did and did not want to see in my data. It also
allowed me to see some problematic and vague values in the dataset. """
df_UT = df[df['State'] == 'Utah'].sort_values('Deaths', ascending=False)
print(df['Cause Name'].unique())
print(df['Year'].unique())
print(df_UT)

#analyzing trends of cause of death from 1999 to 2017 in Utah:
df_1999_2017_UT = df[((df['State'] == 'Utah') & (df['Cause Name'] != 'All causes'))].sort_values('Year', ascending=False, ignore_index=True)

df_pivot_year_UT = df_1999_2017_UT.pivot_table(index='Year', columns='Cause Name', values='Deaths', aggfunc='sum', fill_value=0)
print(df_pivot_year_UT)

#ploting the trends
plt.figure(figsize=(14,8))
for cause in df_pivot_year_UT.columns:
    plt.plot(df_pivot_year_UT.index, df_pivot_year_UT[cause], label=cause)

plt.xlabel('Year')
plt.ylabel('Number of Deaths')
plt.title('Number of Deaths Per Year by Cause in Utah (1999-2017)')
plt.legend(title='Cause of Death', loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2)
plt.xticks(df_pivot_year_UT.index, df_pivot_year_UT.index.astype(int), rotation=45)
plt.tight_layout()
plt.show()

