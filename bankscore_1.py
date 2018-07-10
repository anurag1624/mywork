#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri May 18 17:49:53 2018

@author: siva
"""

#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue May  8 11:22:35 2018

@author: siva
"""

import pandas as pd
import math
from datetime import datetime

score = pd.read_pickle('score_pkl')


class BankScore:

    def __init__(self, b_res, basic_res, ps_res, salary, sal_date, emp_name, an_in):
        
        self.salary = salary
        self.sal_date = sal_date
        self.b_res = b_res
        self.basic_res = basic_res
        self.ps_res = ps_res
        self.emp_name = emp_name
        self.an_in = an_in
    
    def bank_score(self):
        b_res = self.b_res
        b_list = []
        # -----------------------------Avg Salary--------------------------------
        ind_sal = score[(score['Domain'] == 'Financial') & (score['Category'] == 'Salary Avg')].index.tolist()
        sal = self.salary
        for sal_i in ind_sal[:-1]:
            min_sal = ((100+score["Min Range"].values[sal_i])/100)*sal
            max_sal = ((100+score["Max Range"].values[sal_i])/100)*sal
            if max_sal > b_res["AverageSalary"] > min_sal:
                b_list.append(score["Score"].values[sal_i])
                break
        else:
            b_list.append(score["Score"].values[ind_sal[-1]])
            
        # ---------------------------Avg minimum balance ----------------------------
        ind_bal = score[(score['Domain'] == 'Financial') & (score['Category'] == 'Avg. Balance')].index.tolist()
        for bal_i in ind_bal:
            min_sal = ((score["Min Range"].values[bal_i])/100)*sal
            if b_res["AvgMinBalance"] >= min_sal:
                b_list.append(score["Score"].values[bal_i])
                break
        else:
            b_list.append(score["Score"].values[ind_bal[-1]])
        # ----------------------------AvgNoEmi ----------------------------------
        ind_emi = score[(score['Domain'] == 'Financial') & (score['Category'] == 'EMI/ECS/Bounce')].index.tolist()
        for emi_i in ind_emi:
            if b_res["AvgNoOfEmi/Ecs/ChqBne"] >= score["Min Range"].values[emi_i]:
                b_list.append(score["Score"].values[emi_i])
                break
        else:
            b_list.append(score["Score"].values[ind_emi[-1]])
        # ------------------------------Bank Charges------------------------------
        ind_chg = score[(score['Domain'] == 'Financial') & (score['Category'] == 'Bank Charges')].index.tolist() 
        for chg_i in ind_chg:
            if b_res["AvgBankCharges"] >= score["Min Range"].values[chg_i]:
                b_list.append(score["Score"].values[chg_i])
                break
        else:
            b_list.append(score["Score"].values[ind_chg[-1]])
    
        # -----------------------------Avg closing balance-------------------------
        ind_clo = score[(score['Domain'] == 'Financial') & (score['Category'] == 'Closing Bal')].index.tolist()
        for clo_i in range(0,4):
            wd = int(score["Subcategory"].values[ind_clo[clo_i]])
            clo_ran = score["Min Range"].values[ind_clo[clo_i]]/100
            if b_res["AvgWeeklyClosingBalance"][wd-1] <= sal * clo_ran:
                b_list.append(score["Score"].values[ind_clo[clo_i]])
            else:
                b_list.append(0)
    
        # ---------------------Avg number of debits------------------
        ind_deb = score[(score['Domain'] == 'Financial') & (score['Category'] == 'Avg. Debits')].index.tolist()
        for deb_i in ind_deb[:-1]:
            if b_res["AvgNoOfDebits"] <= score["Max Range"].values[deb_i]:
                b_list.append( score["Score"].values[deb_i])
                break
        else:
            b_list.append( score["Score"].values[ind_deb[-1]])
    
        # ----------------------------Avg Atm Withdrawals----------------------
        ind_wdl = score[(score['Domain'] == 'Financial') & (score['Category'] == 'ATM Withdrawals')].index.tolist()
        for wdl_i in ind_wdl[:-1]:
            if b_res["AvgNoOfATMWithdrawals"] <= score["Max Range"].values[wdl_i]:
                b_list.append( score["Score"].values[wdl_i])
                break
        else:
            b_list.append( score["Score"].values[ind_wdl[-1]])
         
        # -----------------------------Avg Emi Amount----------------------------
        ind_emi_amt = score[(score['Domain'] == 'Financial') & (score['Category'] == 'Avg. EMI')].index.tolist()
        for emi_amt_i in ind_emi_amt:   
            if b_res["AvgEmi"] >= sal*(score["Min Range"].values[emi_amt_i])/100:
                b_list.append(score["Score"].values[emi_amt_i])
                break
        else:
            b_list.append(0)
        
        # --------------------------Total Credits ex-salary------------------
        ind_crco = score[(score['Domain'] == 'Financial') & (score['Category'] == 'Credit Count')].index.tolist()
        for cr_i in ind_crco[:-1]:
            if b_res["AvgNoOfCreditsOtherThanSalary"] <= score["Max Range"].values[cr_i]:
                b_list.append( score["Score"].values[cr_i])
                break
        else:
            b_list.append( score["Score"].values[ind_crco[-1]])
            
        # ----------------------------Salary date--------------------------------
        sal_date = str(self.sal_date)
        date_sal = int(sal_date[0:2])
        list_days = range(1, 32)
        ind_date_sal = date_sal - 1
        indx = list_days[ind_date_sal] - 3
        indy = list_days[ind_date_sal] - 5
        try:
            ld3 = [list_days[i] for i in range(indx - 1, ind_date_sal + 4)]
        except IndexError:
            res_val_3 = ind_date_sal + 4 - 31
            ld3 = [list_days[x] for x in range(indx - 1, 31)]
            ld_temp_3 = [list_days[t] for t in range(0, res_val_3)]
            ld3 = ld3 + ld_temp_3
        try:
            ld5 = [list_days[j] for j in range(indy - 1, ind_date_sal + 6)]
        except IndexError:
            res_val = list_days[ind_date_sal] + 5 - 31
            ld5 = [list_days[y] for y in range(indy - 1, 31)]
            ld_temp = [list_days[t] for t in range(0, res_val)]
            ld5 = ld5 + ld_temp
        ind_asd = score[(score['Domain'] == 'Financial') & (score['Category'] == 'Salary Date')].index.tolist()
        if b_res["AvgSalaryDate"] in ld3:
            b_list.append(score["Score"].values[ind_asd[0]])
        elif b_res["AvgSalaryDate"] in ld5:
            b_list.append(score["Score"].values[ind_asd[1]])
        else:
            b_list.append(score["Score"].values[ind_asd[2]])
                
        # -------------------- Salary Neft/Cash-----------------------------------
        ind_mod = score[(score['Domain'] == 'Financial') & (score['Category'] == 'Salary Mode')].index.tolist()
        if math.isnan(b_res["AverageSalary"]):
            b_list.append(score["Score"].values[ind_mod[0]])
        else:
            b_list.append(score["Score"].values[ind_mod[1]])
        # ------------------- Spending Patterns -------------------------------
        spend_dict = {"Entertainment":"AvgEntSpend","Utility Bills":"AvgUtilitySpend", 
                         "Travel Tickets":"AvgTravelSpend", "Food/Grocery":"AvgFoodSpend",
                         "Ecommerce":"AvgEcommSpend"}
        
        for sp_key in spend_dict.keys():
            
            ind_sp = score[(score['Domain'] == 'Financial') & (score['Category'] == 'Spending Pattern') &
                           (score['Subcategory'] == str(sp_key))].index.tolist()
            
            for sp_i in ind_sp:
               
                if score["Min Range"].values[sp_i] == 'Null':
                 
                    if b_res[spend_dict[sp_key]] < sal* (score["Max Range"].values[sp_i]/100):
                        b_list.append(score["Score"].values[sp_i])
                        break
                else:
                    if b_res[spend_dict[sp_key]] > sal* (score["Min Range"].values[sp_i]/100):
                        b_list.append(score["Score"].values[sp_i])
                        break
                    else:
                        b_list.append(0)
                        
        return sum(b_list)
    
    def bank_details(self):
    
        bb_res = self.basic_res    
        bb_list = []
    
        # ---------------------------Document -------------------------------------
        if bb_res["Document"] == 'Matched':
            bb_list.append(score[(score['Domain'] == 'Financial') & (score['Subcategory'] == 'Genuine')].Score.values[0])
        elif bb_res["Document"] == "Null":
            bb_list.append(score[(score['Domain'] == 'Financial') & (score['Subcategory'] == 'Inconclusive')].Score.values[0])
        else:
            bb_list.append(score[(score['Domain'] == 'Financial') & (score['Subcategory'] == 'Fake')].Score.values[0])
    
        # --------------------------Account number-----------------------------------------
        if bb_res["AccountNumber"] == 'Matched':
            bb_list.append(
                score[(score['Domain'] == 'Financial') & (score['Category'] == 'Account Number') &
                     (score['Subcategory'] == "Matched")  ].Score.values[0])
        else:
            bb_list.append(
                    score[(score['Domain'] == 'Financial') & (score['Category'] == 'Account Number') &
                     (score['Subcategory'] == "Mismatched")  ].Score.values[0])
        # -------------------------------UserAddress-----------------------------------------
        if bb_res["UserAddress"] == 'Matched':
            bb_list.append(score[(score['Domain'] == 'Financial') & (score['Category'] == 'User Address') &
                                 (score['Subcategory'] == "Matched")].Score.values[0])
        elif bb_res["UserAddress"] == 'Null':
            bb_list.append(score[(score['Domain'] == 'Financial') & (score['Category'] == 'User Address') &
                                 (score['Subcategory'] == "Null")].Score.values[0])
        else:
            bb_list.append(score[(score['Domain'] == 'Financial') & (score['Category'] == 'User Address') &
                                 (score['Subcategory'] == "Mismatched")].Score.values[0])
    
        # -------------------Bank Branch ------------------------
        if bb_res["BankBranchName"] == 'Matched':
            bb_list.append(score[(score['Domain'] == 'Financial') & (score['Category'] == 'Bank Branch') &
                                 (score['Subcategory'] == "Matched")].Score.values[0])
        elif bb_res["Document"] == "Null":
            bb_list.append(score[(score['Domain'] == 'Financial') & (score['Category'] == 'Bank Branch') &
                                (score['Subcategory'] == "Null") ].Score.values[0])
        else:
            bb_list.append(score[(score['Domain'] == 'Financial') & (score['Category'] == 'Bank Branch') &
                                 (score['Subcategory'] == "Mismatched") ].Score.values[0])
    
        # ----------------------------Statement period ----------------------------------
        now = datetime.now().date()
        date_now = pd.to_datetime(now, dayfirst=True)
        date_in_bs = pd.to_datetime(bb_res["DateOfSubmission"], dayfirst=True)
        days_diff = (date_now - date_in_bs ).days
        if days_diff <= 2 and self.b_res['MonthsSubmitted'] >= 6:
            bb_list.append(score[(score['Domain'] == 'Financial') & (score['Category'] == 'Statements') &
                                (score['Subcategory'] == "Yes")  ].Score.values[0])
        else:
            bb_list.append(score[(score['Domain'] == 'Financial') & (score['Category'] == 'Statements') &
                                (score['Subcategory'] == "No")].Score.values[0])
    
        # --------------------------Employer Name -------------------------
        if bb_res["SalaryCredits"] == "Matched" :
            bb_list.append(score[(score['Domain'] == 'Financial') & (score['Category'] == 'Salary Credits') &
                          (score['Subcategory'] == 'Yes')].Score.values[0])
        else:
            bb_list.append(
                    score[(score['Domain'] == 'Financial') & (score['Category'] == 'Salary Credits') &
                          (score['Subcategory'] == 'No')].Score.values[0])

        return sum(bb_list)
    
    def annual_income(self):
        
        try:
            ind_ai = score[(score['Category'] == 'Income')].index.tolist()
            if self.an_in == 649:
                an_in_score = score["Score"].values[ind_ai[0]]
            elif self.an_in == 650:
                an_in_score = score["Score"].values[ind_ai[1]]
            elif self.an_in == 651:
                an_in_score = score["Score"].values[ind_ai[2]]
            elif self.an_in == 652:
                an_in_score = score["Score"].values[ind_ai[3]]
            elif self.an_in == 653:
                an_in_score = score["Score"].values[ind_ai[4]]
            elif self.an_in == 801:
                an_in_score = score["Score"].values[ind_ai[5]]
            elif self.an_in == 802:
                an_in_score = score["Score"].values[ind_ai[6]]
            elif self.an_in == 803:
                an_in_score = score["Score"].values[ind_ai[7]]
            else:
                an_in_score = score["Score"].values[ind_ai[8]]
            return an_in_score

        except:
            return 0

    def score(self):

        if self.basic_res["Document"] == "Mismatched" or self.ps_res["Document"] == "Mismatched":
            fin_score = -20 + self.annual_income()
        else:
            fin_score = self.bank_score() + self.bank_details() + self.annual_income()
        
        return fin_score
        
        
'''b_res = {'AvgNoOfEmi/Ecs/ChqBne': 0.25, 'AvgTravelSpend': 0, 'AvgMinBalance': 10.8025, 'AvgSalaryDate': 31, 'AvgEcommSpend': 1091.0, 'AvgBankCharges': 0.0, 'AvgEntSpend': 0, 'AvgFoodSpend': 36.22, 'AvgEmi': 0.0, 'AverageSalary': 34493.666666666664, 'AvgNoOfDebits': 23.75, 'AvgNoOfATMWithdrawals': 7.75, 'AvgUtilitySpend': 0, 'MonthsSubmitted': 4, 'AvgNoOfCreditsOtherThanSalary': 1, 'AvgWeeklyClosingBalance': [9543.6375, 287.4125, 109.0525, 15217.24], 'EmployerName': u'NEFT CR-HSBC0400002-INTELENET GLOBAL SERVICES PRIVATE L-AMRIKA DUTTA-HSBCN180318'}
basic_res = {'UserAddress': 'Mismatched', 'SalaryCredits': 'Mismatched', 'DateOfSubmission': '2018-04-28 00:00:00', 'BankBranchName': 'Mismatched', 'AccountNumber': 'Mismatched', 'Document': 'Null'}
ps_res =  {'Salary': 'Matched', 'Name': 'Mismatched', 'DateOfJoin': 'Not Available', 'Month': 'Mismatched', 'LOP': 'Not Found', 'Document': 'Not Available', 'FileFormat': 'PDF'}
f = BankScore(b_res, basic_res, ps_res, 35000, '02.10.2018', "Intelenet","0")    
sco = f.score()'''
        
        
        
        
        
        
        
        
        
        
        
        
        
