import pandas as pd
import requests
import json
import elasticsearch.helpers
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

class UNSDapi():

    # https://unstats.un.org/sdgapi/swagger/#!/GeoArea/V1SdgGeoAreaListGet. Consider this link for Indicators code and areacodes .


    def __init__(self, field=None):

        # Choose your field of data  [Indicator, Series, Target], only Indicators available for now.
        
        self.field=field


    def indicator_link(self, indicatorcode=None,areacode=None, timeperiod=None, page=None, pagesize=None):

        '''
        Generates SDG query link
        '''

        #indicatorcode- The code constitutes series inforamtion and Goal - Target hierarchy, if None- all indicators will be included ,dtype= list

        #areacode-  Unique codes associated with each countries, if None- all countries will be included, dtype = list

        #timeperiod  Years from which we want data eg: ["2000","2010"], if None- all years will be included, dtype = list

        #page   Page number to be displayed, if None- shows page 1 (only 1 page is shown at a time), dtype =  integer 

        #pagesize  Number of records requireds per page, (Number of pages in the call will differ when this field is altered), if None- default size is 25, dtype= integer

        '''
        When pulling large datasets, try to give a higher value for page size to avoid high number of total pages.
        '''
        
        apilink=''
        linkprefix='https://unstats.un.org/SDGAPI/v1/sdg/'+self.field+'/Data?'
        self.indicatorcode=indicatorcode
        self.areacode=areacode
        self.timeperiod=timeperiod
        self.page=page
        self.pagesize=pagesize

        if self.indicatorcode==None:
            pass
        else:
            for i in self.indicatorcode:
                apilink=apilink+'indicator='+i+'&'

        if self.areacode==None:
            pass
        else:
            for i in self.areacode:
                apilink=apilink+'areacode='+i+'&'
        if self.timeperiod==None:
            pass
        else:
            for i in self.timeperiod:
                apilink=apilink+'timeperiod='+i+'&'
        if self.page==None:
            pass
        else:
            for i in self.page:
                apilink=apilink+'page='+i+'&'
        if self.pagesize==None:
            pass
        else:
            apilink=apilink+'pageSize='+str(self.pagesize)+'&'
        
            
            
        self.link=linkprefix+apilink[:len(apilink)-1]
        

    def Extract_json(self):

        # Extracts the Json file through SDG query

        if self.link==None:
            print("Pass a valid api URL")
            pass
        else:
            try:
                req=requests.get(self.link)
                self.json_dataset=json.loads(req.text)['data']
            except Exception as f:
                
                print("{} following error occured. Provide valid queries only".format(f))

                
    def sendtorepo(self, ip, port):

        for i in self.json_dataset:
            i['@timestamp']=str(int(i['timePeriodStart']))+'-12-30'+'T'+'00:00:00'+'Z'
        es = Elasticsearch([{'host': ip, 'port': port}], request_timeout=3000)
        doc_type = 'ticker_type'
        self.index_name= 'unsd_check'
        es.indices.create(index= self.index_name, ignore=400)
        docs=self.json_dataset
        out = bulk(es, docs, index=(self.index_name), doc_type=doc_type, raise_on_error=True, request_timeout=3000)


    def return_json_dataset(self):

        #returs the json dataset(1 page only)
        
        return self.json_dataset


    def return_json_size(self):
        self.json_dataset_size=self.json_dataset['totalElements']
        return self.json_dataset_size

    def return_excel(self):
        pd.DataFrame(self.json_dataset).to_excel("South_africa.xlsx")

    
'''
Following query will pull in all indicators of Senegal and Cote d'Ivoire fot the year 2000 and 2001

curl -X DELETE "localhost:9200/unsd_check" 

if __name__=='__main__':
       
    obj=UNSDapi('Indicator')                                         
    obj.indicator_link(areacode=['384','686'])   # areacode is 686 and 384 for Côte d'Ivoire and Senegal respectively.
    obj.Extract_json()    
    print(obj.return_json_size())
    obj.return_excel()
    
'''
# Following query will create Excel sheet for all indicators of all years for both the countries by the name of output.xlsx for the years 2000,2001,2002,2003

if __name__=='__main__':
       
    obj=UNSDapi('Indicator')                                         
    obj.indicator_link(areacode=['170'], pagesize=9230)  # areacode is 686 and 384 for Côte d'Ivoire and Senegal respectively.timeperiod=['2015','2016','2017','2018']
    print(obj.link)
    obj.Extract_json()
    obj.return_excel()
    #obj.sendtorepo('elasticsearch.taiyo.io',9200)
    #print(obj.return_json_size())
    #obj.return_excel()
    

