#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 13:59:18 2018

@author: siva
"""

from tika import parser
import pandas as pd
import re


class BankInfo:

    def __init__(self,file_path, br, acc_no, add, b_name, emp_name):
        self.file_path = file_path
        self.b_name = b_name
        self.br = br
        self.acc_no = acc_no
        self.add = add
        self.emp_name = emp_name

    def meta_text(self):
        parsed_file = parser.from_file(self.file_path)
        meta_data = parsed_file['metadata']
        return meta_data

    def text_extract(self):

        parsed_file = parser.from_file(self.file_path)
        # meta_data = parsed_file['metadata']
        parsed_content = parsed_file['content']
        return parsed_content

    def conv_to_df(self):

        parsed = self.text_extract()
        parsed_cont = parsed.split('\n')
        initial_list = []
        for content in parsed_cont:
            if content != '':
                initial_list.append(content)
        final_list = []

        for content_1 in range(0, len(initial_list)):
            list_content = initial_list[content_1].split()
            final_list.append(list_content)
        df = pd.DataFrame({'d': final_list})
        df['d'] = df['d'].astype(str)
        df['d'] = df['d'].str.lower()
        return df

    def account(self):
        df = self.conv_to_df()
        try:
            if len(df[df['d'].str.contains(self.acc_no)])>0:
                account_no = "Matched"
            else:
                account_no = "Mismatched"
        except:
                account_no = "Null"

        return account_no

    def branch(self):

        df = self.conv_to_df()
        self.br = self.br.lower()
        try:
            if len(df[df['d'].str.contains(self.br)])>0:
                branch = "Matched"
            else:
                branch = "Mismatched"
        except:
                branch = "Null"

        return branch

    def employer(self):
        df = self.conv_to_df()
        emp_name = self.emp_name.lower().split()[0]
        print(emp_name)
        try:
            if len(df[df['d'].str.contains(emp_name)])>0:
                employer_name = "Matched"
            else:
                employer_name = "Mismatched"
        except:
            employer_name = "Null"
        return employer_name

    def address(self):

        df = self.conv_to_df()
        try:
            add = self.add.lower()
            add_list = add.split()
            count = 0
            for n in add_list:
                if len(df[df['d'].str.contains(n)]) > 0:
                    count += 1
            if count / float(len(add_list)) < 0.5:
                address = "Mismatched"
            else:
                address = "Matched"
        except:
            address = "Null"
        return address

    def metadata(self):
        meta_data = self.meta_text()
        try:
            if meta_data[u'Creation-Date'] == meta_data[u'Last-Modified']:
                m_data = "Matched"
            else:
                m_data = "Mismatched"

        except :
            m_data = "Null"
        return m_data

    def sta_date(self):

        df = self.conv_to_df()
        if self.b_name == 731 or self.b_name == 728 or self.b_name == 734 or self.b_name == 737 :
            df['d'] = df['d'].str.replace('/','-')
            df_dates = df['d'].str.extractall('(\d{2}\-\d{2}\-\d{4})')
            df_dates[0] = pd.to_datetime(df_dates[0],dayfirst =True,errors ='coerce')
            date_submit = df_dates[0].max()
            return str(date_submit)
        elif self.b_name == 730:
            yes_date = df['d'][1][:-1].split(',')
            s_dates = str(yes_date[-3])+str(yes_date[-4])+ str(yes_date[-1])
            s_dates = re.sub(r'[^A-Za-z0-9]',"",s_dates)
            inds = len(s_dates)
            y_day = s_dates[1:3]
            y_year = s_dates[-4:]
            y_month = s_dates[4:(inds-5)]
            fd = y_day+"-"+y_month+"-"+y_year
            date_submit = pd.to_datetime(fd,dayfirst=True)
            return str(date_submit)
        elif self.b_name == 740:
            sbi_date = df[df['d'].str.contains('date') & df['d'].str.contains(':') ].iloc[0,0]
            sbi_date = sbi_date[:-1].split(',')
            sbi_dates = str(sbi_date[-3]).strip()[1:]+'-'+str(sbi_date[-2]).strip()[1:]+ '-'+str(sbi_date[-1]).strip()[1:]
            sbi_dates = sbi_dates.replace("'",'')
            date_submit = pd.to_datetime(sbi_dates,dayfirst=True)
            return str(date_submit)
        elif self.b_name == "SC1234":
            sc_date = df[df['d'].str.contains('date') & df['d'].str.contains('statement') ].iloc[0,0]
            sc_date = sc_date[:-1].split(',')
            sc_dates = str(sc_date[-3]).strip()[1:]+'-'+str(sc_date[-2]).strip()[1:]+ '-'+str(sc_date[-1]).strip()[1:]
            sc_dates = sc_dates.replace("'",'')
            date_submit = pd.to_datetime(sc_dates,dayfirst=True)
            return str(date_submit)
        else:
            return "Invalid Bank"

    def main(self):

        bank_basic_info = dict(UserAddress=self.address(), BankBranchName=self.branch(), AccountNumber=self.account(),
                               Document=self.metadata(), DateOfSubmission=self.sta_date(),
                               SalaryCredits=self.employer())
        return bank_basic_info


'''s = BankInfo("/home/siva/Desktop/BSA/statement.pdf","MAGARPATTA","04861140031621", "MR. SHAIKH RIZWAN FLAT NO 201 SHRE RAM DREAM KAMAL PARK LANE NO 7 LOHEGAON DHANORI RD NEAR KAMAL LAWNS DHANORI PUNE 411015 MAHARASHTRA INDIA",
             731, "Intelenet services")
     
d = s.main()  
print(d)   '''  



