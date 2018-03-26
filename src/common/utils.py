from passlib.hash import pbkdf2_sha512
import requests
class Utils:

    @staticmethod
    def hash_password(password):
        """
        hashes a password using pbkdf2_sha512
        :param password:The sha512 password from the login/register form
        :return:A sha512->pdfk12 password encrypted password
        """
        return pbkdf2_sha512.encrypt(password)

    @staticmethod
    def check_hashed_password(password,hashed_password):
        """
        Checks the password the user sent matches tha password stored in the database
        The password is encrypted more than the user's password at this stage
        :param password: sha-512 hashed password
        :param hashed_password: pbkadf2_sh512 encrypted passsword
        :return: True if password matches false otherwise
        """
        return pbkdf2_sha512.verify(password,hashed_password)

    @staticmethod
    def send_otp(otp, mobile_number):
        payload = {
            "authkey": "203412ABi6bldnL5t5aacbefc",
            "message": "Your Verification Code is "+otp,
            "sender": "OTPSMS",
            "mobile": mobile_number,
            "otp_length": len(otp),
            "otp": otp,
            "otp_expiry": "1440",
            "template": "6",
                   }
        url = 'http://control.msg91.com/api/sendotp.php'
        #if requests.post(url, payload):
            #return True
        return True

