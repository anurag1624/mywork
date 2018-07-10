#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 11 12:11:40 2018

@author: siva
"""

import pandas as pd
# import numpy as np

def kotak_bank(file_path):
    try:
        from tabula import read_pdf
        df = read_pdf(file_path,
                               pages='all',pandas_options={ 'header' : None})
        
        df = df.fillna("miss")
        
        for i in range(0,len(df)):
            if df[5].values[i] == "miss":
                df[5].values[i] = df[4].values[i]
                df[4].values[i] = df[3].values[i]
                
        df.columns = ['Date','Description', 'R1','R2','Debit','Balance']  
        df = df.iloc[3:,:]  
        df.reset_index(drop=True,inplace =True)  
        def fill_miss(df):
            try:
                for i in range(0,len(df)):
                     if df.Balance.values[i]=='miss':
                        df.Description.values[i-1] = df.Description.values[i-1] +  df.Description.values[i]
                        df.Description.values[i] = ''
                        df= df[df.Description !=''] 
                            
            except:
                pass
            
            df.reset_index(drop=True,inplace =True)  
            return df   
        
        df = fill_miss(df)
        df = fill_miss(df)
        df.Balance = df.Balance.astype(str)
        df = df[df.Balance!= "miss"]
        df.reset_index(drop=True,inplace=True)
        df["Credit"] = '0'
        df.Debit = df.Debit.astype(str)
        for cre in range(0,len(df)):
            if 'Cr' in df.Debit.values[cre]:
                #print(1)
                temp = df.Debit.values[cre]
                #print(temp)
                df.Credit.values[cre] = temp
                df.Debit.values[cre] = 0
        
        df.Balance = df.Balance.str.replace('(Cr)','')
        df.Balance = df.Balance.str.replace('(','')
        df.Balance = df.Balance.str.replace(')','')
        df.Balance = df.Balance.str.replace(',','')
        df.Debit = df.Debit.str.replace('Dr','')
        df.Debit = df.Debit.str.replace('(','')
        df.Debit = df.Debit.str.replace(')','')
        df.Debit = df.Debit.str.replace(',','')
        df.Credit = df.Credit.str.replace('(Cr)','')
        df.Credit = df.Credit.str.replace('(','')
        df.Credit = df.Credit.str.replace(')','')
        df.Credit = df.Credit.str.replace(',','')
        
        
        df.Date = pd.to_datetime(df.Date, dayfirst =True, errors = 'coerce')
        df = df.dropna(subset = ["Date"])
        df = df.drop(labels= ["R1","R2"],axis=1)
        
        df.reset_index(drop=True,inplace=True)
        df['Debit'] = pd.to_numeric(df.Debit, errors='coerce')
        #df["Credit"]=df["Credit"].str.replace(",","")
        df['Credit'] = pd.to_numeric(df.Credit, errors='coerce')
        #df["Balance"]=df["Balance"].str.replace(",","")
        df['Balance'] = pd.to_numeric(df.Balance, errors='coerce')
        df = df.fillna(0)
        df.Description = df.Description.astype(str)
        return df
    except ValueError:
        from tika import parser
        parsed_file = parser.from_file(file_path)
        parsed_content = parsed_file['content']
        parsed_content = parsed_content.split('\n')
        initial_list = []
        for content in parsed_content:
            if content != '':
                initial_list.append(content)
        final_list = []
        for content_1 in range(0, len(initial_list)):
            list_content = initial_list[content_1].split()
            final_list.append(list_content)
        
        dft = pd.DataFrame({'d': final_list})
        dft.d = dft.d.astype(str)
        dft = dft[dft.d.str.contains('CR')]
        dft.reset_index(drop= True,inplace = True)
        #df.d = df.d.str.replace('/')
        dates = dft.d.str.extract('(\d{2}/\d{2}\/\d{4})', expand = False)
        debits = dft.d.str.extract('(R\d+.\d+/\d{2}\/\d{4})', expand = False)
        debits1 = dft.d.str.extract('(R\d+,\d+.\d+/\d{2}\/\d{4})', expand = False)
        debits = debits.str.replace('(\d{2}/\d{2}\/\d{4})','')
        debits = debits.str.replace('R','')
        debits1 = debits1.str.replace('(\d{2}/\d{2}\/\d{4})','')
        debits1 = debits1.str.replace('R','')
        df_b = dft.d.str.replace('(R\d+,\d+.\d+/\d{2}\/\d{4})','')
        df_b = df_b.str.replace('(R\d+.\d+/\d{2}\/\d{4})','')
        Balance1 = df_b.str.extract('(CR\d+.\d{2})', expand = False)
        Balance2 = df_b.str.extract('(CR\d+,\d+.\d{2})', expand = False)
        Balance1 = Balance1.str.replace('CR','')
        Balance2 = Balance2.str.replace('CR','')
        
        df2 = pd.DataFrame({'d': final_list})
        df2.d = df2.d.astype(str)
        df2 = df2[df2.d.str.contains('CR')]
        df1 = pd.DataFrame({'d': final_list})
        df1.d = df1.d.astype(str)
        indices = df2.index.tolist()
        f_indices=[]
        for ind in range(0,len(df2)):
            if len(df2.d.values[ind].split())>3:
                f_indices.append(ind)
                
        chq_ind = df1[df1.d.str.contains('Chq')].index[0]
        fl = []
        app_0 = ''
        for fl_0 in range(chq_ind+1,indices[0]):
            app_0 = app_0 + df1.d.values[fl_0]
        fl.append(app_0)
        
        for i in range(1,len(indices)):
            app = ''
            for k in range(indices[i-1]+1, indices[i]):
                app = app + df1.d.values[k]
            fl.append(app)
        
        for index in f_indices:
            fl[index] = dft.d.values[index]+ fl[index]
        
        
        df_final = pd.DataFrame({'Date':dates, 'Debit': debits, 'Credit':'0',
                                 'Debit2': debits1,'Balance':Balance1,'B2':Balance2,
                                 'Description': fl})
        
        df_final = df_final.fillna("miss")
        df_final['Date'] = pd.to_datetime(df_final['Date'],dayfirst = True,errors = 'coerce')
        df_final = df_final.sort_values(by='Date')
        df_final.reset_index(drop=True, inplace = True)
        for bal in range(0,len(df_final)):
            if df_final.B2.values[bal] != "miss":
                df_final.Balance.values[bal] = df_final.B2.values[bal] 
        
        for deb in range(0,len(df_final)):
            if df_final.Debit.values[deb] == "miss":
                df_final.Debit.values[deb] = df_final.Debit2.values[deb] 
        
        
        df_final =  df_final.drop(labels= ["Debit2","B2"],axis=1)
        df_final['Debit'] = df_final['Debit'].str.replace(',','')
        df_final['Debit'] = pd.to_numeric(df_final['Debit'],errors = 'coerce')
        df_final['Balance'] = df_final['Balance'].str.replace(',','')
        df_final['Balance'] = pd.to_numeric(df_final['Balance'],errors = 'coerce')
        
        df_final = df_final.dropna()
        
        for cre in range(1,len(df_final)):
            if df_final.Balance.values[cre-1] != df_final.Balance.values[cre] + df_final.Debit.values[cre]:
                df_final.Credit.values[cre] = df_final.Debit.values[cre]
                df_final.Debit.values[cre] = 0
            
        df_final['Credit'] = pd.to_numeric(df_final['Credit'],errors = 'coerce')
        df_final.fillna(0,inplace=True)
        return df_final
    
# details1 = kotak_bank("/home/siva/Desktop/BSA/kotak1.pdf")