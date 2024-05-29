# import pymysql
# from flask_restful import Resource
# from flask import *
# from functions import *
# # add a member class
# # memeber_signup amd member_signin 
# class MemberSignup(Resource):
#     def post(self):
#         # get data from client
#         data = request.json
#         surname = data["surname"]
#         others =data["others"]
#         gender =data ["gender"]
#         email =data ["email"]
#         phone =data["phone"]
#         dob=data["dob"]
#         status=data["status"]
#         password=data["password"]
#         location_id=data["location_id"]

#         # check if password is valid 
#         response=passwordvalidity(password)
#         if response==True:
#             # connect json database
#             connection =pymysql.connect(host='localhost',user='root',password='',database='medilabs')
#             cursor =connection.cursor()
#             # insert data into database
#             sql= "INSERT INTO members (surname, others, gender, email, phone, dob, status, password, location_id) VALUES =%s,%s,%s,%s,%s,%s,%s,%s,%s"
#             data=( surname, others, gender, email, phone, dob, status, password, location_id)
#             try:
#                 cursor.execute(sql,data)
#                 connection.commit()
#                 send_sms(phone, "Registration successful")
#                 return jsonify({"message":"POST FAILED.MEMBER SAVED"})

#             except:
#                 connection.rollback()
#                 return jsonify({"message":"POST FAILED.MEMBER NOT SAVED"})
#         else:
#                  return jsonify({ "message": "password is not valid"})

import pymysql
from flask_restful import Resource
from flask import *
import pymysql.cursors
from functions import *

# IMPORT JWT packageS
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required 

# Add a member class
# member_signup and member_signin
class MemberSignup(Resource):
    def post(self):
    # get data from client
        data = request.json
        surname= data["surname"]
        others= data["others"]
        gender= data["gender"]
        email= data["email"]
        phone= data["phone"]
        dob= data["dob"]
        status= data["status"]
        password= data["password"]
        location_id= data["location_id"]

        # check if password is valid
        response = passwordvalidity(password)
        if response == True:
        # connect json DB
            connection = pymysql.connect(host='localhost', user='root',password='',database='Medilabs')
            cursor = connection.cursor()
            # instert into database
            sql = "insert into members (surname, others, gender, email, phone, dob, status, password, location_id) values(%s, %s, %s, %s, %s, %s, %s, %s,%s)"
            data = (surname, others, gender, email, phone, dob, status,hash_password(password), location_id)
            try:
                cursor.execute(sql, data)
                connection.commit( )
                send_sms(phone, "Registration successful")
                return jsonify({ "message": "POST SUCCESSFUL. MEMBER SAVED" })

            except:
                connection.rollback()
                return jsonify({ "message": "POST FAILED. MEMBER NOT SAVED" })

        else:
             return jsonify({ "message": response })
        
        # membersignin

class MemberSignin(Resource):
    def post(self):
        # get data from client
        data = request.json
        email = data["email"]
        password = data["password"]

        # connect json DB
        connection = pymysql.connect(host='localhost', user='root', password='', database='Medilabs')
        
        # check if member exists
        sql = "SELECT * FROM members WHERE email = %s"
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql, email)
        if cursor.rowcount == 0:    
             return jsonify({"message": "email does not exist"})
        else:
            # check password
            member =cursor.fetchone()
            hashed_password = member['password']
            is_matchpassword =hash_verify(password,hashed_password)
            if is_matchpassword == True:
                access_token = create_access_token(identity=member,fresh=True)
                return jsonify({"access_token":access_token,
                                "member":member
                                })
            elif is_matchpassword == False:
                return jsonify({"message": "Login Failed"})
            else:
                return jsonify({"message": "Something Went Wrong"})

            
       
               
     # memberprofile

class MemberProfile(Resource):
    @jwt_required(fresh=True)
    def post(self):
        data =request.json
        members_id =data ["members_id"]
        # connect json DB
        connection = pymysql.connect(host='localhost', user='root', password='', database='Medilabs')
       

        # check if member exists
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT * FROM members WHERE member_id = %s"
        cursor.execute(sql, members_id)
        count = cursor.rowcount
        if count == 0:
            return jsonify({"message": "member does not exist"})
        else:
            member = cursor.fetchone()
            return jsonify({"message": member})
        
# add a dependant
class AddDependant(Resource):
    @jwt_required(fresh=True)
    def post(self):
        data= request.json
        members_id =data ["members_id"]
        surname = data["surname"]
        others = data["others"]
        dob = data["dob"]
        # connection 
        connection = pymysql.connect(host='localhost', user='root', password='', database='Medilabs')
        cursor = connection .cursor()

        # insert data 
        sql ="INSERT INTO dependants (member_id, surname, others, dob) VALUES (%s, %s, %s, %s)"
        data =(members_id, surname, others, dob)
        # try:
        cursor.execute(sql,data)
        connection.commit()
        return jsonify({"message": "POST SUCCESSFUL.SAVED"})

        # except:
        #     connection.rollback()
        #     return jsonify({"message":"POST FAILED.NOT SAVED"})
        
# view dependant based on member id 
class ViewDependant(Resource):
    @jwt_required(fresh=True)
    def post(self):
        data = request.json
        members_id = data ["members_id"]
        # connect json DB
        connection = pymysql.connect(host='localhost', user='root', password='', database='Medilabs')
        cursor = connection.cursor()
        sql = "SELECT * FROM dependants WHERE member_id = %s"
        cursor.execute(sql, members_id)
        count = cursor.rowcount
        if count == 0:
            return jsonify({"message": "member does not exist"})
        else:
            dependants = cursor.fetchall()
            return jsonify({"message": dependants})
        
    # see all labs
class ViewAllLabs(Resource):
    def get(self):
        connection = pymysql.connect(host='localhost', user='root', password='', database='Medilabs')
        sql = "SELECT * FROM laboratories "
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql)

        if cursor.rowcount == 0:
            return jsonify({"message":"No Laboratories"})
        else:
            labs =cursor.fetchall()
            return jsonify(labs)
# create a lab test resourse 
class LabTest(Resource):
    def post(self):
        data = request.json
        lab_id = data ["lab_id"]

        # create a connection 
        connection = pymysql.connect(host='localhost', user='root', password='', database='Medilabs')
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT * FROM lab_tests where lab_id =%s"
        cursor.execute(sql, lab_id)
        if cursor.rowcount == 0:
            return jsonify({"message":"No Lab Test Found"})
        else:
            lab_test =cursor.fetchall()
            return jsonify(lab_test)
        

        
# 1. create a Resource called  make bookigs
# the Resource shouled allow post ethode
# save the booking in data BaseException
class MakeBooking(Resource):
    def post(self):
        data = request.json
        member_id =data["member_id"]	
        booked_for = data["booked_for"]	
        dependant_id= data["dependant_id"]	
        test_id=data=["test_id"]	
        appointment_date=["appointment_date"]	
        appointment_time=["appointment_time"]
        where_taken	=["where taken"]
        latitude=["latitude"]	
        longitude=["longitude"]	
        status=["status"]	
        lab_id	=["lab_id"]
        invoice_no =["invoice_no"]

         # connect json DB
        connection = pymysql.connect(host='localhost', user='root', password='', database='Medilabs')
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        
        sql = "INSERT INTO bookings (member_id,booked_for, dependant_id,	test_id	,appointment_date,appointment_time,where_taken,latitude,longitude,status,lab_id,invoice_no) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" 	
        data=(member_id	,booked_for	,dependant_id,test_id,appointment_date,appointment_time,where_taken	,latitude,longitude	,status	,lab_id,invoice_no	)	
        cursor.execute(sql, data)
        
        # try:

        cursor.execute(sql,data)
        connection.commit()
        return jsonify({"message": "Booking Made Successfully"}) 
    
        # except:
        #     connection.rollback()
        #     return jsonify({"message": "Error Occured While Making Booking"})
    


        

        


# 2. create a Resource called my booking 
# the Resource should allow get method
# get booking using member _id
class MyBooking(Resource):
    def get(self):
        data = request.json
        member_id = data["member_id"]
        # connect json DB
        connection = pymysql.connect(host='localhost', user='root', password='', database='Medilabs')
        cursor = connection.cursor()
        sql = "SELECT * FROM bookings  WHERE member_id = %s"
        cursor.execute(sql, member_id)
        count = cursor.rowcount
        if count == 0:
            return jsonify({"message": "member does not exist"})
        else:
            Booking = cursor.fetchall()
            # date and time was not convertible json
            # hence we use json.dumps and json.loads 
            import json
# we pass our bookings
            ourbookings = json.dumps(Booking,indent =1,
                                    sort_keys = True, default=str)
            
            return json.loads(ourbookings)
        

# make payment
class MakePayment(Resource):
    def post(self):
        data = request.json
        invoice_no= data["invoice_no"]
        amount=data["amount"]
        phone= data['phone']	
        mpesa_payment(amount,phone,invoice_no)
        return jsonify({"message": "Payment Made Successfully"})

# # connect to db
#         connection = pymysql.connect(host='localhost', user='root', password='', database='Medilabs')
#         cursor = connection.cursor()
#         sql = "INSERT INTO payments (invoice_no,total_amount) VALUES (%s,%s)"
#         data = (invoice_no,total_amount)
#         cursor.execute(sql, data)
#         connection.commit()

#         try:
#             cursor.execute(sql, data)
#             connection.commit()
#             mpesa_payment(total_amount,phone,invoice_no)
#             return jsonify({"message": "payment successful"})

#         except:
#             connection.rollback()
#             return jsonify({"message": "payment failed"})



    




        

        
        






        
            

        
