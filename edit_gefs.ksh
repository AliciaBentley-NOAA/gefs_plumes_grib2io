#!/bin/ksh

cyc=`cut -c 9-10 holddate.txt`
day=`cut -c 11-13 holddate.txt`
year=`cut -c 1-4 holddate.txt`
month=`cut -c 5-6 holddate.txt`
daydate=`cut -c 7-8 holddate.txt`

ycyc=`cut -c 9-10 yholddate.txt`
yday=`cut -c 11-13 yholddate.txt`
yyear=`cut -c 1-4 yholddate.txt`
ymonth=`cut -c 5-6 yholddate.txt`
ydaydate=`cut -c 7-8 yholddate.txt`

f2=`expr ${month} - 1`
day2=`expr ${daydate} - 0`
cyc2=`expr ${cyc} - 0`

yf2=`expr ${ymonth} - 1`
yday2=`expr ${ydaydate} - 0`
ycyc2=`expr ${ycyc} - 0`

# 296, 297, and 298 are lines within the .html script where 

sed '296s/\([0-9]*,[0-9]*,[0-9]*,[0-9]*,0,0\)/'${year}','${f2}','${day2}','${cyc2}',0,0/' EMCGEFSplumes.html > tmpfile ; mv tmpfile EMCGEFSplumes.html
sed '297s/\([0-9]*,[0-9]*,[0-9]*,[0-9]*,0,0\)/'${year}','${f2}','${day2}','${cyc2}',0,0/' EMCGEFSplumes.html > tmpfile ; mv tmpfile EMCGEFSplumes.html
sed '298s/\([0-9]*,[0-9]*,[0-9]*,[0-9]*,0,0\)/'${yyear}','${yf2}','${yday2}',23,0,0/' EMCGEFSplumes.html > tmpfile ; mv tmpfile EMCGEFSplumes.html


#if [[ $cyc -eq 00 ]]
#then
#  sed '254s/\([0-9]*,[0-9]*,[0-9]*,[0-9]*,0,0\)/'${yyear}','${yf2}','${yday2}',23,0,0/' EMCGEFSplumes.html > tmpfile ; mv tmpfile EMCGEFSplumes.html
#fi
  

exit
