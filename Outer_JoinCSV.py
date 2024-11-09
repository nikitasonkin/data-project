import numpy as np
import pandas as pd
import re  # ייבוא המודול re לשימוש ב-Regex

# קריאת קבצי CSV עם קידוד מתאים
file1_path = 'input1_df.csv'
file2_path = 'input2_df.csv'


df1 = pd.read_csv(file1_path, encoding='ISO-8859-1')
df2 = pd.read_csv(file2_path, encoding='ISO-8859-1')


# ביצוע הצטרפות מלאה ומילוי ערכים חסרים באפס
outer_join_df = df1.merge(df2, on="Country name", how='outer')
print("Number of missing values:\n",outer_join_df.isnull().sum())

# שמירת ה- DataFrame המאוחד לקובץ CSV חדש
outer_join_df.to_csv('outer_join_df.csv', index=False, encoding='ISO-8859-1')

# בחירת עמודות עבור כל DataFrame
df1_columns = ['Name', 'Symbol', 'employees_count', 'price (USD)', 'Country name']
df2_columns = ['Country name', 'year', 'Life Ladder', 'Log GDP per capita', 'Social support', 'Healthy life expectancy at birth', 'Generosity', 'Perceptions of corruption', 'Positive affect']

# יצירת DataFrames חדשים על פי העמודות שנבחרו
df_1 = outer_join_df[df1_columns].copy()
df_2 = outer_join_df[df2_columns].copy()



# פונקציה לתיקון ערכים בעייתיים בעמודות טקסט
def num_fixer(data_frame, series_name):
    if data_frame is None:
        return None
    cnt = 0
    drop_indices = []
    for row in data_frame[series_name]:
        try:
            int(float(row))
        except ValueError:
            if row == 'True' or row == 'False':
                drop_indices.append(cnt)
            elif row == 'nan':
                data_frame.loc[cnt, series_name] = np.nan
            elif re.search(r'[A-Za-z]', str(row)) and re.search(r'[0-9]', str(row)):
                print(f"ערך בעייתי בעמודה: {series_name} הערך: {row} בשורה: {cnt}")
                drop_indices.append(cnt)
            else:
                print(f"ערך בעייתי בעמודה: {series_name} הערך: {row} בשורה: {cnt}")
        cnt += 1

    print(f"הוסרו: {len(drop_indices)} ערכים בעייתיים בעמודה: {series_name}")
    data_frame.drop(index=drop_indices, inplace=True)
    data_frame[series_name] = data_frame[series_name].astype('string', errors='raise')
    data_frame.reset_index(drop=True, inplace=True)
    return data_frame


# פונקציה לתיקון ערכים בעייתיים בעמודות מספריות
def char_fixer(data_frame, series_name):
    if data_frame is None:
        print(f"Data frame is None before processing {series_name}")
        return None
    cnt = 0
    drop_indices = []
    for row in data_frame[series_name]:
        try:
            float(row)
            if re.search(r'[A-Za-z]', str(row)) and re.search(r'[0-9]', str(row)):
                print(f"ערך בעייתי בעמודה: {series_name} הערך: {row} בשורה: {cnt}")
                drop_indices.append(cnt)
        except ValueError:
            print(f"ערך בעייתי בעמודה: {series_name} הערך: {row} בשורה: {cnt}")
            drop_indices.append(cnt)
        cnt += 1

    print(f"הוסרו: {len(drop_indices)} ערכים בעייתיים בעמודה: {series_name}")
    data_frame.drop(index=drop_indices, inplace=True)
    data_frame[series_name] = data_frame[series_name].astype('float64', errors='raise')
    data_frame.reset_index(drop=True, inplace=True)
    return data_frame


# ניקוי df1
df_1 = char_fixer(df_1, 'employees_count')
df_1 = char_fixer(df_1, 'price (USD)')
df_1 = num_fixer(df_1, 'Name')
df_1 = num_fixer(df_1, 'Symbol')
df_1 = num_fixer(df_1, 'Country name')

# הסרת שורות עם ערכים חסרים בעמודות טקסט
df_1.dropna(subset=['Name', 'Symbol', 'Country name'], inplace=True)
df_1.reset_index(drop=True, inplace=True)

# הסרת כפילויות
df_1.drop_duplicates(inplace=True)
df_1.reset_index(drop=True, inplace=True)
df_1_duplicates = df_1[df_1.duplicated(keep=False)]

# ניקוי df2
df_2 = num_fixer(df_2, 'Country name')
df_2 = char_fixer(df_2, 'year')
df_2 = char_fixer(df_2, 'Life Ladder')
df_2 = char_fixer(df_2, 'Log GDP per capita')
df_2 = char_fixer(df_2, 'Social support')
df_2 = char_fixer(df_2, 'Healthy life expectancy at birth')
df_2 = char_fixer(df_2, 'Generosity')
df_2 = char_fixer(df_2, 'Perceptions of corruption')
df_2 = char_fixer(df_2, 'Positive affect')

# המרת עמודות מספריות לטיפוס float64
numeric_columns_df_2 = ['Life Ladder', 'Log GDP per capita', 'Social support', 'Healthy life expectancy at birth', 'Generosity', 'Perceptions of corruption', 'Positive affect']
df_2[numeric_columns_df_2] = df_2[numeric_columns_df_2].astype('float64')
df_2.reset_index(drop=True, inplace=True)

# הסרת שורות עם ערכים חסרים בעמודת year
df_2.dropna(subset=['year'], inplace=True)
df_2.reset_index(drop=True, inplace=True)

# הסרת שורות עם ערכים חסרים בעמודות טקסט
df_2.dropna(subset=['Country name'], inplace=True)
df_2.reset_index(drop=True, inplace=True)

# הסרת כפילויות לפי כל העמודות ב-df2
df_2 = df_2.drop_duplicates()
df_2.reset_index(drop=True, inplace=True)
df_2_duplicates = df_2[df_2.duplicated(keep=False)]
print()


# פונקציה להשלמת ערכים חסרים בעמודות מספריות באמצעות אינטרפולציה
def fill_missing_values_with_interpolation(data_frame, numeric_columns):
    for column in numeric_columns:
        data_frame[column] = data_frame[column].interpolate(method='linear', limit_direction='both')
    return data_frame

# השלמת ערכים חסרים בעמודות מספריות
numeric_columns_df_1 = ['employees_count', 'price (USD)']
df_1 = fill_missing_values_with_interpolation(df_1, numeric_columns_df_1)

# השלמת ערכים חסרים בעמודות מספריות
df_2 = fill_missing_values_with_interpolation(df_2, numeric_columns_df_2)

# בדיקת ערכים כפולים ב-DF1
print("DF1 Duplicate Rows:")
print(df_1_duplicates)
print("Number of duplicate rows:", df_1.duplicated().sum())
print()
# בדיקת ערכים חסרים ב-DF1
print("DF1 Cleaned Final:")
print("Number of missing values:\n", df_1.isnull().sum())
print()

# בדיקת ערכים כפולים ב-DF2
print("DF2 Duplicate Rows:")
print(df_2_duplicates)
print("Number of duplicate rows:", df_2.duplicated().sum())
print()
# בדיקת ערכים חסרים ב-DF2
print("DF2 Cleaned Final:")
print("Number of missing values:\n", df_2.isnull().sum())
print()


print("DF_1 ו-DF_2 הנתונים נוקו , נותחו ונוצרו קבצים עבורם - .")
print()
# שמירת ה-DataFrames הנקיים לקבצי CSV
df_1.to_csv('df_1_cleaned_final.csv', index=True, encoding='ISO-8859-1')
df_2.to_csv('df_2_cleaned_final.csv', index=True, encoding='ISO-8859-1')


print("DF_1 Data Types:")
print(df_1.dtypes)
print()
print("DF_2 Data Types:")
print(df_2.dtypes)
print()


# חלק נוסף עבור df22
df2_norm = df_2.copy()

# בחירת עמודת המספרית לנרמול
column_to_normalize = 'Life Ladder'

# המרת העמודה למספרית תוך התעלמות משגיאות
df2_norm[column_to_normalize] = pd.to_numeric(df2_norm[column_to_normalize], errors='coerce')

# חישוב הערך המקסימלי בעמודה תוך התעלמות מערכי NaN
max_value = df2_norm[column_to_normalize].abs().max()
print('ערך מקסימלי:', max_value)
print()

# יצירת עמודה חדשה עם ערכי NaN
df2_norm[column_to_normalize + '_NORM'] = np.nan

# חישוב הערכים המנורמלים
for index, row in df2_norm.iterrows():
    original_value = row[column_to_normalize]
    if pd.notna(original_value):
        normalized_value = round(abs(original_value) / max_value, 6)
        df2_norm.at[index, column_to_normalize + '_NORM'] = normalized_value

# הסרת שורות עם ערכים חסרים בעמודה המנורמלת
df2_norm.dropna(subset=[column_to_normalize + '_NORM'], inplace=True)
df2_norm.reset_index(drop=True, inplace=True)

# הסרת כפילויות
df22 = df2_norm.drop_duplicates()
df22.reset_index(drop=True, inplace=True)

# הצגת השורות הראשונות לבדיקת העמודה המנורמלת
print("נרמול של עמודת נתונים מספריים הושלם ונשמר בקובץ !!!")
print(df22.head())
print()

# שמירת DataFrame המתוקן בחזרה לקובץ CSV
df22.to_csv('input2_df_cleaned_normalized.csv', index=False, encoding='ISO-8859-1')

# הדפסת 15 השורות הראשונות של DataFrame לאחר הסרת כפילויות
print("DataFrame - הדפסת 15 שורות לאחר הסרת כפילויות ")
print(df2_norm.head(15))
print()

# הדפסת שורות כפולות לאחר הנרמול
print("df2_norm Duplicate Rows:")
print(df2_norm[df2_norm.duplicated()])
print("Number of duplicate rows:", df2_norm.duplicated().sum())
print()

print("df2_norm Data Types:")
print(df2_norm.dtypes)
print()
