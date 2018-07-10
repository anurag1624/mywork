from tika import parser
import pandas as pd
from datetime import datetime


class PaySlip:
    
    def __init__(self,file_path, name, sal, doj):
        self.file_path = file_path
        self.name = name
        # self.emp_id = emp_id
        self.sal = sal
        self.doj = doj
        
    def text_extract(self):
        
        parsed_file = parser.from_file(self.file_path)
        self.meta_data = parsed_file['metadata']
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
        df['d'] = df['d'].str.replace(',', '')
        df['d'] = df['d'].str.replace('-', '.')
        df['d'] = df['d'].str.replace('/', '.')
        df['d'] = df['d'].str.lower()
        return df

    # ----------------------Meta data match------------------

    def metadata(self):
        try:
            if self.meta_data[u'Creation-Date'] == self.meta_data[u'Last-Modified']:
                m_data = "Matched"
            else:
                m_data = "Mismatched"
        except KeyError:
            m_data = "Not Available"
        return m_data

    # ---------------------------Name Match---------------------

    def name_find(self):
        df = self.conv_to_df()
        try:
            self.name = self.name.lower()
            name_list = self.name.split()
            count = 0
            for n in name_list:
                if len(df[df['d'].str.contains(n)]) > 0:
                    count += 1
            if count / float(len(name_list)) < 0.25:
                name = "Mismatched"
            else:
                name = "Matched"
        except:
            name = "not available"
        return name

    # --------------------------emp_id search-------------------------
    '''def id_of_emp(self):
        df = self.conv_to_df()
        self.emp_id = str(self.emp_id)
        try:
            if len(df[df['d'].str.contains(self.emp_id)]) > 0:
                id = "Matched"
            else:
                id = "Mismatched"
        except:
            id = "not available"
        return id'''

    # -------------------------Net Pay check-------------------------------
    def pay_check(self):
        df = self.conv_to_df()
        df_num = df['d'].str.extractall('(\d+)')
        df_num = df_num[df_num.astype(float) < 1000000].dropna()
        df_num = df_num.astype(float)
        try:
            self.sal = float(self.sal)
            if len(df_num[df_num > self.sal * 0.9].dropna()) > 0:
                net_pay = "Matched"
            else:
                net_pay = "Mismatched"
        except:
            net_pay = "Mismatched"

        return net_pay

    # ---------------------Payslip month---------------------------
    def pay_month(self):

        df = self.conv_to_df()
        month_list = {'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6, 'jul': 7, 'aug': 8,
                      'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12}
        try:
            list_mon = []
            for mon in month_list.keys():
                if len(df[df['d'].str.contains(mon)]) > 0:
                    list_mon.append(month_list[mon])
            else:
                month = "not available"

            cur_mon = datetime.now().month

            for mon_check in list_mon:
                if cur_mon - mon_check == 1 or cur_mon - mon_check == -11:
                    month = "Matched"
                else:
                    month = "Mismatched"
        except:

            month = "not available"

        return month

    # ---------------------Payslip format-----------------
    def file_format(self):

        if "pdf" in self.file_path.lower():
            f_format = "PDF"
        else:
            f_format = "Image"
        return f_format

    # ---------------------Date of join-----------------
    def date_of_join(self):

        df = self.conv_to_df()
        try:
            df_join = df['d'].str.extractall('(\d+\.\d+\.\d+)')
            df_join = pd.to_datetime(df_join[0], dayfirst=True)
            input_date = pd.to_datetime(self.doj, dayfirst=True)
            if (df_join[0] - input_date).days == 0:
                join_date = "Matched"
            else:
                join_date = "Mismatched"
        except:

            join_date = "Not Available"

        return join_date

    # ------------------------LOP's------------------------
    def lop_check(self):

        df = self.conv_to_df()

        if len(df[df['d'].str.contains('lop')]) > 0:
            if len(df[df['d'].str.contains(u'0.0/s')]) > 0 or len(df[df['d'].str.contains(u'0')]) > 0:
                lop = 'Not Found'
            else:
                lop = 'Found'
        
        else:
            lop = 'Not Found'

        return lop

    def main(self):
        
        ps = dict()
        ps["Name"] = self.name_find()
        ps["Month"] = self.pay_month()
        ps["Salary"] = self.pay_check()
        ps["Document"] = self.metadata()
        ps["DateOfJoin"] = self.date_of_join()
        ps["LOP"] = self.lop_check()
        ps["FileFormat"] = self.file_format()
        # ps["EmployeeID"] = self.id_of_emp()

        return ps


'''details = PaySlip("payslip2.PDF","Harshal Kadham","00022302","29000","07.02.2017")
d = details.main()
print(d)
# df_te = details.conv_to_df()'''











