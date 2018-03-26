from src.models.users.user import User
from src.models.otp.otp import OTP

class UserAPI:

    @staticmethod
    def get_all_user():
        users = User.list_all_user()
        return [{
            '_id': user._id,
            'aadhaar_no': user.aadhaar_no,
            'name': user.name,
            'dob': user.dob,
            'mobile_no': user.mobile_no,
            'gender': user.gender,
            'address': user.address
        } for user in users if user is not None]\
            if users is not None else None

    @staticmethod
    def create_new_user(aadhaar_no,name,dob,address,mobile_no,gender):
        return User(aadhaar_no=aadhaar_no,name=name,dob=dob,address=address,mobile_no=mobile_no,gender=gender).save_to_db()
    @staticmethod
    def get_user_by_user_id(user_id):
        user = User.get_by_id(user_id)
        return {
            'aadhaar_no': user._id,
            'name': user.name,
            'dob':user.dob,
            'gender':user.gender,
            'address':user.address,
            'mobile_no':user.mobile_no,
            '_id':user_id
                }

    @staticmethod
    def get_sims(user_id):
        sims = User.get_by_id(user_id).get_sim_details()
        return [{'aadhaar':sim.aadhaar_no,'sim_no':sim.sim_no,'lsa':sim.lsa,'tsp':sim.lsa,'_id':sim._id}for sim in sims if sim is not None] if sims is not None else None

    @staticmethod
    def get_otp(aadhaar_no):
        otp = User.get_by_aadhaar(aadhaar_no).send_otp()
        return {'otp': otp.otp, 'generation_time': otp.generation_time, '_id': otp._id, 'user_id': otp.user_id}
    @staticmethod
    def authenticate_user(otp_id, user_otp):
        otp = OTP.get_recent_otp(otp_id)
        if otp.otp == user_otp:
            return 200
        else:
            return 400