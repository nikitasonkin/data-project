from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression

dataset = pd.read_csv('input2_df_cleaned_normalized.csv' , encoding='ISO-8859-1')


#1 גרף תוחלת החיים ביחס לתמ"ג
x = dataset.iloc[:,[3,5]].values # הנחתי שהעמודות הן: Log GDP per capita (3) ו- Healthy life expectancy at birth (5)
wcss = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, init='k-means++' ,random_state=42)
    kmeans.fit(x)
    wcss.append(kmeans.inertia_)

plt.plot(range(1, 11), wcss)
plt.title('The Elbow Method')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.show()

kmeans = KMeans(n_clusters = 4, random_state = 42)
y_kmeans = kmeans.fit_predict(x)
print(y_kmeans)

plt.scatter(x[:, 0], x[:, 1], c=y_kmeans, s=50, cmap='viridis')
centers = kmeans.cluster_centers_
plt.scatter(centers[:, 0], centers[:, 1], c='red', s=200, alpha=0.75)
plt.title('Clusters of Countries')
plt.xlabel('Log GDP per capita')
plt.ylabel('Healthy life expectancy at birth')
plt.show()



# מדד האושר ביחס לתמיכה חברתית 2
x = dataset[['Social support', 'Life Ladder']].values
wcss = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42)
    kmeans.fit(x)
    wcss.append(kmeans.inertia_)

plt.plot(range(1, 11), wcss)
plt.title('The Elbow Method')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.show()

kmeans = KMeans(n_clusters=4, random_state=42)
y_kmeans = kmeans.fit_predict(x)

plt.scatter(x[:, 0], x[:, 1], c=y_kmeans, s=50, cmap='viridis')

centers = kmeans.cluster_centers_
plt.scatter(centers[:, 0], centers[:, 1], c='red', s=200, alpha=0.75)
plt.title('Clusters of Countries')
plt.xlabel('Social support')
plt.ylabel('Life Ladder')
plt.show()



# תפיסות של שחיתות ביחס למדד האושר: 3
x = dataset[['Perceptions of corruption', 'Life Ladder']].values
wcss = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42)
    kmeans.fit(x)
    wcss.append(kmeans.inertia_)

plt.plot(range(1, 11), wcss)
plt.title('The Elbow Method')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.show()

kmeans = KMeans(n_clusters=6, random_state=42)
y_kmeans = kmeans.fit_predict(x)

plt.scatter(x[:, 0], x[:, 1], c=y_kmeans, s=50, cmap='viridis')
centers = kmeans.cluster_centers_
plt.scatter(centers[:, 0], centers[:, 1], c='red', s=200, alpha=0.75)
plt.title('Clusters of Countries')
plt.xlabel('Perceptions of corruption')
plt.ylabel('Life Ladder')
plt.show()




# תמיכה חברתית ותוחלת חיים 4
x = dataset[['Social support', 'Healthy life expectancy at birth']].values
wcss = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42)
    kmeans.fit(x)
    wcss.append(kmeans.inertia_)

plt.plot(range(1, 11), wcss)
plt.title('The Elbow Method')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.show()

kmeans = KMeans(n_clusters=7, random_state=42)
y_kmeans = kmeans.fit_predict(x)
plt.scatter(x[:, 0], x[:, 1], c=y_kmeans, s=50, cmap='viridis')

centers = kmeans.cluster_centers_
plt.scatter(centers[:, 0], centers[:, 1], c='red', s=200, alpha=0.75)
plt.title('Clusters of Countries')
plt.xlabel('Social support')
plt.ylabel('Healthy life expectancy at birth')
plt.show()




 # אשכולות על פי נתונים כלכליים מרובים: 5
economic_data = dataset[['Log GDP per capita', 'Generosity', 'Social support', 'Perceptions of corruption']]
wcss = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42)
    kmeans.fit(economic_data)
    wcss.append(kmeans.inertia_)

plt.plot(range(1, 11), wcss)
plt.title('The Elbow Method')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.show()

kmeans = KMeans(n_clusters=6, random_state=42)
y_kmeans = kmeans.fit_predict(economic_data)

# ציור גרף תלת-ממדי של הנתונים עם האשכולות
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

# צביעת הנקודות לפי האשכולות
scatter = ax.scatter(economic_data['Log GDP per capita'], economic_data['Generosity'], economic_data['Social support'], c=y_kmeans, s=50, cmap='viridis')

# הוספת תוויות וצירים
ax.set_title('Clusters of Countries')
ax.set_xlabel('Log GDP per capita')
ax.set_ylabel('Generosity')
ax.set_zlabel('Social support')

# הוספת מרכזי האשכולות
centers = kmeans.cluster_centers_
ax.scatter(centers[:, 0], centers[:, 1], centers[:, 2], c='red', s=200, alpha=0.75)

# הוספת מקרא
legend1 = ax.legend(*scatter.legend_elements(), title="Clusters")
ax.add_artist(legend1)

plt.show()

# בחירת העמודות לרגרסיה
x = dataset['Log GDP per capita'].values.reshape(-1, 1)
y = dataset['Healthy life expectancy at birth'].values

# יצירת מודל רגרסיה ליניארית
regressor = LinearRegression()
regressor.fit(x, y)

# תחזיות הרגרסיה
y_pred = regressor.predict(x)

# ציור גרף פיזור עם קו הרגרסיה
plt.scatter(x, y, color='blue', label='Data points')
plt.plot(x, y_pred, color='red', linewidth=2, label='Regression line')
plt.title('Log GDP per capita vs Healthy life expectancy at birth')
plt.xlabel('Log GDP per capita')
plt.ylabel('Healthy life expectancy at birth')
plt.legend()
plt.show()