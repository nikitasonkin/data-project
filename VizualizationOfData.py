import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px

df_normalized = pd.read_csv('input2_df_cleaned_normalized.csv', encoding='ISO-8859-1')


# גרף מס 1
happiness_data = df_normalized.groupby('Country name')['Life Ladder'].mean()
happiness_data.sort_values().plot.bar(figsize=(20, 10))
plt.title('Average Happiness Index by Country')
plt.xlabel('Country')
plt.ylabel('Average Happiness Index')
plt.xticks(rotation=90, fontsize=8)
plt.tight_layout()
plt.show()


# גרף מס 2
df_normalized.plot.scatter(x='Log GDP per capita', y='Healthy life expectancy at birth', alpha=0.5)
plt.title('GDP per Capita vs Healthy Life Expectancy')
plt.xlabel('Log GDP per Capita')
plt.ylabel('Healthy Life Expectancy at Birth')
plt.show()

# גרף מס 3
df_normalized['Social support category'] = pd.cut(df_normalized['Social support'], bins=10)
support_corruption = df_normalized.groupby('Social support category', observed=True)['Perceptions of corruption'].mean()
support_corruption.plot.bar(figsize=(14, 8))
plt.title('Average Perceived Corruption by Social Support Level')
plt.xlabel('Social Support Level')
plt.ylabel('Average Perceptions of Corruption')
plt.xticks(rotation=0, fontsize=10)
plt.show()

# גרף מס 4
selected_countries = df_normalized[df_normalized['Country name'].isin(['Afghanistan', 'Albania', 'United States', 'United Kingdom'])]
plt.figure(figsize=(14, 8))
for country in selected_countries['Country name'].unique():
    country_data = selected_countries[selected_countries['Country name'] == country]
    plt.scatter(country_data['year'], country_data['Life Ladder'], s=country_data['Life Ladder']*100, alpha=0.5, label=country)
plt.title('Happiness Index Over Time')
plt.xlabel('Year')
plt.ylabel('Life Ladder')
plt.legend()
plt.show()



# גרף מס 5
# בחירת המדינות הנבחרות
selected_countries = df_normalized[df_normalized['Country name'].isin(['Iceland', 'France', 'Italy', 'Israel'])].copy()

# איחוד הנתונים לפי מדינות ושנים
aggregated_data = selected_countries.groupby(['Country name', 'year']).agg({
    'Log GDP per capita': 'mean',
    'Life Ladder': 'mean',
    'Generosity': 'mean'
}).reset_index()

# הפיכת הנתונים לפורמט ארוך עבור Plotly Express
melted_data = aggregated_data.melt(id_vars=['Country name', 'year'], value_vars=['Log GDP per capita', 'Life Ladder', 'Generosity'], var_name='Metric', value_name='Value')

# יצירת גרף חום
fig = px.density_heatmap(melted_data, x='year', y='Country name', z='Value', facet_col='Metric', title='GDP per Capita, Happiness, and Generosity Levels Over Time')
fig.show()


# גרף מס 6
fig = px.scatter_3d(df_normalized, x='Life Ladder', y='Social support', z='Perceptions of corruption', color='Country name')
fig.update_layout(title='3D Scatter Plot of Happiness, Social Support, and Perceived Corruption')
fig.show()


#גרף מס 7
# בחירת מדינות לדוגמה להצגה בגרף
selected_countries = df_normalized[df_normalized['Country name'].isin(['United States', 'United Kingdom', 'Germany', 'France', 'Israel', 'Japan'])]

# קטגוריזציה של השחיתות הנתפסת כדי להקל על הצפייה
selected_countries.loc[:, 'Corruption Category'] = pd.cut(selected_countries['Perceptions of corruption'], bins=5).astype('category')


# יצירת גרף Box Plot עבור תוחלת החיים הבריאה לפי מדינות
plt.figure(figsize=(14, 8))
sns.boxplot(x='Country name', y='Healthy life expectancy at birth', data=selected_countries, hue='Corruption Category')
plt.title('Box Plot of Healthy Life Expectancy by Country and Perceived Corruption')
plt.xlabel('Country')
plt.ylabel('Healthy Life Expectancy at Birth')
plt.xticks(rotation=45, fontsize=12)
plt.yticks(fontsize=12)
plt.legend(title='Perceived Corruption', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()


# גרף מס 8
# בחירת מדינות לדוגמה להצגה בגרף
selected_countries = df_normalized[df_normalized['Country name'].isin(['United States', 'United Kingdom', 'Germany', 'France', 'Israel', 'Japan'])]

# יצירת גרף Violin Plot עבור ההכנסה לנפש לפי מדינות
plt.figure(figsize=(14, 8))
sns.violinplot(x='Country name', y='Log GDP per capita', data=selected_countries)
plt.title('Violin Plot of GDP per Capita by Country')
plt.xlabel('Country')
plt.ylabel('Log GDP per Capita')
plt.xticks(rotation=45, fontsize=12)
plt.yticks(fontsize=12)
plt.tight_layout()
plt.show()


#גרף מס 9
# בחירת מדינות לדוגמה להצגה בגרף
selected_countries = df_normalized[df_normalized['Country name'].isin(['United States', 'United Kingdom', 'Germany', 'France', 'Israel', 'Japan'])]

plt.figure(figsize=(14, 8))

# הצגת מדדי האושר לאורך זמן
for country in selected_countries['Country name'].unique():
    country_data = selected_countries[selected_countries['Country name'] == country]
    plt.plot(country_data['year'], country_data['Life Ladder'], label=f'{country} - Happiness')

# הצגת מדדי הבריאות לאורך זמן
for country in selected_countries['Country name'].unique():
    country_data = selected_countries[selected_countries['Country name'] == country]
    plt.plot(country_data['year'], country_data['Healthy life expectancy at birth'], linestyle='--', label=f'{country} - Health')

plt.title('Happiness and Health Over Time')
plt.xlabel('Year')
plt.ylabel('Index Value')
plt.legend()
plt.tight_layout()
plt.show()


#גרף מס 10
# יצירת מפה כורופלית של מדדי אושר מנורמלים
fig = px.choropleth(df_normalized,
                    locations="Country name",
                    locationmode='country names',
                    color="Life Ladder_NORM",
                    hover_name="Country name",
                    color_continuous_scale=px.colors.sequential.Plasma,
                    title='World Happiness Levels (Normalized)')

fig.update_layout(geo=dict(showframe=False, showcoastlines=False, projection_type='equirectangular'))
fig.show()



#גרף מס 11
# בחירת עמודות מעניינות לניתוח
columns_of_interest = ['Life Ladder_NORM', 'Log GDP per capita', 'Social support', 'Generosity', 'Healthy life expectancy at birth']

# יצירת גרף תיאום מקבילי
fig = px.parallel_coordinates(df_normalized,
dimensions=columns_of_interest,
color="Life Ladder_NORM",
color_continuous_scale=px.colors.sequential.Plasma,
title='Parallel Coordinates Plot of Key Indicators')
fig.show()



#גרף מס 12
# בחירת מדינות לדוגמה להצגה בגרף
selected_countries = df_normalized[df_normalized['Country name'].isin(['France', 'Germany', 'Israel', 'Japan', 'United Kingdom', 'United States'])]

# יצירת קטגוריות עבור תמיכה חברתית ושחיתות נתפסת
selected_countries.loc[:, 'Social support category'] = pd.cut(selected_countries['Social support'], bins=4, labels=['Low', 'Medium', 'High', 'Very High'])
selected_countries.loc[:, 'Perceptions of corruption category'] = pd.cut(selected_countries['Perceptions of corruption'], bins=4, labels=['Low', 'Medium', 'High', 'Very High'])

# בחירת עמודות מעניינות לניתוח
columns_of_interest = ['Country name', 'Social support category', 'Perceptions of corruption category']

# יצירת גרף קטגוריות מקבילות
fig = px.parallel_categories(selected_countries,
dimensions=columns_of_interest,
color="Life Ladder_NORM",
color_continuous_scale=px.colors.sequential.Plasma,
title='Parallel Categories Plot of Key Indicators for Selected Countries')
fig.show()




# גרף מס 13
# בחירת מדינות להצגה
selected_countries = df_normalized[df_normalized['Country name'].isin(['France', 'Germany', 'Israel', 'Japan', 'United Kingdom', 'United States'])]

# יצירת נתונים לגרף 3D Line Chart
fig = go.Figure()

for country in selected_countries['Country name'].unique():
    country_data = selected_countries[selected_countries['Country name'] == country]
    fig.add_trace(go.Scatter3d(
        x=country_data['year'],
        y=country_data['Social support'],
        z=country_data['Perceptions of corruption'],
        mode='lines',
        name=country
    ))

# בחירת מספר עמודות להצגה בגרף Scatter Matrix
columns_to_plot = ['Life Ladder_NORM', 'Log GDP per capita', 'Social support', 'Generosity', 'Healthy life expectancy at birth']

# יצירת Scatter Matrix
fig = px.scatter_matrix(df_normalized, dimensions=columns_to_plot, color='Country name',
                        title='Scatter Matrix of Key Indicators')
fig.update_layout(
    width=1200,
    height=1200
)
fig.show()