import uuid
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

from src.common.Utility.utils import Utils
from src.common.database import Database
import src.models.api.config as APIConfig
import src.models.api.errors as Errors


class Api_User:
    def __init__(self,username,password,type,_id=None):
        self.username=username
        self.password=password
        self.type=type
        self._id=uuid.uuid4().hex if _id is None else _id

    @classmethod
    def get_by_id(cls, user_id):
        data = Database.find_one(APIConfig.COLLECTION, {'_id':user_id})
        return cls(**data) if data is not None else False

    def json(self):
        return {
            'username':self.username,
            'password':self.password,
            'type':self.type,
            '_id':self._id
        }

    def save_to_db(self):
        return Database.update(APIConfig.COLLECTION, {'_id': self._id}, self.json())

    def generate_auth_token(self, expiration = 600):
        s = Serializer(APIConfig.apiSecretKey,expires_in = expiration)
        return s.dumps({ '_id': self._id })

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(APIConfig.apiSecretKey)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        user = Api_User(data['_id'])
        return user

    @classmethod
    def is_login_valid(cls, username, password):
        """
        This methods verifies that an username/password combo as
        sent by the site form is valid or not. Checks that username
        exists, and the password associated to that username is correct
        :param username:The user's username
        :param password: A sha-512 hashed password
        :return:true if Login successful otherwise false
        """
        api_user = cls.get_by_username(username)
        if not api_user:
            # Tells that user doesn't exist
            raise Errors.UserNotExist('There is no account with the username: {}'.format(username))
        if not Utils.check_hashed_password(password, api_user.password):
            raise Errors.PasswordIncorrect('Incorrect Password ' +password)

        return api_user

    @classmethod
    def get_by_username(cls,username):
        data = Database.find_one(APIConfig.COLLECTION,{'username': username})
        return cls(**data) if data is not None else False