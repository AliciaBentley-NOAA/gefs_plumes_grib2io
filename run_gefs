#!/bin/bash
#PBS -N gefs_plumes
#PBS -o /lfs/h2/emc/stmp/alicia.bentley/cron.out/gefs_plumes.out
#PBS -e /lfs/h2/emc/stmp/alicia.bentley/cron.out/gefs_plumes.err
#PBS -l select=2:ncpus=16:mpiprocs=4:mem=200GB
#PBS -q dev
#PBS -l walltime=03:00:00
#PBS -A VERF-DEV

set +x
source /lfs/h2/emc/vpppg/noscrub/${USER}/gefsv12/versions/run.ver
module purge
module load envvar/${envvar_ver}
module load intel/${intel_ver}
module load PrgEnv-intel/${PrgEnvintel_ver}
module load craype/${craype_ver}
module load cray-mpich/${craympich_ver}
module load cray-pals/${craypals_ver}
module load prod_util/${prod_util_ver}
module load prod_envir/${prod_envir_ver}
module load libjpeg/${libjpeg_ver}
module load grib_util/${grib_util_ver}
module load wgrib2/${wgrib2_ver}
module load cfp/${cfp_ver}
#Load Python
module load python/${python_ver}
module load libjpeg-turbo/${libjpeg_turbo_ver}
#module load proj/${proj_ver}
#module load geos/${geos_ver}
module use /lfs/h1/mdl/nbm/save/apps/modulefiles
module load python-modules/${python_ver}
export PYTHONPATH="${PYTHONPATH}:/lfs/h2/emc/vpppg/noscrub/${USER}/python"

#module list
set -x

cd /lfs/h2/emc/stmp/${USER}/gefsv12
export HOLDIN=/lfs/h2/emc/stmp/${USER}
export GBexec=/apps/ops/prod/nco

echo intoscript
rm -rf /lfs/h2/emc/stmp/${USER}/gefsv12/*.csv
rm -rf /lfs/h2/emc/stmp/${USER}/gefsv12/out*.txt
year=`cut -c 1-4 holddate.txt`
month=`cut -c 5-6 holddate.txt`
day=`cut -c 7-8 holddate.txt`
hour=`cut -c 9-10 holddate.txt`
cyc=`cut -c 9-10 holddate.txt`
ymdh=${year}${month}${day}${hour}


set +x
set -x

'rm' poescript

echo "/lfs/h2/emc/vpppg/noscrub/${USER}/gefsv12/launchgefs4 ${cyc} > out_launchgefs4.txt &" >> poescript
echo "/lfs/h2/emc/vpppg/noscrub/${USER}/gefsv12/launchgefs3 ${cyc} > out_launchgefs3.txt &" >> poescript
echo "/lfs/h2/emc/vpppg/noscrub/${USER}/gefsv12/launchgefs2 ${cyc} > out_launchgefs2.txt &" >> poescript
echo "/lfs/h2/emc/vpppg/noscrub/${USER}/gefsv12/launchgefs1 ${cyc} > out_launchgefs1.txt &" >> poescript

chmod 775 poescript
#export MP_PGMMODEL=mpmd
#export MP_CMDFILE=poescript
#export OMP_NUM_THREADS=1
#
# Execute the script.

echo beforelsf
#mpirun -l cfp poescript > out_poescript.txt
mpiexec  -np 4 --cpu-bind core --depth=2 cfp poescript > out_poescript.txt
echo pastlsf

qsub /lfs/h2/emc/vpppg/noscrub/${USER}/gefsv12/run_ftp_gefs4
qsub /lfs/h2/emc/vpppg/noscrub/${USER}/gefsv12/run_ftp_gefs3
qsub /lfs/h2/emc/vpppg/noscrub/${USER}/gefsv12/run_ftp_gefs2
qsub /lfs/h2/emc/vpppg/noscrub/${USER}/gefsv12/run_ftp_gefs1
exit
