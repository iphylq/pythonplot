#!/bin/env python

import sys
import string
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib import colors
from matplotlib.ticker import NullFormatter

nullfmt = NullFormatter()
font = {'family':'serif','color':'k','weight':'normal','size':16,}
# datafile and pic name, formated with png
datafile = sys.argv[1]
fix = datafile.split('.')
picname = fix[0] + '.png'

# title line preprocessing
with open(datafile) as f:
	pairs = f.readline()
	pairs = pairs.strip('\n')
	pairs = pairs.split(' ')
	pairs.pop(0)
	pairs = sorted(set(pairs),key=pairs.index)
	pairs.pop(0)
	pairs = [pairs[i].rstrip(r'[UU]') for i in range(len(pairs))]

if pairs[2] == 'G3-C10':
	flag = 'wild'
	colorseries = [1,2,3,4,4,5,6,6,4,3,3,2,2,1]
elif pairs[2] == 'C3O-G10':
	flag = 'mut1'
	colorseries = [1,2,3,3,4,5,6,6,4,3,2,2,1]
elif pairs[2] == 'A3-U10':
	flag = 'mut2'
	colorseries = [1,2,3,4,4,5,6,6,4,3,2,1,1]
elif pairs[2] == 'C3N-G12':
	flag = '2koc'
	colorseries = [1,2,3,3,4,5,5,6,6,6,6,5,4,3,2,2,1,1]
elif pairs[2] == 'U3O-A11':
	flag = '1esh'
	colorseries = [1,2,3,4,5,5,6,5,4,4,3,2,2,1,1]
elif pairs[2] == 'G20O-C1':
	flag = 'Tte-3Q51'
#	colorseries = [1,1,1,2,2,3,3,3,4,4,4,5,5,5,6,6,6,7,8,8,8,9,10]
	colorseries = [1,1,1,2,2,3,3,3,4,4,4,5,5,5,6,6,6,1,2,2,2,3,4]
#elif pairs[2] = '':
#	flag = 'Bsu-2L1V'
#	colorseries = []

# definitions for the axes
left,width = 0.1,0.65
bottom,height = 0.1,0.65
bottom_h = left_h = left + width + 0.02

rect_hbmap = [left, bottom, width, height]
rect_barx = [left, bottom_h, width, 0.2]
rect_bary = [left_h, bottom, 0.2, height]

# load data
data = np.loadtxt(datafile,dtype='int')
data = np.delete(data,0,axis=1)		# delete the first colomn since it refer to the frame num
ybar = sum(data)
ybar = ybar[::-1]
xbar = sum(data.T)
data = data.T
xn = len(data[0])
pn = len(pairs)
data = np.array([data[i]*colorseries[i] for i in range(len(colorseries))])

# sef-define colors
#colorset = [[1,1,1],
#		[1,0,0],
#		[0,1,0],
#		[0,0,1],
#		[0,1,1],
#		[1,0,1],
#		[1,1,0]]
#colorset = [
#	'white',
#	'crimson',
#	'forestgreen',
#	'dodgerblue',
#	'darkorchid',
#	'turquoise',
#	'orangered',
#	'firebrick',
#	'plum',
#	'steelblue',
#	'darksalmon'
#]
colorset = [
	'white',
	'crimson',
	'forestgreen',
	'dodgerblue',
	'darkorchid',
	'turquoise',
	'orangered'
]
cmap = colors.ListedColormap(colorset)
barcolor = [colorset[i] for i in colorseries]
print barcolor
# xticks setting
timeunit = 'Time/ns'
if xn < 500:
	xticks = np.linspace(0,(xn/100+1)*100,xn/100+2)
elif xn < 1000:
	xticks = np.linspace(0,(xn/200+1)*200,xn/200+2)
elif xn < 1500:
	xticks = np.linspace(0,(xn/300+1)*300,xn/300+2)
elif xn < 2000:
	xticks = np.linspace(0,(xn/400+1)*400,xn/400+2)
elif xn < 2500:
	xticks = np.linspace(0,(xn/500+1)*500,xn/500+2)
elif xn < 3000:
	xticks = np.linspace(0,(xn/600+1)*600,xn/600+2)
else:
	xticks = np.linspace(0,(xn/1000+1)*1000,xn/1000+2)
	timeunit = 'Time/us'
xtickslabel = np.delete(xticks,-1)
xtickslabel = [int(i) for i in xtickslabel]
xtickslabel.append('') 
# figure
fi = plt.figure(1,figsize=(8,6),dpi=300)
#fi.title('HBond Profile')
axhbmap = plt.axes(rect_hbmap)
#plt.title('HBond Profile')
axbarx = plt.axes(rect_barx)
axbary = plt.axes(rect_bary)
#plt.title('HBond Profile')
axbarx.xaxis.set_major_formatter(nullfmt)
axbary.yaxis.set_major_formatter(nullfmt)

axhbmap.imshow(data,aspect='auto',interpolation='none',cmap=cmap)
axbarx.bar(np.arange(xn),xbar,width=1.0,color='gray')
axbary.barh(np.arange(pn),ybar/float(xn),height=1.0,color=barcolor[::-1])

# axis and label
axhbmap.set_yticks(np.linspace(0,pn-1,pn))
axhbmap.set_yticklabels(pairs)
axhbmap.set_xticks(xticks)
axhbmap.set_xticklabels(xtickslabel)
axhbmap.set_xlabel(timeunit,fontdict=font)

axbarx.set_xlim([0,xn])
axbarx.set_xticks(xticks)
axbarx.set_ylabel("Hbond Num")

axbary.set_yticks(np.linspace(0,pn-1,pn))
axbary.set_ylim([-0.5,pn-0.5])
axbary.set_xlim([0,1.0])
axbary.set_xlabel("Fraction")
#axbarx.axis('tight')
#axbary.axis('tight')
#ax = plt.gca()
#ax.set_yticks(range(len(pairs)))
#ax.set_yticklabels(ylabel)
#fi.tight_layout()
#plt.title('HBond Profile')
plt.savefig(picname)
#plt.show()

