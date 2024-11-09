import pandas as pd
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'



# טעינת הקובץ עם קידוד שונה
file_path = 'input2_df.csv'
df2 = pd.read_csv(file_path, encoding='ISO-8859-1')


print('הדפסת מידע על מערך הנתונים')
print(df2.info())
print()

missing_values = df2.isnull().sum()
print('הדפסת סכום הערכים החסרים בכל עמודה')
print(missing_values)
print()

missing_percentage = (missing_values / len(df2)) * 100
print('חישוב אחוז הערכים החסרים בכל עמודה')
print(missing_percentage)
print()

column_names = df2.columns
data_types = df2.dtypes

print(column_names, ": שמות העמודות ")
print()

nan_locations = df2[df2.isnull().any(axis=1)]
print("מיקום הערכים החסרים :",nan_locations)

print('הדפסת חמש השורות הראשונות')
print(df2.head())
print()
print('הדפסת חמש השורות האחרונות')
print(df2.tail())
print()

#חישוב והדפסה 5 שורות שנמצעות באמצע
print('הדפסת חמש השורות האמצעיות')
mid_start = (len(df2) // 2) -2 #כי רוצים להדפיס את העמצע בדיוק
mid_end = mid_start + 5
print(df2.iloc[mid_start:mid_end])
print()

print('סטטיסטיקה תיאורית של הנתונים :')
print(df2.describe(include = 'all'))