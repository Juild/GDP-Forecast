import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASE_PATH = os.path.join(BASE_DIR, "db.sqlite3")

MODELS_PATH = os.path.join(BASE_DIR, "models")

LOGS_PATH = os.path.join(BASE_DIR, "logs")

# may look a bit stupid, but if the database indexes change, we only have to change them here
GDP_GROWTH  = "NY.GDP.MKTP.KD.ZG"
COUNTRY_CODE = "CountryCode"
YEAR = "Year" 
INDICATOR_CODE = "IndicatorCode"
INDICATOR_VALUES = "Value"
TABLE_NAME = "CountryIndicators"
SERIALIZED_MODEL = "GDP_predictor_model.dat"
PREDICTIONS_TABLE = "EstimatedGDPGrowth"
MODEL_FEATURES = [GDP_GROWTH,
 'TM.VAL.MRCH.XD.WD',
 'SH.XPD.PCAP',
 'TX.VAL.MRCH.XD.WD',
 'NE.EXP.GNFS.KD.ZG',
 'CM.MKT.INDX.ZG',
 'NV.SRV.TETC.KD.ZG',
 'BN.TRF.CURR.CD',
 'NY.ADJ.AEDU.GN.ZS',
 'NV.AGR.TOTL.KD.ZG',
 'DT.DOD.DSTC.IR.ZS',
 'NY.GDP.DEFL.KD.ZG',
 'NE.GDI.TOTL.ZS',
 'NY.GDP.PCAP.KD.ZG',
 'EG.USE.COMM.GD.PP.KD',
 'NE.RSB.GNFS.ZS',
 'SP.POP.GROW',
 'SH.MED.BEDS.ZS',
 'SP.DYN.CDRT.IN',
 'BX.KLT.DINV.WD.GD.ZS',
 'SH.VAC.TTNS.ZS',
 'EN.ATM.METH.AG.ZS',
 'SP.POP.DPND.OL',
 'NY.ADJ.DKAP.GN.ZS',
 'NV.IND.TOTL.KD.ZG',
 'NE.IMP.GNFS.ZS',
 'NV.IND.MANF.KD.ZG',
 'DT.GRE.DPPG',
 'TX.QTY.MRCH.XD.WD',
 'NE.EXP.GNFS.ZS',
 'TM.VAL.MRCH.R5.ZS',
 'IT.NET.BBND.P2',
 'SH.MED.PHYS.ZS',
 'NY.ADJ.DPEM.GN.ZS',
 'NE.GDI.TOTL.KD.ZG',
 'NY.GNP.MKTP.KD.ZG',
 'EN.CO2.OTHX.ZS',
 'GC.TAX.YPKG.RV.ZS',
 'NE.CON.GOVT.ZS',
 'NE.CON.GOVT.KD.ZG',
 'SH.XPD.OOPC.TO.ZS',
 'TM.VAL.MRCH.R1.ZS',
 'SH.DYN.MORT.FE',
 'NE.GDI.FTOT.ZS',
 'NE.CON.PRVT.PC.KD',
 'NE.CON.PRVT.KD.ZG',
 'NY.GNP.PCAP.KD.ZG',
 'EN.ATM.CO2E.PP.GD.KD',
 'FS.AST.DOMS.GD.ZS',
 'IQ.WEF.CUST.XQ']

def clean_and_pivote(df):
    countries_gdp = df[df[INDICATOR_CODE] == GDP_GROWTH][COUNTRY_CODE].to_list() #countries with gdp
    countries = df[COUNTRY_CODE].unique()
    countries_no_gdp = list(set(countries) - set(countries_gdp)) # set difference =  countries with no gdp

    df_pivoted = pd.pivot(df, index=[COUNTRY_CODE, YEAR],
                    columns=INDICATOR_CODE,
                    values=INDICATOR_VALUES)
    return df_pivoted.drop(countries_no_gdp)[MODEL_FEATURES]

