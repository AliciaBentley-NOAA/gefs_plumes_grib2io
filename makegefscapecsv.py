#!/bin/usr/env python
#import pygrib
import grib2io
import csv
import datetime
import ncepy
import numpy as np
import matplotlib
import math
import subprocess
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import interpolate
import sys

#input argument in YYYYMMDDHH
ymdh = str(sys.argv[1])
#station info arrays
slist=[]
slats=[]
slons=[]
with open('gfsxstations.txt','r') as f:
  for row in f:
    x=row.split(',')
    slist.append(x[0])
    slats.append(float(x[1]))
    slons.append(float(x[2]))
#column headers
members=['time','date','c00','p01','p02','p03','p04','p05','p06','p07','p08','p09','p10','p11','p12','p13','p14','p15','p16','p17','p18','p19','p20','p21','p22','p23','p24','p25','p26','p27','p28','p29','p30','GFS']
fhours=[]
preciptotal=[]
amount=1.0
fhour=60
closest=0  #starting range of forecast hour
furthest=195 #3 hours more than the actual ending forecast hour you want
ymd=ymdh[0:8]
year=int(ymdh[0:4])
month=int(ymdh[4:6])
day=int(ymdh[6:8])
hour=int(ymdh[8:10])
print(year, month , day, hour)
dtime=datetime.datetime(year,month,day,hour,0)
date_list = [dtime + datetime.timedelta(hours=x) for x in range(closest,furthest,3)]
firstdate=dtime - datetime.timedelta(hours=fhour)
fhours1=list(range(closest,furthest,3))

#array that gets written to csv. Everything will be put in it 
nmbtotal=np.empty((len(slist),len(fhours1),len(members)+1),dtype='object')
print(nmbtotal.shape)

for i in range(len(members)):
  print(members[i])
  ptotal=0
  #do different things for different columns and forecast hours
  for j in range(len(fhours1)):
    if i==0:
      nmbtotal[:,j,i]=fhours1[j]
    elif i==1:
      nmbtotal[:,j,i]=date_list[j].strftime("%m-%d-%Y:%H")
    elif i>1 and members[i]!='GFS':
      grbs = grib2io.open('/lfs/h1/ops/prod/com/gefs/v12.2/gefs.'+str(ymd)+'/'+str(hour).zfill(2)+'/atmos/pgrb2bp5/ge'+members[i]+'.t'+str(hour).zfill(2)+'z.pgrb2b.0p50.f'+str(fhours1[j]).zfill(3), mode='r') 
      #grib message order changes from f00 to f03 to f06
      if j==0:
        #precip=grbind.select(name='Convective available potential energy',level=0)[0].values
        #precip=grbs[297][0].data()
        precip=grbs.select(shortName='CAPE',level='surface')[0].data()
        precip=np.asarray(precip[::-1,:])
      elif j==1:
        #precip=grbind.select(name='Convective available potential energy',level=0)[0].values
        #precip=grbs[308][0].data()
        precip=grbs.select(shortName='CAPE',level='surface')[0].data()
        precip=np.asarray(precip[::-1,:])
      else:
        #precip=grbind.select(name='Convective available potential energy',level=0)[0].values
        #precip=grbs[308][0].data()
        precip=grbs.select(shortName='CAPE',level='surface')[0].data()
        precip=np.asarray(precip[::-1,:])
      lats,lons = grbs[31][0].latlons()
      latlist=lats[::-1,0]
      lonlist=lons[0,:]
      lonlist=np.asarray(lonlist)
      latlist=np.asarray(latlist)

      #create interpolation function
      f=interpolate.interp2d(lonlist,latlist,precip,kind='linear')
      for k in range(len(slats)):
        znew=np.round(f((360+slons[k]),slats[k]),3)
        nmbtotal[k,j,i]=znew

    #get GFS data
    else:
      grbs = grib2io.open('/lfs/h1/ops/prod/com/gfs/v16.2/gfs.'+str(ymd)+'/'+str(hour).zfill(2)+'/atmos/gfs.t'+str(hour).zfill(2)+'z.pgrb2.0p50.f'+str(fhours1[j]).zfill(3), mode='r')
      if j==0:
        #precip=grbs[602][0].data()
        precip=grbs.select(shortName='CAPE',level='surface')[0].data()
        precip=np.asarray(precip[::-1,:])
      elif j==1:
        #precip=grbs[624][0].data()
        precip=grbs.select(shortName='CAPE',level='surface')[0].data()
        precip=np.asarray(precip[::-1,:])
      else:
        #precip=grbs[624][0].data()
        precip=grbs.select(shortName='CAPE',level='surface')[0].data()
        precip=np.asarray(precip[::-1,:])
      lats,lons = grbs[31][0].latlons()
      latlist=lats[::-1,0]
      lonlist=lons[0,:]
      lonlist=np.asarray(lonlist)
      latlist=np.asarray(latlist)

      #create interpolation function
      f=interpolate.interp2d(lonlist,latlist,precip,kind='linear')
      for k in range(len(slats)):
        znew=np.round(f((360+slons[k]),slats[k]),3)
        nmbtotal[k,j,34]=znew

#compute mean
for k in range(len(slats)):
  for j in range(len(fhours1)):
    nmbtotal[k,j,33]=np.round(np.sum(nmbtotal[k,j,2:33])/31.0,3)

#write csv files
for k in range(len(slats)):
  f = open("GEFS"+slist[k]+ymdh+"cape.csv","wt")
  try:
    writer = csv.writer(f)
    writer.writerow(('time','date','c0','p1','p2','p3','p4','p5','p6','p7','p8','p9','p10','p11','p12','p13','p14','p15','p16','p17','p18','p19','p20','p21','p22','p23','p24','p25','p26','p27','p28','p29','p30','mean','GFS'))
    for i in range(nmbtotal.shape[1]):
      writer.writerow((str(m).replace("[","")).replace("]","") for m in nmbtotal[k,i,:])
  finally:
    f.close()
