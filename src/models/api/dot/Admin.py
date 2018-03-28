from src.models.dot.dot import Admin
from flask import jsonify

class AdminAPI:
    @staticmethod
    def get_all_admin():
        users = Admin.list_all_admin()
        return [{
            '_id': user._id,
            'username': user.username,
            'password': user.password,
            'name': user.name,
            'dob': user.dob,
            'privileges': user.privileges,
            'title': user.title
        } for user in users if user is not None] \
            if users is not None else None

    @staticmethod
    def create_new_user(username, password, name, dob, privileges, title):
        return Admin(username=username, password=password, name=name, dob=dob, privilages=privileges, title=title).save_to_db()

    @staticmethod
    def get_admin_by_admin_id(user_id):
        user = Admin.get_by_id(user_id)
        return {
            '_id': user._id,
            'username': user.username,
            'password': user.password,
            'name': user.name,
            'dob': user.dob,
            'privileges': user.privileges,
            'title': user.title
        }

    @staticmethod
    def authenticate_admin(username, password):
        admin = Admin.get_by_username(username)
        if admin.is_login_valid(username, password):
            return {'username': admin.username,
                    'name':admin.name,
                    'dob':admin.dob.strftime("%Y-%m-%d"),
                    'privileges': admin.privileges
            }
        else:
            return "No Valid User"
