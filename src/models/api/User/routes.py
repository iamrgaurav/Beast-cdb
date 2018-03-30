from flask_restplus import Resource, Namespace, fields, reqparse
from flask import jsonify, request

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
    '': fields.String(required=True, description='User Aadhaar Number'),
    'name': fields.String(required=True, description='User Name'),
    'dob': fields.String(required=True, description='User Date of Birth'),
    'mobile_no': fields.String(required=True, description='User Mobile Number'),
    'gender': fields.String(required=True, description='User Gender'),
    'address': fields.String(required=True, description='User Address'),
})


@user_namespace.route('/')
class ListUser(Resource):
    def get(self):
        users = UserAPI.get_all_user()
        return jsonify({"data": users})

    @user_namespace.response(201, 'User Has been created Successfuly', user_model)
    @user_namespace.doc(params={
        'aadhaar_no': {'in': 'formData', 'description': 'User Aadhaar Number', 'required': 'True'},
        'name': {'in': 'formData', 'description': 'User Name', 'required': 'True'},
        'dob': {'in': 'formData', 'description': 'User Date of Birth', 'required': 'True'},
        'address': {'in': 'formData', 'description': 'User Address', 'required': 'True'},

        'mobile_no': {'in': 'formData', 'description': 'User Mobile Number', 'required': 'True'},
        'gender': {'in': 'formData', 'description': 'User Gender', 'required': 'True'},
    })
    def post(self):
        aadhaar_no = request.form['aadhaar_no']
        name = request.form['name']
        dob = request.form['dob']
        address = request.form['address']
        mobile_no = request.form['mobile_no']
        gender = request.form['gender']
        if UserAPI.create_new_user(aadhaar_no=aadhaar_no, name=name, dob=dob, address=address, mobile_no=mobile_no,
                                   gender=gender):
            return 201
        else:
            return 400


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
    @user_namespace.response(200, "You are Authorize")
    def post(self, otp_id):
        user_otp = request.form['otp']
        return jsonify(UserAPI.authenticate_user(otp_id, user_otp))


@user_namespace.route('/sim-registered/<string:user_id>')
class UserSims(Resource):
    def get(self, user_id):
        return jsonify({'data': UserAPI.get_sims(user_id)})