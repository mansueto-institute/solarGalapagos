import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gsp
import datetime as dt

source = 'solar_plotB_raw.csv'
# 5.6 kWh/m^2/year.
calcMean =  5.6
threshold = 2.53

df = pd.read_csv(source, usecols=['YEAR', 'MO', 'DY', 'ALLSKY_SFC_SW_DWN'])
df.columns = ['year', 'month', 'day', 'Radiation']
df.year = df.year+2000
df['Date'] = pd.to_datetime(df.iloc[:, :3])
df = df[['Radiation', 'Date']]
df['perc'] = df.Radiation / calcMean

days = 90

f1 = plt.figure(figsize = (16,7))
spec1 = gsp.GridSpec(ncols = 2, nrows = 1)

ax1 = f1.add_subplot(spec1[0,0])
ax4 = f1.add_subplot(spec1[0,1])

ax1.fill_between(df.Date, calcMean+df.Radiation.std(), calcMean-df.Radiation.std(), alpha=0.4, color='grey')
df.plot('Date', 'Radiation', ax=ax1, label='Average daily radiation', color='black')
ax1.set_ylabel('Solar Radiation [kwH/m2/day]')
ax1.axhline(calcMean, color='green', alpha=0.8, label='Average annual radiation')
ax1.legend()

dfm = df[df.Radiation < threshold]

mins = []
maxs = []
for i in range(1, 60):
    cmin = 10000
    cmax = -1
    for j in range(df.shape[0]-i):
        cmean = np.nanmean(df.iloc[j:j+i, 0])
        if cmean < cmin:
            cmin = cmean
        if cmean > cmax:
            cmax = cmean
    mins.append(cmin)
    maxs.append(cmax)
ax4.plot(mins, label='Lowest average radiation', color='black')
ax4.axhline(calcMean, color='green', alpha=0.8, label='Average annual radiation')
ax4.set_xlabel('Consecutive days')
ax4.set_ylabel('Solar Radiation [kwH/m2/day]')
ax4.legend()

f1.tight_layout()
f1.savefig('plot.pdf')
f1.savefig('plot.png')
f1.savefig('plot.tiff')
