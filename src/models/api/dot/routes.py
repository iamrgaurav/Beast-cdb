from flask_restplus import Resource, Namespace,fields
from flask import jsonify
from flask import request

from flask_httpauth import HTTPTokenAuth
import src.models.api.guser as guser
from src.models.api.dot.Admin import AdminAPI

admin_namespace = Namespace('DOT Admin','There are Various Operations regarding Admin')

auth = HTTPTokenAuth(scheme='Token')

@auth.verify_token
def verify_token(token):
    if token in guser.tokens:
        g.current_user = guser.tokens[token]

        return True
    return False


admin_model = admin_namespace.model('Admin', {
    'username': fields.String(required=True, description='Admin Username'),
    'password': fields.String(required=True, description='Admin Password'),
    'dob': fields.String(required=True, description='Admin Date of Birth'),
    'name': fields.String(required=True, description='Admin Name'),
    'privileges': fields.String(required=True, description='Admin Privileges'),
    'title': fields.String(required=True, description='Admin title'),
})


@admin_namespace.route('/')
class ListUser(Resource):
    def get(self):
        users = AdminAPI.get_all_admin()
        return jsonify({"data": users})

    @admin_namespace.response(201, 'User Has been created Successfuly', admin_model)
    @admin_namespace.doc(params={
        'username': {'in': 'formData', 'description': 'Admin Username', 'required': 'True'},
        'password': {'in': 'formData', 'description': 'Admin Password', 'required': 'True'},
        'dob': {'in': 'formData', 'description': 'User Date of Birth', 'required': 'True'},
        'name': {'in': 'formData', 'description': 'User Name', 'required': 'True'},

        'privileges': {'in': 'formData', 'description': 'User Privileges', 'required': 'True'},
        'title': {'in': 'formData', 'description': 'User Title', 'required': 'True'},
    })
    def post(self):
        username = request.form['username']
        name = request.form['name']
        dob = request.form['dob']
        password = request.form['password']
        privileges = request.form['privileges']
        title = request.form['title']
        if AdminAPI.create_new_user(username, name, dob, password, privileges, title):
            return 201
        else:
            return 400


@admin_namespace.route('/<string:admin_id>')
class SingleUser(Resource):
    def get(self, user_id):
        return jsonify(AdminAPI.get_admin_by_admin_id(user_id))


@admin_namespace.route('/login')
class Authorize(Resource):
    @admin_namespace.doc(params={
        'username': {'in': 'formData', 'description': 'Username of Dot Admin', 'required': 'True'},
        'password': {'in': 'formData', 'description': 'Username of Dot Admin', 'required': 'True'}})
    @admin_namespace.response(200, "You are Authorize")
    def post(self):
        username = request.form['username']
        password = request.form['password']
        data = AdminAPI.authenticate_admin(username, password)
        if data:
            return {
                'status': 'success',
                'data': [AdminAPI.authenticate_admin(username, password)]
            }

    @admin_namespace.route('/list')
    class ListResource(Resource):
        @admin_namespace.doc(params={
            'count': {'in': 'formData', 'description': 'The no of count you want to query', 'required': 'True'}})
        def post(self):
            count = request.form['count']
            return AdminAPI.gets_user_by_count(count), 200




