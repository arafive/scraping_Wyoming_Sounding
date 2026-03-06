
import re
import os
import requests

import pandas as pd

from concurrent.futures import ThreadPoolExecutor

from io import StringIO

import time
import random

def f_costruzione_url(codice, data):
    radice = 'https://weather.uwyo.edu/cgi-bin/sounding?region=europe&TYPE=TEXT%3ALIST'
    year = f'YEAR={data.year}'
    month = f'MONTH={data.month:02d}'
    _from = f'FROM={data.day:02d}{data.hour:02d}'
    _to = f'TO={data.day:02d}{data.hour:02d}'
    str_codice = f'STNM={codice}'
    ice = 'ICE=1'

    url = f'{radice}&{year}&{month}&{_from}&{_to}&{str_codice}&{ice}'
    # print(url)

    return url


def f_prendi_risposta_sito(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/117.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Referer": url
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    return response.text


def f_elabora_risposta(risposta):
    # Estraggo il primo blocco con i dati (quello <PRE>)
    match = re.search(r"<PRE>(.*?)</PRE>", risposta, re.DOTALL)
    if not match:
        return False
    
    blocco_testo = match.group(1)
    
    # Tolgo le linee di separazione
    linee = blocco_testo.strip().split("\n")
    linee_pulite = []
    
    for i in linee:
        if not i.strip().startswith("-") and i.strip() != "":
            linee_pulite.append(i)
    
    # Ricostruisco il testo
    testo_ripulito = "\n".join(linee_pulite)

    return testo_ripulito


def f_lettura_risposta_pandas(testo_ripulito):
    df = pd.read_fwf(StringIO(testo_ripulito))
    
    df = df.drop(0, axis=0) # la prima riga contiene le unità di misura, le ho salvate in un dizionario
    df = df.astype(float)
    df = df.iloc[::-1].reset_index(drop=True) # lo ruoto come fosse un vero radiosondaggio
    
    dict_colonne = {
        'PRES': {'name': 'Atmospheric Pressure', 'shortName': 'p', 'orig_units': 'hPa'},
        'HGHT': {'name': 'Geopotential Height', 'shortName': 'gh', 'orig_units': 'hPa'},
        'TEMP': {'name': 'Temperature', 'shortName': 't', 'orig_units': 'C'},
        'DWPT': {'name': 'Dewpoint Temperature', 'shortName': 'd', 'orig_units': 'C'},
        'FRPT': {'name': 'Frost Point Temperature', 'shortName': 'fp', 'orig_units': 'C'},
        'RELH': {'name': 'Relative Humidity', 'shortName': 'rh', 'orig_units': '%'},
        'RELI': {'name': 'Relative Humidity with respect to Ice', 'shortName': 'rhi', 'orig_units': '%'},
        'MIXR': {'name': 'Mixing Ratio', 'shortName': 'q', 'orig_units': 'g/kg'},
        'DRCT': {'name': 'Wind Direction', 'shortName': 'dir', 'orig_units': 'deg true'},
        'SKNT': {'name': 'Wind Speed', 'shortName': 'speed', 'orig_units': 'knot'},
        'THTA': {'name': 'Potential Temperature', 'shortName': 'theta', 'orig_units': 'K'},
        'THTE': {'name': 'Equivalent Potential Temperature', 'shortName': 'thetae', 'orig_units': 'K'},
        'THTV': {'name': 'Virtual Potential Temperature', 'shortName': 'tv', 'orig_units': 'K'}
    }

    df = df.rename(columns={k: v['shortName'] for k, v in dict_colonne.items()})

    return df
    
    
def f_scarica_sounding(codice, data):
    
    time.sleep(random.uniform(1,3))
        
    cartella_stazione = f'../data/{codice}'
    os.makedirs(cartella_stazione, exist_ok=True)
    
    file_out = f"{cartella_stazione}/{data.strftime('%Y-%m-%d_%H')}"
        
    if os.path.exists(f"{cartella_stazione}/{data.strftime(format='%Y-%m-%d_%H')}"):
        print(codice, data.strftime('%Y-%m-%d %H:%M'), 'OK (già esiste)')
        return

    url = f_costruzione_url(codice, data)
    risposta = f_prendi_risposta_sito(url)
    if "Forbidden" in risposta:
        time.sleep(300)
    testo_ripulito = f_elabora_risposta(risposta)
    
    if testo_ripulito:
        df = f_lettura_risposta_pandas(testo_ripulito)
        df.to_csv(file_out)
        print(codice, data.strftime('%Y-%m-%d %H:%M'), 'OK')
    else:
        print(codice, data.strftime('%Y-%m-%d %H:%M'), 'non scaricato')


# %%
max_workers = 5
df_codici = pd.read_excel('../data/stazioni.xlsx', dtype={"codice": str})
range_date = pd.date_range('2025-01-01 00:00:00', '2025-12-31 12:00:00', freq='12h')
                
if __name__ == '__main__':
    
    tasks = []
    
    for codice in df_codici['codice'][10:11]:
        for data in range_date:
            tasks.append((codice, data))
            
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        executor.map(lambda x: f_scarica_sounding(*x), tasks)
        
print('\n\nDone')