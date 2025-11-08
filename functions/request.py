import requests


def request_API(url):

    try:
        reponse_url=requests.get(url)

        if reponse_url.status_code==200:
            return(reponse_url.json())
        else:
            print(reponse_url.status_code)
            return{}
        
    except Exception as e:
        return ({"Error":f"Error {e} during the process"})
    

# def reqest_URL(list_api):
    
#     try:
#         request_list=[]
#         if isinstance(list_api,list) and list_api:
#             for one_api in list_api:
#                 answer_api=request_API(one_api)
#                 request_list.append(answer_api)
#         return request_list
#     except Exception as e:
#         return ({"Error":f"Error {e} during the process"})



        