from celery_config import app
from pymongo import MongoClient
import gridfs
import os
import shutil
from datetime import datetime, timedelta

# ----------------Bio Packages---------------------
from Bio import BioInfo
import bioscore_1 as bs

# -----------------Social packages-----------------------
import fb_final as fb
import gmailparser as gp
import social_score_1 as ss

# ---------------------Financial -------------------------
from Bank_final import Bank
from payslip import PaySlip
from bank_basic import BankInfo
from bankscore_1 import BankScore

# --------------------Cr.Limit --------------------
from crlimit import credit_limit

# ----------------ID Conversion ---------------------
from config import conversion, cities_conv

# ----------------- Profile Score --------------
from profilescore import ProfileScore

@app.task
def lobot(uid):
    try:
        uri = "mongodb://atlmongo:KcNrtLOiTlz3J7UEgzUl978r3GK8ycJu9d3iPYnQ0yr4hYwpQwVatiFOt6NYJurpq4Q4Odmdl0AcSSo6vYkftw==@atlmongo.documents.azure.com:10255/?ssl=true&replicaSet=globaldb"
        client = MongoClient(uri)
        db = client.LOBOT
        doc = db.BorrowerRegInfo.find_one({"UserId": uid})
        mid = doc["MongoUpdatePersonalInfo"]["Emailid"]
        mar_status = conversion(doc["MongoUpdatePersonalInfo"]["MaritalStatus"])
        edu = conversion(doc["MongoUpdatePersonalInfo"]["QualificationTypeId"])
        loc = cities_conv(doc["MongoAddressInfo"]["MongoPresentAddress"]["CityId"])
        rmn = doc["MongoAddressInfo"]["MongoPresentAddress"]["MobileNumber"]
        fam_con = doc["MongoUpdatePersonalInfo"]["NoOfChildren"]
        name = doc["FirstName"] + ' ' + doc["LastName"]
        sal = doc["MongoProfileForSalariedAndProfesionalTypeInfo"]["MonthlyTakeHome"]
        doj = doc["MongoProfileForSalariedAndProfesionalTypeInfo"]["PractisingSince"]
        bank = doc["MongoBankInfo"]["BankId"]
        branch = doc["MongoBankInfo"]["IFSCCode"]
        acc_no = doc["MongoBankInfo"]["AccountNumber"]
        add = doc["MongoAddressInfo"]["MongoPresentAddress"]["AddressLine1"]
        sal_date_temp = doc["MongoProfileForSalariedAndProfesionalTypeInfo"]["SalaryPayDate"]
        sal_date = str(datetime(1, 1, 1) + timedelta(microseconds= sal_date_temp/10))[8:10]
        emp_name = doc["MongoProfileForSalariedAndProfesionalTypeInfo"]["CompanyId"]
        annual_inc = doc["MongoProfileForSalariedAndProfesionalTypeInfo"]["AnnualIncomeRangeId"]

        # -------------------- Profile ----------------------------------------
        pan = doc["MongoUpdatePersonalInfo"]["PANNUMBER"]
        p_code = doc["MongoAddressInfo"]["MongoPresentAddress"]["Pincode"]
        jd = doc["MongoProfileForSalariedAndProfesionalTypeInfo"]["Designation"]
        dept = conversion(doc["MongoProfileForSalariedAndProfesionalTypeInfo"]["DeparmentId"])
        dob = doc["MongoUpdatePersonalInfo"]["DateOfBirth"]
        yom = doc["MongoUpdatePersonalInfo"]["YearOfMarriage"]
        gender = conversion(doc["MongoUpdatePersonalInfo"]["Gender"])
        try:
            spo_prof = conversion(doc["MongoUpdatePersonalInfo"]["SpouseProfessionTypeId"])
        except:
            spo_prof = "#####"

        kids = doc["MongoUpdatePersonalInfo"]["NoOfChildren"]
        lang = conversion(doc["MongoUpdatePersonalInfo"]["MotherTongueLanguageOptionId"])
        manager_no = doc["MongoProfileForSalariedAndProfesionalTypeInfo"]["ReportingManagerContact"]
        friend_no = doc["MongoSecurityInfo"]["BestFriendMobile"]
        neigh_no = doc["MongoSecurityInfo"]["NeighboursMobile"]
        device = "Android"
        # ---------------------------Geo--------------------------
        geo_doc = db.LocationDetails.find_one({"UserId": uid})
        geo_lat = geo_doc["Latitude"]
        geo_lon = geo_doc["Longitude"]
        from_hrs = doc["MongoProfileForSalariedAndProfesionalTypeInfo"]["FromOfficeHours"]
        to_hrs = doc["MongoProfileForSalariedAndProfesionalTypeInfo"]["ToOfficeHours"]
        off_p_code = doc["MongoProfileForSalariedAndProfesionalTypeInfo"]["CompanyAddress"]["Pincode"]
        try:
            sib_no = doc["MongoRelationInfo"]["SiblingInfo"]["MobileNumber"]
        except:
            sib_no = None
        mom_no = doc["MongoRelationInfo"]["MotherMobile"]
        dad_no = doc["MongoRelationInfo"]["FatherMobile"]
        spo_no = doc["MongoUpdatePersonalInfo"]["SpouseMobile"]

        # -----------------Auth Tokens-----------
        try:
            tokens = db.SocialAuthTokenDetails.find_one({"UserId":uid})["TokenDetails"]
            for token in tokens:
                try:
                    if token["Type"] == 1:
                        fb_token = token["Token"]
                except:
                    fb_token = "#####"

            for token1 in tokens:
                try:
                    if token1["Type"] == 2:
                        gmail_token = token1["Token"]
                except:
                    gmail_token = "#####"
        except:
            fb_token = "#####"
            gmail_token = "#####"
        # -----------------------------------------------------------

        user_id = {"UserId": uid}
        rvw_status0 = {"ReviewStatus":1}
        rvw_status1 = {"ReviewStatus":2}
        fs = gridfs.GridFS(db)
        basedir = os.path.join(os.getcwd(), 'upload/', uid + '/')
        os.mkdir(basedir)

        # --------------- Bio --------------------------------
        try:
            front_path = os.path.join(basedir, 'front.jpg')
            print(front_path)
            right_path = os.path.join(basedir, 'right.jpg')
            ff = fs.find_one({"UserId": uid, "filetype": "\"FrontFace\""})
            frf = ff.read()
            with open(front_path, "wb") as front:
                front.write(frf)
            sf = fs.find_one({"UserId": uid, "filetype": "\"RightFace\""})
            sff = sf.read()
            with open(right_path, "wb") as right:
                right.write(sff)
            bio_res = BioInfo(front_path, right_path)
            print(bio_res)
            bio_response = bio_res.main()
            score_bio = {"Score": bs.b_score(bio_response)}
            print(score_bio)
            response_bl = reduce(lambda x, y: dict(x, **y), (bio_response, user_id, score_bio, rvw_status0))
            response_bm = reduce(lambda x, y: dict(x, **y), (bio_response, user_id, score_bio, rvw_status1))
            db.Bio.insert_one(response_bl)
            db.Bio.insert_one(response_bm)
        except ImportError:
            bio_response1 = "Too many Faces Found or No Face Found !! "
            bio_err = {'Error': bio_response1}
            print(bio_err)
            bio_response_errl = reduce(lambda x, y: dict(x, **y), (bio_err, user_id, rvw_status0))
            bio_response_errm = reduce(lambda x, y: dict(x, **y), (bio_err, user_id, rvw_status1))
            db.Bio.insert_one(bio_response_errm)
            db.Bio.insert_one(bio_response_errl)
            score_bio = {"Score": 0}
        except:
            bio_err1 = {'Error': 'Unable to read image'}
            bio_response_err1l = reduce(lambda x, y: dict(x, **y), (bio_err1, user_id, rvw_status0))
            bio_response_err1m = reduce(lambda x, y: dict(x, **y), (bio_err1, user_id, rvw_status1))
            db.Bio.insert_one(bio_response_err1l)
            db.Bio.insert_one(bio_response_err1m)
            score_bio = {"Score": 0}
            print(bio_err1)

        # --------------------Social------------------------------
        soc_err = {"Error": "Invalid Token"}
        try:
            fb_response1 = fb.face_book(fb_token)
            act_loc = fb_response1["ActiveLocation"]
            fb_score = {'Score': ss.fb_score(fb_response1, mar_status, edu, loc, rmn, fam_con)}
            response_fbl = reduce(lambda x, y: dict(x, **y), (fb_response1, user_id, fb_score, rvw_status1))
            response_fbm = reduce(lambda x, y: dict(x, **y), (fb_response1, user_id, fb_score, rvw_status0))
            db.Facebook.insert_one(response_fbl)
            db.Facebook.insert_one(response_fbm)
        except:
            act_loc = ["######"]
            db.Facebook.insert_one(reduce(lambda x, y: dict(x, **y), (user_id, soc_err, rvw_status0)))
            db.Facebook.insert_one(reduce(lambda x, y: dict(x, **y), (user_id, soc_err, rvw_status1)))
            fb_score = {'Score': 0}
            print("Invalid FB Token")
        try:
            g_email = mid
            g_response2 = gp.info_mail(g_email, gmail_token)
            gm_score = {'Score': ss.g_score(g_response2) + 1}
            response_gl = reduce(lambda x, y: dict(x, **y), (g_response2, user_id, gm_score, rvw_status0))
            response_gm = reduce(lambda x, y: dict(x, **y), (g_response2, user_id, gm_score, rvw_status1))
            db.Mail.insert_one(response_gm)
            db.Mail.insert_one(response_gl)
        except:
            gm_score = {'Score': 0}
            db.Mail.insert_one(reduce(lambda x, y: dict(x, **y), (user_id, soc_err, rvw_status0)))
            db.Mail.insert_one(reduce(lambda x, y: dict(x, **y), (user_id, soc_err, rvw_status1)))
            print("Invalid Gmail Authentication Details")

        # ------------------------Financial -------------------------

        try:
            bs_path = os.path.join(basedir, 'statement.pdf')
            ps_path = os.path.join(basedir, 'payslip.pdf')
            bst = fs.find_one({"UserId": uid, "filetype": "\"BankStatement\""})
            bst_r = bst.read()
            with open(bs_path, "wb") as b_file:
                b_file.write(bst_r)
            pst = fs.find_one({"UserId": uid, "filetype": "\"Payslip\""})
            pst_r = pst.read()
            with open(ps_path, "wb") as p_file:
                p_file.write(pst_r)
            ps_resp = PaySlip(ps_path, name, sal, doj)
            resp_ps = ps_resp.main()
            doj_p = resp_ps["DateOfJoin"]
            response_psl = reduce(lambda x, y: dict(x, **y), (resp_ps, user_id, rvw_status0))
            response_psm = reduce(lambda x, y: dict(x, **y), (resp_ps, user_id, rvw_status1))
            db.Payslip.insert_one(response_psl)
            db.Payslip.insert_one(response_psm)
            print("Payslip Done")
        except:
            doj_p = "Unavailable"
            ps_err = {"Error": "File Format not supported"}
            db.Payslip.insert_one(reduce(lambda x, y: dict(x, **y), (ps_err, user_id, rvw_status0)))
            db.Payslip.insert_one(reduce(lambda x, y: dict(x, **y), (ps_err, user_id, rvw_status1)))

        try:
            resp_bf = Bank(bs_path, bank, emp_name)
            ban_res = resp_bf.main()
            print(ban_res)
            A = ban_res["AverageSalary"]
            B = ban_res["AvgEmi"]
            resp_bb = BankInfo(bs_path, branch, acc_no, add, bank, emp_name)
            bb_res = resp_bb.main()
            print(bb_res)
            resp_bs = BankScore(ban_res, bb_res, resp_ps, sal, sal_date, emp_name, annual_inc)
            fin_score = {'Score': resp_bs.score()}
            print(fin_score)
            response_finl = reduce(lambda x, y: dict(x, **y), (ban_res, bb_res, user_id, fin_score, rvw_status0))
            response_finm = reduce(lambda x, y: dict(x, **y), (ban_res, bb_res, user_id, fin_score, rvw_status1))
            db.Bank.insert_one(response_finm)
            db.Bank.insert_one(response_finl)
            print("Bank Done")
        except:
            A = 0
            B = 0
            fin_err1 = {'Error': "File Format Error"}
            db.Bank.insert_one(reduce(lambda x, y: dict(x, **y), (fin_err1, user_id, rvw_status0)))
            db.Bank.insert_one(reduce(lambda x, y: dict(x, **y), (fin_err1, user_id, rvw_status1)))
            fin_score = {"Score": 0}
            print("Bank File format error")

        # -----------------Profile Score -------------------------

        resp_prof = ProfileScore(pan, rmn, mid, p_code, jd, dept, emp_name, dob, yom, mar_status, gender, edu,
                                 doj, spo_prof, kids, lang, uid, loc, name, device, friend_no, neigh_no,
                                 manager_no, act_loc, doj_p, geo_lat, geo_lon, from_hrs, to_hrs,off_p_code, sib_no, dad_no,
                                 mom_no, spo_no)
        score_profile = resp_prof.result()
        print(score_profile)

        # ----------------- Total Score -----------------
        score_final = score_bio["Score"] + fb_score["Score"] + gm_score["Score"] + fin_score["Score"] + score_profile
        print(score_final)
        print(A)
        cr_limit = credit_limit(score_final, A, B)
        print(cr_limit)
        db.CreditLimit.insert_one({"UserId": uid,'CreditLimit': cr_limit, 'Score': score_final, 'ReviewStatus': 1})
        shutil.rmtree(basedir)
    except Exception as e:
        print(e)
        db.CreditLimit.insert_one({"UserId": uid, 'CreditLimit': 0,'Score': 0, 'ReviewStatus': 2})



