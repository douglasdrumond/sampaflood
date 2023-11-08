import pandas as pd

import meteo

df_distritos = pd.read_excel("../BD FINAL.xlsx", sheet_name="BD expandido")

latitude_list = []
longitude_list = []
abbrev_list = []
name_list = []
for i in df_distritos.index:
    latitude_list.append(df_distritos.at[i, "latitude"])
    longitude_list.append(df_distritos.at[i, "longitude"])
    abbrev_list.append(df_distritos.at[i, "DS_SIGLA"])
    name_list.append(df_distritos.at[i, "DS_NOME"])

# latitude_list = [df_distritos.at[0, "latitude"], df_distritos.at[1, "latitude"]]
# longitude_list = [df_distritos.at[0, "longitude"], df_distritos.at[1, "longitude"]]
# abbrev_list = [df_distritos.at[0, "DS_SIGLA"], df_distritos.at[1, "DS_SIGLA"]]
# name_list = [df_distritos.at[0, "DS_NOME"], df_distritos.at[1, "DS_NOME"]]
append_data = {
    "abbreviation": abbrev_list,
    "district_name": name_list
}
daily_dataframe = meteo.get_weather_data(latitude_list, longitude_list, append_data)
print(daily_dataframe)
daily_dataframe.to_excel("openmeteo.xlsx", index=False)
daily_dataframe.to_csv("openmeteo.csv", index=False, encoding="utf-8", decimal=",")
