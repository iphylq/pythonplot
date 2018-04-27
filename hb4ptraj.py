#!/usr/bin/env python
#-*-encoding:utf-8-*-
"""
	a python shell for generate hbond series analysis with cpptraj from a hb.dat, which consist of all the hbond within the field.
"""
import numpy as np
import re
import os
import sys

file = sys.argv[1]
txt = np.loadtxt(file,dtype='str')
with open('tmp.dat','a') as f:
	for i in txt:
		k = re.findall(r"_(.+)@",i[0])
		kn = k[0]
		f.write(kn+"\t")
		for j in i:
			f.write(j+"\t")
		f.write("\n")
os.system('sort -n tmp.dat>tmp.dat.bak')
txt = np.loadtxt('tmp.dat.bak',dtype='str')
# generate analysis file
with open('hbanalysis','w+') as f:
	f.write('#!/bin/bash\n')
	f.write('direc=$(basename `pwd`)\n')
	f.write('hbmap=$direc-hb\n')
	f.write('step=50\n')
	f.write('ntrj=1\n')
	f.write('for i in `seq 50 -1 1`\n')
	f.write('do\n')
	f.write('\t[ -e md$i.ncdf ] && ntrj=$i && break\n')
	f.write('done\n')
	f.write("echo 'parm abc.top'>ptraj.in\n")
	f.write("for i in `seq 1 1 $ntrj`\n")
	f.write("do\n")
	f.write("\techo 'trajin md$i.ncdf 1 last $step'>>ptraj.in\n")
	f.write("done\n")
	f.write("echo 'strip :WAT'>>ptraj.in\n")
	f.write("echo 'autoimage'>>ptraj.in\n")
	f.write("cat <<eof>>ptraj.in\n")
	for i in txt:
		acceptor = re.findall(r"_(.+)",i[1])
		acceptor = acceptor[0]
		donorh = re.findall(r"_(.+)",i[2])
		donorh = donorh[0]
		donor = re.findall(r"_(.+)",i[3])
		donor = donor[0]
		capA = re.findall(r"(.+)_",i[1])
		capA = capA[0]
		capAA = re.findall(r"@(.+)\d",i[1])
		capAA = capAA[0]
		capB = re.findall(r"(.+)_",i[2])
		capB = capB[0]
		capBB = re.findall(r"_(.+)@",i[2])
		capBB = capBB[0]
		f.write('hbond '+capA[0]+i[0]+capAA+'-'+capB[0]+capBB+' acceptormask '+':'+acceptor+\
			' donorhmask  '+':'+donorh+' donormask '+':'+donor+' '+'series out '+\
			'$hbmap.dat\n'
			)
	f.write('go\n')
	f.write("eof\n")
	f.write("cpptraj -i ptraj.in\n")	
os.system('rm tmp.dat tmp.dat.bak')
os.system('chmod +x hbanalysis')
#print capA[0]+i[0]+capAA+'-'+capB[0]+capBB,acceptor,donorh,donor

