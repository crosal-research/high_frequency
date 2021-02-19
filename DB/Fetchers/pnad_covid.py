# import external packages
import requests
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO
from dateutil.rrule import rrule, WEEKLY
import datetime as dt

# app imports
from DB.transactions import add_batch_observations


url = "https://www.ibge.gov.br/estatisticas/"
url = url + "investigacoes-experimentais/estatisticas-experimentais/27946-divulgacao-semanal-pnadcovid1?"
url = url + "t=resultados&utm_source=covid19&utm_medium=hotsite&utm_campaign=covid_19"

resp = requests.get(url)

soup = BeautifulSoup(resp.content, "html.parser")
resource = [l for l in soup.select("p a") 
            if l.text == 'Tabelas de resultados'][0]["href"]


dfs = pd.read_excel(resource, skiprows=[0, 1, 2, 3, 4], sheet_name= [0, 1],
                   na_values=["-", 0])

print("data fetched")


dp = (dfs[0]).loc[[("CV" not in str(i)) for i in dfs[0].Indicador], 
                  [("Situação" not in c) for c in dfs[0].columns]]


# separates data
dp_td = dp[[("Taxa de desocupação" in str(i)) for i in dp.Indicador]].iloc[[0],:]
dp_tp = dp[[("Taxa de participação" in str(i)) for i in dp.Indicador]].iloc[[0], :]
dp_ts = dp[[("distanciamento" in str(i)) for i in dp.Indicador]].iloc[[6],:]
df_final = pd.concat([dp_td, dp_tp, dp_ts]).set_index(["Indicador"])
df_final = df_final.drop(["Nível Territorial", "Abertura Territorial"], axis=1).T

# fix dtes
start_date = dt.datetime(2020, 5, 9)
dates = list(rrule(freq=WEEKLY, count=df_final.shape[0], dtstart=start_date))
df_final.index = dates

# insert in the database
try:
    add_batch_observations("ibge.desemp_covid", df_final.iloc[:, [0]])
    add_batch_observations("ibge.part_covid", df_final.iloc[:, [1]])
    add_batch_observations("ibge.afast_covid", df_final.iloc[:, [2]])
    print("Data saved into the database!")
except:
    print("Some data failed to be saved into the database")
