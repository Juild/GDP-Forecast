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

FEATURE_LABELS = ['GDP growth(annual %)',
                'Import value index(c.i.f)',
                 'Health expenditure per capita(current US$)',
                 'Export value index(f.o.b)',
                 'Exports of goods and services(annual % growth)',
                 'S&P Global Equity Indices(annual % change)',
                 'Services value added(annual % growth)',
                 'Net secondary income(BoP, current US$)',
                 'Adjusted education expenditure(% of GNI)',
                 'Agriculture, value added(annual % growth)',
                 'Short-term debt(% of total reserves)',
                 'Inflation, GDP deflator(annual %)',
                 'Gross capital formation(% of GDP)',
                 'GDP per capita growth(annual %)',
                 'Energy use (kg of oil) per $1k GDP',
                 'External balance on goods and services(% of GDP)',
                 'Population growth(annual %)',
                 'Hospital beds(per 1k people)',
                 'Death rate, crude(per 1k people)',
                 'Foreign direct investment, net inflows(% of GDP)',
                 'Newborns protected against tetanus(%)',
                 'Agricultural methane emissions(% of total)',
                 'Age dependency ratio, old(% of working-age pop)',
                 'Adjusted consumption of fixed capital(% of GNI)',
                 'Industry, value added(annual % growth)',
                 'Imports of goods and services(% of GDP)',
                 'Manufacturing, value added(annual % growth)',
                 'Average grant element on new external debt(%)',
                 'Export volume index',
                 'Exports of goods and services(% of GDP)',
                 'Merchandise imports in South Asia(% of total)',
                 'Fixed broadband subscriptions(per 100 people)',
                 'Physicians(per 1k people)',
                 'Adjusted particulate emission damage(% of GNI)',
                 'Gross capital formation(annual % growth)',
                 'GNI growth(annual %)',
                 'CO2 emissions from other sectors',
                 'Taxes on income, profits and capital gains(% of revenue)',
                 'Government consumption expenditure(% of GDP)',
                 'Government consumption expenditure(annual % growth)',
                 'Out-of-pocket health expenditure(% of total)',
                 'Merchandise imports in East Asia & Pacific(% of total)',
                 'Mortality rate, under-5, female(per 1k live births)',
                 'Gross fixed capital formation(% of GDP)',
                 'Household consumption expenditure per capita',
                 'Household consumption expenditure(annual % growth)',
                 'GNI per capita growth(annual %)',
                 'CO2 emissions(kg per 2011 PPP $ of GDP)',
                 'Domestic credit by financial sector(% of GDP)',
                 'Burden of customs procedure'
]

def clean_and_pivote(df):
    countries_gdp = df[df[INDICATOR_CODE] == GDP_GROWTH][COUNTRY_CODE].to_list() #countries with gdp
    countries = df[COUNTRY_CODE].unique()
    countries_no_gdp = list(set(countries) - set(countries_gdp)) # set difference =  countries with no gdp

    df_pivoted = pd.pivot(df, index=[COUNTRY_CODE, YEAR],
                    columns=INDICATOR_CODE,
                    values=INDICATOR_VALUES)
    return df_pivoted.drop(countries_no_gdp)[MODEL_FEATURES]

