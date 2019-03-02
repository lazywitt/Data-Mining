import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
from pandas import ExcelWriter
import urllib.request


'''
#from bs4 import Beautifulsoup
#import requests


Offered fields -

Reference_rate_of_the_interbank_market
Result_of_Treasury_bill_exchange_transactions
Repo_market_benchmark
Treasury_bill_issuance_results
Interbank_money_market
Weighted_average_monthly_rates_of_Treasury_issues  : Needs configuration

'''

market_att={ 'Result_of_Treasury_bill_exchange_transactions':'http://www.bkam.ma/Marches/Principaux-indicateurs/Marche-obligataire/Marche-des-bons-de-tresor/Marche-des-adjudications-des-bons-du-tresor/Resultat-des-operations-d-echange-de-bons-du-tresor',\
             'Reference_rate_of_treasury_bills':'http://www.bkam.ma/Marches/Principaux-indicateurs/Marche-obligataire/Marche-des-bons-de-tresor/Marche-secondaire/Taux-de-reference-des-bons-du-tresor?date=01%2F11%2F2018&block=e1d6b9bbf87f86f8ba53e8518e882982#address-c3367fcefc5f524397748201aee5dab8-e1d6b9bbf87f86f8ba53e8518e882982',\
             'Reference_rate_of_the_interbank_market':'http://www.bkam.ma/Marches/Principaux-indicateurs/Marche-monetaire/Taux-de-reference-du-marche-interbancaire',\
             'Interbank_money_market':'http://www.bkam.ma/Marches/Principaux-indicateurs/Marche-monetaire/Marche-monetaire-interbancaire',\
             'Repo_market_benchmark' : 'http://www.bkam.ma/Marches/Principaux-indicateurs/Marche-monetaire/Taux-de-reference-du-marche-repo',\
             'Treasury_bill_issuance_results':'http://www.bkam.ma/Marches/Principaux-indicateurs/Marche-obligataire/Marche-des-bons-de-tresor/Marche-des-adjudications-des-bons-du-tresor/Resultats-des-emissions-de-bons-du-tresor'}
             #'Weighted_average_monthly_rates_of_Treasury_issues':'http://www.bkam.ma/Marches/Principaux-indicateurs/Marche-obligataire/Marche-des-bons-de-tresor/Marche-des-adjudications-des-bons-du-tresor/Taux-moyens-ponderes-mensuels-des-emissions-du-tresor?startMonth=12&startYear=2010&endMonth=5&endYear=2018&block=f93d86e8efc6f73bf329cf984d12deb5'}




class Morocco_cb:


    def __init__(self, market_attribute='', startdate='',enddate=''):

        self.field= market_attribute
        self.startdate=startdate
        self.enddate=enddate
        url=market_att[self.field]
        print(url)
        self.driver=webdriver.Chrome(executable_path='/Users/tushargupta/Desktop/chromedriver')
        self.driver.implicitly_wait(10)
        self.driver.get(url)


    def get_data(self):

        # columns=str(df.columns).split(';')
      
        el_head=self.driver.find_element_by_tag_name('fieldset')
        
        if self.field=='Reference_rate_of_the_interbank_market':
            try:
                self.col=['Maturities','Bid Rate','Ask Rate']
                self.index=None
                self.skiprow=1
                #self.date=self.startdate
                self.date='05/10/2018'
                element=el_head.find_element_by_tag_name('input')
                element.clear()
                element.send_keys(self.date) 
                element.find_element_by_xpath('//*[@id="address-653bdde8b6fec21285482975d9f99b8d-45e260d56b5e3253e58dec4f20984f6e"]/div[1]/form/fieldset/div/input').click()
                xpath='//*[@id="address-653bdde8b6fec21285482975d9f99b8d-45e260d56b5e3253e58dec4f20984f6e"]/div[2]/a'

                if self.driver.find_element_by_xpath(xpath)==False:
                    print('Respective data is unavailable')
                    sys.exit(0)
                    
                df_html=self.driver.find_element_by_xpath(xpath) #.click()
            except:
                print('Unexpected error')
                sys.exit(0)


                        
        elif self.field=='Repo_market_benchmark':

            try:
                self.col=['Maturities','Weighted Average Rate']
                self.index=None
                self.skiprow=1
                #self.date=self.startdate
                self.date='31/10/2018'
                element=el_head.find_element_by_tag_name('input')
                element.clear()
                element.send_keys(self.date)
                element.find_element_by_xpath('//*[@id="address-44027697aed90221f57ef87f48a4a2c6-bc36c3366156ef245f6944238f06cab2"]/div[1]/form/fieldset/div/input').click()
                xpath='//*[@id="address-44027697aed90221f57ef87f48a4a2c6-bc36c3366156ef245f6944238f06cab2"]/div[2]/a'
            
                
                if self.driver.find_element_by_xpath(xpath)==False:
                    print('Respective data is unavailable')
                    sys.exit(0)

                df_html=self.driver.find_element_by_xpath(xpath) #.click()

            except:
                print('Unexpected exception occurred')
                sys.exit(0)




        elif self.field=='Interbank_money_market':

            try:
                self.index='Dated'
                self.col=['Dated','Weighted Average Rate','Volume JJ','In Progress']
                self.skiprow=2
                
                element=el_head.find_element_by_name('startDate')
                element.clear()
                element.send_keys(self.startdate)
            
                element=el_head.find_element_by_name('endDate')
                element.clear()
                element.send_keys(self.enddate)
            
                el_head.find_element_by_css_selector('#address-d3239ec6d067cd9381f137545720a6c9-ae14ce1a4ee29af53d5645f51bf0e97d > div.mbl > form > fieldset > div > input[type="submit"]').click()
                xpath='//*[@id="address-d3239ec6d067cd9381f137545720a6c9-ae14ce1a4ee29af53d5645f51bf0e97d"]/div[2]/a'
                if self.driver.find_element_by_xpath(xpath)==False:
                    print('Respective data is unavailable')
                    sys.exit(0)
                df_html=self.driver.find_element_by_xpath(xpath) #.click()

            except:
                print('Respective data is unavialable')
                sys.exit(0)


        
        elif self.field=='Result_of_Treasury_bill_exchange_transactions':

            try:
                self.index='Due Date 1'
                self.col=['Settlement Date','Maturities 1','Due Date 1','Nominal Rate 1','Proposed Amount','Amount Retained 1','Maturities 2','Due Date 2','Nominal Rate 2','Min Price','Max Price','Amount Retained 2','PMP']
                self.skiprow=2
                #self.date=self.startdate
                self.date='31/10/2018'
                element=el_head.find_element_by_tag_name('input')
                element.clear()
                element.send_keys(self.date)
                el_head.find_element_by_css_selector('#address-1741d8920cd912afc2b64c4e0821fcfd-1bd6321a86b991af85ebad9b89b4e819 > div.mbl > form > fieldset > div > input[type="submit"]').click()
                #xpath='//*[@id="address-1741d8920cd912afc2b64c4e08e21fcfd-1bd6321a86b991af85ebad9b89b4e819"]/div[2]/a'
                css='#address-1741d8920cd912afc2b64c4e0821fcfd-1bd6321a86b991af85ebad9b89b4e819 > div.block-table > a'
                
                
                if self.driver.find_element_by_css_selector(css)==False:
                    print('Respective data is unavialable')
                    sys.exit(0)

                df_html=self.driver.find_element_by_css_selector(css) #.click()

                
            except:
                print('Respective data is unavaialable')
                sys.exit(0)


        elif self.field=='Treasury_bill_issuance_results':
             

            try:
                self.index=None
                self.col=['Settlement Date','Maturities','Characteristics','Proposed Amount','Rate Min Price','Rate MAx Price','Amount Awarded','Rate or Limit Price','Rate or Weighted Average Price']
                self.skiprow=1
                #self.date=self.startdate
                self.date='05/11/2018'
                element=el_head.find_element_by_tag_name('input')
                element.clear()
                element.send_keys(self.date)
                self.driver.find_element_by_css_selector('#address-c84c024076969f9a943da18ad33b34d5-f8d362b3c0ed59471cdd44431682a04a > div.mbl > form > fieldset > div > input[type="submit"]').click()
                #element.find_element_by_xpath('//*[@id="address-c84c024076969f9a943da18ad33b34d5-f8d362b3c0ed59471cdd44431682a04a"]/div[1]/form/fieldset/div/font/font/input').click()
                #xpath='//*[@id="address-44027697aed90221f57ef87f48a4a2c6-bc36c3366156ef245f6944238f06cab2"]/div[2]/a'
                xpath='//*[@id="address-c84c024076969f9a943da18ad33b34d5-f8d362b3c0ed59471cdd44431682a04a"]/div[2]/a'
                if self.driver.find_element_by_xpath(xpath)==False:
                    print('Respective data is unavailable')
                    sys.exit(0)

                #el_head.find_element_by_css_selector('#address-c84c024076969f9a943da18ad33b34d5-f8d362b3c0ed59471cdd44431682a04a > div.mbl > form > fieldset > div > font > font > input[type="submit"]').click()
                df_html=self.driver.find_element_by_xpath(xpath) #.click()

            except:
                print('Unexpected error')
                sys.exit(0)
                

        elif self.field=='Reference_rate_of_treasury_bills':
            
            try:
                self.index='Due Date'
                self.col=['Due Date','Transaction','Weighted Average Rate','Date Of Value']
                self.skiprow=2
                #self.date=self.startdate
                self.date='01/11/2017'
                element=el_head.find_element_by_tag_name('input')
                element.clear()
                element.send_keys(self.date)
                element.send_keys(Keys.ENTER)
                element.send_keys(Keys.ENTER)
                #self.driver.find_element_by_css_selector('#address-c3367fcefc5f524397748201aee5dab8-e1d6b9bbf87f86f8ba53e8518e882982 > div.mbl > form > fieldset > div > font > font > font > font > input[type="submit"]').click()
                                 
                xpath='//*[@id="address-c3367fcefc5f524397748201aee5dab8-e1d6b9bbf87f86f8ba53e8518e882982"]/div[2]/a'

            
                if self.driver.find_element_by_xpath(xpath)==False:
                    print('Respective data is unavailable')
                    sys.exit(0)
                    
                df_html=self.driver.find_element_by_xpath(xpath) #.click()

            
            except:
                print('Unexpected error')
                sys.exit(0)
                

        elif self.field == 'Weighted_average_monthly_rates_of_Treasury_issues':
            
            self.skiprow=1
            print(self.startdate.split('/')[1])
            count=-1
            for element in el_head.find_elements_by_id('startMonth'):
                element.click()
                print(count)
                if count==self.startdate.split('/')[1]:
                    print('yaye')
                    element.click()
                    break
                count+=1
                print(element.text)
            sys.exit(0)

        
        path=df_html.get_attribute('href')
        filename=self.field+'.csv'
        urllib.request.urlretrieve(path, filename)
        df=pd.read_csv(filename,sep='delimiter', engine='python', skiprows=self.skiprow)
        self.df=pd.DataFrame([str(x).split(';') for x in df.values] ,columns=self.col)

        for col in self.df.columns:
            for i in self.df.index:
                val=self.df[col][i]
                if isinstance(val,str) and val!='':
                    if val[0]=='[' and len(val)>=3:
                        val=val[2:]
                    if val[len(val)-1]==']' and len(val)>=3:
                        val=val[:-2]
                    if val[0]=='"' and len(val)>=3:
                        val=val[1:len(val)-1]
                self.df.set_value(i,col,val)

        
        if self.index==None:
            pass
        else:
            self.df.set_index(self.index, inplace=True)
        print(self.df.head())        

        
    def excel_compile(self):
        self.df.to_excel(writer,self.field)

        
    def close_driver(self):
        self.driver.close()


    def return_df(self):
        return self.df


    def return_excel(self):
        name=self.field+'.xlsx'
        self.df.to_excel(name)
    
    


if __name__=='__main__':
    writer = pd.ExcelWriter('Morocco_final.xlsx')
    for i in market_att:
        obj=Morocco_cb(i,'01/01/2001','31/10/2018')
        obj.get_data()
        obj.close_driver()
        obj.excel_compile()
    writer.save()
'''
if __name__=='__main__':    
    obj=Morocco_cb('Reference_rate_of_treasury_bills','01/01/2001','31/10/2018')
    obj.get_data()
    obj.close_driver()
'''

'''
    http://www.bkam.ma/Marches/Principaux-indicateurs/Marche-obligataire/Marche-des-bons-de-tresor/Marche-des-adjudications-des-bons-du-tresor/Resultat-des-operations-d-echange-de-bons-du-tresor
    http://www.bkam.ma/Marches/Principaux-indicateurs/Marche-obligataire/Marche-des-bons-de-tresor/Marche-des-adjudications-des-bons-du-tresor/Resultats-des-operations-de-rachat-de-bons-du-tresor
    http://www.bkam.ma/Marches/Principaux-indicateurs/Marche-obligataire/Marche-des-bons-de-tresor/Marche-des-adjudications-des-bons-du-tresor/Resultats-des-emissions-de-bons-du-tresor
    http://www.bkam.ma/Marches/Principaux-indicateurs/Marche-obligataire/Marche-des-bons-de-tresor/Marche-des-adjudications-des-bons-du-tresor/Taux-moyens-ponderes-mensuels-des-emissions-du-tresor
'''
