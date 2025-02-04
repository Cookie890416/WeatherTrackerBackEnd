from pymongo import MongoClient
from bson.objectid import ObjectId
import json  
connect = MongoClient("mongodb://localhost:27017/calculated")
db= connect.calculated
historyData=db.Station_history_data
hotCounter=0
years=[2012,2013,2014,2015,2016,2017,2018,2019,2020]
for j in years:
    print(j)
    station=db.Station_list.find_one({'year':j}).get('datas')
    for k in station:
        target={}
        if(type(k)==dict):
            if(type(db.Station_history_data.find_one({'name':k.get('站名'),'year':j}))==dict):
                target=db.Station_history_data.find_one({'name':k.get('站名'),'year':j}).get('datas')
            else:
                continue
        s=[0,0,0,0,0]
        new_tag=target.copy()
        for i in target:
                #print(i.get('最高氣溫(C)'))
            new_tag.get(i)['dynamicTags']=[]
            if type(target.get(i).get('最高氣溫(C)'))==float:
                if(target.get(i).get('最高氣溫(C)')>=36):
                    new_tag.get(i).get('dynamicTags').append('炎熱')
            if type(target.get(i).get('最低氣溫(C)'))==float:
                if(target.get(i).get('最低氣溫(C)')<=10):
                    if(target.get(i).get('最低氣溫(C)')<=6):
                        new_tag.get(i).get('dynamicTags').append('寒冷(橘燈)')
                    else:
                        new_tag.get(i).get('dynamicTags').append('寒冷(黃燈)')

            if type(target.get(i).get('日最高紫外線指數'))==float:
                if(target.get(i).get('日最高紫外線指數')>=8):
                    new_tag.get(i).get('dynamicTags').append('強紫外線')
        
            if type(target.get(i).get('相對溼度(%)'))==float:
                if(target.get(i).get('相對溼度(%)')>=70):
                    new_tag.get(i).get('dynamicTags').append('潮濕')

            if type(target.get(i).get('最小相對溼度(%)'))==float:
                if(target.get(i).get('最小相對溼度(%)')<=40):
                    new_tag.get(i).get('dynamicTags').append('乾燥')

            if type(target.get(i).get('最大陣風(m/s)'))==float:
                if(target.get(i).get('最大陣風(m/s)')>=10.8):
                    new_tag.get(i).get('dynamicTags').append('強風')

        db.Station_history_data.update_one(
                {"name" : k.get('站名'),'year':j},
                {"$set":{
                "datas":new_tag
                }
                },upsert=True)