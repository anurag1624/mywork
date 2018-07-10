#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 10 16:32:15 2018

@author: siva
"""

from tabula import read_pdf
import pandas as pd
import numpy as np
from kotakfinal import kotak_bank


class Bank:

    def __init__(self, file_path, b, emp_name):
        self.keywords = dict(ATM_WDL="ATW|EAW|NWD|ATM|CASH WDL", FAG="CATER|MART|FOOD|KITCHEN|DAIRY|HOTEL|SHOP|SUPER",
                             ENT="MOVIE|BOOKMYSHOW", TRAVEL="BUS|TRAIN|TICKET",
                             UTILITY="WATER|AIRTEL|VODAFONE|IDEA|DOCOMO", ECOMM="PAYTM|ONE97|AMAZON|FLIPKART|FLIP KART",
                             EMI="EMI|ECS|ACH", CHARGES="CHGS")
        self.file_path = file_path
        self.b = b
        self.emp_name = emp_name

    def hdfc_bank(self):
        print("Entered Bank...")
        df = read_pdf(self.file_path, pages='all')
        df.rename(columns={'Narration': 'Description',
                           'Withdrawal Amt.': 'Debit',
                           'Deposit Amt.': 'Credit',
                           'Closing Balance': 'Balance'}, inplace=True)

        df['Date'] = df['Date'].fillna("null")
        df['Description'] = df['Description'].fillna("null")

        for i in range(1, len(df)):
            if df['Date'].values[i] == 'null':
                df.Description.values[i - 1] = df.Description.values[i - 1] + df.Description.values[i]
                df.Description.values[i] = 'null'

        df = df.replace('null', np.NaN)
        df = df.dropna(subset=["Date"])
        df.reset_index(inplace=True, drop=True)

        df['Balance'] = df['Balance'].fillna("null")

        for j in range(1, len(df)):
            if df['Balance'].values[j] == 'null':
                df.Balance.values[j] = df.Credit.values[j]
                df.Credit.values[j] = np.nan

        df = df.fillna(0)

        df = df.drop(labels=["Chq./Ref.No.", "Value Dt"], axis=1)

        df["Debit"] = df["Debit"].str.replace(",", "")
        df['Debit'] = pd.to_numeric(df.Debit, errors='coerce')
        df["Credit"] = df["Credit"].str.replace(",", "")
        df['Credit'] = pd.to_numeric(df.Credit, errors='coerce')
        df["Balance"] = df["Balance"].str.replace(",", "")
        df['Balance'] = pd.to_numeric(df.Balance, errors='coerce')
        df = df.fillna(0)
        df.Date = pd.to_datetime(df.Date, dayfirst=True)

        for k in range(1, len(df)):
            if df['Debit'].values[k] == 0:
                if df['Balance'].values[k - 1] > df['Balance'].values[k]:
                    df.Debit.values[k] = df.Credit.values[k]
                    df.Credit.values[k] = 0

        # df["Description"] = df["Description"].str.upper()
        df = df.dropna()
        return df

    def yes_bank(self):

        df = read_pdf(self.file_path, pages='all')
        df = df.iloc[1:, :]
        df.reset_index(inplace=True, drop=True)

        df.rename(columns={'Transaction': 'Date'}, inplace=True)
        df['Date'] = df['Date'].fillna("null")
        df['Description'] = df['Description'].fillna("null")

        for i in range(1, len(df)):
            if df['Date'].values[i] == 'null':
                df.Description.values[i - 1] = df.Description.values[i - 1] + ' ' + df.Description.values[i]
                df.Description.values[i] = 'null'

        df = df.replace('null', np.nan)
        df = df.dropna(how='all')
        df = df.dropna(subset=["Balance"])
        df = df[df.Balance != "Balance"]
        df.reset_index(inplace=True, drop=True)
        df["Debit"] = df["Debit"].str.replace(",", "")
        df['Debit'] = pd.to_numeric(df.Debit, errors='coerce')
        df["Credit"] = df["Credit"].str.replace(",", "")
        df['Credit'] = pd.to_numeric(df.Credit, errors='coerce')
        df["Balance"] = df["Balance"].str.replace(",", "")
        df['Balance'] = pd.to_numeric(df.Balance, errors='coerce')
        df.Date = pd.to_datetime(df.Date, dayfirst=True)
        df = df.fillna(0)
        df = df.dropna()

        return df

    def sbi_bank(self):

        df = read_pdf(self.file_path, lattice=True, pages='all')
        df.rename(columns={'Txn Date': 'Date'}, inplace=True)

        df = df.drop(labels=["Ref No./Cheque\rNo.", 'Value\rDate'], axis=1)
        df = df[df.Balance != "Balance"]
        df = df.dropna(subset=["Balance"])
        df.reset_index(inplace=True, drop=True)
        df = df.fillna(0)
        df["Debit"] = df["Debit"].str.replace(",", "")
        df['Debit'] = pd.to_numeric(df.Debit, errors='coerce')
        df["Credit"] = df["Credit"].str.replace(",", "")
        df['Credit'] = pd.to_numeric(df.Credit, errors='coerce')
        df["Balance"] = df["Balance"].str.replace(",", "")
        df['Balance'] = pd.to_numeric(df.Balance, errors='coerce')
        df.Date = pd.to_datetime(df.Date, dayfirst=True)
        df = df.fillna(0)
        df= df.dropna()
        return df

    def icici_bank(self):

        df = read_pdf(self.file_path,
                      pages='all',
                      lattice=True,
                      pandas_options={
                          'warn_bad_lines': False,
                          'error_bad_lines': False})

        df = df.dropna(how='all')
        df = df.drop(labels=["S No.", "heque Number", "Transaction Date"], axis=1)
        df.reset_index(inplace=True, drop=True)

        df.rename(columns={'Value Date': 'Date', 'ransaction Remarks': 'Description',
                           'Withdrawal Amount\r(INR )': 'Debit',
                           'Deposit Amount\r(INR )': 'Credit',
                           'Balance (INR )': 'Balance'}, inplace=True)

        # df["Debit"] = df["Debit"].str.replace(",", "")
        df['Debit'] = pd.to_numeric(df.Debit, errors='coerce')
        # df["Credit"] = df["Credit"].str.replace(",", "")
        df['Credit'] = pd.to_numeric(df.Credit, errors='coerce')
        # df["Balance"] = df["Balance"].str.replace(",", "")
        df['Balance'] = pd.to_numeric(df.Balance, errors='coerce')
        df = df.fillna(0)
        df.Date = pd.to_datetime(df.Date, dayfirst=True)
        df = df.dropna()
        return df

    def axis_bank(self):
        df = read_pdf(self.file_path,
                      pages='all',
                      lattice=True,
                      pandas_options={
                          'warn_bad_lines': False,
                          'error_bad_lines': False})
        df = df.dropna(how='all')
        df.columns = df.iloc[0]
        df = df.drop_duplicates()
        df = df.dropna(subset=["Balance"])
        df = df.iloc[1:, :]
        df.fillna(0, inplace=True)
        df['Debit'] = pd.to_numeric(df.Debit, errors='coerce')
        # df["Credit"]=df["Credit"].str.replace(",","")
        df['Credit'] = pd.to_numeric(df.Credit, errors='coerce')
        # df["Balance"]=df["Balance"].str.replace(",","")
        df['Balance'] = pd.to_numeric(df.Balance, errors='coerce')
        df = df.fillna(0)
        df.rename(columns={'Tran Date': 'Date', 'Particulars': 'Description'}, inplace=True)
        df = df.drop(labels=["Chq No", "Init.\rBr"], axis=1)
        df.Description = df.Description.astype(str)
        df.Date = pd.to_datetime(df.Date, dayfirst=True, errors='coerce')
        df = df.dropna()
        return df

    def std_bank(self):

        df_new = read_pdf(self.file_path,
                          pages='all', multiple_tables=True)

        # --------------------Last row modification-------------------

        df_new[-1] = df_new[-1].iloc[:-1, :]
        df_new[-1] = df_new[-1].dropna(how='all', axis=1)
        df_new[-1].columns = df_new[-1].iloc[0]

        # --------------------Middle rows------------------------------
        for frame in range(1, len(df_new) - 1):
            df_new[frame].columns = df_new[frame].iloc[0]

        for fr in range(1, len(df_new)):
            df_new[fr] = df_new[fr].drop(labels=["Value", "Cheque"], axis=1)
            df_new[fr] = df_new[fr].iloc[2:, :]
            df_new[fr] = df_new[fr].reset_index(drop=True)

        # --------------------------------First row modification-------------
        date_ind = df_new[0][df_new[0][0] == "Date"].index.tolist()[0]
        df_new[0] = df_new[0].iloc[date_ind:, :]
        df_new[0].columns = df_new[0].iloc[0]
        df_new[0] = df_new[0].iloc[2:, :]
        df_new[0].rename(columns={'ValueDescription Cheque': 'Description'}, inplace=True)
        df_new[0] = df_new[0].reset_index(drop=True)

        # ------------------------------Joining all DF's--------------------
        df = pd.concat(df_new, axis=0, join='outer', join_axes=None, ignore_index=False,
                       keys=None, levels=None, names=None, verify_integrity=False,
                       copy=True)

        # -----------------------Final df ------------------------------
        df.rename(columns={'Withdrawal': 'Debit', 'Deposit': 'Credit'}, inplace=True)

        df.Description = df.Description.astype(str)

        def fill_miss(df1):
            df1.fillna("miss", inplace=True)
            df1.reset_index(drop=True, inplace=True)

            try:
                for i in range(0, len(df1)):
                    if df1.Balance.values[i] == 'miss':
                        df1.Description.values[i - 1] = df1.Description.values[i - 1] + df.Description.values[i]
                        df1.Description.values[i] = ''
                        df1 = df1[df1.Description != '']

            except:
                pass

            df1.reset_index(drop=True, inplace=True)
            return df1

        # ---------------------Cleaning Data----------------------
        for iterations in range(0, 10):

            if len(df.Balance.str.contains('miss')) > 0:
                df = fill_miss(df)
            else:
                break

        try:
            for k in range(0, len(df)):
                if df.Date.values[k] == 'miss':
                    df.Date.values[k] = df.Date.values[k - 1]
        except:
            pass

            # ---------------------Final DF Output returned--------------------
        df["Debit"] = df["Debit"].str.replace(",", "")
        df['Debit'] = pd.to_numeric(df.Debit, errors='coerce')
        df["Credit"] = df["Credit"].str.replace(",", "")
        df['Credit'] = pd.to_numeric(df.Credit, errors='coerce')
        df["Balance"] = df["Balance"].str.replace(",", "")
        df['Balance'] = pd.to_numeric(df.Balance, errors='coerce')
        df.Date = pd.to_datetime(df.Date, errors='coerce')
        df = df.fillna(0)
        df = df.dropna()
        return df
    
    def kotak(self):
        df = kotak_bank(self.file_path)
        return df

    def statement(self, df, keywords):

        bank = {}

        # df.Date = pd.to_datetime(df.Date, dayfirst=True)
        df.Description = df.Description.str.upper()

        # Last six months avg salary credit date------Done
        df_sal = df[df.Description.str.contains("SALARY")]              
        try:            
            df_sal = df_sal[df_sal["Credit"]>0] 
            if len(df_sal) >0:
                dates = [t.day for t in df_sal.Date.dt.date]
                bank['AvgSalaryDate'] = int(np.median(dates))
            else:
                emp_name_temp = self.emp_name.upper().split()[0]              
                df_sal = df[df.Description.str.contains(emp_name_temp)]
                if len(df_sal)>0:                    
                    dates = [t.day for t in df_sal.Date.dt.date]
                    bank['AvgSalaryDate'] = int(np.median(dates))
                else:
                    df_sal = df[df.Description.str.contains(emp_name_temp[1:])] 
                    dates = [t.day for t in df_sal.Date.dt.date]
                    bank['AvgSalaryDate'] = int(np.median(dates))                   
        except:
            try:
                bank['AvgSalaryDate'] = np.median(dates)
            except:
                bank['AvgSalaryDate'] = 0

        # average salary credit for last six months-----Done
        try:
            avg_sal = list(df_sal["Credit"])
            bank['AverageSalary'] = np.mean([i for i in avg_sal if i > 0])
        except:
            bank['AverageSalary'] = 0

        # Monthly minimum balance------ Done
        try:
            df["month"] = [t.month for t in df.Date.dt.date]
            df_min_bal = df.groupby(["month"]).min()
            bank["AvgMinBalance"] = df_min_bal["Balance"].mean()
    
            # ----Weekly minimum balance-------- Not yet Done
            df["day"] = [t.day for t in df.Date.dt.date]
            list_months = list(set([t.month for t in df.Date.dt.date]))
            week = {1: [], 2: [], 3: [], 4: []}
            l = []
            for x in range(1, 5):
                for month in range(0, len(list_months)):
                    for a in range(0, len(df)):
    
                        if df["month"].values[a] == list_months[month]:
                            if x == 1:
                                if 0 < df["day"].values[a] < 8:
                                    l.append(df["Balance"].values[a])
                            if x == 2:
                                if 7 < df["day"].values[a] < 15:
                                    l.append(df["Balance"].values[a])
                            if x == 3:
                                if 14 < df["day"].values[a] < 22:
                                    l.append(df["Balance"].values[a])
                            if x == 4:
                                if df["day"].values[a] > 21:
                                    l.append(df["Balance"].values[a])
    
                    try:
                        week[x].append(l[-1])
                    except:
                        week[x].append(0)
            
            

            bank['AvgWeeklyClosingBalance'] = [sum(week[1]) / len(week[1]), sum(week[2]) / len(week[2]),
                                           sum(week[3]) / len(week[3]), sum(week[4]) / len(week[4])]
        except:
            bank['AvgWeeklyClosingBalance'] = [0,0,0,0]
        # print(week)
        # ------ATM withdrawals--------- Done

        try:
            df_atw = df[df.Description.str.contains(keywords["ATM_WDL"])]
            bank["AvgNoOfATMWithdrawals"] = len(df_atw) / float(len(list_months))
        except:
            bank["AvgNoOfATMWithdrawals"] = 0

        # Number of months the statement had submitted----Done
        bank["MonthsSubmitted"] = len(list_months)

        # ----------- Bills----------------------

        # ---------Foods and groceries--------
        try:
            df_fag = df[df.Description.str.contains(keywords["FAG"])]
            bank["AvgFoodSpend"] = df_fag["Debit"].mean()
        except:
            bank["AvgFoodSpend"] = 0

        # --------------Entertainment--------------
        try:            
            df_ent = df[df.Description.str.contains(keywords["ENT"])]
            bank["AvgEntSpend"] = df_ent["Debit"].mean()
        except:
            bank["AvgEntSpend"] = 0

        # -------Travel Bills------------------------
        try:
            df_travel = df[df.Description.str.contains(keywords["TRAVEL"])]
            bank["AvgTravelSpend"] = df_travel["Debit"].mean()
        except:
            bank["AvgTravelSpend"] = 0

        # ----------Utility------------------------
        try:
            df_utility = df[df.Description.str.contains(keywords["UTILITY"])]
            bank['AvgUtilitySpend'] = df_utility["Debit"].mean()
        except:
            bank['AvgUtilitySpend'] = 0

        # ---------E-commerce---------------------
        try:
            df_ecomm = df[df.Description.str.contains(keywords["ECOMM"])]
            bank['AvgEcommSpend'] = df_ecomm["Debit"].mean()
        except:
            bank['AvgEcommSpend'] = 0

        # ------------- EMI -----------------------------
        try:
            df_emi = df[df.Description.str.contains(keywords["EMI"])]
            bank['AvgNoOfEmi/Ecs/ChqBne'] = len(df_emi) / float(len(list_months))
        except:
            bank['AvgNoOfEmi/Ecs/ChqBne'] = 0
        # -------------------Avg credits other than salary--------
        try:
            tot_credits = len(df[df["Credit"] > 0])
            tot_sal = len(df_sal)
            bank['AvgNoOfCreditsOtherThanSalary'] = (tot_credits - tot_sal) / len(list_months)
        except:
            bank['AvgNoOfCreditsOtherThanSalary'] = 0
        # ---------------------Bank Charges------------
        try:            
            df_chgs = df[df.Description.str.contains(keywords["CHARGES"])]
            bank['AvgBankCharges'] = len(df_chgs) / float(len(list_months))
        except:
            bank['AvgBankCharges'] = 0

        # --------------------Avg debits number--------------
        try:
            avg_debits = list(df['Debit'] > 0)
            bank['AvgNoOfDebits'] = len(avg_debits) / float(len(list_months))
        except:
            bank['AvgNoOfDebits'] = 0
        # -------------- Avg Emi amt ------------------
        try:
            df_emi = df[df.Description.str.contains(keywords["EMI"])]
            bank['AvgEmi'] = df_emi["Debit"].mean()
        except:
            bank['AvgEmi'] = 0
        # print(bank)

        # ---------------- Salary Credits--------------------------
        try:
            bank['EmployerName'] = list(df_sal["Description"])[0]
        except:
            bank['EmployerName'] = ""
        
        return bank

    def main(self):

        if self.b == 740:
            df = self.sbi_bank()
        elif self.b == 731:
            df = self.hdfc_bank()
        elif self.b == 730:
            df = self.yes_bank()
        elif self.b == 728:
            df = self.icici_bank()
        elif self.b == 737:
            df = self.axis_bank()
        elif self.b == 1098:
            df = self.std_bank()
        elif self.b == 734:
            df = self.kotak()

        else:
            raise ImportWarning(" Not a valid bank")

        details = self.statement(df, self.keywords)
        for k in details.keys():
            try:
                if np.isnan(details[k]).all():
                    details[k]=0 
            except:
                pass
        return details


'''s = Bank("/home/siva/Desktop/BSA/kotak1.pdf","Kotak Mahindra Bank","INFOLABS PRIVATE LIMITED")    
b1 = s.main()
keywords = dict(ATM_WDL="ATW|EAW|NWD|ATM|CASH WDL", FAG="CATER|MART|FOOD|KITCHEN|DAIRY|HOTEL|SHOP|SUPER",
                             ENT="MOVIE|BOOKMYSHOW", TRAVEL="BUS|TRAIN|TICKET",
                             UTILITY="WATER|AIRTEL|VODAFONE|IDEA|DOCOMO", ECOMM="PAYTM|ONE97|AMAZON|FLIPKART|FLIP KART",
                             EMI="EMI", CHARGES="CHGS")
b2 = s.icici_bank()
print(b1)

data = pd.DataFrame({'Detail': b.keys(),'Value':b.values()})
data = data.fillna(0)
data.to_csv("bank_analysis.csv",index = False)  '''

