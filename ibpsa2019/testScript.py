# test script
import functions as func

################################################################################
# DATA COLLECTION
################################################################################
# load building gnome dataset (BDG)
df_bdg = func.loadDataset('BDG')
print("Building Gnome Dataset: hourly meter data from {} buildings".format(len(df_bdg.columns)))

# load dc building dataset (DC)
df_dc = func.loadDataset('DC')
print("DC Dataset: 15min interval meter data (resampled to hourly) from {} buildings".format(len(df_dc.columns)))

################################################################################
# EXTRACT CONTENT
################################################################################

df_weekday_BDG = func.getContext('weekday', df_bdg, 'BDG')
df_weekend_BDG = func.getContext('weekend', df_bdg, 'BDG')
df_weekday_DC = func.getContext('weekday', df_dc, 'DC')
df_weekend_DC = func.getContext('weekend', df_dc, 'DC')

################################################################################
# LOAD CURVES AGGREGATION
################################################################################

df_average_weekday_BDG = func.doAggregation('average', df_weekday_BDG, 'day')

df_median_weekday_BDG = func.doAggregation('median', df_weekday_BDG, 'day')


