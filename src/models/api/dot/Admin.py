from src.common.Utility.utils import Utils
from src.models.dot.dot import Admin


from src.models.users.user import User


class AdminAPI:
    @staticmethod
    def get_all_admin():
        users = Admin.list_all_admin()
        return [{
            '_id': user._id,
            'username': user.username,
            'password': user.password,
            'name': user.name,
            'privileges': user.privileges
        } for user in users if user is not None] \
            if users is not None else None

    @staticmethod
    def create_new_user(username, password, name, privileges):
        return Admin(username=username, password= Utils.hash_password(password), name=name,  privileges=privileges).save_to_db()

    @staticmethod
    def get_admin_by_admin_id(user_id):
        user = Admin.get_by_id(user_id)
        return {
            '_id': user._id,
            'username': user.username,
            'password': user.password,
            'name': user.name,
            'privileges': user.privileges
        }

    @staticmethod
    def authenticate_admin(username, password):
        admin = Admin.get_by_username(username)
        if admin.is_login_valid(username, password):
            return {'username': admin.username,
                    'name':admin.name,
                    'privileges': admin.privileges,
                    '_id':admin._id
            }
        else:
            return "No Valid User"
    @staticmethod
    def gets_user_by_count(count):
        return Admin.gets_user_by_count(count)

    @staticmethod
    def list_users_by_lsa(lsa):
        return Admin.list_users_by_lsa(lsa)

