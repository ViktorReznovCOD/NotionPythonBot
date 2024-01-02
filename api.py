import requests, pprint,json,random
from requests.auth import HTTPBasicAuth
import time
class Api:
    def __init__(self,token):

        self.token = token
        self.urlv1 = "https://api.notion.com/v1/"
        self.headers ={
            'Authorization':'Bearer {}'.format(self.token),
            'Notion-Version':'2022-06-28'
        }
        self.max_retries = 10
        self.seconds_time_between_retries = 3

    def call(self, api_type, endpoint,page_id,method="GET",additional_attributes={},body=None,retry=0):
        # print(body)
        if api_type == "query":
            finalurl = str(self.urlv1 + endpoint + "/" + page_id + "/" + "query")
            print(finalurl)
        else:
            finalurl = str(self.urlv1 + endpoint + "/" + page_id)
            print(finalurl)

        try:
            if method == "POST":
                print('entrei em post')
                response = requests.post(finalurl,headers=self.headers,json=body)
            else:
                response = requests.get(finalurl, headers=self.headers)
            if response.status_code==400:
                print(response.url)
                print(response.text)
                raise Exception("response.status_code == 400")
            elif response.status_code==401:
                print(response.url)
                print(response.text)
                raise Exception("response.status_code == 401")
            return response.json(),response.url,response.text
                
        except Exception as err:
            retry +=1
            if retry < self.max_retries:
                print("Failed due to {}. Waiting for {} seconds before attepting {} to {}".format(err,self.seconds_time_between_retries,retry, self.max_retries))
                time.sleep(self.seconds_time_between_retries)
                return self.call(api_type,endpoint, page_id, method, additional_attributes, body, retry)
            else:
                raise Exception("Maximum number of attempts exceeded",err)

