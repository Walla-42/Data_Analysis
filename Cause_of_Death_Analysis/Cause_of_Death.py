import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(
    'AH_Monthly_Provisional_Counts_of_Deaths_for_Select_Causes_of_Death_by_Sex__Age__and_Race_and_Hispanic_Origin.csv')

# print(df.head())
# print(df.columns)

#Create data set isolating alzheimer's disease deaths with other identifiers for analysis:
df_Alzheimers = df[['Date Of Death Year', 'Sex', 'Race/Ethnicity', 'AgeGroup', 'Jurisdiction of Occurrence',
                    'Alzheimer disease (G30)']]
df_Alzheimers_sort = df_Alzheimers[df_Alzheimers['Alzheimer disease (G30)'] > 0].sort_values('Alzheimer disease (G30)',
                                                                                             ascending=False)
#Unify Male and Female Values to just 'M' and 'F'
df_Alzheimers_sort['Sex'] = df_Alzheimers_sort['Sex'].replace({'Female': 'F', 'Male': 'M'})

Alzheimer_Sex = df_Alzheimers_sort['Sex'].value_counts()['M']
print(Alzheimer_Sex)

#Count how many deaths in the US were caused by Alzheimer's disease from 2019 to 2021:
print("Number of Deaths by Alzheimer's disease in the US in 2019-2021: ",
      df_Alzheimers['Alzheimer disease (G30)'].sum())

#Create a unique data set summarizing deaths by Alzheimer's disease per year
A_Death_by_year = df_Alzheimers_sort.groupby('Date Of Death Year').sum().reset_index()
print(A_Death_by_year)
print("Number of Deaths in 2019: ", A_Death_by_year.loc[0, 'Alzheimer disease (G30)'])
print("Number of Deaths in 2020: ", A_Death_by_year.loc[1, 'Alzheimer disease (G30)'])
print("Number of Deaths in 2021: ", A_Death_by_year.loc[2, 'Alzheimer disease (G30)'])

# Graph the death by year data on a bar plot for visualization
plt.bar(A_Death_by_year['Date Of Death Year'], A_Death_by_year['Alzheimer disease (G30)'], width=0.4)
plt.title('Alzheimer Disease Deaths by Year')
plt.xlabel("Deaths Per Year")
plt.ylabel('Number of Deaths')
plt.title('Year of Deaths')
plt.xticks(A_Death_by_year['Date Of Death Year'], rotation=45)
plt.tight_layout()
plt.show()

# Graph the death by age group for Alzheimer Disease on a bar plot for visualization
Alz_death_by_age = df.groupby('AgeGroup')[['Alzheimer disease (G30)']].sum().reset_index().drop(index=5)
print(Alz_death_by_age['AgeGroup'])
plt.bar(Alz_death_by_age['AgeGroup'], Alz_death_by_age['Alzheimer disease (G30)'], width=0.4)
plt.title('Number of Alzheimer Deaths by Age 2019 - 2021')
plt.xticks(Alz_death_by_age['AgeGroup'], rotation=45, size=9)
plt.yticks(size=9)
plt.xlabel('Age Group', size=12)
plt.ylabel('Number of Deaths', size=12)
plt.tight_layout()
plt.show()

# Let's show how deaths from heart disease correlate with your age group
Heart_death_by_age = df.groupby('AgeGroup')['Diseases of heart (I00-I09,I11,I13,I20-I51)']\
    .sum().reset_index().drop(index=5)
plt.bar(Heart_death_by_age['AgeGroup'], Heart_death_by_age['Diseases of heart (I00-I09,I11,I13,I20-I51)'], width=0.4)
plt.title('Heart Related Deaths by Age Group')
plt.xticks(Heart_death_by_age['AgeGroup'], rotation=45, size=9)
plt.yticks(size=9)
plt.ylabel('Number of Deaths', size=12)
plt.xlabel('Age Group', size=12)
plt.tight_layout()
plt.show()

#How many people die from heart disease each year of the data set? How does this compare to Alzheimer Disease?
Heart_deaths_by_year = df.groupby('Date Of Death Year')['Diseases of heart (I00-I09,I11,I13,I20-I51)'].sum()\
    .reset_index()
print(Heart_deaths_by_year)
plt.bar(Heart_deaths_by_year['Date Of Death Year'],
         Heart_deaths_by_year['Diseases of heart (I00-I09,I11,I13,I20-I51)'], width=0.4)
plt.title('Number of Heart Disease Deaths by Year ')
plt.xlabel('Year', size=12)
plt.ylabel('Number of Deaths', size=12)
plt.xticks(Heart_deaths_by_year['Date Of Death Year'], rotation=45, size=9)
plt.yticks(size=9)
plt.tight_layout()
plt.show()


#Compare Heart Disease deaths to Alzheimer Deaths 
Heart_Alzheimer_comp = Heart_deaths_by_year.merge(A_Death_by_year, on='Date Of Death Year', how='inner')
print(Heart_Alzheimer_comp)

plt.bar(Heart_Alzheimer_comp['Date Of Death Year'], Heart_Alzheimer_comp['Alzheimer disease (G30)'],
        label='Alzheimer Disease', color='black', width=0.4)
plt.bar(Heart_Alzheimer_comp['Date Of Death Year'], Heart_Alzheimer_comp['Diseases of heart (I00-I09,I11,I13,I20-I51)'],
        label='Heart Disease', color='r', alpha=0.3, width=0.4)
plt.title('Heart Disease vs Alzheimer Disease Deaths')
plt.xlabel('Year', size=12)
plt.ylabel('Number of Deaths', size=12)
plt.xticks(Heart_deaths_by_year['Date Of Death Year'], size=9)
plt.yticks(size=9)
plt.legend()
plt.tight_layout()
plt.show()


