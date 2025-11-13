#import necessaire
from .request import request_API
from .traduct import trad
from dotenv import load_dotenv
import os
import json

load_dotenv()

#recup via getenv
API_KEY_NEWS=os.getenv("API_KEY_NEWS")
LONG=os.getenv("LONG")
LAT=os.getenv("LAT")
API_KEY_WEATHER=os.getenv("API_KEY_WEATHER")
API_KEY_CRYPTO=os.getenv("API_KEY_CRYPTO")


URL_NEWS = f"https://newsdata.io/api/1/latest?apikey={API_KEY_NEWS}&language=fr"

URL_WEATHER = f"https://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LONG}&appid={API_KEY_WEATHER}"
     
URL_CRYPTO=f"https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"
     
    

#traitement de la reponse de weather
def treat_response_weather():

    weather_data={}
    weather={}
    try:
        reponse_weather=request_API(URL_WEATHER)
        if isinstance(reponse_weather,dict) and reponse_weather:
            weather_data=reponse_weather['weather'][0]
            weather['meteo']=trad(weather_data['main'])
            return(weather)
        else:
            return({"empty":"sorry"})
    except Exception as e:
        return({"Sorry error ":str(e)})
            

#traitement de la reponse de news
def treat_response_news():

    all_data={}
    datas=[]
    try:
        reponse_news=request_API(URL_NEWS)
        if isinstance(reponse_news,dict) and reponse_news:
            all_data=reponse_news['results']
            for one_data in all_data:
                if isinstance(one_data,dict):
                    data={}
                    data['title']=one_data['title']
                    data['text']=one_data['description']
                    data['image']=one_data['image_url']
                    datas.append(data) 
            return datas
    except Exception as e:
        return({"Sorry error ":str(e)})
    

#traitement de la reponse de cryptos
def treat_response_crypto():

    my_crypto={}

    try:
        response_crypto=request_API(URL_CRYPTO)
        if isinstance(response_crypto,dict):
            for name_crypto,price in response_crypto.items():
                if 'usd' in price:
                    my_crypto[name_crypto]=price['usd']
            return my_crypto
    except Exception as e:
        return({"Sorry error ":str(e)})
    

#recuperation de tt les reponses traitées
def treat_all_url():

    all={}
    try:
        all['crypto']= treat_response_crypto()
        all['weather']=treat_response_weather()
        all['news']=treat_response_news()
        return all
    
    except Exception as e:
        print({"Error":str((e))})
        return {}
    

