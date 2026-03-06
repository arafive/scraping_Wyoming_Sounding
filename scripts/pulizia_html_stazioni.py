
import re
import os

import pandas as pd

html_stazioni = """
<area coords="223,23,5" shape="CIRCLE" href="javascript:g('01241')" title="01241  Orland (ENOL)">
<area coords="197,75,5" shape="CIRCLE" href="javascript:g('01415')" title="01415  Stavanger/Sola (ENZV)">
<area coords="262,36,5" shape="CIRCLE" href="javascript:g('02365')" title="02365  Sundsvall-Harnosand Fpl">
<area coords="236,91,5" shape="CIRCLE" href="javascript:g('02527')" title="02527  Goteborg/Landvetter">
<area coords="271,90,5" shape="CIRCLE" href="javascript:g('02591')" title="02591  Visby Aerologiska Stn (ESQV)">
<area coords="161,54,5" shape="CIRCLE" href="javascript:g('03005')" title="03005  Lerwick">
<area coords="145,109,5" shape="CIRCLE" href="javascript:g('03238')" title="03238  Albemarle">
<area coords="141,132,5" shape="CIRCLE" href="javascript:g('03354')" title="03354  Nottingham/Watnall">
<area coords="104,155,5" shape="CIRCLE" href="javascript:g('03808')" title="03808  Camborne">
<area coords="146,158,5" shape="CIRCLE" href="javascript:g('03882')" title="03882  Herstmonceux">
<area coords="114,106,5" shape="CIRCLE" href="javascript:g('03918')" title="03918  Castor Bay">
<area coords="77,123,5" shape="CIRCLE" href="javascript:g('03953')" title="03953  Valentia Observatory">
<area coords="139,25,5" shape="CIRCLE" href="javascript:g('06011')" title="06011  Torshavn">
<area coords="199,134,5" shape="CIRCLE" href="javascript:g('10113')" title="10113  Norderney">
<area coords="242,132,5" shape="CIRCLE" href="javascript:g('10184')" title="10184  Greifswald">
<area coords="218,146,5" shape="CIRCLE" href="javascript:g('10238')" title="10238  Bergen (ETGB)">
<area coords="247,153,5" shape="CIRCLE" href="javascript:g('10393')" title="10393  Lindenberg">
<area coords="195,161,5" shape="CIRCLE" href="javascript:g('10410')" title="10410  Essen (EDZE)">
<area coords="219,172,5" shape="CIRCLE" href="javascript:g('10548')" title="10548  Meiningen">
<area coords="196,181,5" shape="CIRCLE" href="javascript:g('10618')" title="10618  Idar-Oberstein (ETGI)">
<area coords="209,192,5" shape="CIRCLE" href="javascript:g('10739')" title="10739  Stuttgart/Schnarrenberg">
<area coords="231,186,5" shape="CIRCLE" href="javascript:g('10771')" title="10771  Kuemmersbruck (ETGK)">
<area coords="228,200,5" shape="CIRCLE" href="javascript:g('10868')" title="10868  Muenchen-Oberschlssheim">
<area coords="266,199,5" shape="CIRCLE" href="javascript:g('11035')" title="11035  Wien/Hohe Warte">
<area coords="250,179,5" shape="CIRCLE" href="javascript:g('11520')" title="11520  Praha-Libus">
<area coords="271,185,5" shape="CIRCLE" href="javascript:g('11747')" title="11747  Prostejov">
<area coords="296,187,5" shape="CIRCLE" href="javascript:g('11952')" title="11952  Poprad-Ganovce">
<area coords="269,123,5" shape="CIRCLE" href="javascript:g('12120')" title="12120  Leba">
<area coords="295,147,5" shape="CIRCLE" href="javascript:g('12374')" title="12374  Legionowo">
<area coords="289,207,5" shape="CIRCLE" href="javascript:g('12843')" title="12843  Budapest/Lorinc">
<area coords="298,220,5" shape="CIRCLE" href="javascript:g('12982')" title="12982  Szeged (LHUD)">
<area coords="303,238,5" shape="CIRCLE" href="javascript:g('13275')" title="13275  Beograd/Kosutnjak">
<area coords="318,253,5" shape="CIRCLE" href="javascript:g('13388')" title="13388  Nis (LYNI)">
<area coords="265,228,5" shape="CIRCLE" href="javascript:g('14240')" title="14240  Zagreb/Maksimir (LDDD)">
<area coords="260,250,5" shape="CIRCLE" href="javascript:g('14430')" title="14430  Zadar">
<area coords="352,232,5" shape="CIRCLE" href="javascript:g('15420')" title="15420  Bucuresti Inmh-Banesa (LRBS)">
<area coords="239,227,5" shape="CIRCLE" href="javascript:g('16045')" title="16045  Rivolto (LIPI)">
<area coords="207,233,5" shape="CIRCLE" href="javascript:g('16080')" title="16080  Milano/Linate (LIML)">
<area coords="192,243,5" shape="CIRCLE" href="javascript:g('16113')" title="16113  Cuneo-Levaldigi">
<area coords="227,243,5" shape="CIRCLE" href="javascript:g('16144')" title="16144  S Pietro Capofiume">
<area coords="234,280,5" shape="CIRCLE" href="javascript:g('16245')" title="16245  Pratica Di Mare (LIRE)">
<area coords="286,291,5" shape="CIRCLE" href="javascript:g('16320')" title="16320  Brindisi (LIBR)">
<area coords="234,328,5" shape="CIRCLE" href="javascript:g('16429')" title="16429  Trapani/Birgi (LICT)">
<area coords="198,308,5" shape="CIRCLE" href="javascript:g('16546')" title="16546  Decimomannu (LIED)">
<area coords="334,286,5" shape="CIRCLE" href="javascript:g('16622')" title="16622  Thessaloniki (Airport) (LGTS)">
<area coords="369,347,5" shape="CIRCLE" href="javascript:g('16754')" title="16754  Heraklion (Airport) (LGIR)">
<area coords="452,241,5" shape="CIRCLE" href="javascript:g('17030')" title="17030  Samsun">
<area coords="390,268,5" shape="CIRCLE" href="javascript:g('17064')" title="17064  Istanbul/Kartal">
<area coords="428,269,5" shape="CIRCLE" href="javascript:g('17130')" title="17130  Ankara/Central">
<area coords="458,274,5" shape="CIRCLE" href="javascript:g('17196')" title="17196  Kayseri (LTAU)">
<area coords="380,304,5" shape="CIRCLE" href="javascript:g('17220')" title="17220  Izmir/Guzelyali">
<area coords="415,303,5" shape="CIRCLE" href="javascript:g('17240')" title="17240  Isparta (LTBM)">
<area coords="465,295,5" shape="CIRCLE" href="javascript:g('17351')" title="17351  Adana/Bolge">
<area coords="347,25,5" shape="CIRCLE" href="javascript:g('22820')" title="22820  Petrozavodsk, LE">
<area coords="371,18,5" shape="CIRCLE" href="javascript:g('22845')" title="22845  Kargopol, AR">
<area coords="304,65,5" shape="CIRCLE" href="javascript:g('26038')" title="26038  Tallinn, LE (ULTT)">
<area coords="336,50,5" shape="CIRCLE" href="javascript:g('26075')" title="26075  St.Petersburg(Voejkovo), St.Petersburg(Voejkovo), LE (ULLI)">
<area coords="362,66,5" shape="CIRCLE" href="javascript:g('26298')" title="26298  Bologoe, LE">
<area coords="348,89,5" shape="CIRCLE" href="javascript:g('26477')" title="26477  Velikie Luki, LE (ULOL)">
<area coords="289,121,5" shape="CIRCLE" href="javascript:g('26702')" title="26702  Kaliningrad, MI">
<area coords="362,103,5" shape="CIRCLE" href="javascript:g('26781')" title="26781  Smolensk, MI">
<area coords="387,37,5" shape="CIRCLE" href="javascript:g('27038')" title="27038  Vologda, AR (ULWW)">
<area coords="439,14,5" shape="CIRCLE" href="javascript:g('27199')" title="27199  Kirov, MS">
<area coords="425,55,5" shape="CIRCLE" href="javascript:g('27459')" title="27459  Niznij Novgorod, MS">
<area coords="452,44,5" shape="CIRCLE" href="javascript:g('27594')" title="27594  Kolkhoznaya Ulitsa, MS">
<area coords="390,78,5" shape="CIRCLE" href="javascript:g('27713')" title="27713  Moskva/Dolgoprudny, MS">
<area coords="386,103,5" shape="CIRCLE" href="javascript:g('27707')" title="27707  Suhinici, MS">
<area coords="410,85,5" shape="CIRCLE" href="javascript:g('27730')" title="27730  Rjazan, MS">
<area coords="449,83,5" shape="CIRCLE" href="javascript:g('27962')" title="27962  Penza, MS (UWPP)">
<area coords="476,67,5" shape="CIRCLE" href="javascript:g('27995')" title="27995  Samara (Bezencuk), MS">
<area coords="364,131,5" shape="CIRCLE" href="javascript:g('33041')" title="33041  Gomel, MI">
<area coords="344,164,5" shape="CIRCLE" href="javascript:g('33317')" title="33317  Shepetivka, KI">
<area coords="368,155,5" shape="CIRCLE" href="javascript:g('33345')" title="33345  Kyiv, KI (UKKK)">
<area coords="322,174,5" shape="CIRCLE" href="javascript:g('33393')" title="33393  Lviv, KI (UKLL)">
<area coords="401,125,5" shape="CIRCLE" href="javascript:g('34009')" title="34009  Kursk, MS">
<area coords="422,117,5" shape="CIRCLE" href="javascript:g('34122')" title="34122  Voronez, MS (UUOO)">
<area coords="465,94,5" shape="CIRCLE" href="javascript:g('34172')" title="34172  Saratov, MS">
<area coords="440,124,5" shape="CIRCLE" href="javascript:g('34247')" title="34247  Kalac, MS">
<area coords="409,145,5" shape="CIRCLE" href="javascript:g('34300')" title="34300  Kharkiv, KI (UKHH)">
<area coords="472,129,5" shape="CIRCLE" href="javascript:g('34467')" title="34467  Volgograd, TB (URWW)">
<area coords="449,162,5" shape="CIRCLE" href="javascript:g('34731')" title="34731  Rostov-Na-Donu, TB (URRR)">
<area coords="460,199,5" shape="CIRCLE" href="javascript:g('37011')" title="37011  Tuapse, TB">
<area coords="14,344,5" shape="CIRCLE" href="javascript:g('60155')" title="60155  Casablanca (GMMC)">
<area coords="137,335,5" shape="CIRCLE" href="javascript:g('60390')" title="60390  Dar-El-Beida (DAAG)">
<area coords="210,341,5" shape="CIRCLE" href="javascript:g('60715')" title="60715  Tunis-Carthage (DTTA)">
"""

if not os.path.exists("../data/stazioni.xlsx"):
    df = pd.DataFrame(columns=['codice', 'nome', 'icao'])
else:
    df = pd.read_excel("../data/stazioni.xlsx", dtype={"codice": str})

pattern = r"javascript:g\('(\d+)'\).*?title=\"([^\"]+)\""

matches = re.findall(pattern, html_stazioni)

for codice, title in matches:
    resto = title.replace(codice, "").strip()
    
    icao_match = re.search(r"\(([^)]+)\)\s*$", resto)
    
    if icao_match:
        icao = icao_match.group(1)
        nome = resto[:icao_match.start()].strip()
    else:
        icao = ""
        nome = resto.strip()
        
    riga = pd.DataFrame([{'codice': codice, 'nome': nome, 'icao': icao}])
    
    if codice not in df['codice'].tolist():
        df = pd.concat([df, riga], axis=0)

df = df.sort_values(by='codice')
df = df.reset_index(drop=True)

df.to_excel("../data/stazioni.xlsx", index=False, engine="openpyxl")