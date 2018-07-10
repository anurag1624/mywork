#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  7 18:00:23 2018

@author: siva
"""

from pymongo import MongoClient
import pandas as pd
from datetime import datetime, timedelta
import re
import geocoder
from bson.objectid import ObjectId
from dateutil import tz

score = pd.read_pickle('score_pkl')


class ProfileScore:
    def __init__(self, pan, rmn, mid, pcode, jd, dept, emp_name, dob, yrs_of_mrg,
                 mar_status, gender, edu, doj, spo_prof, kids, language,
                 uid, city, name, device, friend_no, neigh_no, manager_no,
                 act_loc, doj_ps, geo_lat, geo_long, from_off, to_off, off_pcode,
                 sib_no, dad_no, mom_no, spo_no):
        self.pan = pan
        self.rmn = rmn
        self.mid = mid
        self.pcode = pcode
        self.jd = jd
        self.dept = dept
        self.act_loc = act_loc
        self.emp_name = emp_name
        self.dob = dob
        self.yrs_of_mrg = yrs_of_mrg
        self.mar_status = mar_status
        self.gender = gender
        self.edu = edu
        self.doj_ps = doj_ps
        self.doj = doj
        self.spo_prof = spo_prof
        self.kids = kids
        self.language = language
        self.uid = uid
        self.city = city
        self.name = name
        self.device = device
        self.friend_no = friend_no
        self.neigh_no = neigh_no
        self.manager_no = manager_no
        self.geo_lat = geo_lat
        self.geo_long = geo_long
        self.from_off = from_off
        self.to_off = to_off
        self.off_pcode = off_pcode
        self.sib_no = sib_no
        self.dad_no = dad_no
        self.mom_no = mom_no
        self.spo_no = spo_no
        
    def d_base(self):
        uri = "mongodb://atlmongo:KcNrtLOiTlz3J7UEgzUl978r3GK8ycJu9d3iPYnQ0yr4hYwpQwVatiFOt6NYJurpq4Q4Odmdl0AcSSo6vYkftw==@atlmongo.documents.azure.com:10255/?ssl=true&replicaSet=globaldb"
        cli = MongoClient(uri)
        db = cli.LOBOT
        return db

    def foogle_score(self):
        try:
            l = []
            df = pd.read_pickle('foogle_pkl')
            df = df.drop(labels=["_id", 'id'], axis=1)
            if len(df[df['Email'].str.contains(self.mid)]) > 0:
                impact = df[df['Email'].str.contains(self.mid)].Impact.values.tolist()
                l.append(impact[0])
            if len(df[df['MobileNo'].str.contains(self.rmn)]) > 0:
                impact = df[df['MobileNo'].str.contains(self.rmn)].Impact.values.tolist()
                l.append(impact[0])
            if len(df[df['PanCardNo'].str.contains(self.pan)]) > 0:
                impact = df[df['PanCardNo'].str.contains(self.pan)].Impact.values.tolist()
                l.append(impact[0])

            if len(l) > 0:
                if 'High' in l:
                    f_imp = 'High'
                elif 'Medium' in l:
                    f_imp = 'Medium'
                else:
                    f_imp = 'Low'
                foo_score = score[(score['Category'] == 'Foogle') &
                                  (score['Subcategory'] == f_imp)].Score.values[0]

            else:
                foo_score = 0
            print("Foo Score---", foo_score)
        except:
            foo_score = 0

        return foo_score

    def neg_pincode(self):
        try:
            db = self.d_base()
            l_pin = db.Negativepincodes.find_one({"Type": "NegativePincodes"})["Pincodes"]
            if self.pcode in l_pin:
                pin_score = score[(score['Category'] == 'Negative Pincode')].Score.values[0]
            else:
                pin_score = 0
        except:
            pin_score = 0
        print("Pincode---", pin_score)
        return pin_score

    def neg_job(self):
        try:

            db = self.d_base()
            nj_dict = db.Jobdesignations.find_one({"Type": "NegativeDesignations"})["Designations"]
            for nj in nj_dict:
                if nj["Designation"] == self.jd:
                    imp = nj["Impact"]
                    j_score = score[(score['Category'] == 'Negative JD') &
                                    (score['Subcategory'] == imp)].Score.values[0]
                    break
                else:
                    j_score = 0
        except:
            j_score = 0
        print("Neg.Job---", j_score)
        return j_score

    def neg_sect(self):
        try:
            db = self.d_base()
            nj_dict = db.Negativesectors.find_one({"Type": "NegativeSectors"})["Sectors"]
            for nj in nj_dict:
                if nj["Department"] == self.dept:
                    imp = nj["Impact"]
                    j_score = score[(score['Category'] == 'Negative Sectors') &
                                    (score['Subcategory'] == imp)].Score.values[0]
                    break
                else:
                    j_score = 0
        except:
            j_score = 0
        print("Neg.Sect---", j_score)
        return j_score

    def comp_found(self):
        try:
            db = self.d_base()
            apps = db.AppDetails.find_one({"UserId": self.uid})["AppDetails"]
            apps_user = [app["AppName"] for app in apps]
            apps_comp = db.Competitors.find_one({"Type": "Competitors"})['Competitors']
            count = 0
            for ap in apps_user:
                if ap in apps_comp:
                    count = count + 1

            ind_com = score[(score['Category'] == 'Competitors')].index.tolist()
            for com in ind_com[:-1]:
                if count == score["Max Range"].values[com]:
                    c_score = score["Score"].values[com]
                    break
            else:
                c_score = score["Score"].values[ind_com[-1]]
        except:
            c_score = 0
        print("Comp--", c_score)
        return c_score

    def tour_places(self):
        try:
            db = self.d_base()
            dct_tour = db.Touristplaces.find_one({"Type": "TouristPlaces"})["Places"]
            act_loc_list = self.act_loc
            for loc in act_loc_list:
                if loc in dct_tour:
                    t_score = score[(score['Category'] == 'Tourist Place')].Score.values[0]
                    break
            else:
                t_score = 0
        except:
            t_score = 0
        print(" tour---", t_score)
        return t_score

    def pilgrim(self):
        try:
            db = self.d_base()
            dct_pilgrim = db.Pilgrimages.find_one({"Type": "Pilgrimages"})["Places"]
            act_pil = self.act_loc
            for loc in act_pil:
                if loc in dct_pilgrim:
                    p_score = score[(score['Category'] == 'Pilgrimage')].Score.values[0]
                    break
            else:
                p_score = 0
        except:
            p_score = 0
        print("pilgrim--", p_score)
        return p_score

    def neg_emp(self):
        try:
            db = self.d_base()
            nj_dict = db.Negativeemployers.find_one({"Type": "Employers"})["Employers"]
            for nj in nj_dict:
                if nj["EmployerName"] == self.emp_name:
                    imp = nj["Impact"]
                    j_score = score[(score['Category'] == 'Employer Category') &
                                    (score['Subcategory'] == imp)].Score.values[0]
                    break
                else:
                    j_score = 0
        except:
            j_score = 0
        print("neg.Emp---", j_score)
        return j_score

    def marital_score(self):
        try:
            bir = datetime(1, 1, 1) + timedelta(microseconds= self.dob / 10)
            yom = self.yrs_of_mrg
            mar = self.mar_status
            now = pd.to_datetime(datetime.now().date(), dayfirst=True)
            dob_conv = pd.to_datetime(bir, dayfirst=True)
            year = now.year
            age_of_mrg = year - int(yom)
            age_user = (now - dob_conv).days / 365
            m_score = []
            if mar == "Married":
                if self.gender == "Female":
                    m_score.append(score[(score['Max Range'] == 0) &
                                         (score['Subcategory'] == 'Widower')].Score.values[0])
                if self.gender == "Male":
                    if self.spo_prof == "Employee":
                        m_score.append(score[(score['Category'] == 'Spouse Profession') &
                                             (score['Subcategory'] == 'Salaried')].Score.values[0])
                    elif self.spo_prof == "HomeMaker":
                        m_score.append(score[(score['Category'] == 'Spouse Profession') &
                                             (score['Subcategory'] == 'Home Maker')].Score.values[0])
                    else:
                        m_score.append(score[(score['Category'] == 'Spouse Profession') &
                                             (score['Subcategory'] == 'Self Employed')].Score.values[0])

                m_score.append(score[(score['Max Range'] == 0) &
                                     (score['Subcategory'] == 'Divorcee')].Score.values[0])

                m_score.append(score[(score['Max Range'] == 0) &
                                     (score['Subcategory'] == 'Bachelor')].Score.values[0])

                ind_mrg = score[
                    (score['Category'] == 'Age of Marriage') & (score['Subcategory'] == 'Married')].index.tolist()
                for mrg in ind_mrg[:-1]:
                    if age_of_mrg <= score["Max Range"].values[mrg]:
                        m_score.append(score["Score"].values[mrg])
                        break
                else:
                    m_score.append(score["Score"].values[ind_mrg[-1]])

                ind_mou = score[(score['Category'] == 'Age') & (score['Subcategory'] == 'Married')].index.tolist()
                for mou in ind_mou[:-1]:
                    if age_user <= score["Max Range"].values[mou]:
                        m_score.append(score["Score"].values[mou])
                        break
                else:
                    m_score.append(score["Score"].values[ind_mou[-1]])

            elif mar == 'Single':
                m_score.append(score[(score['Max Range'] == 1) &
                                     (score['Subcategory'] == 'Bachelor')].Score.values[0])

                ind_sin = score[(score['Category'] == 'Age') & (score['Subcategory'] == 'Unmarried')].index.tolist()
                for sin in ind_sin[:-1]:
                    if age_user <= score["Max Range"].values[sin]:
                        m_score.append(score["Score"].values[sin])
                        break
                else:
                    m_score.append(score["Score"].values[ind_sin[-1]])

            elif mar == "Divorced":
                m_score.append(score[(score['Max Range'] == 1) &
                                     (score['Subcategory'] == 'Divorcee')].Score.values[0])

            elif mar == "Widow":
                m_score.append(score[(score['Max Range'] == 1) &
                                     (score['Subcategory'] == 'Widower')].Score.values[0])

            else:
                m_score.append(0)
            print(m_score)
        except:
            m_score = [0]

        return sum(m_score)

    def gender_func(self):

        try:
            if self.gender == 'Male':
                g_score = score[(score['Category'] == 'Gender') &
                                (score['Subcategory'] == 'Male')].Score.values[0]
            elif self.gender == 'Female':
                g_score = score[(score['Category'] == 'Gender') &
                                (score['Subcategory'] == 'Female')].Score.values[0]
            else:
                g_score = score[(score['Category'] == 'Gender') &
                                (score['Subcategory'] == 'Transgender')].Score.values[0]
        except:
            g_score = 0
        print("Gender---", g_score)
        return g_score

    def qualification(self):
        try:
            if self.edu == '10th':
                q_score = score[(score['Subcategory'] == '10th')].Score.values[0]
            elif self.edu == '12th':
                q_score = score[(score['Subcategory'] == 'Inter')].Score.values[0]
            elif self.edu == 'Graduate':
                q_score = score[(score['Subcategory'] == 'Graduate')].Score.values[0]
            else:
                q_score = score[(score['Subcategory'] == 'PG')].Score.values[0]
        except:
            q_score = 0
        print("qualify--", q_score)
        return q_score

    def payslip(self):

        doj_temp = datetime(1, 1, 1) + timedelta(microseconds= self.doj/10)
        now = pd.to_datetime(datetime.now().date(), dayfirst=True)
        doj_conv = pd.to_datetime(doj_temp, dayfirst=True)
        age_job = (now - doj_conv).days / 365

        try:
            if self.doj_ps == "Matched" or self.doj_ps == "Not Available":
                ps_score = score[(score['Max Range'] == 1) &
                                 (score['Category'] == 'DOJ')].Score.values[0]
                ind_doj = score[(score['Category'] == 'DOJ Age')].index.tolist()
                for doj in ind_doj[:-1]:
                    if age_job <= score["Max Range"].values[doj]:
                        ex_score = score["Score"].values[doj]
                        break
                else:
                    ex_score = score["Score"].values[ind_doj[-1]]

            else:
                ps_score = score[(score['Max Range'] == 0) &
                                 (score['Category'] == 'DOJ')].Score.values[0]
                ex_score = 0
        except:
            ps_score = score[(score['Max Range'] == -1) &
                             (score['Category'] == 'DOJ')].Score.values[0]
            ex_score = 0
        print("payslip", ps_score, ex_score)
        return ps_score + ex_score

    def kids_func(self):
        try:
            if self.mar_status == "Married" or self.mar_status == "Divorced" or self.mar_status == "Widow":

                ind_kid = score[(score['Category'] == 'Kids')].index.tolist()
                for kid in ind_kid[:-1]:
                    if self.kids == score["Max Range"].values[kid]:
                        k_score = score["Score"].values[kid]
                        break
                else:
                    k_score = score["Score"].values[ind_kid[-1]]
            else:
                k_score = 0
        except:
            k_score = 0
        print("kids", k_score)
        return k_score

    def mother_tongue(self):

        try:
            language = self.language
            l_score = score[(score['Category'] == "Mother Tongue") &
                            (score['Subcategory'] == str(language))].Score.values[0]

        except:

            l_score = 1
        print("Lang---", l_score)

        return l_score

    def cities(self):
        try:
            db = self.d_base()
            nj_dict = db.Cities.find_one({"Type": "Cities"})["Cities"]
            for nj in nj_dict:
                if nj["City"] == self.city:
                    imp = nj["CityType"]
                    j_score = score[(score['Category'] == 'City') &
                                    (score['Subcategory'] == imp)].Score.values[0]
                    break
                else:
                    j_score = 0
        except:
            j_score = 0
        print("City--", j_score)
        return j_score

    def emailid(self):

        try:
            mail = self.mid.split('@')[0]
            name_list = self.name.split()
            cnt = 0
            for nam in name_list:
                if nam.lower() in mail:
                    cnt = cnt + 1

            if cnt == len(name_list):
                id_score = score[(score['Category'] == 'Email') &
                                 (score['Subcategory'] == "Contains Name Surname")].Score.values[0]
            elif cnt == 1:
                if bool(re.match('[^0-9]', mail)):
                    id_score = score[(score['Category'] == 'Email') &
                                     (score['Subcategory'] == "Contains Name Number")].Score.values[0]

                else:
                    id_score = score[(score['Category'] == 'Email') &
                                     (score['Subcategory'] == "Contains Name")].Score.values[0]

            else:
                id_score = score[(score['Category'] == 'Email') &
                                 (score['Subcategory'] == "No Name")].Score.values[0]
            print("email---", id_score)
        except:
            id_score = 0

        return id_score

    def rmn_check(self):
        db = self.d_base()
        try:
            call_hist = db.Callhistory.find_one({"UserId": self.uid})["ContactsCallHistory"]
            for call in call_hist:
                if str(call["Callnumber"]) == str(self.rmn):
                    c_score = score[(score['Category'] == 'RMN') &
                                    (score['Max Range'] == 1)].Score.values[0]

                    break
            else:
                c_score = score[(score['Category'] == 'RMN') &
                                (score['Max Range'] == 0)].Score.values[0]
        except:
            c_score = 0
        print("rmn--", c_score)
        return c_score

    def permissions(self):
        db = self.d_base()
        call_hist = db.Callhistory.find_one({"UserId": self.uid})
        sms_hist = db.Smshistory.find_one({"UserId": self.uid})
        apps = db.AppDetails.find_one({"UserId": self.uid})
        pbook = db.Phonebookcontacts.find_one({"UserId": self.uid})

        if call_hist is None and sms_hist is None and apps is None and pbook is None:
            c_score = score[(score['Category'] == 'App Data') &
                            (score['Subcategory'] == 'No Data')].Score.values[0]
        else:
            c_score = score[(score['Category'] == 'App Data') &
                            (score['Subcategory'] == 'App Data')].Score.values[0]

        print("permi--", c_score)
        return c_score

    def messages(self):
        db = self.d_base()
        msg_score = []
        due_key = ["overdue", "severe due", "due"]
        def_key = ["default"]
        comp_key = db.Competitors.find_one({"Type": "Competitors"})["Competitors"]
        sms_hist = db.Smshistory.find_one({"UserId": self.uid})
        if sms_hist is None:
            if self.device == "Android":
                msg_score.append(score[(score['Category'] == 'Messages') &
                                       (score['Subcategory'] == 'Android')].Score.values[0])
            else:
                msg_score.append(score[(score['Category'] == 'Messages') &
                                       (score['Subcategory'] == 'iOS')].Score.values[0])

        else:
            due_cnt = 0
            for due in due_key:
                for sms in sms_hist["ContactSmsHistory"]:
                    if due.lower() in sms["Smstext"].lower():
                        due_cnt = due_cnt + 1
                        break
            if due_cnt < 3:
                msg_score.append(score[(score['Category'] == 'Messages') &
                                       (score['Subcategory'] == 'due') & (score['Min Range'] == due_cnt)].Score.values[
                                     0])
            else:
                msg_score.append(score[(score['Category'] == 'Messages') &
                                       (score['Subcategory'] == 'due') & (score['Min Range'] == 3)].Score.values[0])

            def_cnt = 0
            for defa in def_key:
                for sms in sms_hist["ContactSmsHistory"]:
                    if defa.lower() in sms["Smstext"].lower():
                        def_cnt = def_cnt + 1
                        break

            if def_cnt < 2:
                msg_score.append(score[(score['Category'] == 'Messages') &
                                       (score['Subcategory'] == 'due') & (score['Min Range'] == def_cnt)].Score.values[
                                     0])
            else:
                msg_score.append(score[(score['Category'] == 'Messages') &
                                       (score['Subcategory'] == 'due') & (score['Min Range'] == 2)].Score.values[0])

            comp_cnt = 0
            for comp in comp_key:
                for sms in sms_hist["ContactSmsHistory"]:
                    if comp.lower() in sms["Smstext"].lower():
                        comp_cnt = comp_cnt + 1
                        break

            if comp_cnt < 2:
                msg_score.append(score[(score['Category'] == 'Messages') &
                                       (score['Subcategory'] == 'Competitor') & (
                                                   score['Min Range'] == comp_cnt)].Score.values[0])
            else:
                msg_score.append(score[(score['Category'] == 'Messages') &
                                       (score['Subcategory'] == 'Competitor') & (score['Min Range'] == 2)].Score.values[
                                     0])

        print("messages--", msg_score)
        return sum(msg_score)

    def sec_ques(self):
        db = self.d_base()
        def_list = db.Defaulters.find_one({"Type": "Defaulters"})["Defaulters"]
        try:
            cont_hist = db.Phonebookcontacts.find_one({"UserId": self.uid})["UserPhoneContacts"]
            for con in cont_hist:
                if str(con["PrimaryContact"]) in def_list:
                    c_score = score[(score['Category'] == 'Security questions') &
                                    (score['Max Range'] == 1)].Score.values[0]

                    break
            else:
                c_score = score[(score['Category'] == 'Security questions') &
                                (score['Max Range'] == 0)].Score.values[0]
        except:
            c_score = 0

        print("security--", c_score)
        return c_score

    def app_score(self):
        try:
            db = self.d_base()
            apps = db.AppDetails.find_one({"UserId": self.uid})["AppDetails"]
            def_app = db.Appscores.find_one({"Type": "AppScores"})
            app_score = []
            ban_cnt = 0
            gam_cnt = 0
            tra_cnt = 0
            news_cnt = 0
            puz_cnt = 0
            dat_cnt = 0
            job_cnt = 0
            cb_cnt = 0
            hlt_cnt = 0
            mat_cnt = 0
            coo_cnt = 0
            ast_cnt = 0
            for app in apps:
                if app["AppName"] in def_app["Gambling"]:
                    gam_cnt += 1
                if app["AppName"] in def_app["Travel"]:
                    tra_cnt += 1
                if app["Category"] in def_app["News"]:
                    news_cnt += 1
                if app["Category"] in def_app["Brain"]:
                    puz_cnt += 1
                if app["Category"] in def_app["Dating"]:
                    dat_cnt += 1
                if app["AppName"] in def_app["Jobhunting"]:
                    job_cnt += 1
                if app["AppName"] in def_app["CallBlocker"]:
                    cb_cnt += 1
                if app["AppName"] in def_app["Astrology"]:
                    ast_cnt += 1
                if app["AppName"] in def_app["Cooking"]:
                    coo_cnt += 1
                if app["Category"] in def_app["Health"]:
                    hlt_cnt += 1
                if app["AppName"] in def_app["Matrimony"]:
                    mat_cnt += 1
                if app["Category"] in def_app["Bank"]:
                    ban_cnt += 1

            if gam_cnt > 0:
                app_score.append(score[(score['Category'] == 'App Scores') &
                                       (score['Subcategory'] == 'Gambling App')].Score.values[0])
            if tra_cnt > 0:
                app_score.append(score[(score['Category'] == 'App Scores') &
                                       (score['Subcategory'] == 'Ola')].Score.values[0])

            if news_cnt > 0:
                app_score.append(score[(score['Category'] == 'App Scores') &
                                       (score['Subcategory'] == 'News Apps')].Score.values[0])

            if puz_cnt > 0:
                app_score.append(score[(score['Category'] == 'App Scores') &
                                       (score['Subcategory'] == 'Puzzles')].Score.values[0])

            if dat_cnt > 0 and self.mar_status == "Married":
                app_score.append(score[(score['Category'] == 'App Scores') &
                                       (score['Subcategory'] == 'Dating Married')].Score.values[0])

            if dat_cnt > 0 and self.mar_status == "Single":
                app_score.append(score[(score['Category'] == 'App Scores') &
                                       (score['Subcategory'] == 'Dating Unmarried')].Score.values[0])

            if app["AppName"] in def_app["Skype"]:
                app_score.append(score[(score['Category'] == 'App Scores') &
                                       (score['Subcategory'] == 'Skype')].Score.values[0])

            if app["AppName"] in def_app["Viber"]:
                app_score.append(score[(score['Category'] == 'App Scores') &
                                       (score['Subcategory'] == 'Viber')].Score.values[0])

            if job_cnt > 0:
                app_score.append(score[(score['Category'] == 'App Scores') &
                                       (score['Subcategory'] == 'Job hunting')].Score.values[0])

            if app["AppName"] in def_app["Linkedin"]:
                app_score.append(score[(score['Category'] == 'App Scores') &
                                       (score['Subcategory'] == 'Linkedin')].Score.values[0])

            if cb_cnt > 0:
                app_score.append(score[(score['Category'] == 'App Scores') &
                                       (score['Subcategory'] == 'Callblocker')].Score.values[0])

            if ast_cnt > 0:
                app_score.append(score[(score['Category'] == 'App Scores') &
                                       (score['Subcategory'] == 'Astrology')].Score.values[0])

            if mat_cnt > 0 and self.mar_status == "Married":
                app_score.append(score[(score['Category'] == 'App Scores') &
                                       (score['Subcategory'] == 'Matrimony Married')].Score.values[0])

            if mat_cnt > 0 and self.mar_status == "Divorced":
                app_score.append(score[(score['Category'] == 'App Scores') &
                                       (score['Subcategory'] == 'Matrimony Divorcee')].Score.values[0])

            if coo_cnt > 0:
                app_score.append(score[(score['Category'] == 'App Scores') &
                                       (score['Subcategory'] == 'Cooking')].Score.values[0])

            if hlt_cnt > 0:
                app_score.append(score[(score['Category'] == 'App Scores') &
                                       (score['Subcategory'] == 'Health')].Score.values[0])

            if app["Category"] in def_app["Rentomojo"]:
                app_score.append(score[(score['Category'] == 'App Scores') &
                                       (score['Subcategory'] == 'Rentomojo')].Score.values[0])

            if app["Category"] in def_app["Sabrentkar"]:
                app_score.append(score[(score['Category'] == 'App Scores') &
                                       (score['Subcategory'] == 'Sabrentkar')].Score.values[0])

            if ban_cnt > 3:
                app_score.append(score[(score['Category'] == 'App Scores') &
                                       (score['Subcategory'] == 'Bank')].Score.values[0])

            print("AppScores---", app_score)
            return sum(app_score)

        except:
            print("AppScores---", 0)
            return 0

    def geo_tagging(self):

        db = self.d_base()
        geo_loc = geocoder.google([self.geo_lat, self.geo_long], method='reverse')
        geo_pin = geo_loc.postal
        # geo_address = geo_loc.address
        start = datetime(1, 1, 1) + timedelta(microseconds=self.from_off/10)
        from_hrs = str(start.hour) + ":" + str(start.minute)
        start_time = datetime.strptime(from_hrs, "%H:%M")
        end = datetime(1, 1, 1) + timedelta(microseconds=self.to_off/10)
        to_hrs = str(end.hour) + ":" + str(end.minute)         
        end_time = datetime.strptime(to_hrs, "%H:%M") 
        
        geo_object = db.LocationDetails.find_one({"UserId" : self.uid})["_id"]
        geo_time = geo_object.generation_time
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()  
        utc = geo_time.replace(tzinfo=from_zone)
        check_in = utc.astimezone(to_zone)
        check_hrs = str(check_in.hour) + ":" + str(check_in.minute)         
        check_time = datetime.strptime(check_hrs, "%H:%M") 
        
        if start_time < check_time < end_time:
            if self.off_pcode == geo_pin:
                geo_score = score[(score['Category'] == 'Geo Tagging') &
                                   (score['Subcategory'] == 'Office in office Hrs')].Score.values[0]
            elif self.pcode == geo_pin:
                geo_score = score[(score['Category'] == 'Geo Tagging') &
                                   (score['Subcategory'] == 'Home in office Hrs')].Score.values[0]
            else:
                geo_score = score[(score['Category'] == 'Geo Tagging') &
                                   (score['Subcategory'] == 'Outside in office Hrs')].Score.values[0]
           
        else:
            if self.pcode == geo_pin:
                
                geo_score = score[(score['Category'] == 'Geo Tagging') &
                                   (score['Subcategory'] == 'Home in nonoffice Hrs')].Score.values[0]
            else:
                geo_score = 0

        return geo_score
    
    def ios(self):
        i_score = []
        db = self.d_base()
        emp_1 = self.emp_name.split()[0]
        if self.device == 'IOS':
            cont_hist = db.Phonebookcontacts.find_one({"UserId": self.uid})["UserPhoneContacts"]
            if self.sib_no is not None:
                for con_si in cont_hist:
                    if con_si["PrimaryContact"] == self.sib_no:
                        i_score.append(score[(score['Category'] == 'IOS') &
                                        (score['Subcategory'] == 'Sibb No.Found')].Score.values[0])
                        break
                else:
                    i_score.append(score[(score['Category'] == 'IOS') &
                                        (score['Subcategory'] == 'Sibb No.NotFound')].Score.values[0])

            if self.dad_no is not None or self.mom_no is not None:
                for con_p in cont_hist:
                    if con_p["PrimaryContact"] == self.mom_no or con_p["PrimaryContact"] == self.dad_no:
                        i_score.append(score[(score['Category'] == 'IOS') &
                                        (score['Subcategory'] == 'Moth/Fath No.Found')].Score.values[0])
                        break
                else:
                    i_score.append(score[(score['Category'] == 'IOS') &
                                        (score['Subcategory'] == 'Moth/Fath No.NotFound')].Score.values[0])

            if self.spo_no is not None:
                for con_sp in cont_hist:
                    if con_sp["PrimaryContact"] == self.spo_no:
                        i_score.append(score[(score['Category'] == 'IOS') &
                                        (score['Subcategory'] == 'Spouse No.Found')].Score.values[0])
                        break
                else:
                    i_score.append(score[(score['Category'] == 'IOS') &
                                        (score['Subcategory'] == 'Spouse No.NotFound')].Score.values[0])

            if self.neigh_no is not None or self.friend_no is not None:
                for con_sq in cont_hist:
                    if con_sq["PrimaryContact"] == self.neigh_no or con_sq["PrimaryContact"] == self.friend_no:
                        i_score.append(score[(score['Category'] == 'IOS') &
                                        (score['Subcategory'] == 'Sec.Que No.Found')].Score.values[0])
                        break
                else:
                    i_score.append(score[(score['Category'] == 'IOS') &
                                        (score['Subcategory'] == 'Sec.que No.NotFound')].Score.values[0])

                for con_com in cont_hist:
                    if emp_1 in con_com["ContactName"] :
                        i_score.append(score[(score['Category'] == 'IOS') &
                                        (score['Subcategory'] == 'CompName Found')].Score.values[0])
                        break
                else:
                    i_score.append(score[(score['Category'] == 'IOS') &
                                        (score['Subcategory'] == 'CompName Not Found')].Score.values[0])
        else:
            i_score = [0,0]

        return sum(i_score)
    
    def result(self):

        score_profile = self.foogle_score() + self.neg_emp() + self.neg_job() + self.neg_pincode() + self.neg_sect() + self.comp_found() + self.tour_places() + self.pilgrim() + self.marital_score() + self.gender_func() + self.qualification() + self.payslip() + self.kids_func() + self.mother_tongue() + self.cities() + self.emailid() + self.rmn_check() + self.permissions() + self.messages() + self.sec_ques() + self.app_score() + self.geo_tagging() + self.ios()

        return score_profile
