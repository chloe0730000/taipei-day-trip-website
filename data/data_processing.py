# -*- coding: utf-8 -*-
"""
# process json file and import to mysql database
1. connect to mysql to create table and schema first
2. dump json data to mysql db
"""



'''

// create database
create database website;
use website;


// create table

create table travel 
(id bigint primary key auto_increment,
transport text ,
name text ,
xpostDate text ,
longitude float ,
REF_WP text ,
avBegin text ,
langinfo text ,
mrt  text ,
SERIAL_NO text ,
RowNumber text ,
CAT1 text , 
category text ,
MEMO_TIME text ,
POI text ,
file text ,
all_images text,
images text,
idpt text ,
latitude float ,
description text ,
_id int ,
avEnd text ,
address text);

// check schema
describe travel;

'''

# dump json data to mysql db

import pymysql
import pandas as pd
import json
import os
from pathlib import Path


# relative path
base_path = os.path.dirname(os.path.abspath(__file__)) 
json_file = base_path+"/taipei-attractions.json"

#json_file = '/Users/chloe/Documents/GitHub/taipei-day-trip-website/data/taipei-attractions.json'
data = pd.read_json(json_file)
data = data["result"]["results"]
print(data)

# convert dictionary to dataframe 
# df = pd.DataFrame.from_dict(data, orient='columns')

# password for ec2 is <blank> local is different
mydb = pymysql.connect(host='localhost',
                       user='root',
                       passwd='',
                       db='website')
cursor = mydb.cursor()


for item in data:
    #print(item["stitle"])
    
    all_images = ["http:"+ i for i in item["file"].split("http:")[1:]]
    
    # get only jpg and png images
    images = ["http:"+ i for i in item["file"].split("http:")[1:] if "jpg" or 'png' in i]
    
    cursor.execute("insert into travel (transport, name, xpostDate, longitude, REF_WP, avBegin, langinfo, mrt, SERIAL_NO, RowNumber, CAT1, category, MEMO_TIME, POI, file, all_images, images, idpt, latitude, description, _id, avEnd, address) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s)",
                  (item["info"], item["stitle"], item["xpostDate"], item["longitude"], item["REF_WP"], item["avBegin"], item["langinfo"], item["MRT"], item["SERIAL_NO"],item["RowNumber"], item["CAT1"], item["CAT2"], item["MEMO_TIME"], item["POI"], item["file"], str(["http:"+ i for i in item["file"].split("http:")[1:]]), str(["http:"+ i for i in item["file"].split("http:")[1:] if "jpg" or 'png' in i]), item["idpt"], item["latitude"], item["xbody"], item["_id"], item["avEnd"], item["address"]))

    
mydb.commit()
cursor.close()

