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

        
    

    

    

        

