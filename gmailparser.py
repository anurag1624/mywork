"""Fetching the latest GMail email using OAuth 2 and IMAP.
Requires requests-oauthlib, which is available on pypi.
Includes a basic SASL XOAUTH2 authentication method for imaplib.
"""

from requests_oauthlib import OAuth2Session
import email
import imaplib
import datetime


def xoauth_authenticate(email, token):
    access_token = token

    def _auth(*args, **kwargs):
        return 'user=%s\1auth=Bearer %s\1\1' % (email, access_token)

    return 'XOAUTH2', _auth


def mails(subjects, email_id, access_token):
    info = []

    try:
        count = 0
        for i in subjects:
            print('Searching...'+ i)
            mail = imaplib.IMAP4_SSL('imap.gmail.com')
            mail.authenticate(*xoauth_authenticate(email_id, access_token))
            mail.select('Inbox')
            start_date = datetime.datetime.now() + datetime.timedelta(-30)
            start_date = str(start_date.date())
            months = {'01':'Jan','02':'Feb','03':'Mar','04':'Apr','05':'May','06':'Jun',
                      '07':'Jul','08':'Aug', '09':'Sep', '10':'Oct', '11':'Nov', '12':'Dec'}
            d = str(start_date[-2:])
            m = months[str(start_date[5:7])]
            y = str(start_date[0:4])
            s_date = str(d+'-'+m+'-'+y)
            latest_id = mail.search(None, '(SUBJECT ' + '"' + i + '")',  '(SINCE ' + '"' + s_date + '")')[1][0].split()[-1]
            raw = mail.fetch(latest_id, "(RFC822)")[1][0][1]
            message = email.message_from_string(raw)
            for part in message.walk():
                if part.get_content_maintype() != 'multipart' and part.get('Content-Disposition') is not None:
                    open('/home/siva' + '/' + part.get_filename(), 'wb').write(part.get_payload(decode=True))
                    if part.get_filename() is not None:
                        # print("found")
                        # print("part file not found")
                        info.append(part.get_filename())
                        info.append(message['date'])

                else:
                    if i == "Early Salary":
                        count = count + 1
                        # print(count)
                        info.append(message['date'])
    except IndexError:
        pass

    return info


def info_mail(email_id, access_token):
    mail_info = {}
    ps_sub = ["pay slip", "payslip"]
    bs_sub = [ "bank statement"]
    cc_sub = ["Credit Card Statement"]
    mob_sub = ["Airtel Bill"]
    off_sub = ["Offer Letter"]
    comp_sub = ["Early Salary"]

    # ------------------Pay slip----------------------------
    mail_info['PayslipFile'] = mails(ps_sub, email_id, access_token)
    if len(mail_info['PayslipFile']) >1:        
        mail_info['PaySlip'] = "Retrieved"
    else:
        mail_info['PaySlip'] = "Not Retrieved"

    # ----------------------Bank Statement-----------------
    mail_info['BankStatementFile'] = mails(bs_sub, email_id, access_token)
    if len(mail_info['BankStatementFile']) >1:
        mail_info['BankStatement'] = "Retrieved"
    else:
        mail_info['BankStatement'] = "Not Retrieved"

    # ------------------------Credit card statement-------------
    mail_info['CreditCardStatementFile'] = mails(cc_sub, email_id, access_token)
    if len(mail_info['CreditCardStatementFile']) >1:
        mail_info['CreditCardStatement'] = "Retrieved"
    else:
        mail_info['CreditCardStatement'] = "Not Retrieved"
    # -----------------No Of Credit Cards---------------
    if len(mail_info['CreditCardStatementFile']) != 0:
        mail_info['NoOfUniqueCreditCards'] = len(mail_info['CreditCardStatementFile']) / 2
    else:
        mail_info['NoOfUniqueCreditCards'] = 0
    # ----------------Mobile Bill---------------------------
    mail_info['MobileBillFile'] = mails(mob_sub, email_id, access_token)
    if len(mail_info['MobileBillFile']) >1:
        mail_info['MobileBill'] = "Retrieved"
    else:
        mail_info['MobileBill'] = "Not Retrieved"
    # ----------------Offer Letter--------------------------
    mail_info['OfferLetterFile'] = mails(off_sub, email_id, access_token)
    if len(mail_info['OfferLetterFile']) != 0:
        mail_info['OfferLetter'] = "Retrieved"
    else:
        mail_info['OfferLetter'] = "Not Retrieved"
    # ------------------Competitors found -------------
    if len(mails(comp_sub, email_id, access_token)) != 0:
        mail_info['CompetitorsFound'] = len(mails(comp_sub, email_id, access_token))
    else:
        mail_info['CompetitorsFound'] = 0

    return mail_info

# k = info_mail('anytimeloanapp@gmail.com','ya29.Glu3BTpHOgpNbp53r5U4q_H9E8weLGDCNNsqAFQ6cL0dA-U_ci47bOHNQ651Qq-0oTE_rd2tghIaMoEVtgGioZbXsVGq-WomvKz7th9VkUyDdfjGR89mkjDCB-Ys')

