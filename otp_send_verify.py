from flask import Flask, request, jsonify
import traceback
from flask_cors import CORS
import smtplib
from hashlib import sha256
from geopy.geocoders import Nominatim
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from lib import db_ops
app = Flask(__name__)
CORS(app)

def get_email_content(link):
    return f'''
        <div style="background-color:#fff;margin:0 auto 0 auto;padding:30px 0 30px 0;color:#4f565d;font-size:13px;line-height:20px;font-family:'Helvetica Neue',Arial,sans-serif;text-align:left">
            <center>
            <table style="width:550px;text-align:center">
                <tbody><tr>
                    <td style="padding:0 0 20px 0;border-bottom:1px solid #e9edee; text-align:left; ">
                        <h2 style="font-family: trebuchet ms,sans-serif;">
                            Greetings! 
                        </h2>
                        <div style="font-size: larger;">
                            Thank you for your Interest to Open an Account with us.                
                        </div>
                        <br>
                        <div style="margin-block-end: 0; font-size: larger;">
                            Please read the instructions carefully before you start your application.    
                        </div>
                    </td>
                </tr>
                <tr>
                    <td colspan="2" style="padding-bottom:10px; border-bottom:1px solid #e9edee; ">               
                        </span>
                            <p style="margin:20 10px 10px 10px;padding:0">
                                <span style="font-family: trebuchet ms,sans-serif; color: #4f565d; font-size: 15px; line-height: 20px;">
                                    Below is the OTP to start your Video KYC
                                </span>
                            </p>
                        <span>
                            <p>
                                <a style="display:inline-block;text-decoration:none;padding:15px 20px;background-color:#048c88;border:1px solid #048c88;border-radius:3px;color:#fff;font-weight:bold; font-size: medium" href="{link}" target="_blank" >
                                    {link}
                                </a>
                            </p>
                        </span>
                        
                    </td>
                </tr>
                <tr>
                    <td style="padding-bottom: 20px; text-align:left;">
                        <h3 style="margin-block-end: 0px;">Important Instructions</h3>
                        <div style="display: flex; justify-content: center; font-size: 15px;">
                            <ol style="text-align: left; color: #575757;">
                                <li style="padding: 0px 0px 3px 5px;">
                                    Please keep your Aadhaar XML and Pan Card Ready.
                                </li> 
                                <li style="padding: 0px 0px 3px 5px;">
                                    Please be in a well lit room/area. 
                                </li> 
                                <li style="padding: 0px 0px 3px 5px;">
                                    Please be in a place with less/no noise.
                                </li> 
                                <li style="padding: 0px 0px 3px 5px;">
                                    Follow the instructions of Customer Executive Carefully
                                </li>
                            </ol>
                        </div>
                        <p style="margin-block-start: 0px; font-size: larger;">
                            Thank you for your time. Have a nice day! 
                        </p>

                    </td>
                </tr>
                <tr>
                    <td colspan="2" style="padding:30px 0 0 0;border-top:1px solid #e9edee;color:#9b9fa5">
                        If you have any questions you can get in touch at <a style="color:#666d74;text-decoration:none" href="mailto:explore@in-d.ai" target="_blank">explore@in-d.ai</a>
                    </td>
                </tr>
            </tbody></table>
            </center>
        </div></div>'''


def check_null(*args):
    for i in args:
        if not i:
            return False
    return True

def mailing(otp, email):
    s = smtplib.SMTP('smtp.gmail.com', 587) 
    s.ehlo()
    s.starttls() 
    s.ehlo()
    s.login("aitest@intainft.com", "Intain@2019")
    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'Thank you for your interest in VideoKYC'
    msg['From'] = "aitest@intainft.com"
    msg['To'] = email
    body = otp
    body = get_email_content(body)
    body = MIMEText(body,'html')
    msg.attach(body) 
    s.sendmail("aitest@intainft.com", email, msg.as_string()) 
    s.quit() 

app = Flask(__name__)
@app.route('/mail_insert',methods=['POST'])
def mailandinsert():
    try:
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        company = request.form['company']
    except:
        print(traceback.print_exc())
        return jsonify({
                'status': 'fail',
                'flag': 'F',
                'desc': 'Failed'
            }), 207
    try:
        check = check_null(name, email, phone, company)
        if not check:
            return jsonify({
                'status': 'fail',
                'flag': 'F',
                'desc': 'One of the input were null'
            }), 207 
        print('Data:', name,email,phone)
        flag, data = db_ops.add_user(phone, email, name, company=company)
        if flag:
                mailflag = True
                try:
                    mailing(data['otp'], data['email'])
                except:
                    print(traceback.print_exc())
                    mailflag = False

                return jsonify({
                    'status': 'success',
                    'flag': 'C',
                    'UserID': data['user_id'],
                    'OTP':data['otp'],
                    'mail': mailflag
                }), 200
            
        else:
            return jsonify({
                    'status': 'Insertion Failed',
                    'flag': 'F',
                    'desc': data
                }), 207
    except:
        print(traceback.print_exc())
        return jsonify({
                'status': 'fail',
                'flag': 'F',
                'desc': 'Failed'
            }), 207   

@app.route('/otpverify',methods=['POST'])
def compare():
        try:
            otp_entered = request.form['otp']
            user_ID = request.form['userID']
        except:
            print(traceback.print_exc())
            return jsonify({
                    'status': 'fail',
                    'flag': 'F',
                    'desc': 'Failed'
                }), 207 
        
        
        try:
            check = check_null(otp_entered,user_ID)
            if not check:
                return jsonify({
                    'status': 'fail',
                    'flag': 'F',
                    'desc': 'One of the input were null'
                }), 207 
            print('Data:', otp_entered,user_ID)
            flag, res = db_ops.verifyOTP(otp_entered,user_ID)
            return jsonify({
                        'status': res,
                        'flag': 'F',
                        'desc': ''
                    }), 207
            

        except:
            print(traceback.print_exc())
            return jsonify({
                    'status': 'fail',
                    'flag': 'F',
                    'desc': 'Failed'
                }), 207   

if __name__ == "__main__":
    app.debug=True
    app.run(host="0.0.0.0",use_reloader=True, port=5412,threaded=True)

