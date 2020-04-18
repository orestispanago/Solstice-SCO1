import pandas as pdS


df = pd.read_csv("raw/transversal.txt",sep='\s+',names=range(47))


# # proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
# # output = proc.stdout.read()
# # s=str(output,'utf-8')
# # data = StringIO(s) 

# # df=pd.read_csv(data,sep='\s+',names=range(47))


angle = df.loc[0::12,3].values
eff_side1_df = df.loc[9::12, 23].values
eff_side2_df = df.loc[9::12, 45].values

angle_eff = pd.DataFrame({'side1':eff_side1_df,'side2':eff_side2_df}, index=angle)  # 1st row as the column names
angle_eff['total_eff'] = angle_eff['side1'] + angle_eff['side2']
angle_eff['total_eff'].plot()
