#Import the modules needed
from xml.etree import cElementTree as ET
import motuclient as mt
from motuclient import motu_api
import ftputil
import os
import datetime as dt
import time
import calendar
import sys
import math



def download():

# Main functions 

    def countX(lst, x):
        count = 0
        for ele in a:
            if (ele==x):
                count = count+1
        return count


    def extract_from_link(lista):
        for element in lista:
            e = element.split(' ')[1]
            listnew.append(e)


    def extractstart(listast):
        for element in listast:
            e = element.split(' ')
            styyyymmdd.append(e)


    def extractend(listaend):
        for element in listaend:
            e = element.split(' ')
            endyyyymmdd.append(e)


    def load_options(default_values):
        class cmemsval(dict):
            pass
        values=cmemsval()
        for k,v in default_values.items():
            setattr(values, k, v)
        return values


    def perdelta(st,ed,delta):
        curr=st
        while curr <= ed:
            yield curr
            curr += delta

   
    #Line of code from which I extract the information(examples)
    #string = "--user csammarco --pwd MOCs-2018# --motu http://my.cmems-du.eu/motu-web/Motu --service-id NORTHWESTSHELF_REANALYSIS_PHY_004_009-TDS --product-id MetO-NWS-PHY-mm-CUR --longitude-min -19.888885498046875 --longitude-max 12.999671936035156 --latitude-min 40.06666564941406 --latitude-max 65.0001220703125 --date-min "2016-08-16 12:00:00" --date-max "2016-12-16 12:00:00" --depth-min -1 --depth-max 1  --variable vo --variable uo --out-dir /home/parallels/Desktop --out-name file.nc"
    #string = "--user csammarco --pwd MOCs-2018# --motu http://nrt.cmems-du.eu/motu-web/Motu --service-id BALTICSEA_ANALYSIS_FORECAST_WAV_003_010-TDS --product-id dataset-bal-analysis-forecast-wav-hourly --longitude-min 15 --longitude-max 30.207738876342773 --latitude-min 60 --latitude-max 70 --date-min "2017-08-07 03:00:00" --date-max "2017-11-04 12:00:00" --variable VTPK --out-dir /home/parallels/Desktop/xml --out-name file.nc
    
    

    # MONTH, DEPTH, DAY
    typology = input("Please enter which type of download |MONTH|DEPTH|DAY|: ")

    string = input("Based on the selection criteria (showed in the documentation), please input the motuclient script: ")
    
    Out = str(os.getcwd())

    fname = "none.nc"
    

    
    lista = string.split('--')[1:]
    listnew = []
    extract_from_link(lista)
    namenc = fname
    name = namenc.split('.')[0]
    print (name)


    a = string.split()
    x = "--variable"
    z = "--depth-max"

    nV = countX(a, x)
    dV = countX(a, z)

    text1 = "The number of variables are = " + str(nV)      
    text2 = "Your request includes depths(=1)|NO-depth(=0) dimension = " + str(dV)
    text3 = "Please wait... Download in progress using a loop by " + typology 
    
    print ("#####")
    print (text1)
    print ("#####")
    print (text2)
    print ("#####")
    print (text3)
    print ("#####")

    if typology == "MONTH":

        if dV == 0 and nV == 1:
            
            lista = string.split('--')[1:]

            listnew = []

            extract_from_link(lista)

            Us,Pw,Mot,Pr,Ds,Longmin,Longmax,Latmin,Latmax,sd,ed,v1 = listnew

            #and then finally I obtain the Parameters in the correct format
            cmems_user = str(Us)
            cmems_pass = str(Pw)

            proxy_user = None
            proxy_pass = None
            proxy_server = None

            #outputdir = str(Outdir)
            outputname = str(fname)
            motu_server = str(Mot)
            product_id = str(Pr)
            dataset_id = str(Ds)

            #depth_min = float(dmin)
            #depth_max = float(dmax)

            lon_min = float(Longmin)
            lon_max = float(Longmax)
            lat_min = float(Latmin)
            lat_max = float(Latmax)
            
            t1 = sd[1:11]
            t2 = ed[1:11]
            
            date_min = t1 +" 12:00:00"
            date_max = t2+" 12:00:00"

            styyyymmdd = []
            endyyyymmdd = []

            listast = t1.split('-')
            listaend = t2.split('-')
                
            extractstart(listast) 
            extractend(listaend)

            yyyystart,mmstart,dds = styyyymmdd
            yyyyend,mmend,dde = endyyyymmdd

            year1 = int(yyyystart[0])
            month1 = int(mmstart[0])
            d1 = int(dds[0])

            year2 = int(yyyyend[0])
            month2 = int(mmend[0])
            d2 = int(dde[0])

            #print(date_start)
            #print(date_end)

            hhstart = " 12:00:00"
            hhend = " 12:00:00"

            default_values = {'date_min': str(date_min),'date_max': str(date_max),'depth_min': '', 'depth_max': '','longitude_max': lon_max,'longitude_min': lon_min,'latitude_min': lat_min,'latitude_max': lat_max,'describe': None, 'auth_mode': 'cas', 'motu': motu_server,'block_size': 65536, 'log_level': 30, 'out_dir': Out,'socket_timeout': None,'sync': None,  'proxy_server': proxy_server,'proxy_user': proxy_user,'proxy_pwd': proxy_pass, 'user': cmems_user, 'pwd': cmems_pass,'variable': [v1],'product_id': dataset_id,'service_id': product_id,'user_agent': None,'out_name': outputname, 'outputWritten': 'netcdf','size' : '','console_mode': ''}

            #print (default_values)
            date_start = dt.datetime(year1,month1,d1,0,0)
            date_end = dt.datetime(year2,month2,d2,0,0)

            for key, value in default_values.items():
                
                while (date_start <= date_end):
                    
                    date_end_cmd = (dt.datetime(date_start.year, date_start.month,calendar.monthrange(date_start.year, date_start.month)[1]))
                    date_cmd =  date_start.strftime("%Y-%m-%d") + hhstart , date_end_cmd.strftime("%Y-%m-%d") + hhend 
                
                    date_min = date_cmd[0]
                    date_max = date_cmd[1]
                    outputname = "CMEMS_" + date_min[0:10] + "_"+ date_max[0:10] + ".nc"
                
                    default_values = {'date_min': str(date_min),'date_max': str(date_max),'depth_min': '', 'depth_max': '','longitude_max': lon_max,'longitude_min': lon_min,'latitude_min': lat_min,'latitude_max': lat_max,'describe': None, 'auth_mode': 'cas', 'motu': motu_server,'block_size': 65536, 'log_level': 30, 'out_dir': Out,'socket_timeout': None,'sync': None,  'proxy_server': proxy_server,'proxy_user': proxy_user,'proxy_pwd': proxy_pass, 'user': cmems_user, 'pwd': cmems_pass,'variable': [v1],'product_id': dataset_id,'service_id': product_id,'user_agent': None,'out_name': outputname, 'outputWritten': 'netcdf','size' : '','console_mode': ''}
            
                    print(outputname)
                    
                    _opts = load_options(default_values)
                    mt.motu_api.execute_request(_opts)
                
                    date_start = date_end_cmd + dt.timedelta(days=1)



        elif dV == 1 and nV == 1:
            
            lista = string.split('--')[1:]

            listnew = []

            extract_from_link(lista)

            Us,Pw,Mot,Pr,Ds,Longmin,Longmax,Latmin,Latmax,sd,ed,dmin,dmax,v1 = listnew

            #and then finally I obtain the Parameters in the correct format

            cmems_user = str(Us)
            cmems_pass = str(Pw)

            proxy_user = None
            proxy_pass = None
            proxy_server = None

            #outputdir = str(Outdir)
            outputname = str(fname)
            motu_server = str(Mot)
            product_id = str(Pr)
            dataset_id = str(Ds)

            depth_min = float(dmin)
            depth_max = float(dmax)

            lon_min = float(Longmin)
            lon_max = float(Longmax)
            lat_min = float(Latmin)
            lat_max = float(Latmax)
            
            t1 = sd[1:11]
            t2 = ed[1:11]
            
            date_min = t1 +" 12:00:00"
            date_max = t2+" 12:00:00"

            styyyymmdd = []
            endyyyymmdd = []

            listast = t1.split('-')
            listaend = t2.split('-')
                
            extractstart(listast) 
            extractend(listaend)

            yyyystart,mmstart,dds = styyyymmdd
            yyyyend,mmend,dde = endyyyymmdd

            year1 = int(yyyystart[0])
            month1 = int(mmstart[0])
            d1 = int(dds[0])

            year2 = int(yyyyend[0])
            month2 = int(mmend[0])
            d2 = int(dde[0])

            #print(date_start)
            #print(date_end)

            hhstart = " 12:00:00"
            hhend = " 12:00:00"

            default_values = {'date_min': str(date_min),'date_max': str(date_max),'depth_min': depth_min, 'depth_max': depth_max,'longitude_max': lon_max,'longitude_min': lon_min,'latitude_min': lat_min,'latitude_max': lat_max,'describe': None, 'auth_mode': 'cas', 'motu': motu_server,'block_size': 65536, 'log_level': 30, 'out_dir': Out,'socket_timeout': None,'sync': None,  'proxy_server': proxy_server,'proxy_user': proxy_user,'proxy_pwd': proxy_pass, 'user': cmems_user, 'pwd': cmems_pass,'variable': [v1],'product_id': dataset_id,'service_id': product_id,'user_agent': None,'out_name': outputname, 'outputWritten': 'netcdf','size' : '','console_mode': ''}

            #print (default_values)
            date_start = dt.datetime(year1,month1,d1,0,0)
            date_end = dt.datetime(year2,month2,d2,0,0)

            for key, value in default_values.items():
                
                while (date_start <= date_end):
                    
                    date_end_cmd = (dt.datetime(date_start.year, date_start.month,calendar.monthrange(date_start.year, date_start.month)[1]))
                    date_cmd =  date_start.strftime("%Y-%m-%d") + hhstart , date_end_cmd.strftime("%Y-%m-%d") + hhend 
                
                    date_min = date_cmd[0]
                    date_max = date_cmd[1]
                    outputname = "CMEMS_" + date_min[0:10] + "_"+ date_max[0:10] + ".nc"
                
                    default_values = {'date_min': str(date_min),'date_max': str(date_max),'depth_min': depth_min, 'depth_max': depth_max,'longitude_max': lon_max,'longitude_min': lon_min,'latitude_min': lat_min,'latitude_max': lat_max,'describe': None, 'auth_mode': 'cas', 'motu': motu_server,'block_size': 65536, 'log_level': 30, 'out_dir': Out,'socket_timeout': None,'sync': None,  'proxy_server': proxy_server,'proxy_user': proxy_user,'proxy_pwd': proxy_pass, 'user': cmems_user, 'pwd': cmems_pass,'variable': [v1],'product_id': dataset_id,'service_id': product_id,'user_agent': None,'out_name': outputname, 'outputWritten': 'netcdf','size' : '','console_mode': ''}
            
                    print(outputname)
                    
                    _opts = load_options(default_values)
                    mt.motu_api.execute_request(_opts)
                
                    date_start = date_end_cmd + dt.timedelta(days=1)



        elif dV == 0 and nV == 2:
            
            lista = string.split('--')[1:]

            listnew = []

            extract_from_link(lista)

            Us,Pw,Mot,Pr,Ds,Longmin,Longmax,Latmin,Latmax,sd,ed,v1,v2 = listnew

            #and then finally I obtain the Parameters in the correct format

            cmems_user = str(Us)
            cmems_pass = str(Pw)

            proxy_user = None
            proxy_pass = None
            proxy_server = None

            #outputdir = str(Outdir)
            outputname = str(fname)
            motu_server = str(Mot)
            product_id = str(Pr)
            dataset_id = str(Ds)

            #depth_min = float(dmin)
            #depth_max = float(dmax)

            lon_min = float(Longmin)
            lon_max = float(Longmax)
            lat_min = float(Latmin)
            lat_max = float(Latmax)
            
            t1 = sd[1:11]
            t2 = ed[1:11]
            
            date_min = t1 +" 12:00:00"
            date_max = t2+" 12:00:00"

            styyyymmdd = []
            endyyyymmdd = []

            listast = t1.split('-')
            listaend = t2.split('-')
                
            extractstart(listast) 
            extractend(listaend)

            yyyystart,mmstart,dds = styyyymmdd
            yyyyend,mmend,dde = endyyyymmdd

            year1 = int(yyyystart[0])
            month1 = int(mmstart[0])
            d1 = int(dds[0])

            year2 = int(yyyyend[0])
            month2 = int(mmend[0])
            d2 = int(dde[0])

            #print(date_start)
            #print(date_end)

            hhstart = " 12:00:00"
            hhend = " 12:00:00"

            default_values = {'date_min': str(date_min),'date_max': str(date_max),'depth_min': '', 'depth_max': '','longitude_max': lon_max,'longitude_min': lon_min,'latitude_min': lat_min,'latitude_max': lat_max,'describe': None, 'auth_mode': 'cas', 'motu': motu_server,'block_size': 65536, 'log_level': 30, 'out_dir': Out,'socket_timeout': None,'sync': None,  'proxy_server': proxy_server,'proxy_user': proxy_user,'proxy_pwd': proxy_pass, 'user': cmems_user, 'pwd': cmems_pass,'variable': [v1,v2],'product_id': dataset_id,'service_id': product_id,'user_agent': None,'out_name': outputname, 'outputWritten': 'netcdf','size' : '','console_mode': ''}

            #print (default_values)
            date_start = dt.datetime(year1,month1,d1,0,0)
            date_end = dt.datetime(year2,month2,d2,0,0)

            for key, value in default_values.items():
                
                while (date_start <= date_end):
                    
                    date_end_cmd = (dt.datetime(date_start.year, date_start.month,calendar.monthrange(date_start.year, date_start.month)[1]))
                    date_cmd =  date_start.strftime("%Y-%m-%d") + hhstart , date_end_cmd.strftime("%Y-%m-%d") + hhend 
                
                    date_min = date_cmd[0]
                    date_max = date_cmd[1]
                    outputname = "CMEMS_" + date_min[0:10] + "_"+ date_max[0:10] + ".nc"
                
                    default_values = {'date_min': str(date_min),'date_max': str(date_max),'depth_min': '', 'depth_max': '','longitude_max': lon_max,'longitude_min': lon_min,'latitude_min': lat_min,'latitude_max': lat_max,'describe': None, 'auth_mode': 'cas', 'motu': motu_server,'block_size': 65536, 'log_level': 30, 'out_dir': Out,'socket_timeout': None,'sync': None,  'proxy_server': proxy_server,'proxy_user': proxy_user,'proxy_pwd': proxy_pass, 'user': cmems_user, 'pwd': cmems_pass,'variable': [v1,v2],'product_id': dataset_id,'service_id': product_id,'user_agent': None,'out_name': outputname, 'outputWritten': 'netcdf','size' : '','console_mode': ''}
            
                    print(outputname)
                    
                    _opts = load_options(default_values)
                    mt.motu_api.execute_request(_opts)
                
                    date_start = date_end_cmd + dt.timedelta(days=1)



        elif dV == 1 and nV == 2:

            lista = string.split('--')[1:]

            listnew = []

            extract_from_link(lista)

            Us,Pw,Mot,Pr,Ds,Longmin,Longmax,Latmin,Latmax,sd,ed,dmin,dmax,v1,v2 = listnew

            #and then finally I obtain the Parameters in the correct format

            cmems_user = str(Us)
            cmems_pass = str(Pw)

            proxy_user = None
            proxy_pass = None
            proxy_server = None

            #outputdir = str(Outdir)
            outputname = str(fname)
            motu_server = str(Mot)
            product_id = str(Pr)
            dataset_id = str(Ds)

            depth_min = float(dmin)
            depth_max = float(dmax)

            lon_min = float(Longmin)
            lon_max = float(Longmax)
            lat_min = float(Latmin)
            lat_max = float(Latmax)
            
            t1 = sd[1:11]
            t2 = ed[1:11]
            
            date_min = t1 +" 12:00:00"
            date_max = t2+" 12:00:00"

            styyyymmdd = []
            endyyyymmdd = []

            listast = t1.split('-')
            listaend = t2.split('-')
                
            extractstart(listast) 
            extractend(listaend)

            yyyystart,mmstart,dds = styyyymmdd
            yyyyend,mmend,dde = endyyyymmdd

            year1 = int(yyyystart[0])
            month1 = int(mmstart[0])
            d1 = int(dds[0])

            year2 = int(yyyyend[0])
            month2 = int(mmend[0])
            d2 = int(dde[0])

            #print(date_start)
            #print(date_end)

            hhstart = " 12:00:00"
            hhend = " 12:00:00"

            default_values = {'date_min': str(date_min),'date_max': str(date_max),'depth_min': depth_min, 'depth_max': depth_max,'longitude_max': lon_max,'longitude_min': lon_min,'latitude_min': lat_min,'latitude_max': lat_max,'describe': None, 'auth_mode': 'cas', 'motu': motu_server,'block_size': 65536, 'log_level': 30, 'out_dir': Out,'socket_timeout': None,'sync': None,  'proxy_server': proxy_server,'proxy_user': proxy_user,'proxy_pwd': proxy_pass, 'user': cmems_user, 'pwd': cmems_pass,'variable': [v1,v2],'product_id': dataset_id,'service_id': product_id,'user_agent': None,'out_name': outputname, 'outputWritten': 'netcdf','size' : '','console_mode': ''}

            #print (default_values)
            date_start = dt.datetime(year1,month1,d1,0,0)
            date_end = dt.datetime(year2,month2,d2,0,0)

            for key, value in default_values.items():
                
                while (date_start <= date_end):
                    
                    date_end_cmd = (dt.datetime(date_start.year, date_start.month,calendar.monthrange(date_start.year, date_start.month)[1]))
                    date_cmd =  date_start.strftime("%Y-%m-%d") + hhstart , date_end_cmd.strftime("%Y-%m-%d") + hhend 
                
                    date_min = date_cmd[0]
                    date_max = date_cmd[1]
                    outputname = "CMEMS_" + date_min[0:10] + "_"+ date_max[0:10] + ".nc"
                
                    default_values = {'date_min': str(date_min),'date_max': str(date_max),'depth_min': depth_min, 'depth_max': depth_max,'longitude_max': lon_max,'longitude_min': lon_min,'latitude_min': lat_min,'latitude_max': lat_max,'describe': None, 'auth_mode': 'cas', 'motu': motu_server,'block_size': 65536, 'log_level': 30, 'out_dir': Out,'socket_timeout': None,'sync': None,  'proxy_server': proxy_server,'proxy_user': proxy_user,'proxy_pwd': proxy_pass, 'user': cmems_user, 'pwd': cmems_pass,'variable': [v1,v2],'product_id': dataset_id,'service_id': product_id,'user_agent': None,'out_name': outputname, 'outputWritten': 'netcdf','size' : '','console_mode': ''}
            
                    print(outputname)
                    
                    _opts = load_options(default_values)
                    mt.motu_api.execute_request(_opts)
                
                    date_start = date_end_cmd + dt.timedelta(days=1)



        elif dV == 0 and nV == 3:
            
            lista = string.split('--')[1:]

            listnew = []

            extract_from_link(lista)

            Us,Pw,Mot,Pr,Ds,Longmin,Longmax,Latmin,Latmax,sd,ed,v1,v2,v3 = listnew

            #and then finally I obtain the Parameters in the correct format

            cmems_user = str(Us)
            cmems_pass = str(Pw)

            proxy_user = None
            proxy_pass = None
            proxy_server = None

            #outputdir = str(Outdir)
            outputname = str(fname)
            motu_server = str(Mot)
            product_id = str(Pr)
            dataset_id = str(Ds)

            #depth_min = float(dmin)
            #depth_max = float(dmax)

            lon_min = float(Longmin)
            lon_max = float(Longmax)
            lat_min = float(Latmin)
            lat_max = float(Latmax)
            
            t1 = sd[1:11]
            t2 = ed[1:11]
            
            date_min = t1 +" 12:00:00"
            date_max = t2+" 12:00:00"

            styyyymmdd = []
            endyyyymmdd = []

            listast = t1.split('-')
            listaend = t2.split('-')
                
            extractstart(listast) 
            extractend(listaend)

            yyyystart,mmstart,dds = styyyymmdd
            yyyyend,mmend,dde = endyyyymmdd

            year1 = int(yyyystart[0])
            month1 = int(mmstart[0])
            d1 = int(dds[0])

            year2 = int(yyyyend[0])
            month2 = int(mmend[0])
            d2 = int(dde[0])

            #print(date_start)
            #print(date_end)

            hhstart = " 12:00:00"
            hhend = " 12:00:00"

            default_values = {'date_min': str(date_min),'date_max': str(date_max),'depth_min': '', 'depth_max': '','longitude_max': lon_max,'longitude_min': lon_min,'latitude_min': lat_min,'latitude_max': lat_max,'describe': None, 'auth_mode': 'cas', 'motu': motu_server,'block_size': 65536, 'log_level': 30, 'out_dir': Out,'socket_timeout': None,'sync': None,  'proxy_server': proxy_server,'proxy_user': proxy_user,'proxy_pwd': proxy_pass, 'user': cmems_user, 'pwd': cmems_pass,'variable': [v1,v2,v3],'product_id': dataset_id,'service_id': product_id,'user_agent': None,'out_name': outputname, 'outputWritten': 'netcdf','size' : '','console_mode': ''}

            #print (default_values)
            date_start = dt.datetime(year1,month1,d1,0,0)
            date_end = dt.datetime(year2,month2,d2,0,0)

            for key, value in default_values.items():
                
                while (date_start <= date_end):
                    
                    date_end_cmd = (dt.datetime(date_start.year, date_start.month,calendar.monthrange(date_start.year, date_start.month)[1]))
                    date_cmd =  date_start.strftime("%Y-%m-%d") + hhstart , date_end_cmd.strftime("%Y-%m-%d") + hhend 
                
                    date_min = date_cmd[0]
                    date_max = date_cmd[1]
                    outputname = "CMEMS_" + date_min[0:10] + "_"+ date_max[0:10] + ".nc"
                
                    default_values = {'date_min': str(date_min),'date_max': str(date_max),'depth_min': '', 'depth_max': '','longitude_max': lon_max,'longitude_min': lon_min,'latitude_min': lat_min,'latitude_max': lat_max,'describe': None, 'auth_mode': 'cas', 'motu': motu_server,'block_size': 65536, 'log_level': 30, 'out_dir': Out,'socket_timeout': None,'sync': None,  'proxy_server': proxy_server,'proxy_user': proxy_user,'proxy_pwd': proxy_pass, 'user': cmems_user, 'pwd': cmems_pass,'variable': [v1,v2,v3],'product_id': dataset_id,'service_id': product_id,'user_agent': None,'out_name': outputname, 'outputWritten': 'netcdf','size' : '','console_mode': ''}
            
                    print(outputname)
                    
                    _opts = load_options(default_values)
                    mt.motu_api.execute_request(_opts)
                
                    date_start = date_end_cmd + dt.timedelta(days=1)


        elif dV == 1 and nV == 3:

            lista = string.split('--')[1:]

            listnew = []

            extract_from_link(lista)

            Us,Pw,Mot,Pr,Ds,Longmin,Longmax,Latmin,Latmax,sd,ed,dmin,dmax,v1,v2,v3 = listnew

            #and then finally I obtain the Parameters in the correct format

            cmems_user = str(Us)
            cmems_pass = str(Pw)

            proxy_user = None
            proxy_pass = None
            proxy_server = None

            #outputdir = str(Outdir)
            outputname = str(fname)
            motu_server = str(Mot)
            product_id = str(Pr)
            dataset_id = str(Ds)

            depth_min = float(dmin)
            depth_max = float(dmax)

            lon_min = float(Longmin)
            lon_max = float(Longmax)
            lat_min = float(Latmin)
            lat_max = float(Latmax)
            
            t1 = sd[1:11]
            t2 = ed[1:11]
            
            date_min = t1 +" 12:00:00"
            date_max = t2+" 12:00:00"

            styyyymmdd = []
            endyyyymmdd = []

            listast = t1.split('-')
            listaend = t2.split('-')
                
            extractstart(listast) 
            extractend(listaend)

            yyyystart,mmstart,dds = styyyymmdd
            yyyyend,mmend,dde = endyyyymmdd

            year1 = int(yyyystart[0])
            month1 = int(mmstart[0])
            d1 = int(dds[0])

            year2 = int(yyyyend[0])
            month2 = int(mmend[0])
            d2 = int(dde[0])

            #print(date_start)
            #print(date_end)

            hhstart = " 12:00:00"
            hhend = " 12:00:00"

            default_values = {'date_min': str(date_min),'date_max': str(date_max),'depth_min': depth_min, 'depth_max': depth_max,'longitude_max': lon_max,'longitude_min': lon_min,'latitude_min': lat_min,'latitude_max': lat_max,'describe': None, 'auth_mode': 'cas', 'motu': motu_server,'block_size': 65536, 'log_level': 30, 'out_dir': Out,'socket_timeout': None,'sync': None,  'proxy_server': proxy_server,'proxy_user': proxy_user,'proxy_pwd': proxy_pass, 'user': cmems_user, 'pwd': cmems_pass,'variable': [v1,v2,v3],'product_id': dataset_id,'service_id': product_id,'user_agent': None,'out_name': outputname, 'outputWritten': 'netcdf','size' : '','console_mode': ''}

            #print (default_values)
            date_start = dt.datetime(year1,month1,d1,0,0)
            date_end = dt.datetime(year2,month2,d2,0,0)

            for key, value in default_values.items():
                
                while (date_start <= date_end):
                    
                    date_end_cmd = (dt.datetime(date_start.year, date_start.month,calendar.monthrange(date_start.year, date_start.month)[1]))
                    date_cmd =  date_start.strftime("%Y-%m-%d") + hhstart , date_end_cmd.strftime("%Y-%m-%d") + hhend 
                
                    date_min = date_cmd[0]
                    date_max = date_cmd[1]
                    outputname = "CMEMS_" + date_min[0:10] + "_"+ date_max[0:10] + ".nc"
                
                    default_values = {'date_min': str(date_min),'date_max': str(date_max),'depth_min': depth_min, 'depth_max': depth_max,'longitude_max': lon_max,'longitude_min': lon_min,'latitude_min': lat_min,'latitude_max': lat_max,'describe': None, 'auth_mode': 'cas', 'motu': motu_server,'block_size': 65536, 'log_level': 30, 'out_dir': Out,'socket_timeout': None,'sync': None,  'proxy_server': proxy_server,'proxy_user': proxy_user,'proxy_pwd': proxy_pass, 'user': cmems_user, 'pwd': cmems_pass,'variable': [v1,v2,v3],'product_id': dataset_id,'service_id': product_id,'user_agent': None,'out_name': outputname, 'outputWritten': 'netcdf','size' : '','console_mode': ''}
            
                    print(outputname)
                    
                    _opts = load_options(default_values)
                    mt.motu_api.execute_request(_opts)
                
                    date_start = date_end_cmd + dt.timedelta(days=1)

        else:
            print("ERROR: Number of variables not supported. If you need more variables please to contact the author of this script")   



    #################################################################################


    if typology == "DEPTH":

        stringxml = "python -m motuclient " + string + " --describe-product"
        print (stringxml)
        os.system(stringxml)
        tree = ET.parse( name+".xml")
        root = tree.getroot()
        depth = root[2].text
        listadepth = depth.split(';')
        print (listadepth)

        if nV == 1:

            lista = string.split('--')[1:]

            listnew = []

            extract_from_link(lista)

            Us,Pw,Mot,Pr,Ds,Longmin,Longmax,Latmin,Latmax,sd,ed,dmin,dmax,v1 = listnew

            #and then finally I obtain the Parameters in the correct format

            cmems_user = str(Us)
            cmems_pass = str(Pw)

            proxy_user = None
            proxy_pass = None
            proxy_server = None

            #outputdir = str(Outdir)
            outputname = str(fname)
            motu_server = str(Mot)
            product_id = str(Pr)
            dataset_id = str(Ds)

            depth_min = float(dmin)
            depth_max = float(dmax)

            lon_min = float(Longmin)
            lon_max = float(Longmax)
            lat_min = float(Latmin)
            lat_max = float(Latmax)
            
            t1= sd[1:11]
            t2= ed[1:11]

            tmin = t1 + " 12:00:00"
            tmax = t2 + " 12:00:00"
            
            for z in listadepth:

                    def truncate(f, n):
                        return math.floor(f * 10 ** n) / 10 ** n 
                    
                    zformat = truncate(float(z), 2)
                    z1 = zformat
                    z2 = float(zformat) + 0.01

                    outputname1 = "CMEMS_" + tmin[1:11] + "_"+ tmax[1:11]  +"_"+z+"-Depth"+ ".nc"
                    default_values = {'date_min': str(tmin),'date_max': str(tmax),'depth_min': str(z), 'depth_max': str(z),'longitude_max': lon_max,'longitude_min': lon_min,'latitude_min': lat_min,'latitude_max': lat_max,'describe': None, 'auth_mode': 'cas', 'motu': motu_server,'block_size': 65536, 'log_level': 30, 'out_dir': Out,'socket_timeout': None,'sync': None,  'proxy_server': proxy_server,'proxy_user': proxy_user,'proxy_pwd': proxy_pass, 'user': cmems_user, 'pwd': cmems_pass,'variable': [v1],'product_id': dataset_id,'service_id': product_id,'user_agent': None,'out_name': outputname1, 'outputWritten': 'netcdf','size' : '','console_mode': ''}
                    print(outputname1)
                    _opts = load_options(default_values)
                    mt.motu_api.execute_request(_opts)


                    outputname2 = "CMEMS_" + tmin[1:11] + "_"+ tmax[1:11]  +"_"+z+"-Depth"+ ".nc"
                    default_values = {'date_min': str(tmin),'date_max': str(tmax),'depth_min': str(z1), 'depth_max': str(z2),'longitude_max': lon_max,'longitude_min': lon_min,'latitude_min': lat_min,'latitude_max': lat_max,'describe': None, 'auth_mode': 'cas', 'motu': motu_server,'block_size': 65536, 'log_level': 30, 'out_dir': Out,'socket_timeout': None,'sync': None,  'proxy_server': proxy_server,'proxy_user': proxy_user,'proxy_pwd': proxy_pass, 'user': cmems_user, 'pwd': cmems_pass,'variable': [v1],'product_id': dataset_id,'service_id': product_id,'user_agent': None,'out_name': outputname2, 'outputWritten': 'netcdf','size' : '','console_mode': ''}
                    print(outputname2)
                    _opts = load_options(default_values)
                    mt.motu_api.execute_request(_opts)

        elif nV == 2:

            lista = string.split('--')[1:]

            listnew = []

            extract_from_link(lista)

            Us,Pw,Mot,Pr,Ds,Longmin,Longmax,Latmin,Latmax,sd,ed,dmin,dmax,v1,v2 = listnew

            #and then finally I obtain the Parameters in the correct format

            cmems_user = str(Us)
            cmems_pass = str(Pw)

            proxy_user = None
            proxy_pass = None
            proxy_server = None

            #outputdir = str(Outdir)
            outputname = str(fname)
            motu_server = str(Mot)
            product_id = str(Pr)
            dataset_id = str(Ds)

            depth_min = float(dmin)
            depth_max = float(dmax)

            lon_min = float(Longmin)
            lon_max = float(Longmax)
            lat_min = float(Latmin)
            lat_max = float(Latmax)
            
            t1= sd[1:11]
            t2= ed[1:11]

            tmin = t1 + " 12:00:00"
            tmax = t2 + " 12:00:00"
            
            for z in listadepth:

                    def truncate(f, n):
                        return math.floor(f * 10 ** n) / 10 ** n 
                    
                    zformat = truncate(float(z), 2)
                    z1 = zformat
                    z2 = float(zformat) + 0.01

                    outputname1 = "CMEMS_" + tmin[1:11] + "_"+ tmax[1:11]  +"_"+z+"-Depth"+ ".nc"
                    default_values = {'date_min': str(tmin),'date_max': str(tmax),'depth_min': str(z), 'depth_max': str(z),'longitude_max': lon_max,'longitude_min': lon_min,'latitude_min': lat_min,'latitude_max': lat_max,'describe': None, 'auth_mode': 'cas', 'motu': motu_server,'block_size': 65536, 'log_level': 30, 'out_dir': Out,'socket_timeout': None,'sync': None,  'proxy_server': proxy_server,'proxy_user': proxy_user,'proxy_pwd': proxy_pass, 'user': cmems_user, 'pwd': cmems_pass,'variable': [v1,v2],'product_id': dataset_id,'service_id': product_id,'user_agent': None,'out_name': outputname1, 'outputWritten': 'netcdf','size' : '','console_mode': ''}
                    print(outputname1)
                    _opts = load_options(default_values)
                    mt.motu_api.execute_request(_opts)


                    outputname2 = "CMEMS_" + tmin[1:11] + "_"+ tmax[1:11]  +"_"+z+"-Depth"+ ".nc"
                    default_values = {'date_min': str(tmin),'date_max': str(tmax),'depth_min': str(z1), 'depth_max': str(z2),'longitude_max': lon_max,'longitude_min': lon_min,'latitude_min': lat_min,'latitude_max': lat_max,'describe': None, 'auth_mode': 'cas', 'motu': motu_server,'block_size': 65536, 'log_level': 30, 'out_dir': Out,'socket_timeout': None,'sync': None,  'proxy_server': proxy_server,'proxy_user': proxy_user,'proxy_pwd': proxy_pass, 'user': cmems_user, 'pwd': cmems_pass,'variable': [v1,v2],'product_id': dataset_id,'service_id': product_id,'user_agent': None,'out_name': outputname2, 'outputWritten': 'netcdf','size' : '','console_mode': ''}
                    print(outputname2)
                    _opts = load_options(default_values)
                    mt.motu_api.execute_request(_opts)

        elif nV == 3:

            lista = string.split('--')[1:]

            listnew = []

            extract_from_link(lista)

            Us,Pw,Mot,Pr,Ds,Longmin,Longmax,Latmin,Latmax,sd,ed,dmin,dmax,v1,v2,v3 = listnew

            #and then finally I obtain the Parameters in the correct format

            cmems_user = str(Us)
            cmems_pass = str(Pw)

            proxy_user = None
            proxy_pass = None
            proxy_server = None

            #outputdir = str(Outdir)
            outputname = str(fname)
            motu_server = str(Mot)
            product_id = str(Pr)
            dataset_id = str(Ds)

            depth_min = float(dmin)
            depth_max = float(dmax)

            lon_min = float(Longmin)
            lon_max = float(Longmax)
            lat_min = float(Latmin)
            lat_max = float(Latmax)
            
            t1= sd[1:11]
            t2= ed[1:11]

            tmin = t1 + " 12:00:00"
            tmax = t2 + " 12:00:00"
            
            for z in listadepth:

                    def truncate(f, n):
                        return math.floor(f * 10 ** n) / 10 ** n 
                    
                    zformat = truncate(float(z), 2)
                    z1 = zformat
                    z2 = float(zformat) + 0.01

                    outputname1 = "CMEMS_" + tmin[1:11] + "_"+ tmax[1:11]  +"_"+z+"-Depth"+ ".nc"
                    default_values = {'date_min': str(tmin),'date_max': str(tmax),'depth_min': str(z), 'depth_max': str(z),'longitude_max': lon_max,'longitude_min': lon_min,'latitude_min': lat_min,'latitude_max': lat_max,'describe': None, 'auth_mode': 'cas', 'motu': motu_server,'block_size': 65536, 'log_level': 30, 'out_dir': Out,'socket_timeout': None,'sync': None,  'proxy_server': proxy_server,'proxy_user': proxy_user,'proxy_pwd': proxy_pass, 'user': cmems_user, 'pwd': cmems_pass,'variable': [v1,v2,v3],'product_id': dataset_id,'service_id': product_id,'user_agent': None,'out_name': outputname1, 'outputWritten': 'netcdf','size' : '','console_mode': ''}
                    print(outputname1)
                    _opts = load_options(default_values)
                    mt.motu_api.execute_request(_opts)


                    outputname2 = "CMEMS_" + tmin[1:11] + "_"+ tmax[1:11]  +"_"+z+"-Depth"+ ".nc"
                    default_values = {'date_min': str(tmin),'date_max': str(tmax),'depth_min': str(z1), 'depth_max': str(z2),'longitude_max': lon_max,'longitude_min': lon_min,'latitude_min': lat_min,'latitude_max': lat_max,'describe': None, 'auth_mode': 'cas', 'motu': motu_server,'block_size': 65536, 'log_level': 30, 'out_dir': Out,'socket_timeout': None,'sync': None,  'proxy_server': proxy_server,'proxy_user': proxy_user,'proxy_pwd': proxy_pass, 'user': cmems_user, 'pwd': cmems_pass,'variable': [v1,v2,v3],'product_id': dataset_id,'service_id': product_id,'user_agent': None,'out_name': outputname2, 'outputWritten': 'netcdf','size' : '','console_mode': ''}
                    print(outputname2)
                    _opts = load_options(default_values)
                    mt.motu_api.execute_request(_opts)

        else:
            print("ERROR: Number of variables not supported. If you need more variables please to contact the author of this script") 

            

    ##################################################################################


    if typology == "DAY":

        if nV == 1 and dV == 0:

            lista = string.split('--')[1:]

            listnew = []

            extract_from_link(lista)

            Us,Pw,Mot,Pr,Ds,Longmin,Longmax,Latmin,Latmax,sd,ed,v1 = listnew

            #and then finally I obtain the Parameters in the correct format
            cmems_user = str(Us)
            cmems_pass = str(Pw)

            proxy_user = None
            proxy_pass = None
            proxy_server = None

            #outputdir = str(Outdir)
            outputname = str(fname)
            motu_server = str(Mot)
            product_id = str(Pr)
            dataset_id = str(Ds)

            #depth_min = float(dmin)
            #depth_max = float(dmax)

            lon_min = float(Longmin)
            lon_max = float(Longmax)
            lat_min = float(Latmin)
            lat_max = float(Latmax)
            
            t1 = sd[1:11]
            t2 = ed[1:11]

            #print (t1)
            #print (t2)
                
            date_min = t1 +" 12:00:00"
            date_max = t2 +" 12:00:00"

            #print(date_min)
            #print (date_max)

            styyyymmdd = []
            endyyyymmdd = []

            listast = t1.split('-')
            listaend = t2.split('-')
                    
            extractstart(listast) 
            extractend(listaend)

            yyyystart,mmstart,dds = styyyymmdd
            yyyyend,mmend,dde = endyyyymmdd

            year1 = int(yyyystart[0])
            month1 = int(mmstart[0])
            d1 = int(dds[0])

            year2 = int(yyyyend[0])
            month2 = int(mmend[0])
            d2 = int(dde[0])

            default_values = {'date_min': str(date_min),'date_max': str(date_max),'depth_min': '', 'depth_max': '','longitude_max': lon_max,'longitude_min': lon_min,'latitude_min': lat_min,'latitude_max': lat_max,'describe': None, 'auth_mode': 'cas', 'motu': motu_server,'block_size': 65536, 'log_level': 30, 'out_dir': Out,'socket_timeout': None,'sync': None,  'proxy_server': proxy_server,'proxy_user': proxy_user,'proxy_pwd': proxy_pass, 'user': cmems_user, 'pwd': cmems_pass,'variable': [v1],'product_id': dataset_id,'service_id': product_id,'user_agent': None,'out_name': outputname, 'outputWritten': 'netcdf','size' : '','console_mode': ''}

                
            hhstartdaily = "12:00:00" #to modify based on your needs
            hhenddaily = "12:00:00"   #to modify based on your needs

            start = dt.datetime(year1,month1,d1,0,0)
            end = dt.datetime(year2,month2,d2,0,0)
            delta = dt.timedelta(days=1)
                
            with open (Out + "/listdate.txt", 'w') as f:
                for result in perdelta(start,end, delta):
                    print (result, file=f)

            for key, value in default_values.items():

                with open (Out + "/listdate.txt") as f:
                        
                    while True:

                        line = f.readline()
                        date_cmd =  line[0:10] +" " +" " + hhstartdaily , line[0:10] +" " + " " + hhenddaily
                        date_min = date_cmd[0]
                        date_max = date_cmd[1]

                        outputname = "CMEMS_" + date_min[0:10] + "_"+ date_max[0:10] + ".nc"

                        default_values = {'date_min': str(date_min),'date_max': str(date_max),'depth_min': '', 'depth_max': '','longitude_max': lon_max,'longitude_min': lon_min,'latitude_min': lat_min,'latitude_max': lat_max,'describe': None, 'auth_mode': 'cas', 'motu': motu_server,'block_size': 65536, 'log_level': 30, 'out_dir': Out,'socket_timeout': None,'sync': None,  'proxy_server': proxy_server,'proxy_user': proxy_user,'proxy_pwd': proxy_pass, 'user': cmems_user, 'pwd': cmems_pass,'variable': [v1],'product_id': dataset_id,'service_id': product_id,'user_agent': None,'out_name': outputname, 'outputWritten': 'netcdf','size' : '','console_mode': ''}

                        print(outputname)

                        _opts = load_options(default_values)
                        mt.motu_api.execute_request(_opts)

                        if not line: 
                            break 

        
        elif nV == 2 and dV == 0:

            lista = string.split('--')[1:]

            listnew = []

            extract_from_link(lista)

            Us,Pw,Mot,Pr,Ds,Longmin,Longmax,Latmin,Latmax,sd,ed,v1,v2 = listnew

            #and then finally I obtain the Parameters in the correct format
            cmems_user = str(Us)
            cmems_pass = str(Pw)

            proxy_user = None
            proxy_pass = None
            proxy_server = None

            #outputdir = str(Outdir)
            outputname = str(fname)
            motu_server = str(Mot)
            product_id = str(Pr)
            dataset_id = str(Ds)

            #depth_min = float(dmin)
            #depth_max = float(dmax)

            lon_min = float(Longmin)
            lon_max = float(Longmax)
            lat_min = float(Latmin)
            lat_max = float(Latmax)
            
            t1 = sd[1:11]
            t2 = ed[1:11]

            #print (t1)
            #print (t2)
                
            date_min = t1 +" 12:00:00"
            date_max = t2 +" 12:00:00"

            #print(date_min)
            #print (date_max)

            styyyymmdd = []
            endyyyymmdd = []

            listast = t1.split('-')
            listaend = t2.split('-')
                    
            extractstart(listast) 
            extractend(listaend)

            yyyystart,mmstart,dds = styyyymmdd
            yyyyend,mmend,dde = endyyyymmdd

            year1 = int(yyyystart[0])
            month1 = int(mmstart[0])
            d1 = int(dds[0])

            year2 = int(yyyyend[0])
            month2 = int(mmend[0])
            d2 = int(dde[0])

            default_values = {'date_min': str(date_min),'date_max': str(date_max),'depth_min': '', 'depth_max': '','longitude_max': lon_max,'longitude_min': lon_min,'latitude_min': lat_min,'latitude_max': lat_max,'describe': None, 'auth_mode': 'cas', 'motu': motu_server,'block_size': 65536, 'log_level': 30, 'out_dir': Out,'socket_timeout': None,'sync': None,  'proxy_server': proxy_server,'proxy_user': proxy_user,'proxy_pwd': proxy_pass, 'user': cmems_user, 'pwd': cmems_pass,'variable': [v1,v2],'product_id': dataset_id,'service_id': product_id,'user_agent': None,'out_name': outputname, 'outputWritten': 'netcdf','size' : '','console_mode': ''}

                
            hhstartdaily = "12:00:00" #to modify based on your needs
            hhenddaily = "12:00:00"   #to modify based on your needs

            start = dt.datetime(year1,month1,d1,0,0)
            end = dt.datetime(year2,month2,d2,0,0)
            delta = dt.timedelta(days=1)
                
            with open (Out + "/listdate.txt", 'w') as f:
                for result in perdelta(start,end, delta):
                    print (result, file=f)

            for key, value in default_values.items():

                with open (Out + "/listdate.txt") as f:
                        
                    while True:

                        line = f.readline()
                        date_cmd =  line[0:10] +" " +" " + hhstartdaily , line[0:10] +" " + " " + hhenddaily
                        date_min = date_cmd[0]
                        date_max = date_cmd[1]

                        outputname = "CMEMS_" + date_min[0:10] + "_"+ date_max[0:10] + ".nc"

                        default_values = {'date_min': str(date_min),'date_max': str(date_max),'depth_min': '', 'depth_max': '','longitude_max': lon_max,'longitude_min': lon_min,'latitude_min': lat_min,'latitude_max': lat_max,'describe': None, 'auth_mode': 'cas', 'motu': motu_server,'block_size': 65536, 'log_level': 30, 'out_dir': Out,'socket_timeout': None,'sync': None,  'proxy_server': proxy_server,'proxy_user': proxy_user,'proxy_pwd': proxy_pass, 'user': cmems_user, 'pwd': cmems_pass,'variable': [v1,v2],'product_id': dataset_id,'service_id': product_id,'user_agent': None,'out_name': outputname, 'outputWritten': 'netcdf','size' : '','console_mode': ''}

                        print(outputname)

                        _opts = load_options(default_values)
                        mt.motu_api.execute_request(_opts)

                        if not line: 
                            break 


        elif nV == 3 and dV == 0:

            lista = string.split('--')[1:]

            listnew = []

            extract_from_link(lista)

            Us,Pw,Mot,Pr,Ds,Longmin,Longmax,Latmin,Latmax,sd,ed,v1,v2,v3 = listnew

            #and then finally I obtain the Parameters in the correct format
            cmems_user = str(Us)
            cmems_pass = str(Pw)

            proxy_user = None
            proxy_pass = None
            proxy_server = None

            #outputdir = str(Outdir)
            outputname = str(fname)
            motu_server = str(Mot)
            product_id = str(Pr)
            dataset_id = str(Ds)

            #depth_min = float(dmin)
            #depth_max = float(dmax)

            lon_min = float(Longmin)
            lon_max = float(Longmax)
            lat_min = float(Latmin)
            lat_max = float(Latmax)
            
            t1 = sd[1:11]
            t2 = ed[1:11]

            #print (t1)
            #print (t2)
                
            date_min = t1 +" 12:00:00"
            date_max = t2 +" 12:00:00"

            #print(date_min)
            #print (date_max)

            styyyymmdd = []
            endyyyymmdd = []

            listast = t1.split('-')
            listaend = t2.split('-')
                    
            extractstart(listast) 
            extractend(listaend)

            yyyystart,mmstart,dds = styyyymmdd
            yyyyend,mmend,dde = endyyyymmdd

            year1 = int(yyyystart[0])
            month1 = int(mmstart[0])
            d1 = int(dds[0])

            year2 = int(yyyyend[0])
            month2 = int(mmend[0])
            d2 = int(dde[0])

            default_values = {'date_min': str(date_min),'date_max': str(date_max),'depth_min': '', 'depth_max': '','longitude_max': lon_max,'longitude_min': lon_min,'latitude_min': lat_min,'latitude_max': lat_max,'describe': None, 'auth_mode': 'cas', 'motu': motu_server,'block_size': 65536, 'log_level': 30, 'out_dir': Out,'socket_timeout': None,'sync': None,  'proxy_server': proxy_server,'proxy_user': proxy_user,'proxy_pwd': proxy_pass, 'user': cmems_user, 'pwd': cmems_pass,'variable': [v1,v2,v3],'product_id': dataset_id,'service_id': product_id,'user_agent': None,'out_name': outputname, 'outputWritten': 'netcdf','size' : '','console_mode': ''}

                
            hhstartdaily = "12:00:00" #to modify based on your needs
            hhenddaily = "12:00:00"   #to modify based on your needs

            start = dt.datetime(year1,month1,d1,0,0)
            end = dt.datetime(year2,month2,d2,0,0)
            delta = dt.timedelta(days=1)
                
            with open (Out + "/listdate.txt", 'w') as f:
                for result in perdelta(start,end, delta):
                    print (result, file=f)

            for key, value in default_values.items():

                with open (Out + "/listdate.txt") as f:
                        
                    while True:

                        line = f.readline()
                        date_cmd =  line[0:10] +" " +" " + hhstartdaily , line[0:10] +" " + " " + hhenddaily
                        date_min = date_cmd[0]
                        date_max = date_cmd[1]

                        outputname = "CMEMS_" + date_min[0:10] + "_"+ date_max[0:10] + ".nc"

                        default_values = {'date_min': str(date_min),'date_max': str(date_max),'depth_min': '', 'depth_max': '','longitude_max': lon_max,'longitude_min': lon_min,'latitude_min': lat_min,'latitude_max': lat_max,'describe': None, 'auth_mode': 'cas', 'motu': motu_server,'block_size': 65536, 'log_level': 30, 'out_dir': Out,'socket_timeout': None,'sync': None,  'proxy_server': proxy_server,'proxy_user': proxy_user,'proxy_pwd': proxy_pass, 'user': cmems_user, 'pwd': cmems_pass,'variable': [v1,v2,v3],'product_id': dataset_id,'service_id': product_id,'user_agent': None,'out_name': outputname, 'outputWritten': 'netcdf','size' : '','console_mode': ''}

                        print(outputname)

                        _opts = load_options(default_values)
                        mt.motu_api.execute_request(_opts)

                        if not line: 
                            break 

        elif nV == 1 and dV == 1:

            lista = string.split('--')[1:]

            listnew = []

            extract_from_link(lista)

            Us,Pw,Mot,Pr,Ds,Longmin,Longmax,Latmin,Latmax,sd,ed,dmin,dmax,v1 = listnew

            #and then finally I obtain the Parameters in the correct format
            cmems_user = str(Us)
            cmems_pass = str(Pw)

            proxy_user = None
            proxy_pass = None
            proxy_server = None

            #outputdir = str(Outdir)
            outputname = str(fname)
            motu_server = str(Mot)
            product_id = str(Pr)
            dataset_id = str(Ds)

            depth_min = float(dmin)
            depth_max = float(dmax)

            lon_min = float(Longmin)
            lon_max = float(Longmax)
            lat_min = float(Latmin)
            lat_max = float(Latmax)
            
            t1 = sd[1:11]
            t2 = ed[1:11]

            #print (t1)
            #print (t2)
                
            date_min = t1 +" 12:00:00"
            date_max = t2 +" 12:00:00"

            #print(date_min)
            #print (date_max)

            styyyymmdd = []
            endyyyymmdd = []

            listast = t1.split('-')
            listaend = t2.split('-')
                    
            extractstart(listast) 
            extractend(listaend)

            yyyystart,mmstart,dds = styyyymmdd
            yyyyend,mmend,dde = endyyyymmdd

            year1 = int(yyyystart[0])
            month1 = int(mmstart[0])
            d1 = int(dds[0])

            year2 = int(yyyyend[0])
            month2 = int(mmend[0])
            d2 = int(dde[0])

            default_values = {'date_min': str(date_min),'date_max': str(date_max),'depth_min': depth_min, 'depth_max': depth_max,'longitude_max': lon_max,'longitude_min': lon_min,'latitude_min': lat_min,'latitude_max': lat_max,'describe': None, 'auth_mode': 'cas', 'motu': motu_server,'block_size': 65536, 'log_level': 30, 'out_dir': Out,'socket_timeout': None,'sync': None,  'proxy_server': proxy_server,'proxy_user': proxy_user,'proxy_pwd': proxy_pass, 'user': cmems_user, 'pwd': cmems_pass,'variable': [v1],'product_id': dataset_id,'service_id': product_id,'user_agent': None,'out_name': outputname, 'outputWritten': 'netcdf','size' : '','console_mode': ''}

                
            hhstartdaily = "12:00:00" #to modify based on your needs
            hhenddaily = "12:00:00"   #to modify based on your needs

            start = dt.datetime(year1,month1,d1,0,0)
            end = dt.datetime(year2,month2,d2,0,0)
            delta = dt.timedelta(days=1)
                
            with open (Out + "/listdate.txt", 'w') as f:
                for result in perdelta(start,end, delta):
                    print (result, file=f)

            for key, value in default_values.items():

                with open (Out + "/listdate.txt") as f:
                        
                    while True:

                        line = f.readline()
                        date_cmd =  line[0:10] +" " +" " + hhstartdaily , line[0:10] +" " + " " + hhenddaily
                        date_min = date_cmd[0]
                        date_max = date_cmd[1]

                        outputname = "CMEMS_" + date_min[0:10] + "_"+ date_max[0:10] + ".nc"

                        default_values = {'date_min': str(date_min),'date_max': str(date_max),'depth_min': depth_min, 'depth_max': depth_max,'longitude_max': lon_max,'longitude_min': lon_min,'latitude_min': lat_min,'latitude_max': lat_max,'describe': None, 'auth_mode': 'cas', 'motu': motu_server,'block_size': 65536, 'log_level': 30, 'out_dir': Out,'socket_timeout': None,'sync': None,  'proxy_server': proxy_server,'proxy_user': proxy_user,'proxy_pwd': proxy_pass, 'user': cmems_user, 'pwd': cmems_pass,'variable': [v1],'product_id': dataset_id,'service_id': product_id,'user_agent': None,'out_name': outputname, 'outputWritten': 'netcdf','size' : '','console_mode': ''}

                        print(outputname)

                        _opts = load_options(default_values)
                        mt.motu_api.execute_request(_opts)

                        if not line: 
                            break 

        elif nV == 2 and dV == 1:

            lista = string.split('--')[1:]

            listnew = []

            extract_from_link(lista)

            Us,Pw,Mot,Pr,Ds,Longmin,Longmax,Latmin,Latmax,sd,ed,dmin,dmax,v1,v2 = listnew

            #and then finally I obtain the Parameters in the correct format
            cmems_user = str(Us)
            cmems_pass = str(Pw)

            proxy_user = None
            proxy_pass = None
            proxy_server = None

            #outputdir = str(Outdir)
            outputname = str(fname)
            motu_server = str(Mot)
            product_id = str(Pr)
            dataset_id = str(Ds)

            depth_min = float(dmin)
            depth_max = float(dmax)

            lon_min = float(Longmin)
            lon_max = float(Longmax)
            lat_min = float(Latmin)
            lat_max = float(Latmax)
            
            t1 = sd[1:11]
            t2 = ed[1:11]

            #print (t1)
            #print (t2)
                
            date_min = t1 +" 12:00:00"
            date_max = t2 +" 12:00:00"

            #print(date_min)
            #print (date_max)

            styyyymmdd = []
            endyyyymmdd = []

            listast = t1.split('-')
            listaend = t2.split('-')
                    
            extractstart(listast) 
            extractend(listaend)

            yyyystart,mmstart,dds = styyyymmdd
            yyyyend,mmend,dde = endyyyymmdd

            year1 = int(yyyystart[0])
            month1 = int(mmstart[0])
            d1 = int(dds[0])

            year2 = int(yyyyend[0])
            month2 = int(mmend[0])
            d2 = int(dde[0])

            default_values = {'date_min': str(date_min),'date_max': str(date_max),'depth_min': depth_min, 'depth_max': depth_max,'longitude_max': lon_max,'longitude_min': lon_min,'latitude_min': lat_min,'latitude_max': lat_max,'describe': None, 'auth_mode': 'cas', 'motu': motu_server,'block_size': 65536, 'log_level': 30, 'out_dir': Out,'socket_timeout': None,'sync': None,  'proxy_server': proxy_server,'proxy_user': proxy_user,'proxy_pwd': proxy_pass, 'user': cmems_user, 'pwd': cmems_pass,'variable': [v1,v2],'product_id': dataset_id,'service_id': product_id,'user_agent': None,'out_name': outputname, 'outputWritten': 'netcdf','size' : '','console_mode': ''}

                
            hhstartdaily = "12:00:00" #to modify based on your needs
            hhenddaily = "12:00:00"   #to modify based on your needs

            start = dt.datetime(year1,month1,d1,0,0)
            end = dt.datetime(year2,month2,d2,0,0)
            delta = dt.timedelta(days=1)
                
            with open (Out + "/listdate.txt", 'w') as f:
                for result in perdelta(start,end, delta):
                    print (result, file=f)

            for key, value in default_values.items():

                with open (Out + "/listdate.txt") as f:
                        
                    while True:

                        line = f.readline()
                        date_cmd =  line[0:10] +" " +" " + hhstartdaily , line[0:10] +" " + " " + hhenddaily
                        date_min = date_cmd[0]
                        date_max = date_cmd[1]

                        outputname = "CMEMS_" + date_min[0:10] + "_"+ date_max[0:10] + ".nc"

                        default_values = {'date_min': str(date_min),'date_max': str(date_max),'depth_min': depth_min, 'depth_max': depth_max,'longitude_max': lon_max,'longitude_min': lon_min,'latitude_min': lat_min,'latitude_max': lat_max,'describe': None, 'auth_mode': 'cas', 'motu': motu_server,'block_size': 65536, 'log_level': 30, 'out_dir': Out,'socket_timeout': None,'sync': None,  'proxy_server': proxy_server,'proxy_user': proxy_user,'proxy_pwd': proxy_pass, 'user': cmems_user, 'pwd': cmems_pass,'variable': [v1,v2],'product_id': dataset_id,'service_id': product_id,'user_agent': None,'out_name': outputname, 'outputWritten': 'netcdf','size' : '','console_mode': ''}

                        print(outputname)

                        _opts = load_options(default_values)
                        mt.motu_api.execute_request(_opts)

                        if not line: 
                            break 

        elif nV == 3 and dV == 1:

            lista = string.split('--')[1:]

            listnew = []

            extract_from_link(lista)

            Us,Pw,Mot,Pr,Ds,Longmin,Longmax,Latmin,Latmax,sd,ed,dmin,dmax,v1,v2,v3 = listnew

            #and then finally I obtain the Parameters in the correct format
            cmems_user = str(Us)
            cmems_pass = str(Pw)

            proxy_user = None
            proxy_pass = None
            proxy_server = None

            #outputdir = str(Outdir)
            outputname = str(fname)
            motu_server = str(Mot)
            product_id = str(Pr)
            dataset_id = str(Ds)

            depth_min = float(dmin)
            depth_max = float(dmax)

            lon_min = float(Longmin)
            lon_max = float(Longmax)
            lat_min = float(Latmin)
            lat_max = float(Latmax)
            
            t1 = sd[1:11]
            t2 = ed[1:11]

            #print (t1)
            #print (t2)
                
            date_min = t1 +" 12:00:00"
            date_max = t2 +" 12:00:00"

            #print(date_min)
            #print (date_max)

            styyyymmdd = []
            endyyyymmdd = []

            listast = t1.split('-')
            listaend = t2.split('-')
                    
            extractstart(listast) 
            extractend(listaend)

            yyyystart,mmstart,dds = styyyymmdd
            yyyyend,mmend,dde = endyyyymmdd

            year1 = int(yyyystart[0])
            month1 = int(mmstart[0])
            d1 = int(dds[0])

            year2 = int(yyyyend[0])
            month2 = int(mmend[0])
            d2 = int(dde[0])

            default_values = {'date_min': str(date_min),'date_max': str(date_max),'depth_min': depth_min, 'depth_max': depth_max,'longitude_max': lon_max,'longitude_min': lon_min,'latitude_min': lat_min,'latitude_max': lat_max,'describe': None, 'auth_mode': 'cas', 'motu': motu_server,'block_size': 65536, 'log_level': 30, 'out_dir': Out,'socket_timeout': None,'sync': None,  'proxy_server': proxy_server,'proxy_user': proxy_user,'proxy_pwd': proxy_pass, 'user': cmems_user, 'pwd': cmems_pass,'variable': [v1,v2,v3],'product_id': dataset_id,'service_id': product_id,'user_agent': None,'out_name': outputname, 'outputWritten': 'netcdf','size' : '','console_mode': ''}

                
            hhstartdaily = "12:00:00" #to modify based on your needs
            hhenddaily = "12:00:00"   #to modify based on your needs

            start = dt.datetime(year1,month1,d1,0,0)
            end = dt.datetime(year2,month2,d2,0,0)
            delta = dt.timedelta(days=1)
                
            with open (Out + "/listdate.txt", 'w') as f:
                for result in perdelta(start,end, delta):
                    print (result, file=f)

            for key, value in default_values.items():

                with open (Out + "/listdate.txt") as f:
                        
                    while True:

                        line = f.readline()
                        date_cmd =  line[0:10] +" " +" " + hhstartdaily , line[0:10] +" " + " " + hhenddaily
                        date_min = date_cmd[0]
                        date_max = date_cmd[1]

                        outputname = "CMEMS_" + date_min[0:10] + "_"+ date_max[0:10] + ".nc"

                        default_values = {'date_min': str(date_min),'date_max': str(date_max),'depth_min': depth_min, 'depth_max': depth_max,'longitude_max': lon_max,'longitude_min': lon_min,'latitude_min': lat_min,'latitude_max': lat_max,'describe': None, 'auth_mode': 'cas', 'motu': motu_server,'block_size': 65536, 'log_level': 30, 'out_dir': Out,'socket_timeout': None,'sync': None,  'proxy_server': proxy_server,'proxy_user': proxy_user,'proxy_pwd': proxy_pass, 'user': cmems_user, 'pwd': cmems_pass,'variable': [v1,v2,v3],'product_id': dataset_id,'service_id': product_id,'user_agent': None,'out_name': outputname, 'outputWritten': 'netcdf','size' : '','console_mode': ''}

                        print(outputname)

                        _opts = load_options(default_values)
                        mt.motu_api.execute_request(_opts)

                        if not line: 
                            break 

        else:
            print("ERROR: Number of variables not supported. If you need more variables please to contact the author of this script")





            
