
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import create_engine, MetaData, and_
from sqlalchemy.schema import ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
import traceback
from collections import defaultdict
from uuid import uuid4
import random as r
BASE = declarative_base()
engine = create_engine('postgresql+psycopg2://ubuntu:Intain@107.20.66.231/ubuntu')
class Agent(BASE):
    __tablename__ = 'agenttable'
    name = Column(String,nullable=False)
    agent_id = Column(String,primary_key=True)
    avail = Column(String,nullable=False)
    time_stamp = Column(DateTime)
    password = Column(String, nullable=False)
    email = Column(String,nullable=False)
    company = Column(String, nullable=False)

    def __init__(self,name,agent_id,avail,password,email, company):
        self.name = name
        self.agent_id = agent_id
        self.avail = avail
        self.time_stamp = datetime.datetime.now()+datetime.timedelta(hours=5,minutes=30)
        self.password = password
        self.email = email
        self.company = company

class User(BASE):
    __tablename__ = 'usertable'
    user_id = Column(String,primary_key=True)
    phone_number = Column(String,nullable=False)
    email = Column(String,nullable=False)
    name = Column(String,nullable=False)
    agent_id = Column(String, ForeignKey('agenttable.agent_id'))
    status = Column(String)
    time_stamp = Column(DateTime)
    uid = Column(String)
    geo = Column(String)
    liveliness = Column(String)
    validation = Column(String)
    face = Column(String)
    zipfolder_link = Column(String)
    company = Column(String)
    otp = Column(String)

    def __init__(self,user_id,phone,email,name, company,otp, status='W',id1=None,uid=None,geo=None,liveness=None,validation=None,face=None):
        self.user_id = user_id
        self.phone_number = phone
        self.email = email
        self.name = name
        self.agent_id = id1
        self.status = status
        self.company = company
        self.time_stamp = datetime.datetime.now() + datetime.timedelta(hours=5,minutes=30)
        self.uid = uid
        self.geo = geo
        self.liveliness = liveness
        self.validation = validation
        self.face = face
        self.otp = otp

    #OTP generation
    def rand_num_gen():
        otp=""
        for i in range(6):
            otp+=str(r. randint(1,9))
        return otp
    
    #Check whether the user ID exists in the database. If not create  a new userID.
    def check_user_id(user_id, session):
        user = BASE.metadata.tables['usertable']
        try:
            query_result = session.execute(user.select())
        except:
            print(traceback.print_exc())
            print('Could not fetch phone number')
            return False
        data = [list(row) for row in query_result]
        for row in data:
            if user_id == row[0]:
                return False
        return True

    #Create a  new userID which is not in database. Insertion into database.
    def insert_user_db(session, phone, email, name, company, status='W',id1=None,uid=None):
        flag = True
        print("I am here")
        while(flag):
            user_id = str(uuid4())
            flag = not(User.check_user_id(user_id,session))
        otp_num = User.rand_num_gen()
        u1 = User(user_id=user_id, phone=phone, email=email, name=name, company=company, otp = otp_num)
        session.add(u1)
        print(otp_num,user_id)
        return True, user_id,otp_num

    def insert_user_db(session, phone, email, name, company, status='W',id1=None,uid=None):
        flag = True
        print("I am here")
        while(flag):
            user_id = str(uuid4())
            flag = not(User.check_user_id(user_id,session))
        otp_num = User.rand_num_gen()
        u1 = User(user_id=user_id, phone=phone, email=email, name=name, company=company, otp = otp_num)
        session.add(u1)
        print(otp_num,user_id)
        return True, user_id,otp_num

    #If the user Id and name already exists in database, update otp alone and fetch the user ID
    def generate_newOTP_and_update(session,email,name):
        usId = None
        user = BASE.metadata.tables['usertable']
        newotp = User.rand_num_gen()
        arr = session.query(user.c.user_id,user.c.name).filter(user.c.email==email).all()
        #print(arr)
        for each in range(len(arr)):
            #print(arr[each])
            if str(arr[each][1]).lower() == name.lower():
                usId = arr[each][0]
                break
        print(usId)
        if session.query(user).filter(user.c.user_id==usId).update({'otp':newotp},synchronize_session=False):
            return True, usId, newotp
        else:
            return False, usId, newotp


    #Get OTP corresponding to the userID from the database.
    def get_otp_from_db(session,user_id):
        user = BASE.metadata.tables['usertable']
        otp =  session.query(user.c.otp).filter(user.c.user_id==user_id).first()
        return otp

    def check_email_from_db(session,email_id):
        user = BASE.metadata.tables['usertable']
        try:
            query_result = session.execute(user.select())
        except:
            print(traceback.print_exc())
            print('Could not fetch data')
            return False
        data = [list(row) for row in query_result]
        for row in data:
            if email_id == row[2]:

                return True
        return False

    def get_name_from_db(session,email):
        user = BASE.metadata.tables['usertable']
        name =  session.query(user.c.name).filter(user.c.email==email).all()
        print(name)
        return name

