import pandas as pd
from DB.transactions import add_batch_observations

url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv"
df = pd.read_csv(url, index_col="date")
df.index = pd.to_datetime(df.index, dayfirst=False)

countries = ['Italy', 'United Kingdom', 'United States', 'Germany',
             'France', 'Brazil', 'China', "Spain", "Argentina", 
             'Canada', 'World']

events = ['total_vaccinations', 'people_vaccinated',
          'people_fully_vaccinated', 'daily_vaccinations_raw',
          'daily_vaccinations', 'total_vaccinations_per_hundred',
          'people_vaccinated_per_hundred',
          'people_fully_vaccinated_per_hundred',
          'daily_vaccinations_per_million']


def data_insert(df: pd.DataFrame, country: str, event: str):
    """
    takes a dataframe with info on vaccination for all country, and event,
    and insert into the database per country, event and ticker
    """
    tck = f"OWID.{country.replace(' ','_')}_{event}".upper()
    try:
        dg = df[df.location == country].loc[:, [event]].dropna()
#        return tck, dg
        add_batch_observations(tck, dg.loc[:, [event]])
        print(f"Observations from {tck} sucessfully added!")
    except:
        print(f"Observations from {tck} failed to be added!")


for c in countries:
    for e in events:
        data_insert(df, c, e)
