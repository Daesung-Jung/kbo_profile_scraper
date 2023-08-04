# -*- coding: utf-8 -*-
"""
Created on Sun Mar  4 19:49:49 2018

@author: shtnr
"""
from selenium import webdriver
from bs4 import BeautifulSoup
import requests

import numpy as np
import pandas as pd




def profile_crawling(aa,bb):      
    
    #이름, 백넘버, 생일, 포지션, 키몸, 학력, 계약금,연봉, 드래프트,입단년도
    Name=[]
    BackNo=[]
    Status=[]
    NowTeam=[]
    Birthday=[]
    Position=[]
    HeightWeight=[]
    Career=[]
    Payment=[]
    Salary=[]
    Draft=[]
    JoinInfo=[]
    playerid=[]
    
    driver=webdriver.Chrome("C:/Users/shtnr/rapsodo_dashboard-main/assets/chromedriver.exe")
    r=requests.get("https://www.koreabaseball.com/Record/Player/HitterDetail/Basic.aspx?playerId=71564") # 홈페이지 접속
    c=r.content # content(내용) 받아옴
    
    #batter
    for a in range(aa,bb):       
        driver.get("https://www.koreabaseball.com/Record/Player/HitterDetail/Basic.aspx?playerId="+str(a))
        html = driver.page_source
        soup = BeautifulSoup(html,'html.parser')
        tt = soup.select("#contents > div.sub-content > div.player_info > div.player_basic > ul")
        if a%1000==0:
            print(a,"페이지입니다")   
            df=         pd.DataFrame({"Name":Name,
                                    "BackNo":BackNo,
 #                                   "Status":Status,
 #                                   "NowTeam":NowTeam,
                                    "Birthday":Birthday,
                                    "Position":Position,
                                    "HeightWeight":HeightWeight,
                                    "Career":Career,
                                    "Payment":Payment,
                                    "Salary":Salary,
                                    "Draft":Draft,
                                    "JoinInfo":JoinInfo})
            df.to_csv("C:/data/profile_info_.csv")                                                               
        
        for i in tt:
            try:
#                Status.append(soup.select("#contents > h4")[0].text)
#                NowTeam.append(soup.select("#h4Team")[0].text)
                Name.append(i.find(id="cphContents_cphContents_cphContents_playerProfile_lblName").text)
                BackNo.append(str(i.find(id="cphContents_cphContents_cphContents_playerProfile_lblBackNo").text))
                Birthday.append(i.find(id="cphContents_cphContents_cphContents_playerProfile_lblBirthday").text)
                Position.append(i.find(id="cphContents_cphContents_cphContents_playerProfile_lblPosition").text)
                HeightWeight.append(i.find(id="cphContents_cphContents_cphContents_playerProfile_lblHeightWeight").text)
                Career.append(i.find(id="cphContents_cphContents_cphContents_playerProfile_lblCareer").text)
                Payment.append(i.find(id="cphContents_cphContents_cphContents_playerProfile_lblPayment").text)
                Salary.append(i.find(id="cphContents_cphContents_cphContents_playerProfile_lblSalary").text)
                Draft.append(i.find(id="cphContents_cphContents_cphContents_playerProfile_lblDraft").text)
                JoinInfo.append(i.find(id="cphContents_cphContents_cphContents_playerProfile_lblJoinInfo").text)
                playerid.append(a+10000)
            except:
                print(a,"에러")
            
    df.to_csv("d:/diego/data/profile_info_.csv",index='False')  
    
    return df
            
    #pitcher
           

df= profile_crawling(10000,99999)
            

df.index = df.index+10000
df.head()     


df = df[df['Name']!=""]
df.to_csv("d:/diego/data/profile_info_20221107.csv",index='False')  



#batter_info["batter_id"]=batter_info.index+10000

#batter_info2=batter_info[batter_info.Name!=""]
#batter_info2.to_csv("D:/update_data/df2.csv")   



player_info=pd.read_csv("D:/update_data/batter_info2.csv")    
player_info=profile_clean_data(player_info)


df_ = profile_clean_data(df)


def profile_clean_data(df):
    df['batter_id']=df.index
    
    df['PlayerId']=df['batter_id']
    
    df['Born_Year']=df['Birthday'].str[:4]
    df['Born_Month']=df['Birthday'].str[6:8]
    df['Born_Day']=df['Birthday'].str[10:12]
    df['Birthday']=df['Born_Year']+'-'+df['Born_Month']+'-'+df['Born_Day']
    
    df['Height']=df['HeightWeight'].str.split('/').str[0].str.replace('cm','')
    df['Weight']=df['HeightWeight'].str.split('/').str[1].str.replace('kg','')
    
    df['Height']=df['Height'].replace("0",np.nan)
    df['Weight']=df['Weight'].replace("0",np.nan)
    
    del df['HeightWeight']
    
    df['Debut_Year']=df['JoinInfo'].str[:2]
    df['Debut_Team']=df['JoinInfo'].str[2:].str.replace('감독','').str.replace('코치','')
    
    del df['JoinInfo']
    
    df['stands']=df['Position'].str.split('(').str[1].str.split('타').str[0].str[2:]
    df['throws']=df['Position'].str.split('(').str[1].str[:1].str.replace(')','')
    df.loc[(df['Position'].str.split('(').str[1].str[1:2]=='언','throws_under')]='1'
    
    
        
    df['position']=df['Position'].str.split('(').str[0]
    
    del df['Position']
    df['Draft']=df['Draft'].str.replace('자유 선발','자유선발')
    df['Draft']=df['Draft'].str.replace('고졸 신인','고졸신인')
    df['Draft']=df['Draft'].str.replace('순위','위')
    #df['Draft']=df['Draft'].str.replace('위','순위')
    
    df['Draft_Year']=df['Draft'].str.split(' ').str[0]
    df['Draft_Team']=df['Draft'].str.split(' ').str[1]
    
    
    df.loc[(df['Name']=="최희섭",'Draft_Team')]='KIA'
    df.loc[(df['Name']=="송승준",'Draft_Team')]='롯데'
    df.loc[(df['Name']=="채태인",'Draft_Team')]='삼성'
    df.loc[(df['Name']=="김병현",'Draft_Team')]='넥센'
    df.loc[(df['Name']=="류제국",'Draft_Team')]='LG'
    
    #.loc[(df['Position'].str.split('(').str[1].str[1:2]=='언','throws_under')]='1'
    
    df['Draft'].str.split(' ').str[0].unique()
    df['Draft'].str.split(' ').str[1].unique()
    
    
    df['Draft'].str.split(' ').str[2].unique()
    df['Draft'].str.split(' ').str[3].unique()
    df['Draft'].str.split(' ').str[4].unique()
    
    
    
    #뒤에서 부터 해당 순위가 맞으면 다음 열로 가고 
    #또 밀어서 하는 컬럼을 만들자!~
    
    
    df.loc[(df['Draft'].str.split(' ').str[2].str[-1:]=='차','Draft_Type')]=df['Draft'].str.split(' ').str[2]
    df.loc[(df['Draft'].str.split(' ').str[2]=='육성선수','Draft_Type')]=df['Draft'].str.split(' ').str[2]
    df.loc[(df['Draft'].str.split(' ').str[2]=='자유선발','Draft_Type')]=df['Draft'].str.split(' ').str[2]
    df.loc[(df['Draft'].str.split(' ').str[2]=='고졸신인','Draft_Type')]=df['Draft'].str.split(' ').str[2]
    df.loc[(df['Draft'].str.split(' ').str[2]=='특별','Draft_Type')]=df['Draft'].str.split(' ').str[2]
    df.loc[(df['Draft'].str.split(' ').str[2]=='특별지명','Draft_Type')]=df['Draft'].str.split(' ').str[2]
    df.loc[(df['Draft'].str.split(' ').str[2]=='우선지명','Draft_Type')]=df['Draft'].str.split(' ').str[2]
    df.loc[(df['Draft'].str.split(' ').str[2]=='2차우선','Draft_Type')]=df['Draft'].str.split(' ').str[2]
    
    
    
    df.loc[(df['Draft'].str.split(' ').str[2].str[-3:]=="라운드",'Draft_Round')]=df['Draft'].str.split(' ').str[2]
    df.loc[(df['Draft'].str.split(' ').str[3].str[-3:]=='라운드','Draft_Round')]=df['Draft'].str.split(' ').str[3]
    
    df.loc[(df['Draft'].str.split(' ').str[3].str[-1:]=='위','Draft_No')]=df['Draft'].str.split(' ').str[3]
    df.loc[(df['Draft'].str.split(' ').str[4].str[-1:]=='위','Draft_No')]=df['Draft'].str.split(' ').str[4]
    
    
    
    
    df['Career']=df['Career'].str.replace('현대','')
    
    for i in range(0,12):
        df.loc[(df['Career'].str.split('-').str[i].str[-1:]=='초','elemental')]=df['Career'].str.split('-').str[i]
        df.loc[(df['Career'].str.split('-').str[i].str[-1:]=='중','middle')]=df['Career'].str.split('-').str[i]
        df.loc[(df['Career'].str.split('-').str[i].str[-1:]=='고','high')]=df['Career'].str.split('-').str[i]
        df.loc[(df['Career'].str.split('-').str[i].str[-1:]=='대','univ')]=df['Career'].str.split('-').str[i]
        df.loc[(df['Career'].str.split('-').str[i].str[-2:]=='초)','elemental')]=df['Career'].str.split('-').str[i]
        df.loc[(df['Career'].str.split('-').str[i].str[-2:]=='틀)','elemental')]=df['Career'].str.split('-').str[i] 
        df.loc[(df['Career'].str.split('-').str[i].str[-2:]=='중)','middle')]=df['Career'].str.split('-').str[i]
        df.loc[(df['Career'].str.split('-').str[i].str[-2:]=='고)','high')]=df['Career'].str.split('-').str[i]
        df.loc[(df['Career'].str.split('-').str[i].str[-2:]=='대)','univ')]=df['Career'].str.split('-').str[i]
    
    df.loc[:, 'Height'] = pd.to_numeric(df.Height, errors='coerce')
    df.loc[:, 'Weight'] = pd.to_numeric(df.Weight, errors='coerce')
    
    df=df[['PlayerId','Name','BackNo','position','Height','Weight',
                 'stands','throws','throws_under','elemental','middle','high','univ',
                 'Debut_Year','Debut_Team','Draft_Year','Draft_Team','Draft_Type','Draft_Round','Draft_No',
                 'Born_Year','Born_Month','Born_Day','Birthday',
                 'Payment','Salary','Draft','Career']]
    return df
    

df_.to_excel("d:/diego/data/profile_son_20221107.xlsx",index=False)

df_2 = df_[df_.Born_Year.isin(['1999','2000','2001','2002','2002','2003','2004'])]
df_2 = df_2[df_2.PlayerId>30000]



df_2_ = df_[~df_.Born_Year.isin(['1999','2000','2001','2002','2002','2003','2004'])]


df_3_ = df_2_[(df_2_.Draft_Year.isin(['23','22','21']))  & (df_2_.Draft_Type!="자유선발")]

df_3 = df_2[df_2.Draft_Year.isin(['23','22','21'])]
df_4 = df_2[(~df_2.Draft_Year.isin(['23','22','21'])) & df_2.Debut_Year.isin(['23','22','21']) ]

df_3['recent_3yrs']='O'
df_4['notregular_3yrs']='O'

df_4 = df_3.append(df_4)


df_3_.to_excel("d:/diego/data/profile_son_1999_20221107_except.xlsx",index=False)


df_2.to_excel("d:/diego/data/profile_son_1999_20221107.xlsx",index=False)
df_3.to_excel("d:/diego/data/profile_son_3yrs_20221107.xlsx",index=False)

df_4 = pd.read_csv("D:/diego/data/profile_son_4.csv",encoding='cp949')

driver=webdriver.Chrome("d:/diego/data/chromedriver.exe")
import time

df_4 = df_4.reset_index()

del df_4['index']


#선수 팀명 빨기 
for aa in df_3_.index:
    print(aa)    
    driver.get("https://www.koreabaseball.com/Record/Player/HitterDetail/Basic.aspx?playerId="+str(df_3_['PlayerId'][aa]))
    time.sleep(0.01)
    html = driver.page_source
    time.sleep(0.01)
    soup = BeautifulSoup(html,'html.parser')
    time.sleep(0.01)
    tt = soup.select("#h4Team")[0].text
    df_3_.loc[aa,'NowTeam']=tt
    
 

df_4.to_excel("d:/diego/data/profile_son_3yrs_except_20221107.xlsx",index=False)


df_2.Draft_Type.unique()

df_4['NowTeam'].unique()

df_4[(df_4['recent_3yrs']=="O") & (df_4['position']=="투수") & (df_4['NowTeam']=="두산 베어스")]['Name'].to_list()
df_4[(df_4['recent_3yrs']=="O") & (df_4['position']=="포수") & (df_4['NowTeam']=="두산 베어스")]['Name'].to_list()
df_4[(df_4['recent_3yrs']=="O") & (df_4['position']=="내야수") & (df_4['NowTeam']=="두산 베어스")]['Name'].to_list()
df_4[(df_4['recent_3yrs']=="O") & (df_4['position']=="외야수") & (df_4['NowTeam']=="두산 베어스")]['Name'].to_list()

df_4[(df_4['recent_3yrs']=="O") & (df_4['position']=="투수") & (df_4['NowTeam']=="NC 다이노스")]['Name'].to_list()
df_4[(df_4['recent_3yrs']=="O") & (df_4['position']=="포수") & (df_4['NowTeam']=="NC 다이노스")]['Name'].to_list()
df_4[(df_4['recent_3yrs']=="O") & (df_4['position']=="내야수") & (df_4['NowTeam']=="NC 다이노스")]['Name'].to_list()
df_4[(df_4['recent_3yrs']=="O") & (df_4['position']=="외야수") & (df_4['NowTeam']=="NC 다이노스")]['Name'].to_list()

df_4[(df_4['recent_3yrs']=="O") & (df_4['position']=="투수") & (df_4['NowTeam'].isin(["키움 히어로즈","고양 히어로즈"]))]['Name'].to_list()
df_4[(df_4['recent_3yrs']=="O") & (df_4['position']=="포수") & (df_4['NowTeam'].isin(["키움 히어로즈","고양 히어로즈"]))]['Name'].to_list()
df_4[(df_4['recent_3yrs']=="O") & (df_4['position']=="내야수") & (df_4['NowTeam'].isin(["키움 히어로즈","고양 히어로즈"]))]['Name'].to_list()
df_4[(df_4['recent_3yrs']=="O") & (df_4['position']=="외야수") & (df_4['NowTeam'].isin(["키움 히어로즈","고양 히어로즈"]))]['Name'].to_list()


df_4[(df_4['recent_3yrs']=="O") & (df_4['position']=="투수") & (df_4['NowTeam']=="LG 트윈스")]['Name'].to_list()
df_4[(df_4['recent_3yrs']=="O") & (df_4['position']=="포수") & (df_4['NowTeam']=="LG 트윈스")]['Name'].to_list()
df_4[(df_4['recent_3yrs']=="O") & (df_4['position']=="내야수") & (df_4['NowTeam']=="LG 트윈스")]['Name'].to_list()
df_4[(df_4['recent_3yrs']=="O") & (df_4['position']=="외야수") & (df_4['NowTeam']=="LG 트윈스")]['Name'].to_list()

df_4[(df_4['recent_3yrs']=="O") & (df_4['position']=="투수") & (df_4['NowTeam']=="KIA 타이거즈")]['Name'].to_list()
df_4[(df_4['recent_3yrs']=="O") & (df_4['position']=="포수") & (df_4['NowTeam']=="KIA 타이거즈")]['Name'].to_list()
df_4[(df_4['recent_3yrs']=="O") & (df_4['position']=="내야수") & (df_4['NowTeam']=="KIA 타이거즈")]['Name'].to_list()
df_4[(df_4['recent_3yrs']=="O") & (df_4['position']=="외야수") & (df_4['NowTeam']=="KIA 타이거즈")]['Name'].to_list()


df_4[(df_4['recent_3yrs']=="O") & (df_4['position']=="투수") & (df_4['NowTeam']=="SSG 랜더스")]['Name'].to_list()
df_4[(df_4['recent_3yrs']=="O") & (df_4['position']=="포수") & (df_4['NowTeam']=="SSG 랜더스")]['Name'].to_list()
df_4[(df_4['recent_3yrs']=="O") & (df_4['position']=="내야수") & (df_4['NowTeam']=="SSG 랜더스")]['Name'].to_list()
df_4[(df_4['recent_3yrs']=="O") & (df_4['position']=="외야수") & (df_4['NowTeam']=="SSG 랜더스")]['Name'].to_list()

df_4[(df_4['recent_3yrs']=="O") & (df_4['position']=="투수") & (df_4['NowTeam']=="한화 이글스")]['Name'].to_list()
df_4[(df_4['recent_3yrs']=="O") & (df_4['position']=="포수") & (df_4['NowTeam']=="한화 이글스")]['Name'].to_list()
df_4[(df_4['recent_3yrs']=="O") & (df_4['position']=="내야수") & (df_4['NowTeam']=="한화 이글스")]['Name'].to_list()
df_4[(df_4['recent_3yrs']=="O") & (df_4['position']=="외야수") & (df_4['NowTeam']=="한화 이글스")]['Name'].to_list()


df_4[(df_4['recent_3yrs']=="O") & (df_4['position']=="투수") & (df_4['NowTeam']=="롯데 자이언츠")]['Name'].to_list()
df_4[(df_4['recent_3yrs']=="O") & (df_4['position']=="포수") & (df_4['NowTeam']=="롯데 자이언츠")]['Name'].to_list()
df_4[(df_4['recent_3yrs']=="O") & (df_4['position']=="내야수") & (df_4['NowTeam']=="롯데 자이언츠")]['Name'].to_list()
df_4[(df_4['recent_3yrs']=="O") & (df_4['position']=="외야수") & (df_4['NowTeam']=="롯데 자이언츠")]['Name'].to_list()

df_4[(df_4['recent_3yrs']=="O") & (df_4['position']=="투수") & (df_4['NowTeam']=="삼성 라이온즈")]['Name'].to_list()
df_4[(df_4['recent_3yrs']=="O") & (df_4['position']=="포수") & (df_4['NowTeam']=="삼성 라이온즈")]['Name'].to_list()
df_4[(df_4['recent_3yrs']=="O") & (df_4['position']=="내야수") & (df_4['NowTeam']=="삼성 라이온즈")]['Name'].to_list()
df_4[(df_4['recent_3yrs']=="O") & (df_4['position']=="외야수") & (df_4['NowTeam']=="삼성 라이온즈")]['Name'].to_list()



df_4[(df_4['recent_3yrs']=="O") & (df_4['position']=="투수") & (df_4['NowTeam']=="KT 위즈")]['Name'].to_list()
df_4[(df_4['recent_3yrs']=="O") & (df_4['position']=="포수") & (df_4['NowTeam']=="KT 위즈")]['Name'].to_list()
df_4[(df_4['recent_3yrs']=="O") & (df_4['position']=="내야수") & (df_4['NowTeam']=="KT 위즈")]['Name'].to_list()
df_4[(df_4['recent_3yrs']=="O") & (df_4['position']=="외야수") & (df_4['NowTeam']=="KT 위즈")]['Name'].to_list()

df_4[(df_4['recent_3yrs']=="O") & (df_4['position']=="투수") & (df_4['NowTeam']=="상무 ")]['Name'].to_list()
df_4[(df_4['recent_3yrs']=="O") & (df_4['position']=="포수") & (df_4['NowTeam']=="상무 ")]['Name'].to_list()
df_4[(df_4['recent_3yrs']=="O") & (df_4['position']=="내야수") & (df_4['NowTeam']=="상무 ")]['Name'].to_list()
df_4[(df_4['recent_3yrs']=="O") & (df_4['position']=="외야수") & (df_4['NowTeam']=="상무 ")]['Name'].to_list()








df_4[(df_4['notregular_3yrs']=="O") & (df_4['position']=="투수") & (df_4['NowTeam']=="두산 베어스")]['Name'].to_list()
df_4[(df_4['notregular_3yrs']=="O") & (df_4['position']=="포수") & (df_4['NowTeam']=="두산 베어스")]['Name'].to_list()
df_4[(df_4['notregular_3yrs']=="O") & (df_4['position']=="내야수") & (df_4['NowTeam']=="두산 베어스")]['Name'].to_list()
df_4[(df_4['notregular_3yrs']=="O") & (df_4['position']=="외야수") & (df_4['NowTeam']=="두산 베어스")]['Name'].to_list()

df_4[(df_4['notregular_3yrs']=="O") & (df_4['position']=="투수") & (df_4['NowTeam']=="NC 다이노스")]['Name'].to_list()
df_4[(df_4['notregular_3yrs']=="O") & (df_4['position']=="포수") & (df_4['NowTeam']=="NC 다이노스")]['Name'].to_list()
df_4[(df_4['notregular_3yrs']=="O") & (df_4['position']=="내야수") & (df_4['NowTeam']=="NC 다이노스")]['Name'].to_list()
df_4[(df_4['notregular_3yrs']=="O") & (df_4['position']=="외야수") & (df_4['NowTeam']=="NC 다이노스")]['Name'].to_list()

df_4[(df_4['notregular_3yrs']=="O") & (df_4['position']=="투수") & (df_4['NowTeam'].isin(["키움 히어로즈","고양 히어로즈"]))]['Name'].to_list()
df_4[(df_4['notregular_3yrs']=="O") & (df_4['position']=="포수") & (df_4['NowTeam'].isin(["키움 히어로즈","고양 히어로즈"]))]['Name'].to_list()
df_4[(df_4['notregular_3yrs']=="O") & (df_4['position']=="내야수") & (df_4['NowTeam'].isin(["키움 히어로즈","고양 히어로즈"]))]['Name'].to_list()
df_4[(df_4['notregular_3yrs']=="O") & (df_4['position']=="외야수") & (df_4['NowTeam'].isin(["키움 히어로즈","고양 히어로즈"]))]['Name'].to_list()


df_4[(df_4['notregular_3yrs']=="O") & (df_4['position']=="투수") & (df_4['NowTeam']=="LG 트윈스")]['Name'].to_list()
df_4[(df_4['notregular_3yrs']=="O") & (df_4['position']=="포수") & (df_4['NowTeam']=="LG 트윈스")]['Name'].to_list()
df_4[(df_4['notregular_3yrs']=="O") & (df_4['position']=="내야수") & (df_4['NowTeam']=="LG 트윈스")]['Name'].to_list()
df_4[(df_4['notregular_3yrs']=="O") & (df_4['position']=="외야수") & (df_4['NowTeam']=="LG 트윈스")]['Name'].to_list()

df_4[(df_4['notregular_3yrs']=="O") & (df_4['position']=="투수") & (df_4['NowTeam']=="KIA 타이거즈")]['Name'].to_list()
df_4[(df_4['notregular_3yrs']=="O") & (df_4['position']=="포수") & (df_4['NowTeam']=="KIA 타이거즈")]['Name'].to_list()
df_4[(df_4['notregular_3yrs']=="O") & (df_4['position']=="내야수") & (df_4['NowTeam']=="KIA 타이거즈")]['Name'].to_list()
df_4[(df_4['notregular_3yrs']=="O") & (df_4['position']=="외야수") & (df_4['NowTeam']=="KIA 타이거즈")]['Name'].to_list()


df_4[(df_4['notregular_3yrs']=="O") & (df_4['position']=="투수") & (df_4['NowTeam']=="SSG 랜더스")]['Name'].to_list()
df_4[(df_4['notregular_3yrs']=="O") & (df_4['position']=="포수") & (df_4['NowTeam']=="SSG 랜더스")]['Name'].to_list()
df_4[(df_4['notregular_3yrs']=="O") & (df_4['position']=="내야수") & (df_4['NowTeam']=="SSG 랜더스")]['Name'].to_list()
df_4[(df_4['notregular_3yrs']=="O") & (df_4['position']=="외야수") & (df_4['NowTeam']=="SSG 랜더스")]['Name'].to_list()

df_4[(df_4['notregular_3yrs']=="O") & (df_4['position']=="투수") & (df_4['NowTeam']=="한화 이글스")]['Name'].to_list()
df_4[(df_4['notregular_3yrs']=="O") & (df_4['position']=="포수") & (df_4['NowTeam']=="한화 이글스")]['Name'].to_list()
df_4[(df_4['notregular_3yrs']=="O") & (df_4['position']=="내야수") & (df_4['NowTeam']=="한화 이글스")]['Name'].to_list()
df_4[(df_4['notregular_3yrs']=="O") & (df_4['position']=="외야수") & (df_4['NowTeam']=="한화 이글스")]['Name'].to_list()


df_4[(df_4['notregular_3yrs']=="O") & (df_4['position']=="투수") & (df_4['NowTeam']=="롯데 자이언츠")]['Name'].to_list()
df_4[(df_4['notregular_3yrs']=="O") & (df_4['position']=="포수") & (df_4['NowTeam']=="롯데 자이언츠")]['Name'].to_list()
df_4[(df_4['notregular_3yrs']=="O") & (df_4['position']=="내야수") & (df_4['NowTeam']=="롯데 자이언츠")]['Name'].to_list()
df_4[(df_4['notregular_3yrs']=="O") & (df_4['position']=="외야수") & (df_4['NowTeam']=="롯데 자이언츠")]['Name'].to_list()

df_4[(df_4['notregular_3yrs']=="O") & (df_4['position']=="투수") & (df_4['NowTeam']=="삼성 라이온즈")]['Name'].to_list()
df_4[(df_4['notregular_3yrs']=="O") & (df_4['position']=="포수") & (df_4['NowTeam']=="삼성 라이온즈")]['Name'].to_list()
df_4[(df_4['notregular_3yrs']=="O") & (df_4['position']=="내야수") & (df_4['NowTeam']=="삼성 라이온즈")]['Name'].to_list()
df_4[(df_4['notregular_3yrs']=="O") & (df_4['position']=="외야수") & (df_4['NowTeam']=="삼성 라이온즈")]['Name'].to_list()



df_4[(df_4['notregular_3yrs']=="O") & (df_4['position']=="투수") & (df_4['NowTeam']=="KT 위즈")]['Name'].to_list()
df_4[(df_4['notregular_3yrs']=="O") & (df_4['position']=="포수") & (df_4['NowTeam']=="KT 위즈")]['Name'].to_list()
df_4[(df_4['notregular_3yrs']=="O") & (df_4['position']=="내야수") & (df_4['NowTeam']=="KT 위즈")]['Name'].to_list()
df_4[(df_4['notregular_3yrs']=="O") & (df_4['position']=="외야수") & (df_4['NowTeam']=="KT 위즈")]['Name'].to_list()

df_4[(df_4['notregular_3yrs']=="O") & (df_4['position']=="투수") & (df_4['NowTeam']=="상무 ")]['Name'].to_list()
df_4[(df_4['notregular_3yrs']=="O") & (df_4['position']=="포수") & (df_4['NowTeam']=="상무 ")]['Name'].to_list()
df_4[(df_4['notregular_3yrs']=="O") & (df_4['position']=="내야수") & (df_4['NowTeam']=="상무 ")]['Name'].to_list()
df_4[(df_4['notregular_3yrs']=="O") & (df_4['position']=="외야수") & (df_4['NowTeam']=="상무 ")]['Name'].to_list()






df_4['notregular_3yrs']=="O"





df_2['ID']= df_2['Name']+df_2['Birthday']
df_3['ID']= df_3['Name']+df_3['Birthday']
df_3=df_3[df_3.Draft_Type!="자유선발"]
df_2= df_2[df_2.Draft_Type.notnull()]

df_4['ID']=df_4['투수']+df_4['생년월일']
df_fileter_1 = df_2[df_2['ID'].isin(df_4['ID'])]
df_fileter_2 = df_3[df_3['ID'].isin(df_4['ID'])]


df_fileter_1.to_excel("d:/diego/data/profile_son_1999_20220819_.xlsx",index=False)
df_fileter_2.to_excel("d:/diego/data/profile_son_3yrs_20220819_.xlsx",index=False)

    
#그외 6개 항목 조건 시 Draft_Type으로 때려 박는 걸 




#연봉 및 계약금은 달러와 원화가 있기에 나중에 변환해서 쓰길 권장
#df['Salary']=batter_info['Salary'].str.replace('만원','')
#batter_info['Salary']=batter_info['Salary'].str.replace('달러','')



####호주 



https://statsapi.mlb.com/api/v1/teams/4064/roster?hydrate=person&language=en&season=2022&rosterType=allTime



