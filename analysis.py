import os
import matplotlib.pyplot as plt
import seaborn as sns
from run import transversal_traces
import reader
import utils

sns.set_theme()

params = {'figure.figsize': (14, 4),
          'axes.titlesize': 20,
          'axes.titleweight': 'bold',
          'axes.labelsize': 20,
          'axes.labelweight': 'bold',
          'xtick.labelsize': 20,
          'ytick.labelsize': 20,
          'font.weight' : 'bold',
          'font.size': 20,
          'legend.fontsize': 16,
          'savefig.format': 'png',
          # 'savefig.dpi': 300.0,
          'figure.constrained_layout.use': True}
plt.rcParams.update(params)

def get_label(string):
    if string.isupper():
        return string
    return string.title().replace("_"," ")

def plot_geometries_quantity(df_list, quantity="efficiency"):
    """ Plots a column of each dataframe """
    ylabel = get_label(quantity)
    fig, ax = plt.subplots(figsize=(9,6))
    for df in df_list:
        ax.plot(df[quantity], label=df.trace_geometry)
        ax.set_xlabel("$\\theta_z \quad  (\degree)$")
        ax.set_ylabel(get_label(quantity))
        if contains_flux_or_losses([quantity]):
            ylabel = ylabel + " (W)"
        ax.set_ylabel(ylabel)
    ax.legend()
    fig.savefig(f"comparison-plots/{df.trace_direction}-{quantity}")
    plt.show()


def plot_heatmap(trace, values='efficiency'):
    df = reader.read_mean(trace)
    pic_path = os.path.join(trace.exp_dir, "heatmaps", trace.name)
    utils.mkdir_if_not_exists(os.path.dirname(pic_path))
    df1 = df.pivot(index='abs_y', columns='abs_x', values=values)
    fig, ax = plt.subplots(figsize=(10,7))  
    sns.heatmap(df1, cbar_kws={'label': 'efficiency'},
                xticklabels=10, yticklabels=10)
    plt.title(trace.title)
    plt.savefig(pic_path)
    plt.show()

def contains_flux_or_losses(main_str_list, substr_list=["flux", "losses"]):
    for m in main_str_list:
        for s in substr_list:
            if s in m:
                return True
    return False

def plot_geometry_quantities(df, quantities_list):
    """ Plots list of df columns in same plot """
    pic_path = os.path.join(os.getcwd(), "export", df.trace_geometry, "plots", 
                        df.trace_direction,'-'.join(quantities_list))
    utils.mkdir_if_not_exists(os.path.dirname(pic_path))
    fig, ax = plt.subplots(figsize=(9,6))
    for col in quantities_list:        
        ax.plot(df[col], label=get_label(col))
    ax.set_xlabel("$\\theta_z \quad  (\degree)$")
    if contains_flux_or_losses(quantities_list):
        ax.set_ylabel("Watts")
    ax.legend()
    plt.savefig(pic_path)
    plt.show()
    
def plot_all_quantities(df):
    for i in df.columns:
        plot_geometry_quantities(df, [i])

tr_df_list = [reader.read(tr) for tr in transversal_traces]

my_trace = tr_df_list[1].copy()
my_trace.trace_geometry = "real-virtual"
my_trace.trace_direction = "Transversal"

my_trace["potential_flux"] = tr_df_list[1]["potential_flux"] - tr_df_list[0]["missing_losses"] - tr_df_list[0]["shadow_losses"]
my_trace["shadow_losses"] = 0 #tr_df_list[1]["shadow_losses"] - tr_df_list[0]["shadow_losses"]
# my_trace["missing_losses"] = 0
my_trace["absorbed_flux"] = my_trace["potential_flux"]* my_trace["cos_factor"] - my_trace["shadow_losses"] - my_trace["missing_losses"]
my_trace["efficiency"] = my_trace["absorbed_flux"] / my_trace["potential_flux"]
reader.calc_intercept_factor(my_trace)

# plot_geometries_quantity([*tr_df_list, my_trace], quantity="intercept_factor")
# plot_geometries_quantity([*tr_df_list, my_trace], quantity="efficiency")

for i in my_trace.columns:
    plot_geometries_quantity([*tr_df_list, my_trace], quantity=i)