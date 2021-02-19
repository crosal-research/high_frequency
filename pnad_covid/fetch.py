import requests
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO
from dateutil.rrule import rrule, WEEKLY
import datetime as dt


url = "https://www.ibge.gov.br/estatisticas/"
url = url + "investigacoes-experimentais/estatisticas-experimentais/27946-divulgacao-semanal-pnadcovid1?"
url = url + "t=resultados&utm_source=covid19&utm_medium=hotsite&utm_campaign=covid_19"

resp = requests.get(url)

soup = BeautifulSoup(resp.content, "html.parser")
resource = [l for l in soup.select("p a") 
            if l.text == 'Tabelas de resultados'][0]["href"]


dfs = pd.read_excel(resource, skiprows=[0, 1, 2, 3, 4], sheet_name= [0, 1],
                   na_values=["-", 0])

dfs[0].to_excel("./data/covid_pnad.xlsx")
dfs[1].to_excel("./data/covid_saude.xlsx")

print("data fetched and saved")

dp = (dfs[0]).loc[[("CV" not in str(i)) for i in dfs[0].Indicador], 
                  [("Situação" not in c) for c in dfs[0].columns]]



# chart
dp_td = dp[[("Taxa de desocupação" in str(i)) for i in dp.Indicador]].iloc[[0],:]
dp_tp = dp[[("Taxa de participação" in str(i)) for i in dp.Indicador]].iloc[[0], :]
dp_ts = dp[[("distanciamento" in str(i)) for i in dp.Indicador]].iloc[[6],:]
df_final = pd.concat([dp_td, dp_tp, dp_ts]).set_index(["Indicador"])
df_final = df_final.drop(["Nível Territorial", "Abertura Territorial"], axis=1).T

# fix dtes

start_date = dt.datetime(2020, 5, 9)
dates = [rrule(freq=WEEKLY, count=10, dtstart=start_date)]
dfinal.index = dates
