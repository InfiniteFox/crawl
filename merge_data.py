import pandas as pd

climate_change = pd.read_json('un_news_climate_change.json')
law = pd.read_json('un_news_law-and-crime-prevention.json')
eco = pd.read_json('un_news_economic-development.json')
hollywood = pd.read_json('hollywood.json')
abcnet = pd.read_json('abcnet.json')

un_news = pd.concat([climate_change, law, eco, hollywood, abcnet],sort=False).reset_index(drop=True)

un_news.to_json('un_news.json')