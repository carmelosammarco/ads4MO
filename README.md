
# ads4mo - Added Download Services for Mercator-Ocean

[![Build Status](https://travis-ci.com/carmelosammarco/ads4mo.png)](https://travis-ci.com/carmelosammarco/ads4mo) [![Build status](https://ci.appveyor.com/api/projects/status/y4glc7d7ccjb8diq?svg=true)](https://ci.appveyor.com/project/carmelosammarco/ads4mo) [![Gitter](https://badges.gitter.im/ads4mo/community.svg)](https://gitter.im/ads4mo/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge) 

I developed this software while working as [AKKA](https://www.akka-technologies.com) consultant engeneer for the [CMEMS's Service Desk (Copernicus Marine Environment Monitoring Service)](http://marine.copernicus.eu). I was and I am inspired by the Mercator-Ocean's community (users, co-workers, web-forum discussions and many more) which gave me ideas and the motivational power to build this tool. It is the first python application of its kind created inside the CMEMS environment and I hope that with time it will became an ufficial CMEMS tool. The main goals that I wanted to adress were solving the most common user problems as the data-download requests and the netCDF file manipulations.

**This project gave me also ideas to develop other tools** as [tool4nc](https://github.com/carmelosammarco/tool4nc), [MerOCenv](https://github.com/carmelosammarco/MerOCenv) and [MerOC](https://github.com/carmelosammarco/MerOC). To know more about them just visit the projects web pages which are hyperlinked above.

I created also a **chat-community** powered by "Gitter" where is possible have an exchange of ideas,functionalities,bugs and many more. Just click ![Gitter](https://badges.gitter.im/ads4mo/community.svg) to acces the chat room.

Many thanks to visit this page and try this software.

**Carmelo Sammarco**

## Introduction:
Python module containing added downloads services for download the netCDF files from the CMEMS's catalogue and especially usefull for big data requests. It is possible download data by MONTH, DEPTH or DAY until a maximum of three selected variables(Planning to increase this number thought).
It brings in a very intuitive scripting way what was already proposed with [MerOC](https://github.com/carmelosammarco/MerOC).

<p align="center">
  <img width="" height="380" src="DATA/FILE.gif">
</p>

## Be aware that:

The tool is in development so it can be possible find bugs, errors and imprecisions. Please to report them if you find one.

## Dependencies:

The dependencies required which are not installed by default are listed below:

- [x] motuclient>=1.8.1
- [x] ftputil>=3.4

## Installation and module usage

It is possible to install and then use in both UNIX and Windows operative systems following the below steps:

```
pip install ads4mo
```
we can import the module as:

```
from ads4mo import download
```
Once the module is imported we can call the interactive download process typing;

```
download()
```

At this point the system is going to ask:

- **Username and password**

- **Type of the download** which can be set typing one of the following:

     - **MONTH**: The entire period selected will be downloaded by months
     - **DEPTH**: The entire period selected will be downloaded by depth levels
     - **DAY**: The entire period selected will download as daily files
     - **MONTH&DEPTH**: The entire period selected will be downloaded by months and depth levels
     - **YEAR**: The entire period selected will be downloaded by years. Very usefull just when you want extract a grid point (The --longitude-min = --longitude-min and --latitude-min = --latitude-max).

- **Starting/Ending Time**: If not values as HH:MM:SS are typed then "12:00:00" is going to be used as default value.

- **Motu client script** which is generated by the CMEMS web portal.
Please to copy and paste just from the "--motu" until the end. You can leave untouched   "--out-dir <OUTPUT_DIR> --out-name <OUTPUT_FILENAME> --user <USERNAME.> --pwd <PASSWORD.>" because they were already set previously.

Following an example of the full script generted by the Web-portal:

```
python -m motuclient  --motu http://nrt.cmems-du.eu/motu-web/Motu --service-id GLOBAL_ANALYSIS_FORECAST_PHY_001_024-TDS --product-id global-analysis-forecast-phy-001-024 --longitude-min -180 --longitude-max 179.9166717529297 --latitude-min -80 --latitude-max 90 --date-min "2019-04-19 12:00:00" --date-max "2019-04-19 12:00:00" --depth-min 0.493 --depth-max 0.4942 --variable thetao --variable bottomT  --out-dir <OUTPUT_DIR> --out-name <OUTPUT_FILENAME> --user <USERNAME> --pwd <PASSWORD>
```

What you need to use as module's input:

```
--motu http://nrt.cmems-du.eu/motu-web/Motu --service-id GLOBAL_ANALYSIS_FORECAST_PHY_001_024-TDS --product-id global-analysis-forecast-phy-001-024 --longitude-min -180 --longitude-max 179.9166717529297 --latitude-min -80 --latitude-max 90 --date-min "2019-04-19 12:00:00" --date-max "2019-04-19 12:00:00" --depth-min 0.493 --depth-max 0.4942 --variable thetao --variable bottomT  --out-dir <OUTPUT_DIR> --out-name <OUTPUT_FILENAME> --user <USERNAME> --pwd <PASSWORD>
```

The results are going to be downloaded in the file path in which the terminal/command-prompt was at the moment of the data request.

## Stand-alone applications (No Python installation required):

---------

**The stand-alone App for Windows OS can be downloaded from [HERE](https://www.dropbox.com/s/e5ilv9x84m4m0gk/ads4mo-win.exe?dl=0).**

The APP was developed, compiled and tested in Windows 10 environment. As soon as I have time I will try to test it in other Windows environments. It will generate a folder called "CMEMS_DATA" in which all the data downloaded are going to be stored. This folder will be stored in the same system path where the executable "ads4mo-win.exe" is located.

---------

**The stand-alone App for macOS can be downloaded from [HERE](https://www.dropbox.com/s/vimrdqhcri5tevm/ads4mo-macOS.zip?dl=0).**

If the APP doesn't start because of "unidentified developer" message then you need to give the system the permission to run it. In more details, please to go in **Security & Privacy** (Tab "General") and then click on the button which will allows the execution of the tool. It will create a Desktop folder called "CMEMS_DATA" which will store all the data downloaded.

---------
