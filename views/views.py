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
#             # connect to database
#             connection =pymysql.connect(host='localhost',user='root',password='',database='medilab')
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
        # connect to DB
            connection = pymysql.connect(host='localhost', user='root',password='',database='Medilab')
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

        # connect to DB
        connection = pymysql.connect(host='localhost', user='root', password='', database='Medilab')
        
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
                return jsonify({"message": "login successful"})
            elif is_matchpassword == False:
                return jsonify({"message": "Login Failed"})
            else:
                return jsonify({"message": "Something Went Wrong"})

            
       
               
     # memberprofile

class MemberProfile(Resource):
    def post(self):
        data =request.json
        members_id =data ["members_id"]
        # connect to DB
        connection = pymysql.connect(host='localhost', user='root', password='', database='Medilab')
       

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
    def post(self):
        data= request.json
        members_id =data ["members_id"]
        surname = data["surname"]
        others = data["others"]
        dob = data["dob"]
        # connection 
        connection = pymysql.connect(host='localhost', user='root', password='', database='Medilab')
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
    def post(self):
        data = request.json
        members_id = data ["members_id"]
        # connect to DB
        connection = pymysql.connect(host='localhost', user='root', password='', database='Medilab')
        cursor = connection.cursor()
        sql = "SELECT * FROM dependants WHERE member_id = %s"
        cursor.execute(sql, members_id)
        count = cursor.rowcount
        if count == 0:
            return jsonify({"message": "member does not exist"})
        else:
            dependants = cursor.fetchall()
            return jsonify({"message": dependants})
        
        






        
            

        
