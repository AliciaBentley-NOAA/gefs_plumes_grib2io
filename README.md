# gefs_plumes_grib2io
Scripts used to create/populate the EMC GEFS plumes webpage on WCOSS2 (static 2022 version). 

The largest difference from the static 2021 version of the GEFS plumes scripts (https://github.com/AliciaBentley-NOAA/gefs_plumes) is that the python scripts in this repository use grib2io instead of pygrib to read in GEFS/GFS grib2 files (gefs_plumes_grib2io). Scripts have also been streamlined and commented in the static 2022 version.

/----------------

Prior to running the scripts in this GitHub repository, you will need to download the a) 3-hourly 0.5-degree GEFS forecast files for each ensemble member and b) 3-hourly 0.5-degree GFS forecast files from NOMADS using your own code. Both the "a" and "b" forecast files are required for GEFS and GFS. 

Location of 0.5-degree GEFS forecast files on NOMADS:
https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/

Location of 0.5-degree GFS forecast files on NOMADS:
https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/

/-----------------

Here is a brief description of what is contained in the GEFS plumes repository and how it works:

1) The GEFS plumes webpage is updated 4 times a day (00, 06, 12, 18 cycles of the GEFS) via a cronjob. Example cronjobs can be found in gefs_cron, where each cronjob starts the drive_gefs script for a different initialization time (00, 06, 12, 18). Output is sent to an initialization-time specific log file.

2) The drive_gefs script loads the modules needed to run the GEFS plumes scripts. It also creates temporary directories where the cronjob log files will be stored and where the .csv files (that are ultimately read in and displayed by the GEFS plumes webpage) will be created. The drive_gefs script then cd's into the temporary directory where the .csv files will be created and copies the list of stations displayed on the webpage, matplotlibrc, and the GEFS plumes webpage itself. The drive_gefs script also makes short text files of the current date and yesterday's date before submitting the job run_gefs, which launches the GEFS plumes python scripts in segments.

3) The run_gefs script sets up the job submission resources (located near the top) and creates a POE script that starts launchgefs1, launchgefs2, launchgefs3, and launchgefs4. Each launchgefs script launches 3 to 4 python scripts that create the various .csv files that are ultimately read in and displayed by the GEFS plumes webpage (e.g., makegefs2mtcsv.py). Please change the paths in these python scripts to the locations of the GEFS ensemble member forecasts and GFS deterministic forecasts that you downloaded from NOMADS (see links above to NOMADS data).  

4) The final step of launchgefs1 edits the GEFS plumes webpage file (EMCGEFSplumes.html) to display the current date using the edit_gefs.ksh script. The final step of run_gefs submits run_ftp_gefs1 and run_ftp_gefs2, which transfer all of the .csv files and GEFS plumes webpage (with the adjusted date) to the web directory where they will be displayed. Notes: a) The webpage is only transferred if greater than 3700 csv files have been created. b) Please update run_ftp_gefs1 and run_ftp_gefs2 to transfer to a web directory of your choosing. 

5) All of the contents of the /webpage directory need to copied into the same directory where you intend to display the GEFS plumes webpage. This will allow the webpage to be formatted correctly.
