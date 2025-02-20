import pandas as pd
import ast

file_path = "/mnt/data/mumbai.csv"
df = pd.read_csv(file_path)

df.drop(columns=['UNUSED_COLUMN'], errors='ignore', inplace=True)
df.dropna(subset=['map_details'], inplace=True)

df.fillna({
    'PRICE': df['PRICE'].median(),
    'BEDROOM_NUM': df['BEDROOM_NUM'].mode()[0],
}, inplace=True)

df['PRICE'] = pd.to_numeric(df['PRICE'].str.replace('[^\d.]', '', regex=True), errors='coerce')

def extract_lat_lon(map_details):
    try:
        loc_dict = ast.literal_eval(map_details)
        return float(loc_dict.get('LATITUDE', 0)), float(loc_dict.get('LONGITUDE', 0))
    except (ValueError, SyntaxError, AttributeError, TypeError):
        return None, None

df[['latitude', 'longitude']] = df['map_details'].apply(lambda x: pd.Series(extract_lat_lon(x)))
df[['latitude', 'longitude']] = df[['latitude', 'longitude']].apply(pd.to_numeric, errors='coerce')

df.drop_duplicates(subset=['PROP_ID'], keep='first', inplace=True)

print("Cleaned Data Sample:\n", df[['latitude', 'longitude', 'PRICE']].head(10))

cleaned_file_path = "/mnt/data/mumbai_cleaned.csv"
df.to_csv(cleaned_file_path, index=False)
print("Cleaned dataset saved successfully!")
