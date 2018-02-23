# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 11:27:04 2017

@author: Ilya Eryzhenskiy
"""
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import scipy
matplotlib.style.use('ggplot')
#GDP dataset
file = open('oecd_gdp.csv')
headings = file.readline().strip().split(';')
file.close()
gdpdf = pd.read_csv('oecd_gdp.csv')
stringname = list(gdpdf)[0]
gdpdf = gdpdf.rename(columns={stringname:'Country','TIME':'Time'})
gdpdf.Time = gdpdf.Time.apply(lambda x: str(x)) #converting years from ints to strings, because it is so in unemp dataset
#Unemployment dataset
file = open('oecd_unemp.csv')
headings = file.readline().strip().split(';')
file.close()
unempdf = pd.read_csv('oecd_unemp.csv')
stringname = list(unempdf)[0]
unempdf = unempdf.rename(columns={stringname:'Country','TIME':'Time'})
#list of countries
#cntry_list = list(set(list(gdpdf.LOC))) #all the oecd countries
cntry_list = ['AUT','BEL','DEU','ESP','EST','FIN','FRA','GRC','IRL','ITA','LTU','LUX','LVA','NLD','PRT','SVK','SVN']
gdpdf = pd.pivot_table(gdpdf, index = ['Country','Time'], values = 'Value')
gdpdf = pd.DataFrame(list(gdpdf),columns = ['gdp'], index = gdpdf.index)
gdpdf['gdp_growth'] = gdpdf.gdp.pct_change()

unempdf = pd.pivot_table(unempdf, index = ['Country','Time'], values = 'Value')
unempdf = pd.DataFrame(list(unempdf),columns = ['unemp'], index = unempdf.index)
unempdf = unempdf.loc[gdpdf.index]
ugdf = pd.merge(unempdf, gdpdf, left_index = True, right_index = True, how='outer')
cntry_full_list = {'AUT':'Austria','BEL':'Belgium','DEU':'Germany','ESP':'Spain','EST':'Estonia','FIN':'Finland','FRA':'France','GRC':'Greece','IRL':'Ireland','ITA':'Italy','LTU':'Lithuania','LUX':'Luxembourg','LVA':'Latvia','NLD':'Netherlands','PRT':'Portugal','SVK':'Slovakia','SVN':'Slovenia'}

# fig, oneplot = plt.subplots()
# for cntry in cntry_list:
# 	oneplot.plot(gdpdf.ix[cntry],label=cntry_full_list[cntry])
# legend = oneplot.legend(loc='upper left')
# plt.show()

# fig, (gdp_f, unemp_f) = plt.subplots(2,1,sharex=True)
# core_list = ['DEU','FRA','NLD','AUT']
# for cntry in cntry_list:
# 	ugdf.gdp_growth.loc[cntry, slice('2007','2015')].plot().legend(loc = 'center left')
# plt.show()
core_list = ['DEU','FRA','NLD','AUT','BEL','ITA','LUX', 'FIN','IRL']
periph_list = set(cntry_list)-set(core_list)
time_slice = slice('2006','2015')
gdp_core_df = ugdf.unstack('Country').gdp_growth.loc[time_slice,core_list]
unemp_core_df = ugdf.unstack('Country').unemp.loc[time_slice,core_list]
gdp_periph_df = ugdf.unstack('Country').gdp_growth.loc[time_slice,periph_list]
unemp_periph_df = ugdf.unstack('Country').unemp.loc[time_slice,periph_list]
fig, ax = plt.subplots(2,1)
cmap = plt.get_cmap('hsv')
mycolors = cmap(np.linspace(0, 1.0, len(core_list)+1))
gdp_core_df.plot(linewidth = 1.5, ylim = (-1.5, 0.2),color = mycolors,ax = ax[0],sharex =True,title = 'Real GDP per capita growth')
plt.close()
mycolors = cmap(np.linspace(0, 1.0, len(periph_list)+1))
gdp_periph_df.plot(style = '--', ylim = (-0.15, 0.2),color= mycolors, ax = ax[0],sharex =True,)
plt.close()
mycolors = cmap(np.linspace(0, 1.0, len(core_list)+1))
unemp_core_df.plot(linewidth = 1.5, color=mycolors, ax = ax[1],sharex = True, title = 'Unemployment',legend=False)
plt.close()
mycolors = cmap(np.linspace(0, 1.0, len(periph_list)+1))
unemp_periph_df.plot(style = '--', color=mycolors, ax = ax[1],sharex = True,legend=False)
plt.close()
lgd = ax[0].legend(loc = 'center left',bbox_to_anchor=(1.05,0))
fig.savefig('gdp_unemp.png', dpi=300, format='png', bbox_extra_artists=(lgd,), bbox_inches='tight')


# gdpfigs = []
# unempfigs = []
# for cntry in cntry_list:
# 	gdp_piece, unemp_piece = ugdf.gdp_growth.loc[cntry, slice('2007','2015')], ugdf.unemp.loc[cntry, slice('2007','2015')]
# 	gdp_ser, unemp_ser = gdp_piece.loc[cntry], unemp_piece.loc[cntry]
# 	if (cntry in core_list):
# 		gdp_f.plot(gdp_ser,label=cntry_full_list[cntry])
# 		unempfig = unemp_f.plot(unemp_ser,label=cntry_full_list[cntry])
# 	else: 
# 		gdp_f.plot(gdp_ser,'--',label=cntry_full_list[cntry]).legend(loc='center left')
# 		unempfig = unemp_f.plot(unemp_ser,'--',label=cntry_full_list[cntry])
# 	unempfigs.append(unempfig)
# gdptitle = gdp_f.set_title('GDP growth')
# unemptitle = unemp_f.set_title('Unemployment rate')
# #legend = unemp_f.legend(loc='lower center')
# unemp_f.set_xticks(list(np.arange(2007,2016)))
# unemp_f.set_xticklabels(list(np.arange(2007,2016)))
# plt.show()
    

