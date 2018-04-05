from flask_restplus import Resource, Namespace, fields
from flask import jsonify, request, g

from src.models.api.User.user import UserAPI

from flask_httpauth import HTTPTokenAuth
import src.models.api.guser as guser
user_namespace = Namespace('Users', 'There are Various Operations regarding User')

auth = HTTPTokenAuth(scheme='Token')

@auth.verify_token
def verify_token(token):
    if token in guser.tokens:
        g.current_user = guser.tokens[token]

        return True
    return False

user_model = user_namespace.model('User', {
    'aadhaar_no': fields.String(required=True, description='User Aadhaar Number'),
    'mobile_no': fields.String(required=True, description='User Mobile Number')
})


@user_namespace.route('/')
class ListUser(Resource):
    def get(self):
        users = UserAPI.get_all_user()
        return jsonify({"data": users})

    @user_namespace.response(201, 'User Has been created Successfuly', user_model)
    @user_namespace.doc(params={
        'aadhaar_no': {'in': 'formData', 'description': 'User Aadhaar Number', 'required': 'True'},
        'mobile_no': {'in': 'formData', 'description': 'User Mobile Number', 'required': 'True'}
    })
    def post(self):
        aadhaar_no = request.form['aadhaar_no']
        mobile_no = request.form['mobile_no']
        if UserAPI.create_new_user(aadhaar_no=aadhaar_no, mobile_no=mobile_no):
            return {"msg":"User Created successfully"}, 201
        else:
            return {"msg": "User can't be Created"}, 400


@user_namespace.route('/<string:user_id>')
class SingleUser(Resource):
    def get(self, user_id):
        return jsonify(UserAPI.get_user_by_user_id(user_id))


@user_namespace.route('/login')
class SendOTPtoUser(Resource):
    @user_namespace.doc(params={
        'aadhaar_no': {'in': 'formData', 'description': 'User Aadhaar Number', 'required': 'True'}})
    def post(self):
        aadhaar_no = request.form['aadhaar_no']
        return jsonify(UserAPI.get_otp(aadhaar_no))


@user_namespace.route('/verify-otp/<string:otp_id>')
class Authorize(Resource):
    @user_namespace.doc(params={
        'otp': {'in': 'formData', 'description': 'OTP Sent To User', 'required': 'True'}})
    def post(self, otp_id):
        user_otp = request.form['otp']
        return UserAPI.authenticate_user(otp_id, user_otp), 200


@user_namespace.route('/sim-registered/<string:user_id>')
class UserSims(Resource):
    def get(self, user_id):
        return {'data': UserAPI.get_sims(user_id)}