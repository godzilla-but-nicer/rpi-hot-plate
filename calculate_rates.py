#%%
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.formula.api as smf

cooling = pd.read_csv("temps_cooling.txt", names=["time", "dcs", "temp"])
heating = pd.read_csv("temps_heating.txt", names=["time", "dcs", "temp"])

# %%
plt.plot(cooling["time"], cooling["temp"])
plt.plot(cooling["time"], heating["temp"])
plt.xlabel("Time (s)")
plt.ylabel("Temperature (C)")
plt.show()
# %%
print("cooling")
print(smf.ols("temp ~ time", data=cooling).fit())
# %%
print(smf.ols("temp ~ time", data=heating).fit().summary())
