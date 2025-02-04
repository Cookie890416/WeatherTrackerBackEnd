from setup import get_station
import math
db = get_station()
def CWS_min_distance(now_lat,now_lon):
    all_data=db.CWB_station_location.find()
    inf = float('Inf')
    min_d=inf
    SiteName=""
    city=""
    for item in all_data:
        for location in item["data"]:
            for district in item["data"][location]:
                station_lat=item["data"][location][district]["lat"]
                station_lon=item["data"][location][district]["lon"]
                x=float(now_lat)-station_lat
                y=float(now_lon)-station_lon
                distance=math.sqrt(abs(x)**(2)+abs(y)**(2))
                if distance<min_d:
                    min_d=distance
                    city=location
                    SiteName=district
    result=[]
    result.append(city)
    result.append(SiteName)
    return result
def EPA_min_distance(now_lat,now_lon):
    all_data=db.EPA_station_location.find()
    inf = float('Inf')
    min_d=inf
    SiteName=""
    for item in all_data:
        for location in item["data"]:
            station_lat=item["data"][location]["lat"]
            station_lon=item["data"][location]["lon"]
            x=float(now_lat)-station_lat
            y=float(now_lon)-station_lon
            distance=math.sqrt(abs(x)**(2)+abs(y)**(2))
            if distance<min_d:
                min_d=distance
                SiteName=location
    return SiteName
def write_3Days(now_lat,now_lon):
    result=CWS_min_distance(now_lat,now_lon)#傳回測站的地區和縣市
    SiteName=EPA_min_distance(now_lat,now_lon)#傳回測站的名稱
    city=result[0]
    district=result[1]
    print(city+" "+district+" "+SiteName)

    target_SiteName=db.PM2_5.find({"SiteName": SiteName})
    AQI_data=[]
    for i in target_SiteName:
        i.pop("_id")
        for j in range(len(i["forecast"])):
            timeString = i["forecast"][j]["ForecastDate"].strftime("%Y-%m-%d %H:%M:%S") # 轉成字串
            AQI_data.append({timeString:i["forecast"][j]["AQI"]})
    target_city=db.CWB_7Days.find({"city": city})
    UV=[]
    for i in target_city:
        i.pop("_id")
        for j in i["locations"]:
            if j==district:
                for k in range(len(i["locations"][j]["times"])):
                    UV_dict=i["locations"][j]["times"][k]["data"]
                    if "紫外線指數" in UV_dict.keys():
                        timeString = i["locations"][j]["times"][k]["startTime"].strftime("%Y-%m-%d %H:%M:%S") # 轉成字串
                        UV.append({timeString:i["locations"][j]["times"][k]["data"]["紫外線指數"]})
    
    target_city=db.CWB_3Days.find({"city": city})
    rain_12hr=[]
    rain_6hr=[]
    temperature=[]
    humidity=[]
    wind=[]
    for i in target_city:
        i.pop("_id")
        for j in i["locations"]:
            if j==district:
                for k in range(len(i["locations"][j]["times_12HR"])):
                    timeString = i["locations"][j]["times_12HR"][k]["startTime"].strftime("%Y-%m-%d %H:%M:%S") # 轉成字串
                    rain_12hr.append({timeString:i["locations"][j]["times_12HR"][k]["data"]["12小時降雨機率"]})
                for k in range(len(i["locations"][j]["times_6HR"])):
                    timeString = i["locations"][j]["times_6HR"][k]["startTime"].strftime("%Y-%m-%d %H:%M:%S") # 轉成字串
                    rain_6hr.append({timeString:i["locations"][j]["times_6HR"][k]["data"]["6小時降雨機率"]})
                for k in range(len(i["locations"][j]["times_3HR_point"])):
                    timeString = i["locations"][j]["times_3HR_point"][k]["dataTime"].strftime("%Y-%m-%d %H:%M:%S") # 轉成字串
                    temperature.append({timeString:i["locations"][j]["times_3HR_point"][k]["data"]["溫度"]})
                    humidity.append({timeString:i["locations"][j]["times_3HR_point"][k]["data"]["相對濕度"]})
                    wind.append({timeString:i["locations"][j]["times_3HR_point"][k]["data"]["風速"]})
    data_3Days={}
    data_3Days.update({"12小時降雨機率":rain_12hr,"6小時降雨機率":rain_6hr,"溫度":temperature,"相對濕度":humidity,"風速":wind,"AQI":AQI_data,"紫外線":UV})
    # print(data_3Days)
    return data_3Days
def write_3_to_7Days(now_lat,now_lon):
    result=CWS_min_distance(now_lat,now_lon)#傳回測站的地區和縣市
    city=result[0]
    district=result[1]
    print(city+" "+district)

    target_city=db.CWB_7Days.find({"city": city})
    rain_12hr=[]
    temperature=[]
    humidity=[]
    wind=[]
    UV=[]
    for i in target_city:
        i.pop("_id")
        for j in i["locations"]:
            if j==district:
                for k in range(len(i["locations"][j]["times"])):
                    timeString = i["locations"][j]["times"][k]["startTime"].strftime("%Y-%m-%d %H:%M:%S") # 轉成字串
                    rain_12hr.append({timeString:i["locations"][j]["times"][k]["data"]["12小時降雨機率"]})
                    
                    temperature.append({timeString:i["locations"][j]["times"][k]["data"]["平均溫度"]})
                    
                    humidity.append({timeString:i["locations"][j]["times"][k]["data"]["平均相對濕度"]})
                    
                    wind.append({timeString:i["locations"][j]["times"][k]["data"]["最大風速"]})
                    
                    UV_dict=i["locations"][j]["times"][k]["data"]
                    if "紫外線指數" in UV_dict.keys():
                        UV.append({timeString:i["locations"][j]["times"][k]["data"]["紫外線指數"]})
    data_7Days={}
    data_7Days.update({"12小時降雨機率":rain_12hr,"平均溫度":temperature,"平均相對濕度":humidity,"最大風速":wind,"紫外線指數":UV})
    # print(data_7Days)
    return data_7Days