import pandas as pd
from traces import Transversal
import os
import glob
import matplotlib.pyplot as plt

transversal = Transversal(135,225,1,10000)
transversal.run()
transversal.export_vtk()
transversal.export_obj()

txtfiles = glob.glob('raw/*.txt')

# step=14 # 12 for plain, 14 for aux surface
# angle = df.loc[0::step,3].values # first_row::step,column
# eff_side1_df = df.loc[9::step, 23].values
# eff_side2_df = df.loc[9::step, 45].values

df = pd.read_csv(txtfiles[0],sep='\s+',names=range(47))
fname = os.path.basename(txtfiles[0]).split(".")[0]

angles = df.loc[df[1] == 'Sun'][3]  # set 4 for longitudinal
potential =  df[0].iloc[angles.index+2].astype('float')
absorbed_flux = df[0].iloc[angles.index+3].astype('float')
cosf = df[0].iloc[angles.index+4].astype('float')
shadow = df[0].iloc[angles.index+5].astype('float')
missing = df[0].iloc[angles.index+6].astype('float')
eff = df.loc[df[0] == 'target',[23]] # Add [23,24] for error
eff['shadow'] = shadow.values
eff['potential'] = potential.values
eff['cosf'] = cosf.values
eff['absorbed'] = absorbed_flux.values
eff['missing'] = missing.values
eff['interceptf'] = eff['absorbed'] / (eff['potential']*eff['cosf'] - eff['shadow'] - eff['missing'])
eff['af'] = eff['potential']*eff['cosf'] - eff['shadow'] - eff['missing']
angle_df = pd.DataFrame(eff.values, index=angles.values, 
                        columns=["efficiency", 
                                 "shadow",
                                 "absorbed", 
                                 "potential",
                                 "cosf",
                                 "interceptf",
                                 "missing",
                                 "af"])
angle_df.name = fname


# angle_eff = pd.DataFrame({'side1':eff_side1_df,'side2':eff_side2_df}, index=angle)  # 1st row as the column names
# angle_eff['total_eff'] = angle_eff['side1'] + angle_eff['side2']
# angle_eff['total_eff'].plot()


# plt.plot(angle_df["efficiency"])
# plt.title(angle_df.name)
# plt.ylabel("Optical efficieicy")
# plt.show()

# plt.plot(angle_df["shadow"])
# plt.title(angle_df.name)
# plt.ylabel("Shadow losses (W)")
# plt.show()

plt.plot(angle_df["absorbed"])
plt.title(angle_df.name)
plt.ylabel("Absorbed flux by receiver (W)")
plt.show()

# plt.plot(angle_df["potential"])
# plt.title(angle_df.name)
# plt.ylabel("Potential flux (W)")
# plt.show()

# plt.plot(angle_df["cosf"])
# plt.title(angle_df.name)
# plt.ylabel("Cos factor")
# plt.show()

# plt.plot(angle_df["interceptf"])
# plt.title(angle_df.name)
# plt.ylabel("intercept f")
# plt.show()

plt.plot(angle_df["af"])
plt.title(angle_df.name)
plt.ylabel("af")
plt.show()

# plt.plot(angle_df["missing"])
# plt.title(angle_df.name)
# plt.ylabel("missong losses")
# plt.show()