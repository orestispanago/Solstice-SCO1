import pandas as pd
from traces import Transversal
import os
import glob
import matplotlib.pyplot as plt

def mkdir_if_not_exists(dirname):
    if not os.path.exists(dirname):
        os.makedirs(dirname)


columns = {"potential_flux": 2,
           "absorbed_flux": 3,
           "cos_factor": 4,
           "shadow_losses": 5,
           "missing_losses": 6,
           "reflectivity_losses": 7,
           "absorptivity_losses": 8
           }


transversal = Transversal(135,225,1,10000)
transversal.run()
transversal.export_vtk()
transversal.export_obj()

txtfiles = glob.glob('raw/*.txt')

df = pd.read_csv(txtfiles[0],sep='\s+',names=range(47))
fname = os.path.basename(txtfiles[0]).split(".")[0]

def calc_intercept_factor(df):
    df["intercept_factor"] = df["absorbed_flux"]/ (df["potential_flux"] * df["cos_factor"])
 


df = pd.read_csv(txtfiles[0], sep='\s+', names=range(47))
trace_df = df.loc[df[1] == 'Sun', [3]]  # set 4 for longitudinal
trace_df.columns = ["angle"]
trace_df["efficiency"] = df.loc[df[0] == 'target', [23]].values  # Overall effficiency, add [23,24] for error
for key in columns.keys():
    trace_df[key] = df[0].iloc[trace_df.index + columns.get(key)].astype('float').values
trace_df = trace_df.set_index("angle")
calc_intercept_factor(trace_df)



def plot_geometry_quantities(df, quantities_list):
    """ Plots list of df columns in same plot """
    fig, ax = plt.subplots(figsize=(9,6))
    for col in quantities_list:        
        ax.plot(df[col], label=col)
    ax.set_xlabel("$\\theta_z \quad  (\degree)$")
    ax.legend()
    plt.show()
    
def plot_all_quantities(df):
    for i in df.columns:
        plot_geometry_quantities(df, [i])


# plot_all_quantities(trace_df)
plot_geometry_quantities(trace_df, ["missing_losses"])