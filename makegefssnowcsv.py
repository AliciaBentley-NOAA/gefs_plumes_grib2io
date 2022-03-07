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

ymdh = str(sys.argv[1])

def find_nearest(array,value):
  idx=(np.abs(array-value)).argmin()
  return idx
slist=[]
slats=[]
slons=[]
with open('gfsxstations.txt','r') as f:
  for row in f:
    x=row.split(',')
    slist.append(x[0])
    slats.append(float(x[1]))
    slons.append(float(x[2]))
members=['time','date','c00','p01','p02','p03','p04','p05','p06','p07','p08','p09','p10','p11','p12','p13','p14','p15','p16','p17','p18','p19','p20','p21','p22','p23','p24','p25','p26','p27','p28','p29','p30','GFS']
type=['rain','snow','freezing rain','ice pellets']
membertype=['time','date','rain','snow','freezing rain','ice pellets']
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
lastcycle=dtime - datetime.timedelta(hours=6)
lastymd=lastcycle.strftime("%Y%m%d")
lasthour=lastcycle.strftime("%H")
fhours1=list(range(closest,furthest,3))
nmbtotal=np.empty((len(slist),len(fhours1),len(members)+1),dtype='object')
nmbrain=np.empty((len(slist),len(fhours1),len(members)+1),dtype='object')
nmbsnow=np.empty((len(slist),len(fhours1),len(members)+1),dtype='object')
nmbfreezing=np.empty((len(slist),len(fhours1),len(members)+1),dtype='object')
nmbice=np.empty((len(slist),len(fhours1),len(members)+1),dtype='object')
print(nmbtotal.shape)
for i in range(len(members)):
  print(members[i])
  ptotal=0
  for j in range(len(fhours1)):
    if i==0:
      nmbtotal[:,j,i]=fhours1[j]
    elif i==1:
      nmbtotal[:,j,i]=date_list[j].strftime("%m-%d-%Y:%H")
    elif i>1 and members[i]!='GFS':
      if j==0:
        nmbtotal[:,j,i]=0.0
        snowtotal=np.zeros((361,720))
        continue
      elif (j%2)!=0:
        grbs = grib2io.open('/gpfs/dell4/nco/ops/com/gefs/prod/gefs.'+str(ymd)+'/'+str(hour).zfill(2)+'/atmos/pgrb2ap5/ge'+members[i]+'.t'+str(hour).zfill(2)+'z.pgrb2a.0p50.f'+str(fhours1[j]).zfill(3), mode='r')
        precip=grbs.select(shortName='APCP')[0].data()*.03937
        catsnow=grbs.select(shortName='CSNOW')[0].data()
        precip=np.asarray(precip[::-1,:])
        catsnow=np.asarray(catsnow[::-1,:])
      else:
        grbsprev = grib2io.open('/gpfs/dell4/nco/ops/com/gefs/prod/gefs.'+str(ymd)+'/'+str(hour).zfill(2)+'/atmos/pgrb2ap5/ge'+members[i]+'.t'+str(hour).zfill(2)+'z.pgrb2a.0p50.f'+str(fhours1[j-1]).zfill(3), mode='r')
        grbs = grib2io.open('/gpfs/dell4/nco/ops/com/gefs/prod/gefs.'+str(ymd)+'/'+str(hour).zfill(2)+'/atmos/pgrb2ap5/ge'+members[i]+'.t'+str(hour).zfill(2)+'z.pgrb2a.0p50.f'+str(fhours1[j]).zfill(3), mode='r')
        precipnewc=grbs.select(shortName='APCP')[0].data()*.03937
        precipnewp=grbsprev.select(shortName='APCP')[0].data()*.03937
        catsnow=grbs.select(shortName='CSNOW')[0].data()
        precipnewc=np.asarray(precipnewc[::-1,:])
        precipnewp=np.asarray(precipnewp[::-1,:])
        catsnow=np.asarray(catsnow[::-1,:])
        precip=precipnewc-precipnewp

      lats,lons = grbs[31][0].latlons()
      latlist=lats[::-1,0]
      lonlist=lons[0,:]
      lonlist=np.asarray(lonlist)
      latlist=np.asarray(latlist)
      precip[catsnow==0]=0
      snowtotal=snowtotal+precip
      f=interpolate.interp2d(lonlist,latlist,snowtotal,kind='linear')
      for k in range(len(slats)):
        nearestlat=find_nearest(latlist,slats[k])
        nearestlon=find_nearest(lonlist,slons[k]+360)
        thisprecip=precip[nearestlat,nearestlon]
        thissnow=catsnow[nearestlat,nearestlon]
        if thissnow==1 and thisprecip>0.01:
          znew=f((360+slons[k]),slats[k])*10.0
          if j>0:
            if nmbtotal[k,j-1,i]>np.round(np.absolute(znew),5):
              nmbtotal[k,j-1,i]=np.round(np.absolute(znew),5)
              nmbtotal[k,j,i]=np.round(np.absolute(znew),5)
              print("bad things")
            else:
              nmbtotal[k,j,i]=np.round(np.absolute(znew),5)
        else:
          nmbtotal[k,j,i]=nmbtotal[k,j-1,i]
    else:      
      if j==0:
        nmbtotal[:,j,34]=0.0
        snowtotal=np.zeros((361,720))
        continue
      elif (j%2)!=0:
        grbs = grib2io.open('/gpfs/dell1/nco/ops/com/gfs/prod/gfs.'+str(ymd)+'/'+str(hour).zfill(2)+'/atmos/gfs.t'+str(hour).zfill(2)+'z.pgrb2.0p50.f'+str(fhours1[j]).zfill(3), mode='r')
        precip=grbs.select(shortName='APCP')[0].data()*.03937
        catsnow=grbs.select(shortName='CSNOW')[0].data()
        precip=np.asarray(precip[::-1,:])
        catsnow=np.asarray(catsnow[::-1,:])

      else:
        grbsprev = grib2io.open('/gpfs/dell1/nco/ops/com/gfs/prod/gfs.'+str(ymd)+'/'+str(hour).zfill(2)+'/atmos/gfs.t'+str(hour).zfill(2)+'z.pgrb2.0p50.f'+str(fhours1[j-1]).zfill(3), mode='r')
        grbs = grib2io.open('/gpfs/dell1/nco/ops/com/gfs/prod/gfs.'+str(ymd)+'/'+str(hour).zfill(2)+'/atmos/gfs.t'+str(hour).zfill(2)+'z.pgrb2.0p50.f'+str(fhours1[j]).zfill(3), mode='r')
        precipnewc=grbs.select(shortName='APCP')[0].data()*.03937
        precipnewp=grbsprev.select(shortName='APCP')[0].data()*.03937
        catsnow=grbs.select(shortName='CSNOW')[0].data()
        precipnewc=np.asarray(precipnewc[::-1,:])
        precipnewp=np.asarray(precipnewp[::-1,:])
        catsnow=np.asarray(catsnow[::-1,:])
        precip=precipnewc-precipnewp

      lats,lons = grbs[31][0].latlons()
      latlist=lats[::-1,0]
      lonlist=lons[0,:]
      lonlist=np.asarray(lonlist)
      latlist=np.asarray(latlist)
      precip[catsnow==0]=0
      snowtotal=snowtotal+precip
      f=interpolate.interp2d(lonlist,latlist,snowtotal,kind='linear')
      for k in range(len(slats)):
        nearestlat=find_nearest(latlist,slats[k])
        nearestlon=find_nearest(lonlist,slons[k]+360)
        thisprecip=precip[nearestlat,nearestlon]
        thissnow=catsnow[nearestlat,nearestlon]
        if thissnow==1 and thisprecip>0.01:
          znew=f((360+slons[k]),slats[k])*10.0
          if j>0:
            if nmbtotal[k,j-1,34]>np.round(np.absolute(znew),5):
              nmbtotal[k,j-1,34]=np.round(np.absolute(znew),5)
              nmbtotal[k,j,34]=np.round(np.absolute(znew),5)
              print("bad things")
            else:
              nmbtotal[k,j,34]=np.round(np.absolute(znew),5)
        else:
          nmbtotal[k,j,34]=nmbtotal[k,j-1,34]


for k in range(len(slats)):
  for j in range(len(fhours1)):
    nmbtotal[k,j,33]=np.round(np.sum(nmbtotal[k,j,2:33])/31.0,5)

for k in range(len(slats)):
  f = open("GEFS"+slist[k]+ymdh+"snow.csv","wt")
  try:
    writer = csv.writer(f)
    writer.writerow(('time','date','c0','p1','p2','p3','p4','p5','p6','p7','p8','p9','p10','p11','p12','p13','p14','p15','p16','p17','p18','p19','p20','p21','p22','p23','p24','p25','p26','p27','p28','p29','p30','mean','GFS'))
    for i in range(nmbtotal.shape[1]):
      writer.writerow((str(m).replace("[","")).replace("]","") for m in nmbtotal[k,i,:])
  finally:
    f.close()
