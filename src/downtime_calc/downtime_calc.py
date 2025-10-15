import pandas as pd
import asyncio
from icmplib import async_multiping
import sqlalchemy

df_infra = ORM.extraer_dim_camaras()
print(df_infra)

"""
for id in id_list: pull_from_Azure(count[id] in desconexiones where date is between PERÍODO, engine), df[id].append(count*30)
return df"""

"""buscar manera de renderizar este dataframe.
enviarlo a powerapps?
enviarlo a azure_db, en una tabla rari?
correrlo en powerBI?
"""
