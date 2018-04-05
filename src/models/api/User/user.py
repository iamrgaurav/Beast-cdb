from src.models.users.user import User
from src.models.otp.otp import OTP


class UserAPI:
    @staticmethod
    def get_all_user():
        users = User.list_all_user()
        return [user.json() for user in users] \
            if users is not None else None

    @staticmethod
    def create_new_user(aadhaar_no, mobile_no):
        return User(aadhaar_no=aadhaar_no, mobile_no=mobile_no).save_to_db()

    @staticmethod
    def get_user_by_user_id(user_id):
        user = User.get_by_id(user_id)
        return {
            'aadhaar_no': user.aadhaar_no,
            'mobile_no': user.mobile_no,
            '_id': user._id
        }

    @staticmethod
    def get_sims(user_id):
        sims = User.get_by_id(user_id).get_sim_details()
        return [{'aadhaar': sim.aadhaar_no, 'sim_no': sim.sim_no, 'lsa': sim.lsa, 'tsp': sim.lsa, '_id': sim._id} for
                sim in sims if sim is not None] if sims is not None else None

    @staticmethod
    def get_otp(aadhaar_no):
        otp = User.get_by_aadhaar(aadhaar_no).send_otp()
        return {'otp': otp.otp, 'generation_time': otp.generation_time, '_id': otp._id, 'aadhaar_no': otp.aadhaar_no}

    @staticmethod
    def authenticate_user(otp_id, user_otp):
        otp = OTP.get_recent_otp(otp_id)
        user = User.get_by_aadhaar(otp.aadhaar_no)
        if int(otp.otp) == int(user_otp):
            return {
                'aadhaar_no': user.aadhaar_no,
                'mobile_no': user.mobile_no,
                "_id": user._id
            }
        else:
            return None


