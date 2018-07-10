from celery_config import app
from pymongo import MongoClient

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


@app.task
def bio_task(bio_data):
    uri = "mongodb://atlmongo:KcNrtLOiTlz3J7UEgzUl978r3GK8ycJu9d3iPYnQ0yr4hYwpQwVatiFOt6NYJurpq4Q4Odmdl0AcSSo6vYkftw==@atlmongo.documents.azure.com:10255/?ssl=true&replicaSet=globaldb"
    client = MongoClient(uri)
    db = client.LOBOT
    try:
        uid = bio_data["UserID"]
        doc = db.BorrowerInfo.find_one({"UserID": uid})
        front = doc["front"]
        right = doc['right']
        bio_res = BioInfo(front, right)
        response = bio_res.main()
        d3 = {"UserID": uid}
        d4 = {"Score": bs.b_score(response)}
        response_b = reduce(lambda x, y: dict(x, **y), (response, d3, d4))
        db.Bio.insert_one(response_b)
    except ImportError:
        d6 = {"UserID": uid}
        response1 = "Too many Faces Found or No Face Found !! "
        err = {'Error': response1}
        response_err = reduce(lambda x, y: dict(x, **y), (err, d6))
        db.Bio.insert_one(response_err)
    except:
        d7 = {"UserID": uid}
        response2 = "Unable to read image!!"
        err1 = {'Error': response2}
        response_err1 = reduce(lambda x, y: dict(x, **y), (err1, d7))
        db.Bio.insert_one(response_err1)


@app.task
def social_task(tokens):
    uri = "mongodb://atlmongo:KcNrtLOiTlz3J7UEgzUl978r3GK8ycJu9d3iPYnQ0yr4hYwpQwVatiFOt6NYJurpq4Q4Odmdl0AcSSo6vYkftw==@atlmongo.documents.azure.com:10255/?ssl=true&replicaSet=globaldb"
    client = MongoClient(uri)
    db = client.LOBOT
    try:
        uid = tokens["UserID"]
        g_token = tokens["GmailToken"]
        fb_token = tokens["FBToken"]
        doc = db.BorrowerInfo.find_one({"UserID": uid})
        email = doc["EmailID"]
        mar_status = doc["MaritalStatus"]
        edu = doc["HighestQualification"]
        loc = doc["PresentLocation"]
        rmn = doc["MobileNumber"]
        fam_con = doc["FamilyConnections"]
        d3 = {"UserID": uid}
        err = {"Error": "Invalid Token"}
        try:
            response1 = fb.face_book(fb_token)
            d5 = {'Score': ss.fb_score(response1, mar_status, edu, loc, rmn, fam_con)}
            response_a = reduce(lambda x, y: dict(x, **y), (response1, d3, d5))
            db.Facebook.insert_one(response_a)
        except:
            db.Facebook.insert_one(reduce(lambda x, y: dict(x, **y), (d3, err)))
        try:
            response2 = gp.info_mail(email, g_token)
            d4 = {'Score': ss.g_score(response2)}
            response_b = reduce(lambda x, y: dict(x, **y), (response2, d3, d4))
            db.Mail.insert_one(response_b)
        except:
            db.Mail.insert_one(reduce(lambda x, y: dict(x, **y), (d3, err)))
    except:
        db.Mail.insert_one(reduce(lambda x, y: dict(x, **y), ({"UserID":tokens["UserID"]}, {"Error":"Key Error"})))


@app.task
def fin_task(data):
    uri = "mongodb://atlmongo:KcNrtLOiTlz3J7UEgzUl978r3GK8ycJu9d3iPYnQ0yr4hYwpQwVatiFOt6NYJurpq4Q4Odmdl0AcSSo6vYkftw==@atlmongo.documents.azure.com:10255/?ssl=true&replicaSet=globaldb"
    client = MongoClient(uri)
    db = client.LOBOT
    try:
        uid = data["UserID"]
        doc = db.BorrowerInfo.find_one({"UserID": uid})
        name = doc["Name"]
        emp_id = doc["EmployeeID"]
        sal = doc["MonthlyIncome"]
        doj = doc["DateOfJoining"]
        file_path = doc["BankStatementPath"]
        pay_fp = doc["PaySlipPath"]
        bank = doc["BankName"]
        branch = doc["BankBranchName"]
        acc_no = doc["AccountNumber"]
        add = doc["Address"]
        sal_date = doc["SalaryDate"]
        d3 = {"UserID": uid}
        try:
            resp = PaySlip(pay_fp, name, emp_id, sal, doj)
            resp3 = resp.main()
            response_p = reduce(lambda x, y: dict(x, **y), (resp3, d3))
            db.Payslip.insert_one(response_p)
            print("Payslip Done")
        except:
            err2 = {"Error": "File Format not supported"}
            resp_err2 = reduce(lambda x, y: dict(x, **y), (err2, d3))
            db.Payslip.insert_one(resp_err2)

        try:
            resp1 = Bank(file_path, bank, emp_id)
            d1 = resp1.main()
            resp2 = BankInfo(file_path, branch, acc_no, add, bank, emp_id)
            d2 = resp2.main()
            resp4 = BankScore(d1, d2, resp3, sal, sal_date, emp_id)
            d4 = {'Score': resp4.score()}
            response_b = reduce(lambda x, y: dict(x, **y), (d1, d2, d3, d4))
            db.Bank.insert_one(response_b)
            print("Bank Done")
        except:
            err1 = {'Error': "File Format Error"}
            resp_err1 = reduce(lambda x, y: dict(x, **y), (err1, d3))
            db.Bank.insert_one(resp_err1)
    except:
        err_key = {'Error': "Unable to find some keys"}
        err_k = reduce(lambda x, y: dict(x, **y), (err_key, {"UserID":data["UserID"]}))
        db.Bank.insert_one(err_k)























