import pandas as pd

import json

pricesList = []
namePhone = []

with open('df.json', 'r') as f:
    df_json = json.load(f)

Data = {
    'Modelo': namePhone,
    'Precio medio': pricesList
}

df_json = pd.DataFrame(Data, columns=['Modelo', 'Precio medio'])

print(df_json)
