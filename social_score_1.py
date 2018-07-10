#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue May  8 10:51:21 2018

@author: siva
"""
import pandas as pd

score = pd.read_pickle('score_pkl')


def g_score(g_res):
    gail_list = []
    # ---------------- bank statement retrieval-----------------
    if g_res["BankStatement"] == "Retrieved":
        gail_list.append(
            score[(score['Category'] == 'GMAIL') & (score['Subcategory'] == 'BS') &
                  (score['Max Range'] == 1)].Score.values[0])
    else:
        gail_list.append(score[(score['Category'] == 'GMAIL') & (score['Subcategory'] == 'BS') &
                               (score['Max Range'] == 0)].Score.values[0])
        # ----------------Credit statement retrieval------------------
    if g_res["CreditCardStatement"] == "Retrieved":
        gail_list.append(
            score[(score['Category'] == 'GMAIL') & (score['Subcategory'] == 'CC') &
                  (score['Max Range'] == 1)].Score.values[0])
    else:
        gail_list.append(
            score[(score['Category'] == 'GMAIL') & (score['Subcategory'] == 'CC') &
                  (score['Max Range'] == 0)].Score.values[0])

    # ---------------------------Pay slip retrieval---------------
    if g_res["PaySlip"] == "Retrieved":
        gail_list.append(
            score[(score['Category'] == 'GMAIL') & (score['Subcategory'] == 'PS') &
                  (score['Max Range'] == 1)].Score.values[0])
    else:
        gail_list.append(
            score[(score['Category'] == 'GMAIL') & (score['Subcategory'] == 'PS') &
                  (score['Max Range'] == 0)].Score.values[0])
    # -------------------------Mobile bill----------------------------
    if g_res["MobileBill"] == "Retrieved":
        gail_list.append(
            score[(score['Category'] == 'GMAIL') & (score['Subcategory'] == 'Mobile Bill') &
                  (score['Max Range'] == 1)].Score.values[0])
    else:
        gail_list.append(
            score[(score['Category'] == 'GMAIL') & (score['Subcategory'] == 'Mobile Bill') &
                  (score['Max Range'] == 0)].Score.values[0])
    # --------------------------Off letters---------------------------
    if g_res["OfferLetter"] == "Retrieved":
        gail_list.append(
            score[(score['Category'] == 'GMAIL') & (score['Subcategory'] == 'Interview offers') &
                  (score['Max Range'] == 1)].Score.values[0])
    else:
        gail_list.append(
            score[(score['Category'] == 'GMAIL') & (score['Subcategory'] == 'Interview offers') &
                  (score['Max Range'] == 0)].Score.values[0])
    # -------------------------credit cards number--------------------------
    if g_res["NoOfUniqueCreditCards"] == 0:
        gail_list.append(
            score[(score['Category'] == 'GMAIL') & (score['Subcategory'] == 'CC Number') &
                  (score['Max Range'] == 0)].Score.values[0])
    elif g_res["NoOfUniqueCreditCards"] == 1:
        gail_list.append(
            score[(score['Category'] == 'GMAIL') & (score['Subcategory'] == 'CC Number') &
                  (score['Max Range'] == 1)].Score.values[0])
    if g_res["NoOfUniqueCreditCards"] == 2:
        gail_list.append(
            score[(score['Category'] == 'GMAIL') & (score['Subcategory'] == 'CC Number') &
                  (score['Max Range'] == 2)].Score.values[0])
    else:
        gail_list.append(
            score[(score['Category'] == 'GMAIL') & (score['Subcategory'] == 'CC Number') &
                  (score['Min Range'] == 3)].Score.values[0])
    # ---------------------competitors found-----------------------------
    if g_res["CompetitorsFound"] == 0:
        gail_list.append(
            score[(score['Category'] == 'GMAIL') & (score['Subcategory'] == 'Competitors' &
                                                    (score['Max Range'] == 0))].Score.values[0])
    elif g_res["CompetitorsFound"] == 1:
        gail_list.append(
            score[(score['Category'] == 'GMAIL') & (score['Subcategory'] == 'Competitors') &
                  (score['Max Range'] == 1)].Score.values[0])
    elif g_res["CompetitorsFound"] == 2:
        gail_list.append(
            score[(score['Category'] == 'GMAIL') & (score['Subcategory'] == 'Competitors2') &
                  (score['Max Range'] == 2)].Score.values[0])
    else:
        gail_list.append(
            score[(score['Category'] == 'GMAIL') & (score['Subcategory'] == 'Competitors3') &
                  (score['Min Range'] == 3)].Score.values[0])

    return sum(gail_list)


def fb_score(f_res, mar_status, edu, loc, rmn, fam_con):
    fb_list = []

    # --------------------------Connections----------------------------
    ind_conn = score[(score['Domain'] == 'Social') & (score['Subcategory'] == 'No. of Connections')].index.tolist()
    for conn in ind_conn:
        if f_res["NoOfConnections"] < score['Min Range'].values[conn + 1] and conn != ind_conn[-1]:
            fb_list.append(score["Score"].values[conn])
            break
    else:
        fb_list.append(score["Score"].values[ind_conn[-1]])

    # --------------------------Age of account-------------------------
    ind_age = score[(score['Domain'] == 'Social') & (score['Subcategory'] == 'Age of Account')].index.tolist()
    for ages in ind_age:
        if f_res["AgeOfAccount"] < score['Min Range'].values[ages + 1] and ages != ind_age[-1]:
            fb_list.append(score["Score"].values[ages])
            break
    else:
        fb_list.append(score["Score"].values[ind_age[-1]])
    # --------------------------Activity Score------------------------------
    ind_act = score[(score['Domain'] == 'Social') & (score['Subcategory'] == 'Activity Rate')].index.tolist()
    for act in ind_act:
        if f_res["ActivityRate"] >= score['Min Range'].values[act]:
            fb_list.append(score["Score"].values[act])
            break

            # ---------------------Marital status--------------------------------
    if f_res["MaritalStatus"] == mar_status:
        fb_list.append(
            score[(score['Domain'] == 'Social') & (score['Subcategory'] == 'Marital Status') &
                  (score['Max Range'] == 1)].Score.values[0])
    elif f_res["MaritalStatus"] == "Null":
        fb_list.append(
            score[(score['Domain'] == 'Social') & (score['Subcategory'] == 'Marital Status') &
                  (score['Max Range'] == "Null")].Score.values[0])
    else:
        fb_list.append(
            score[(score['Domain'] == 'Social') & (score['Subcategory'] == 'Marital Status') &
                  (score['Max Range'] == 0)].Score.values[0])
    # --------------------------Qualification----------------------------------
    # edu = self.edu
    if f_res["Qualification"] == edu:
        fb_list.append(
            score[(score['Domain'] == 'Social') & (score['Subcategory'] == 'Qualification Match') &
                  (score['Max Range'] == 1)].Score.values[0])
    elif f_res["Qualification"] == "Null":
        fb_list.append(
            score[(score['Domain'] == 'Social') & (score['Subcategory'] == 'Qualification Match') &
                  (score['Max Range'] == "Null")].Score.values[0])
    else:
        fb_list.append(
            score[(score['Domain'] == 'Social') & (score['Subcategory'] == 'Qualification Match') &
                  (score['Max Range'] == 0)].Score.values[0])

    # ---------------------------Present-location---------------------
    # loc = self.location
    if f_res["PresentLocation"] == loc:
        fb_list.append(
            score[(score['Domain'] == 'Social') & (score['Subcategory'] == 'Present Location') &
                  (score['Max Range'] == 1)].Score.values[0])
    elif f_res["PresentLocation"] == "Null":
        fb_list.append(
            score[(score['Domain'] == 'Social') & (score['Subcategory'] == 'Present Location') &
                  (score['Max Range'] == "Null")].Score.values[0])
    else:
        fb_list.append(
            score[(score['Domain'] == 'Social') & (score['Subcategory'] == 'Present Location') &
                  (score['Max Range'] == 0)].Score.values[0])

    # ----------------------------------RMN--------------------------------
    # mob = "9848327776"
    if f_res["RMN"] == rmn:
        fb_list.append(score[(score['Domain'] == 'Social') & (score['Subcategory'] == 'RMN') &
                             (score['Max Range'] == 1)].Score.values[0])
    else:
        fb_list.append(score[(score['Domain'] == 'Social') & (score['Subcategory'] == 'RMN') &
                             (score['Max Range'] == 0)].Score.values[0])

    # --------------------------Family-Connections----------------------
    # fam_conn = 12
    if f_res["Family"] == fam_con:
        fb_list.append(
            score[(score['Domain'] == 'Social') & (score['Subcategory'] == 'Family Connections') &
                  (score['Max Range'] == 1)].Score.values[0])
    elif f_res["Family"] == "Null":
        fb_list.append(
            score[(score['Domain'] == 'Social') & (score['Subcategory'] == 'Family Connections') &
                  (score['Max Range'] == "Null")].Score.values[0])
    else:
        fb_list.append(
            score[(score['Domain'] == 'Social') & (score['Subcategory'] == 'Family Connections') &
                  (score['Max Range'] == 0)].Score.values[0])
    return sum(fb_list)
