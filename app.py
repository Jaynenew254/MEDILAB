from flask import *
from flask_restful import Api
app=Flask (__name__)
api = Api(app)

from datetime import timedelta
from flask_jwt_extended import JWTManager
# set up jwt 

app.secret_key ='(!@#$%^&*)'
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=30)
jwt = JWTManager(app)



# end points 
from views . views import MemberSignup ,MemberSignin,MemberProfile,AddDependant,ViewDependant,ViewAllLabs,LabTest,MakeBooking,MyBooking
api.add_resource(MemberSignup,'/api/member_signup')

api.add_resource(MemberSignin,'/api/member_signin')

api.add_resource(MemberProfile,'/api/member_profile')

api.add_resource(AddDependant,'/api/add_dependant')

api.add_resource(ViewDependant,'/api/view_dependant')

api.add_resource(ViewAllLabs,'/api/laboratories')

api.add_resource(LabTest,'/api/lab_test')

api.add_resource(MakeBooking,'/api/make_booking')

api.add_resource(MyBooking,'/api/mybooking')

if __name__ == '__main__' :
    app.run(debug=True)


