# import required modules 
import pymysql
from flask_restful import *
from flask import *
from functions import *
import pymysql.cursors

# jwt packages 

from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required 

class labsignup(Resource):
    def post(self):
       data=request.json
       lab_name=data["lab_name"]
       permit_id=data["permit_id"]
       email=data["email"]
       phone =data["phone"]
       password= data["password"]

    #    connect to data base 
  
     
        # connect json DB
       connection = pymysql.connect(host='localhost', user='root',password='',database='Medilabs')
       cursor = connection.cursor()


    #         # instert into database
    #    sql = "insert into laboratories (lab_name,permit_id, email, phone, password ) values( %s, %s, %s, %s,%s)"
    #    data = ( lab_name,permit_id, email, phone,password)
    # #    try:
    #    cursor.execute(sql, data)
    #    connection.commit()
            
    #    return jsonify({ "message": "POST SUCCESSFUL. " })
     #    except:
    #         connection.rollback()
    #         return jsonify({ "message": "POST FAILED. " })

       Response=passwordvalidity(password)
       if Response:
           if check_phone(phone):
                  
                sql = "insert into laboratories (lab_name,permit_id, email, phone, password ) values( %s, %s, %s, %s,%s)"
                data = ( lab_name,permit_id, email,encrypt(phone) ,hash_password(password))
                try:

                    cursor.execute(sql, data)
                    connection.commit()
                    code=generate_random()
                    send_sms(phone,'''Thank you for joining Medilab.
                             Your secret No:{}.Do not sahre.'''.format(code)
                             )
                    return jsonify({ "message": "POST SUCCESSFUL. " })
                except:
                    connection.rollback()
                    return jsonify({ "message": "POST FAILED. " })

                # phone is correct 
           else:
                    # IF NOT IN CORRECT FORMAT 
                    return jsonify({"message": "phone number is not correct.Enter +254"})
        
       else:
            return jsonify({ "message":Response})
       
# labsignin

class labsignin (Resource):
     def post(self):
          data = request.get_json()
          email=data["email"]
          password=data["password"]

        #   connect to db 
          connection = pymysql.connect(host='localhost', user='root',password='',database='Medilabs')
          cursor = connection.cursor()
          sql = "SELECT * FROM laboratories WHERE email = %s"
          cursor = connection.cursor(pymysql.cursors.DictCursor)
          cursor.execute(sql, email)
          if cursor.rowcount == 0:    
               return jsonify({"message": "email does not exist"})
          else:
            lab =cursor.fetchone()
            hashed_password = lab['password']
            is_matchpassword =hash_verify(password,hashed_password)
            if is_matchpassword == True:
                access_token = create_access_token(identity=lab,fresh=True)
                return jsonify({"access_token":access_token,
                                "lab":lab
                                })
            elif is_matchpassword == False:
                return jsonify({"message": "Login Failed"})
            else:
                return jsonify({"message": "Something Went Wrong"})

             

# view labProfile 
class labprofile(Resource):
    @jwt_required(fresh=True)
    def post(self):
        data = request.json
        lab_id = data["lab_id"]
        connection = pymysql.connect(host='localhost', user='root', password='', database='Medilabs')
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT * FROM laboratories WHERE lab_id = %s"
        cursor.execute(sql, lab_id)
        if cursor.rowcount == 0:
            return jsonify({"message": "Lab Profile Not Found"})
        
        else:
            lab = cursor.fetchone()
            return jsonify({"message": lab})

# create  aresource called addlabtest 
class addlabtest(Resource):
    @jwt_required(fresh=True)
    def post(self):
        data = request.json
        lab_id = data["lab_id"]
        test_name = data["test_name"]
        test_description=data["test_descrition"]
        test_cost=data["test_cost"]
        test_discount=data["test_discount"]
        connection = pymysql.connect(host='localhost', user='root', password='', database='Medilabs')
        cursor = connection .cursor()
        sql ="INSERT INTO lab_tests (lab_id, test_name, test_description,test_cost, test_discount) VALUES (%s, %s, %s, %s,%s)"
        data =(lab_id, test_name, test_description, test_cost,test_discount)
        try:
            cursor.execute(sql,data)
            connection.commit()
            return jsonify({"message": "POST SUCCESSFUL.SAVED"})
        except:
            connection.rollback()
            return jsonify({"message":"POST FAILED.NOT SAVED"})
        
# create a resource named view lab test ..method is post ..where lab_id =%S
class Viewlabtest(Resource):
    @jwt_required(fresh=True)
    def post(self):
        data = request.json
        lab_id = data ["lab_id"]
        # connect json DB
        connection = pymysql.connect(host='localhost', user='root', password='', database='Medilabs')
        cursor = connection.cursor()
        sql = "SELECT * FROM lab_tests WHERE lab_id = %s"
        cursor.execute(sql, lab_id)
        count = cursor.rowcount
        if count == 0:
            return jsonify({"message": "lab does not exist"})
        else:
            labtests = cursor.fetchall()
            return jsonify({"message": labtests})
        
# view labbookings ...method post..where lab_id =%s
class Viewlabbookings(Resource):
    @jwt_required(fresh=True)
    def post(self):
        data = request.json
        lab_id = data ["lab_id"]
        connection = pymysql.connect(host='localhost', user='root', password='', database='Medilabs')
        cursor = connection.cursor()
        sql = "SELECT * FROM bookings WHERE lab_id = %s"
        cursor.execute(sql, lab_id)
        count = cursor.rowcount
        if count == 0:
            return jsonify({"message": "no bookings found for this lab"})
        else:
            Booking = cursor.fetchall()
            # associate member_id with the booking
            # we want to loop 
            for booking in Booking:
                member_id = booking["member_id"]
                # return jsonify(member_id)
                sql = "SELECT * FROM members WHERE member_id = %s"
                cursor=connection.cursor(pymysql.cursors.DictCursor)
                cursor.execute(sql, member_id)
                member = cursor.fetchone()
                # the result is attached to booking dictionary under key 
                booking["key"] = member
                return jsonify(member)
            


            # date and time was not convertible json
            # hence we use json.dumps and json.loads 
            import json
# we pass our bookings
            ourbookings = json.dumps(Booking,indent =1,
                                    sort_keys = True, default=str)
            
            return json.loads(ourbookings)
        

# add nurse
class Addnurse(Resource):
    @jwt_required(fresh=True)
    def post(self):
        data = request.json
        surname	=data["surname"]
        others	=data["others"]
        lab_id =data["lab_id"]	
        gender = data["gender"]
        # connection 
        connection = pymysql.connect(host='localhost', user='root', password='', database='Medilabs')
        cursor = connection.cursor()
        sql = "INSERT INTO nurses (surname, others, lab_id, gender) VALUES (%s,%s,%s,%s)"
        try:
            cursor.execute(sql, (surname, others, lab_id, gender))
            connection.commit()
            return jsonify({"message": "nurse added successfully"})
        except:
            return jsonify({"message": "nurse not added"})
        

# view nurse using nurse id
class Viewnurse(Resource):
    @jwt_required(fresh=True)
    def post(self):
        data =request.json
        nurse_id=data["nurse_id"]
        connection = pymysql.connect(host='localhost', user='root', password='', database='Medilabs')
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT * FROM nurses WHERE nurse_id = %s"
        cursor.execute(sql, nurse_id)
        count = cursor.rowcount
        if count == 0:
            return jsonify({"message": "No nurse found"})
        else:
            nurse = cursor.fetchall()
            return jsonify({"message": nurse})
                                     


        

        
        







        



    

    

        

