from flask import Flask, render_template, request, redirect, session
from flask_session import Session
import requests


# Configure app
app = Flask(__name__)

# Configuration Of Auto Reload Of All The Templates
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["POST", "GET"])
def index():
    try:
        if session["log_email"] is not None:
            return redirect("/gdashboard")
        else:
             return render_template('index.html')
    except:
       pass
    try:
        if session["log_user_email"] is not None:
            return redirect("/dashboard")
        else:
            return render_template('index.html')
    except:
        pass
    return render_template("index.html")

@app.route("/login", methods=["POST","GET"])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        url = "https://espnodewebsite.000webhostapp.com/API/loginapi.php"
        params = {
            "email": email,
            "password": password
        }
        r2 = requests.post(url=url, data=params)
        # print(r2.text)

        res = r2.json()
        ev = res['error']
        if not ev:
            uloginid = res['user']['LOGIN_ID']
            role = res['user']['ROLE']
            ufname = res['user']['FIRST_NAME']
            ulname = res['user']['LAST_NAME']
            ugender = res['user']['GENDER']
            uaddress = res['user']['ADDRESS']
            uemail = res['user']['EMAIL_ID']
            uhex = res['user']['HEXCODE']
            uphone=res['user']['PHIONE_NO']

            # This will store information of guard.
            if role == "0":
                session['log_email'] = uemail
                session['log_role'] = role
                session['log_id'] = uloginid
                session['log_fname'] = ufname
                session['log_lname'] = ulname
                session['log_gender'] = ugender
                session['log_address'] = uaddress
                session['log_uhex'] = uhex
                session['log_phone'] = uphone
                return redirect("/gdashboard")

            # This will store information of admin.
            else:
                session['log_user_email'] = uemail
                session['log_user_id'] = uloginid
                session['log_user_fname'] = ufname
                session['log_user_lname'] = ulname
                session['log_user_gender'] = ugender
                session['log_user_address'] = uaddress
                session['log_user_uhex'] = uhex
                session['log_user_phone'] = uphone
                session['log_user_role'] = role

                return redirect("/dashboard")

    try:
        if session["log_email"] is not None:
            return redirect("/gdashboard")
        else:
             return render_template('index.html')
    except:
       pass
    try:
        if session["log_user_email"] is not None:
            return redirect("/dashboard")
        else:
            return render_template('index.html')
    except:
        pass
    return render_template('index.html')

@app.route("/dashboard")
def admin_dashboard():
    try:
        if session['log_user_email'] is None:
            return redirect("/login")
        else:
            records = {}
            url = "https://espnodewebsite.000webhostapp.com/API/fetchwarningsensordataapi.php"
            response = requests.get(url=url)
            warning_res = response.json()
            last_val= []
            ev = warning_res['error']
            records['data'] = warning_res
            for i in records["data"]["warning_table"]:
                last_val.append(i)
            irsensor_value=last_val[-1]["IR_VALUE"]
            pirsensor_value=last_val[-1]["PIR_VALUE"]
            ultrasonicsensor_value=last_val[-1]["ULTRASONIC_VALUE"]
            ldrsensor_value=last_val[-1]["LDR_VALUE"]
            context={'irvalue':irsensor_value,
                     "pirvalue":pirsensor_value,
                     "ultravalue":ultrasonicsensor_value,
                     "ldrvalue":ldrsensor_value
                    }
            return render_template('dashboard.html',context=context)
    except:
        pass
    return render_template('index.html')

@app.route("/profile")
def profile():
    try:
        if session["log_user_email"] is None:
            return render_template('index.html')
        else:
            return render_template('profile.html')
    except:
        pass
    return render_template('index.html')

@app.route("/gprofile")
def guard_profile():
    try:
        if session["log_email"] is None:
            return redirect("/login")
        else:
            return render_template('guard_profile.html')
    except:
        pass
    return render_template('index.html')

@app.route("/sitemap")
def admin_map():
    try:
        if session["log_user_email"] is None:
            return redirect("/login")
        else:
            return render_template('sitemap.html')
    except:
        pass
    return render_template('index.html')

@app.route("/logout")
def logout():
    try:
        del session['log_user_email']
        del session['log_user_id']
        del session['log_user_fname']
        del session['log_user_lname']
        del session['log_user_gender']
        del session['log_user_address']
        del session['log_user_uhex']
        del session['log_user_phone']
        del session['log_user_role']

    except:
        pass
    return render_template('logout.html')

@app.route("/glogout")
def guard_logout():
    try:
        del session['log_email']
        del session['log_id']
        del session['log_fname']
        del session['log_lname']
        del session['log_gender']
        del session['log_address']
        del session['log_uhex']
        del session['log_phone']
        del session['log_role']
    except:
        pass
    return render_template('guard_logout.html')

@app.route("/crossing")
def admin_crossing():
    try:
        if session['log_user_email'] is None:
            return redirect("/login")
        else:
            url = "https://espnodewebsite.000webhostapp.com/API/fetchldrsensorapi.php"
            response = requests.get(url=url)
            r2 = response.json()
            records1={}
            records1['data'] = r2
            # ldrvalue={}
            # ldrgraphdata=[]
            # ldrgraphtime=[]
            # ldrvalue['ldr_val']= r2['ldr']
            # for i in ldrvalue['ldr_val']:
            #     ldrgraphdata.append(i['LDR_VALUE'])
            #     ldrgraphtime.append(i['READING_TIME'][11:16])
            # ev = r2['error']
            # fig, ax = plt.subplots()
            # ax.barh(ldrgraphtime[::10], ldrgraphdata[::10], align='center')
            # plt.savefig('hackathon/static/src/images/ldr/ldr_crossing.jpg')
            return render_template('Level_crossing.html', records1=records1)
    except:
        pass
    return render_template("index.html")

@app.route("/obstacle")
def admin_obstacle():
    try:
        if session["log_user_email"] is None:
            return redirect("/login")
        else:
            url = "https://espnodewebsite.000webhostapp.com/API/fetchirsensordata.php"
            response = requests.get(url=url)
            ir_res = response.json()
            records = {}
            records['data'] = ir_res
            # irvalue={}
            # irgraph=[]
            # irtime=[]
            # irvalue['ir_val'] = records['data']['ir']
            # for i in irvalue['ir_val']:
            #     irgraph.append(i['IR_VALUE'])
            #     irtime.append(i['READING_TIME'][11:16])
            # fig, ax = plt.subplots()
            # ax.barh(irtime, irgraph, align='center')
            # plt.savefig('hackathon/static/src/images/ir/ir_obstacle.jpg')
            return render_template('Obstacle detection.html',records=records)
    except:
        pass
    return render_template('index.html')

@app.route("/human")
def admin_human():
    try:
        if session["log_user_email"] is None:
            return redirect("/login")
        else:
            url = "https://espnodewebsite.000webhostapp.com/API/fetchpirsensordata.php"
            response = requests.get(url=url)
            pir_res = response.json()
            records = {}
            records['data'] = pir_res
            # pirvalue={}
            # pirgraph=[]
            # pirtime=[]
            # pirvalue['pir_val'] = records['data']['pir']
            # for i in pirvalue['pir_val']:
            #     pirgraph.append(i['PIR_VALUE'])
            #     pirtime.append(i['READING_TIME'][11:16])
            # fig, ax = plt.subplots()
            # ax.barh(pirtime[::5], pirgraph[::5], align='center')
            # plt.savefig('hackathon/static/src/images/pir/pir_human.jpg')
            return render_template('Human Detection.html',records=records)
    except:
        pass
    return render_template('index.html')

@app.route("/distance")
def admin_distance():
    try:
        if session['log_user_email'] is None:
            return redirect("/login")
        else:
            url = "https://espnodewebsite.000webhostapp.com/API/fetchultrasonic.php"
            response = requests.get(url=url)
            ultra_res = response.json()
            records = {}
            records['data'] = ultra_res
            # ultravalue = {}
            # ultragraph = []
            # ultratime = []
            # ultravalue['ultra_val'] = records['data']['ultrasonic']
            # for i in ultravalue['ultra_val']:
            #     ultragraph.append(i['ULTRASONIC_VALUE'])
            #     ultratime.append(i['READING_TIME'][11:16])
            # fig, ax = plt.subplots()
            # ax.barh(ultratime, ultragraph, align='center')
            # plt.savefig('hackathon/static/src/images/ultra/ultra_distance.jpg')
            return render_template('Distance Calculator.html',records=records)
    except:
        pass
    return render_template('index.html')

@app.route("/warning")
def admin_warning():
    try:
        if session['log_user_email'] is None:
            return redirect("/login")
        else:
            url = "https://espnodewebsite.000webhostapp.com/API/fetchwarningsensordataapi.php"
            response = requests.get(url=url)
            ultra_res = response.json()
            records = {}
            records['data'] = ultra_res
            return render_template('datatable.html',records)
    except:
        pass
    return render_template('index.html')

@app.route("/gdashboard")
def guard_dashboard():
    try:
        if session['log_email'] is None:
            return redirect("/login")
        else:
            records = {}
            url = "https://espnodewebsite.000webhostapp.com/API/fetchwarningsensordataapi.php"
            response = requests.get(url=url)
            warning_res = response.json()
            last_val= []
            ev = warning_res['error']
            records['data'] = warning_res
            for i in records["data"]["warning_table"]:
                last_val.append(i)
            irsensor_value=last_val[-1]["IR_VALUE"]
            pirsensor_value=last_val[-1]["PIR_VALUE"]
            ultrasonicsensor_value=last_val[-1]["ULTRASONIC_VALUE"]
            ldrsensor_value=last_val[-1]["LDR_VALUE"]
            context={'irvalue':irsensor_value,
                     "pirvalue":pirsensor_value,
                     "ultravalue":ultrasonicsensor_value,
                     "ldrvalue":ldrsensor_value
                    }
            return render_template('guard_dashboard.html',context=context)
    except:
        pass
    return render_template('index.html')

@app.route("/add")
def admin_add():
    try:
        if session["log_user_email"] is None:
            return render_template('index.html')
        else:
            if request.method == 'POST':
                fname = request.form.get("fname")
                lname = request.form.get("lname")
                email = request.form.get("email")
                phone = request.form.get("phone")
                address = request.form.get("address")
                gender = request.form.get("inlineRadioOptions")
                hexcode = request.form.get('hexcode')

                # Random Password generator code
                import random
                import array
                MAX_LEN = 12
                DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

                LOCASE_CHARACTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',

                                     'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q',

                                     'r', 's', 't', 'u', 'v', 'w', 'x', 'y',

                                     'z']

                UPCASE_CHARACTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',

                                     'I', 'J', 'K', 'M', 'N', 'O', 'P', 'Q',

                                     'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',

                                     'Z']

                SYMBOLS = ['@', '#', '$','*']
                COMBINED_LIST = DIGITS + UPCASE_CHARACTERS + LOCASE_CHARACTERS + SYMBOLS

                rand_digit = random.choice(DIGITS)

                rand_upper = random.choice(UPCASE_CHARACTERS)

                rand_lower = random.choice(LOCASE_CHARACTERS)

                rand_symbol = random.choice(SYMBOLS)

                temp_pass = rand_digit + rand_upper + rand_lower + rand_symbol

                for x in range(MAX_LEN - 4):
                    temp_pass = temp_pass + random.choice(COMBINED_LIST)

                    temp_pass_list = array.array('u', temp_pass)

                    random.shuffle(temp_pass_list)

                password = ""

                for x in temp_pass_list:
                    password = password + x
                # print(password)

                # Email Code
                import smtplib
                gmail_user = 'projectrailway002@gmail.com'
                gmail_password = 'spicljeotjmnwzdh'
                sent_from = gmail_user
                to = [email]
                subject = 'Railway Project Account New Password.'
                body = 'The password for Railway Project.\n ' \
                       'Your password for your Railway Project Account is ' \
                       ' ' + str(password)

                email_text = """\
                                     From: %s
                                     To: %s
                                     Subject: %s

                                     %s
                                     """ % (sent_from, ", ".join(to), subject, body)
                try:
                    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                    smtp_server.ehlo()
                    smtp_server.login(gmail_user, gmail_password)
                    smtp_server.sendmail(sent_from, to, email_text)
                    smtp_server.close()
                    # print("Email sent successfully!")
                except Exception as ex:
                    print("Something went wrong….", ex)
                message = 'New Password has been sent to your email.'

                # Phone sms code
                url3 = "https://espnodewebsite.000webhostapp.com/API/sms.php"
                params3 = {
                    'number': phone,
                    'pass': password
                }

                r3 = requests.post(url=url3, data=params3)
                # print(r3.text)
                url2 = "https://espnodewebsite.000webhostapp.com/API/signupapi.php"
                params1 = {
                    'fname': fname,
                    'lname': lname,
                    'email': email,
                    'password': password,
                    'phone': phone,
                    'address': address,
                    'gender': gender,
                    'hexcode':hexcode
                }

                rtt55 = requests.post(url=url2, data=params1)
                # print(rtt55.text)
                res = rtt55.json()
                ev = res['error']
                if not ev:
                    return render_template('form-basic.html', params1=params1)
            else:
                return render_template('form-basic.html')
    except:
        pass
    return render_template('index.html')

@app.route("/status")
def admin_status():
    try:
        if session["log_user_email"] is None:
            return redirect(login)
        else:
            records = {}
            url = "https://espnodewebsite.000webhostapp.com/API/fetchcomplainapi.php"
            response = requests.get(url=url)
            complain = response.json()
            ev = complain['error']
            records['complain'] = complain
            return render_template('form-wizard.html',records=records)
    except:
        pass
    return render_template('index.html')

@app.route("/attendance")
def admin_attendance():
    try:
        if session["log_user_email"] is None:
            return redirect("/login")
        else:
            url = "https://espnodewebsite.000webhostapp.com/API/fetchattendance.php"
            response = requests.get(url=url)
            attendance = response.json()
            records = {}
            records['data'] = attendance
            return render_template('Attendance_Table.html',records=records)
    except:
        pass
    return render_template('index.html')

@app.route("/complain")
def guard_complain():
    try:
        if session["log_email"] is None:
            return redirect("/login")
        else:
            if request.method == "POST":
                fname = request.form.get("fname")
                lname = request.form.get("lname")
                email = request.form.get("email")
                phone = request.form.get("phone")
                state=request.form.get("state")
                sensor_type=request.form.get("sensortype")
                company_name=request.form.get("companyname")
                problem = request.form.get("problem")
                url = "https://espnodewebsite.000webhostapp.com/API/addcomplaint.php"
                last_val1=[]
                params = {
                           'FIRST_NAME': fname,
                           'LAST_NAME': lname,
                           'COMPLAIN_EMAIL': email,
                           'PHONE_NUMBER': phone,
                           'SELECT_STATE': state,
                           'SENSOR_TYPE': sensor_type,
                           'COMPANY_NAME': company_name,
                           'PROBLEM': problem,
                           'COMPLAIN_STATUS': 'IN PROGRESS'
                }
                for i in params.values():
                    last_val1.append(i)
                COMPLAIN_EMAIL=last_val1[2]
                COMPLAIN_FIRST_NAME=last_val1[0]
                COMPLAIN_LAST_NAME=last_val1[1]
                COMPLAIN_PROBLEM=last_val1[-2]
                import smtplib
                gmail_user = 'railwayguard345@gmail.com'
                gmail_password = 'igotyvtmlaqkchej'
                sent_from = gmail_user
                to = ['projectrailway002@gmail.com']
                subject = 'Complain Added.'
                body = 'Complain Registered\n ' \
                       'NEW COMPLAIN REGISTERED' \
                       ' ' + str( "COMPLAIN ADDED--\t"+"\nCOMPLAIN SENDER'S EMAIL - ID --\t"+COMPLAIN_EMAIL+ " \nAND THE COMPLAIN IS REGISTERD BY\t" + COMPLAIN_FIRST_NAME+"\t" + COMPLAIN_LAST_NAME
                                  +"\nAND THE PROBLEM REGISTERED IN THE COMPLAIN IS\t" + COMPLAIN_PROBLEM)
                email_text = """\
                                                     From: %s
                                                     To: %s
                                                     Subject: %s

                                                     %s
                                                     """ % (sent_from, ", ".join(to), subject, body)
                try:
                    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                    smtp_server.ehlo()
                    smtp_server.login(gmail_user, gmail_password)
                    smtp_server.sendmail(sent_from, to, email_text)
                    smtp_server.close()
                    # print("Email sent successfully!")
                except Exception as ex:
                    print("Something went wrong….", ex)
                r2 = requests.post(url=url, data=params)
                # print(r2.text)
                # print(params)
                res = r2.json()
                return render_template('guard_form-wizard.html',params=params)
            else:
                return render_template('guard_form-wizard.html')
    except:
        pass
    return render_template('index.html')
