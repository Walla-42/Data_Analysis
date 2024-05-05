import pandas as pd
import matplotlib.pyplot as plt

# Read in dataset for March Netflix Usage
data = pd.read_csv('Netflix_Usage_March_2024.csv', delimiter=',')

# Set 'Date (Pacific)' column to a datetime variable and remove the Usage units. Also
# Change Usage to a float for statistical analysis later
data['Date (Pacific)'] = pd.to_datetime(data['Date (Pacific)'], format='%m/%d/%y %H:%M')
data['Usage'] = data['Usage'].str.replace(' MB', '').astype(float)

# Parse 'Date (Pacific)' into separate date and time columns to be sorted later.
data['Date'] = data['Date (Pacific)'].dt.date
data['Time'] = data['Date (Pacific)'].dt.time

# Create a new dataset from the old to focus on date and usage data
df = data[["Date", "Usage"]]

# Combine all entries of the same date to get overall usage for a single date
df_grouped = df.groupby('Date').sum().reset_index()

# Add Day of the week to gain an understanding of usage on specific days of the week
df_grouped['Date'] = pd.to_datetime(df_grouped['Date'])
df_grouped['Day'] = df_grouped['Date'].dt.day_name()

# Create new column showing possible number of hours watching TV (Based off of 1 Gb/hour for HD Video)
df_grouped['Hours_Watched'] = df_grouped['Usage'] / 1000

# Sort usage data to see which days have the most usage
Usage_perDay = df_grouped.sort_values(['Day', 'Usage'], ascending=[True, True])
print("Usage grouped by day of the week:\n" + str(Usage_perDay))

# Find which days have data usages over 5 Gb (approximately 5 hours of Netflix in HD)
Most_Data = df_grouped[df_grouped['Usage'] > 5000].sort_values(['Usage'], ascending=False)
print("Days with the most Usage in the month of March:\n" + str(Most_Data))

# Find daily data usage averages by grouping by day and taking the mean
daily_averages = df_grouped.groupby('Day')['Usage'].mean().reset_index()

# Convert the 'Date' column to categorical data in order of days of the week
daily_averages['Day'] = pd.Categorical(daily_averages['Day'], categories=['Monday', 'Tuesday', 'Wednesday',
                                                                          'Thursday', 'Friday', 'Saturday',
                                                                          'Sunday'], ordered=True)
# Sort the DataFrame by the categorical 'Date' column and assign to its own variable
daily_averages_sorted = daily_averages.sort_values('Day')

print("Daily average usage:\n" + str(daily_averages_sorted))

# graph daily average usage for the month of March
plt.bar(daily_averages_sorted['Day'], daily_averages_sorted['Usage'])
plt.xlabel('Day of the Week')
plt.ylabel('MB Usage')
plt.title('WiFi Data Usage March 2024')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
