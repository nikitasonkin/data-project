import pandas as pd
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

file_path = 'input1_df.csv'
df1 = pd.read_csv(file_path, encoding='ISO-8859-1')

# ----------------------------------------------------------------
print('הדפסת מידע על מערך הנתונים')
print(df1.info())
print()

missing_values = df1.isnull().sum()
print('הדפסת סכום הערכים החסרים בכל עמודה')
print(missing_values)
print()

missing_percentage = (missing_values / len(df1)) * 100
print('חישוב אחוז הערכים החסרים בכל עמודה')
print(missing_percentage)
print()

column_names = df1.columns
data_types = df1.dtypes

print(column_names,": שמות העמודות ")
print()

nan_locations = df1[df1.ilsnul().any(axis=1)]
print("מיקום הערכים החסרים :",nan_locations)

print('הדפסת חמש השורות הראשונות')
print(df1.head())
print()
print('הדפסת חמש השורות האחרונות')
print(df1.tail())
print()

# חישוב והדפסה 5 שורות שנמצעות באמצע
print('הדפסת חמש השורות האמצעיות')
mid_start = (len(df1) // 2) - 2 # כי רוצים להדפיס את העמצע בדיוק
mid_end = mid_start + 5
print(df1.iloc[mid_start:mid_end])
print()

print('סטטיסטיקה תיאורית של הנתונים :')
print(df1.describe(include= 'all'))











