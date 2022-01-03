
from app import app 
from db_config import mysql
from flask import abort, Flask, jsonify, render_template, request
from flask_cors import CORS
from datetime import date,datetime
import time
import atexit
import smtplib
from apscheduler.schedulers.background import BackgroundScheduler

CORS(app)

def daily_task():
    today = date.today()
    now=today.strftime("%Y-%m-%d")
    cur=None
    try: 
        cur=mysql.connection.cursor()
        cur.execute('select c.name,v.category,v.hiring_price,b.date_of_hire,b.date_of_ret from Car_Hire_Management_System.bookings as b  inner join Car_Hire_Management_System.vehicles as v on b.vehicle_id=v.vehicle_id inner join Car_Hire_Management_System.customers as c on b.customer_id=c.customer_id where b.date_of_hire=%s;',(str(now)))
        Invoices=cur.fetchall()
        print (jsonify(Invoices))
       
        cur.execute('select v.vehicle_id from Car_Hire_Management_System.bookings as b  inner join Car_Hire_Management_System.vehicles as v on b.vehicle_id=v.vehicle_id inner join Car_Hire_Management_System.customers as c on b.customer_id=c.customer_id where b.date_of_ret=%s;',(str(now)))
        rows=cur.fetchall()
        for i in range(len(rows)):  
            cur.execute('update Car_Hire_Management_System.vehicles SET is_available = 1 WHERE vehicle_id = %s ',(str(rows[i][0])))
            mysql.connection.commit() 
        
        cur.execute('select c.customer_id from Car_Hire_Management_System.bookings as b  inner join Car_Hire_Management_System.vehicles as v on b.vehicle_id=v.vehicle_id inner join Car_Hire_Management_System.customers as c on b.customer_id=c.customer_id where b.date_of_hire=%s;',(str(now)))
        rows=cur.fetchall()
        for i in range(len(rows)):  
            cur.execute('update Car_Hire_Management_System.customers SET is_paid = 1 WHERE customer_id = %s ',(str(rows[i][0])))
            mysql.connection.commit()     
         
    except Exception as e:
        print(e)
    finally:
        cur.close()


scheduler = BackgroundScheduler()
scheduler.add_job(func=daily_task, trigger="interval",days=1)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

def check_vehicle_availability( vehicle_category):
    cur=None
    try: 
        cur=mysql.connection.cursor()
        cur.execute('select * from Car_Hire_Management_System.vehicles where is_available=1 and category="'+vehicle_category+'";')
        row=cur.fetchone()
        
        if row==None:
            return False
        
        return row
    except Exception as e:
        print(e)
    finally:
        cur.close()
    return True

def send_email(user, pwd, recipient, subject, body):
    FROM = user
    TO = recipient if isinstance(recipient, list) else [recipient]
    SUBJECT = subject
    TEXT = body
    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(user, pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print ('successfully sent the mail')
    except:
        print ("failed to send mail")
def send_confirmation(customer_name,vehicle_category,mail,phone,date_hire,date_ret):
    msg="""
        Dear %s,
        Please be informed that the vehicle with category "%s" has been booked from date: %s, to date: %s
        a confirmation sms message will be sent to your phone number: %s
        
        if you wish to cancel please visit our main office
        
        Thanks and Regards,
        Wael Anwar
    """% (customer_name, vehicle_category,date_hire,date_ret,phone)
    send_email('dummymail@gmail.com','password',mail,'Vehicle Booking Confirmation',msg)
    return msg

def validate_dates(customer_name,vehicle_category,mail,phone,date_hire,date_ret):
    today = date.today()
    now=today.strftime("%Y-%m-%d")
    date_format = "%Y-%m-%d"
    a = datetime.strptime(now, date_format)
    b = datetime.strptime(date_hire, date_format)
    c=  datetime.strptime(date_ret, date_format)
    deltaAdvance = b - a
    daysAdvance=deltaAdvance.days
    deltaDuration=c-b
    daysDuration=deltaDuration.days
    if daysAdvance>0:
        send_confirmation(customer_name,vehicle_category,mail,phone,date_hire,date_ret)
    elif daysAdvance<=7 and daysDuration<=7:
        return True
    elif daysDuration>7:
        return "Cannot hire a vehicle for more than 7 days"
    else:
        return "Cannot hire a vehicle more than 7 days in advance"
        
def add_customer(customer_name,phone,mail,is_paid):
    cur=None
    try: 
        cur=mysql.connection.cursor()
        cur.execute('select customer_id from Car_Hire_Management_System.customers where name="'+customer_name+'";')
        id=cur.fetchone()
        if id==None:
            cur.execute("SELECT COALESCE(MAX(customer_id), 0) + 1 FROM Car_Hire_Management_System.customers;")
            id=cur.fetchone()
            cur.execute('insert into Car_Hire_Management_System.customers values (%s,%s,%s,%s,%s)',(id[0],customer_name,phone,mail,is_paid))
            mysql.connection.commit()
        return id[0]
    except Exception as e:
        print(e)
    finally:
        cur.close()
    

def add_booking(customer_id,vehicle_id,date_hire,date_ret):
    cur=None
    try: 
        cur=mysql.connection.cursor()
        cur.execute("select COALESCE(MAX(booking_id), 0) + 1 FROM Car_Hire_Management_System.bookings;")
        id=cur.fetchone()
        cur.execute('insert into Car_Hire_Management_System.bookings values (%s,%s,%s,%s,%s)',(id[0],vehicle_id,customer_id,date_hire,date_ret))
        mysql.connection.commit()
        print("vehicle_ID: "+str(vehicle_id))
        cur.execute('update Car_Hire_Management_System.vehicles SET is_available = 0 WHERE vehicle_id = %s ',(str(vehicle_id)))
        mysql.connection.commit() 
        return True
    except Exception as e:
        print(e)
    finally:
        cur.close()
    

@app.route('/api/customer', methods=['GET','POST'])
def customer():
    # Get all Customers
    if request.method == 'GET':
        cur=None
        try: 
            cur=mysql.connection.cursor()
            cur.execute('select * from Car_Hire_Management_System.customers;')
            rows=cur.fetchall()
            res=jsonify(rows)
            return res
        except Exception as e:
            print(e)
        finally:
            cur.close()
    # Create Customer
    elif request.method == 'POST':
        try: 
            data=request.json
            vehicle_id=check_vehicle_availability(data['vehicle_category'])
            if vehicle_id==False:
               return {"Message":"No '"+data['vehicle_category']+"' available right now"}
           
            msg=validate_dates(data['name'],data['vehicle_category'],data['mail'],data['phone'],data['date_of_hire'],data['date_of_ret'])
            if not msg:
                return {"Message":msg}
            customer_id=add_customer(data['name'],data['phone'],data['mail'],0)
            res=add_booking(customer_id,vehicle_id[0],data['date_of_hire'],data['date_of_ret'])
            if res:
                return jsonify({'status': 'Customer with ID= '+customer_id+' is created Successfully!'})
            return jsonify({'status': 'Failed create customer'})
        except Exception as e:
            print(e)

@app.route('/api/customer/<string:id>', methods=['GET','PUT','DELETE'])
def one_customer(id):
    
    # GET a specific Customer by id
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM Car_Hire_Management_System.customers WHERE customer_id = %s', (id))
        row = cursor.fetchone()
        return jsonify(row)
        
    # DELETE a Customer
    if request.method == 'DELETE':
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM Car_Hire_Management_System.customers WHERE customer_id = %s', (id))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'status': 'Customer with ID= '+id+' is deleted Successfully!'})

    # UPDATE a Customer by id
    if request.method == 'PUT':
        body = request.json
        name = body['name']
        mail = body['mail']
        phone= body['phone']

        cursor = mysql.connection.cursor()
        cursor.execute('UPDATE Car_Hire_Management_System.customers SET name = %s, mail = %s, phone=%s WHERE customer_id = %s', (name, mail, phone,id))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'status': 'Customer with ID= '+id+' is updated Successfully!'})
if __name__=="__main__":
    app.run()