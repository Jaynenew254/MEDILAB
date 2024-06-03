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
from views . views import MemberSignup ,MemberSignin,MemberProfile,AddDependant,ViewDependant,ViewAllLabs,LabTest,MakeBooking,MyBooking,MakePayment
from views.views_dashboard import labsignup,labsignin,labprofile,addlabtest,Viewlabtest,Viewlabbookings,Addnurse,Viewnurse,TaskAllocation,CheckInvoice
api.add_resource(MemberSignup,'/api/member_signup')

api.add_resource(MemberSignin,'/api/member_signin')

api.add_resource(MemberProfile,'/api/member_profile')

api.add_resource(AddDependant,'/api/add_dependant')

api.add_resource(ViewDependant,'/api/view_dependant')

api.add_resource(ViewAllLabs,'/api/laboratories')

api.add_resource(LabTest,'/api/lab_test')

api.add_resource(MakeBooking,'/api/make_booking')

api.add_resource(MyBooking,'/api/mybooking')

api.add_resource(MakePayment,'/api/make_payment')

api.add_resource(labsignup,'/api/lab_signup')

api.add_resource(labsignin,'/api/lab_signin')

api.add_resource(labprofile,'/api/lab_profile')

api.add_resource(addlabtest,'/api/add_labtest')

api.add_resource(Viewlabtest,'/api/view_labtest')

api.add_resource(Viewlabbookings,'/api/view_labbookings')

api.add_resource(Addnurse,'/api/add_nurse')

api.add_resource(Viewnurse,'/api/view_nurse')

api.add_resource(TaskAllocation,'/api/nurse_allocation')

api.add_resource(CheckInvoice,'/api/check_invoice')

if __name__ == '__main__' :
    app.run(debug=True)


