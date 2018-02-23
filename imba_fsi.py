import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import scipy
imba_fsi_df = None; imba_df = None; fsi_df = None
matplotlib.style.use('ggplot')
##imbalances database
file = open('oecd_imba.csv')
headings = file.readline().strip().split(';')
imba_df = pd.read_csv('oecd_imba.csv')
file.close()
stringname = list(imba_df)[0]
imba_df = imba_df.rename(columns={stringname:'Country','TIME':'Time'})
imba_df.Time = imba_df.Time.apply(lambda x: str(x)) #converting years from ints to strings, because it is so in fsi dataset#list of countries
#cntry_list = list(set(list(imbadf.LOC))) #all the oecd countries
cntry_list = ['AUT','BEL','DEU','ESP','EST','FIN','FRA','GRC','IRL','ITA','LTU','LUX','LVA','NLD','PRT','SVK','SVN']
imba_df = pd.pivot_table(imba_df, index = ['Country','Time'], values = 'Value')
imba_df = pd.DataFrame(list(imba_df),columns = ['imba'], index = imba_df.index)
imba_df = imba_df.loc[cntry_list]
#Financial Soundness Indicators database
file = open("Financial_Soundness_Indicators_FSI.csv")
fsi_df = pd.read_csv(file,delimiter = ';')
file.close()
fsi_df = fsi_df.rename(columns={fsi_df.columns[0]:'Country'})
cntry_full_list = {'AUT':'Austria','BEL':'Belgium','DEU':'Germany','ESP':'Spain',
					'EST':'Estonia','FIN':'Finland','FRA':'France','GRC':'Greece','IRL':'Ireland',
					'ITA':'Italy','LTU':'Lithuania','LUX':'Luxembourg','LVA':'Latvia','NLD':
					'Netherlands','PRT':'Portugal','SVK':'Slovak Republic','SVN':'Slovenia'}
def dictinvert(d):
    inv = {}
    for k, v in d.items():
        keys = inv.setdefault(v, k)
    return inv
shorten_dict = dictinvert(cntry_full_list)
##harmonize fsi countries with OCDE list
cntry_list_long = [cntry_full_list[x] for x in cntry_list]
#cntry_shorten = dictinvert(cntry_full_list)
fsi_df = fsi_df[fsi_df.Country.isin(cntry_list_long)] #choosing only those in fsi that are OCDE list
fsi_df.Country = fsi_df.Country.apply(lambda x: shorten_dict[x]) #shorten country names 
fsi_df.index = fsi_df.Country
fsi_df = fsi_df[np.array(fsi_df.columns)[1:]].stack()
fsi_df = pd.DataFrame(list(fsi_df),columns = ['fsi'], index = fsi_df.index)
fsi_df = fsi_df.loc[imba_df.index]
imba_fsi_df = pd.merge(imba_df, fsi_df, left_index = True, right_index = True, how='outer')
#Plots
time_slice = slice('2009','2015')
core_list = ['DEU','FRA','NLD','AUT','BEL','ITA','LUX','FIN', 'IRL']
periph_list = set(cntry_list)-set(core_list)
imba_core_df = imba_fsi_df.unstack('Country').imba.loc[time_slice,core_list]
fsi_core_df = imba_fsi_df.unstack('Country').fsi.loc[time_slice,core_list]
imba_periph_df = imba_fsi_df.unstack('Country').imba.loc[time_slice,periph_list]
fsi_periph_df = imba_fsi_df.unstack('Country').fsi.loc[time_slice,periph_list]
fig, ax = plt.subplots(2,1)
cmap = plt.get_cmap('hsv')
mycolors = cmap(np.linspace(0, 1.0, len(core_list)+1))
imba_core_df.plot(linewidth = 1.5, ylim = [-15,15],color = mycolors,ax = ax[0],sharex =True,title = 'CA imbalances as % of GDP')
plt.close()
mycolors = cmap(np.linspace(0, 1.0, len(periph_list)+1))
imba_periph_df.plot(style = '--', ylim = [-15,15],color= mycolors, ax = ax[0],sharex =True,)
plt.close()
mycolors = cmap(np.linspace(0, 1.0, len(core_list)+1))
fsi_core_df.plot(linewidth = 1.5, ylim = [5,30], color=mycolors, ax = ax[1],sharex = True, title = ''' IMF's Financial Soundness Indicator ''',legend=False)
plt.close()
mycolors = cmap(np.linspace(0, 1.0, len(periph_list)+1))
fsi_periph_df.plot(style = '--', ylim = [5,30], color=mycolors, ax = ax[1],sharex = True,legend=False)
plt.close()
lgd = ax[0].legend(loc = 'center left',bbox_to_anchor=(1.05,0))
fig.savefig('imba and soundness.png', dpi=300, format='png', bbox_extra_artists=(lgd,), bbox_inches='tight')

mean_vars = imba_fsi_df.groupby(level = 'Country').mean()
fig2, ax2 = plt.subplots()
plo_core = ax2.scatter(mean_vars.imba.loc[core_list], mean_vars.fsi.loc[core_list], color = 'r')
plo_periph = ax2.scatter(mean_vars.imba.loc[periph_list], mean_vars.fsi.loc[periph_list], color = 'b')
for i, cntry in enumerate(list(mean_vars.index)):
	ax2.annotate(cntry, (mean_vars.imba.iloc[i], mean_vars.fsi.iloc[i]))
xtitle = ax2.set_xlabel('Mean 2009-2015 imbalances')
xtitle = ax2.set_ylabel('Mean 2009-2015 Financail Soundness')
fig2.savefig('scatter.png',dpi = 300, format = 'png')

