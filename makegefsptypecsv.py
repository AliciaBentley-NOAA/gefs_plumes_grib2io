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

def find_nearest(array,value):
  idx=(np.abs(array-value)).argmin()
  return idx

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
members=['time','date','c00','p01','p02','p03','p04','p05','p06','p07','p08','p09','p10','p11','p12','p13','p14','p15','p16','p17','p18','p19','p20','p21','p22','p23','p24','p25','p26','p27','p28','p29','p30']
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

#array that gets written to csv. Everything will be put in it 
nmbtotal=np.empty((len(slist),len(fhours1),len(membertype)),dtype='object')
nmbrain=np.empty((len(slist),len(fhours1),len(members)+1),dtype='object')
nmbsnow=np.empty((len(slist),len(fhours1),len(members)+1),dtype='object')
nmbfreezing=np.empty((len(slist),len(fhours1),len(members)+1),dtype='object')
nmbice=np.empty((len(slist),len(fhours1),len(members)+1),dtype='object')
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
      #grib message order changes from f00 to f03 to f06
      if j==0:
        grbsprev = grib2io.open('/lfs/h1/ops/prod/com/gefs/v12.3/gefs.'+str(lastymd)+'/'+str(lasthour).zfill(2)+'/atmos/pgrb2ap5/ge'+members[i]+'.t'+str(lasthour).zfill(2)+'z.pgrb2a.0p50.f003', mode='r')
        grbs = grib2io.open('/lfs/h1/ops/prod/com/gefs/v12.3/gefs.'+str(lastymd)+'/'+str(lasthour).zfill(2)+'/atmos/pgrb2ap5/ge'+members[i]+'.t'+str(lasthour).zfill(2)+'z.pgrb2a.0p50.f006', mode='r')
        precipnewc=grbs.select(shortName='APCP')[0].data()*.03937
        precipnewp=grbsprev.select(shortName='APCP')[0].data()*.03937
        catrain=grbs.select(shortName='CRAIN')[0].data()
        catsnow=grbs.select(shortName='CSNOW')[0].data()
        catfreezing=grbs.select(shortName='CFRZR')[0].data()
        catice=grbs.select(shortName='CICEP')[0].data()
        precipnewc=np.asarray(precipnewc[::-1,:])
        precipnewp=np.asarray(precipnewp[::-1,:])
        catrain=np.asarray(catrain[::-1,:])
        catsnow=np.asarray(catsnow[::-1,:])
        catfreezing=np.asarray(catfreezing[::-1,:])
        catice=np.asarray(catice[::-1,:])

        precip=precipnewc-precipnewp
        
      elif (j%2)!=0:
        grbs = grib2io.open('/lfs/h1/ops/prod/com/gefs/v12.3/gefs.'+str(ymd)+'/'+str(hour).zfill(2)+'/atmos/pgrb2ap5/ge'+members[i]+'.t'+str(hour).zfill(2)+'z.pgrb2a.0p50.f'+str(fhours1[j]).zfill(3), mode='r')
        precip=grbs.select(shortName='APCP')[0].data()*.03937
        catrain=grbs.select(shortName='CRAIN')[0].data()
        catsnow=grbs.select(shortName='CSNOW')[0].data()
        catfreezing=grbs.select(shortName='CFRZR')[0].data()
        catice=grbs.select(shortName='CICEP')[0].data()
        precip=np.asarray(precip[::-1,:])
        catrain=np.asarray(catrain[::-1,:])
        catsnow=np.asarray(catsnow[::-1,:])
        catfreezing=np.asarray(catfreezing[::-1,:])
        catice=np.asarray(catice[::-1,:])
      else:
        grbsprev = grib2io.open('/lfs/h1/ops/prod/com/gefs/v12.3/gefs.'+str(ymd)+'/'+str(hour).zfill(2)+'/atmos/pgrb2ap5/ge'+members[i]+'.t'+str(hour).zfill(2)+'z.pgrb2a.0p50.f'+str(fhours1[j-1]).zfill(3), mode='r')
        grbs = grib2io.open('/lfs/h1/ops/prod/com/gefs/v12.3/gefs.'+str(ymd)+'/'+str(hour).zfill(2)+'/atmos/pgrb2ap5/ge'+members[i]+'.t'+str(hour).zfill(2)+'z.pgrb2a.0p50.f'+str(fhours1[j]).zfill(3), mode='r')
        precipnewc=grbs.select(shortName='APCP')[0].data()*.03937
        precipnewp=grbsprev.select(shortName='APCP')[0].data()*.03937
        catrain=grbs.select(shortName='CRAIN')[0].data()
        catsnow=grbs.select(shortName='CSNOW')[0].data()
        catfreezing=grbs.select(shortName='CFRZR')[0].data()
        catice=grbs.select(shortName='CICEP')[0].data()
        precipnewc=np.asarray(precipnewc[::-1,:])
        precipnewp=np.asarray(precipnewp[::-1,:])
        catrain=np.asarray(catrain[::-1,:])
        catsnow=np.asarray(catsnow[::-1,:])
        catfreezing=np.asarray(catfreezing[::-1,:])
        catice=np.asarray(catice[::-1,:])

        precip=precipnewc-precipnewp
      lats,lons = grbs[31][0].latlons()
      latlist=lats[::-1,0]
      lonlist=lons[0,:]
      lonlist=np.asarray(lonlist)
      latlist=np.asarray(latlist)
      for k in range(len(slats)):
        nearestlat=find_nearest(latlist,slats[k])
        nearestlon=find_nearest(lonlist,slons[k]+360)
        thisprecip=precip[nearestlat,nearestlon]
        if thisprecip>0.01:
          thisrain=catrain[nearestlat,nearestlon]
          thissnow=catsnow[nearestlat,nearestlon]
          thisice=catice[nearestlat,nearestlon]
          thisfreezing=catfreezing[nearestlat,nearestlon]
          if thisrain==1:
            #print slist[k],'rain'
            nmbrain[k,j,i]=1
          elif thissnow==1:
            #print slist[k],'snow'
            nmbsnow[k,j,i]=1
          elif thisfreezing==1:
            #print slist[k],'freezing rain'
            nmbfreezing[k,j,i]=1
          elif thisice==1:
            #print slist[k],'ice pellets'
            nmbice[k,j,i]=1

#compute mean
for k in range(len(slats)):
  for j in range(len(fhours1)):
    nmbtotal[k,j,2]= np.round((np.sum([x for x in nmbrain[k,j,:] if x != None])/31.0)*100,1)
    nmbtotal[k,j,3]= np.round((np.sum([x for x in nmbsnow[k,j,:] if x != None])/31.0)*100,1)
    nmbtotal[k,j,4]= np.round((np.sum([x for x in nmbfreezing[k,j,:] if x != None])/31.0)*100,1)
    nmbtotal[k,j,5]= np.round((np.sum([x for x in nmbice[k,j,:] if x != None])/31.0)*100,1)
          
#write csv files
for k in range(len(slats)):
  f = open("GEFS"+slist[k]+ymdh+"ptype.csv","wt")
  try:
    writer = csv.writer(f)
    writer.writerow(('time','date','rain','snow','freezing rain','ice pellets'))
    for i in range(nmbtotal.shape[1]):
      writer.writerow((str(m).replace("[","")).replace("]","") for m in nmbtotal[k,i,:])
  finally:
    f.close()
