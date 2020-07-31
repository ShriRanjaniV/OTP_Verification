
from sqlalchemy.orm import sessionmaker
import traceback
from sqlalchemy import create_engine, MetaData
from models.cous_exc import Agent,  User
from uuid import uuid4
import json
import requests

#BASE = declarative_base()
engine = create_engine('postgresql+psycopg2://ubuntu:Intain@107.20.66.231/ubuntu')

def fail(session,message):
    session.rollback()
    session.close()
    print(message)
    return False, message

def add_user(phone, email, name, company, status='W',id1=None):
    try:
        Session = sessionmaker(bind = engine)
        session = Session()
        #If email exists in db, comapre the names, if email and names match, update otp by fetching the existing userID
        check = User.check_email_from_db(session,email)
        print(check)
        if check == True:
            names_from_db = User.get_name_from_db(session,email)
            #print(str(list(name_from_db)[0]).lower())
            print(name.lower())
            name = name.lower()
            newl = []
            for name_from_db in names_from_db:
                newl.append(str(list(name_from_db)[0]).lower())
                #print(str(list(name_from_db)[0]).lower())
            if name.lower() in newl:
                print("hgfjhgkjh")
                usdb, user_id, otp = User.generate_newOTP_and_update(session,email,name)
                if not usdb:
                    ret,ret1 = fail(session,'Could not add user in DB')
                    return ret,ret1
                    

            else:
                usdb, user_id, otp = User.insert_user_db(session, phone=phone, email=email, name=name, company=company, status='W')
                if not usdb:
                    ret,ret1 = fail(session,'Could not add user in DB')
                    return ret,ret1
                #break
        else:
            usdb, user_id,otp = User.insert_user_db(session, phone=phone, email=email, name=name, company=company, status='W')
            if not usdb:
                ret,ret1 = fail(session,'Could not add user in DB')
                return ret,ret1

        session.commit()
        session.close()
    except:
        print(traceback.print_exc())
        ret,ret1 = fail(session,'Could not add user')
        return ret,ret1
    
    finally:
        session.close()
    
    data = {'email': email, 'user_id': user_id, 'company': company,'otp':otp}
    return True, data

def verifyOTP(otp_entered,user_ID):
    result = ''
    flag = True
    try:
            Session = sessionmaker(bind = engine)
            session = Session()
            res = User.get_otp_from_db(session,user_ID)
            print(res)
            if res == None:
                result = 'User ID not in DB'
                return False,result
            otp_database = [str(a) for a in res]
            print(otp_database)
            session.commit()
            if otp_database[0] == otp_entered:
                result = "OTP verified"
                flag = True
            else:
                result = "Incorrect OTP. Please try again"
                flag = False

            
    except:
            print(traceback.print_exc())
            session.rollback()
            session.close()
            flag = False
            return flag,result
    finally:
            session.close()
    return flag,result





