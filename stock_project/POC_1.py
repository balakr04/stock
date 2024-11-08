import requests
import pandas as pd
pd.set_option('display.max_columns', None)


github_api_url = "https://api.github.com/repos/squareshift/stock_analysis/contents/"
response = requests.get(github_api_url)
# print(response)
# print(response.status_code)
# # a = response.json()
a = response.text
# print(a)
a = response.json()
# print(b)

csv_files = [file['download_url'] for file in a if file['name'].endswith('.csv')]
a = csv_files[0]
# print(a)
csv_file = csv_files.pop()
# print(csv_file)
d = pd.read_csv(csv_file)
# print(d)
dataframes = []
file_names = []
for url in csv_files:
    file_name = url.split("/")[-1].replace(".csv", "")
    # print(file_name)
    df = pd.read_csv(url)
    df['Symbol'] = file_name
    dataframes.append(df)
    file_names.append(file_name)

print(file_names)

combined_df = pd.concat(dataframes)
# print(combined_df)

o_df = pd.merge(combined_df,d,on='Symbol',how = 'left')
# print(o_df)
result = o_df.groupby("Sector").agg({'open':'mean','close':'mean','high':'max','low':'min','volume':'mean'}).reset_index()
# print(result)
print(len(o_df.columns))
o_df["timestamp"] = pd.to_datetime(o_df["timestamp"])
# print(o_df.columns)  # This will show you all column names in o_df
# print(o_df.dtypes)
# print(len(o_df))
filtered_df = o_df[(o_df['timestamp'] >= "2021-01-01") & (o_df['timestamp'] <= "2021-05-26")]
# print(filtered_df)
result_time = filtered_df.groupby("Sector").agg({'open':'mean','close':'mean','high':'max','low':'min','volume':'mean'}).reset_index()
print(result_time)
list_sector = ["TECHNOLOGY","FINANCE"]
result_time = result_time[result_time["Sector"].isin(list_sector)].reset_index(drop=True)
print(result_time)
path = r"stock_data.csv"
result_time.to_csv(path,header=True)
print("data has been written successfully")