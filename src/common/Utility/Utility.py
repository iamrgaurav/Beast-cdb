import src.common.errors as Errors
from src.common.Utility.utils import Utils
class CommonUtility:
    @staticmethod
    def formating_name(name):
        f_name = name.strip()
        if Utils.is_name_has_valid_format(f_name):
            return f_name
        else:
            raise Errors.NameError(
                    "Name must Have only alphabet and Whitespace and can have length 2-30 Characters"
                )

    @staticmethod
    def formating_aadhaar(aadhaar):
        f_adhaar = aadhaar.strip()
        if Utils.is_adhaar_valid(f_adhaar):
            if len(f_adhaar)==14:
                f_adhaar = f_adhaar[0:4]+f_adhaar[5:9]+f_adhaar[10:14]
            return f_adhaar
        else:
            raise Errors.AadhaarError(
                "Aadhaar can be of length 12 or 14(with space) and can contain only digit"
            )

    @staticmethod
    def formating_phone(phone):
        f_phone = phone.strip()
        if Utils.is_phone_valid(f_phone):
            if f_phone[0:3]=="+91":
                return f_phone
            if f_phone[5]=="-":
                f_phone = "+91"+f_phone[0:5]+f_phone[6:11]
            else:
                f_phone = "+91"+f_phone
            return f_phone
        else:
            raise Errors.PhoneError("Phone Number must be of the format xxxxx-xxxxx or xxxxxxxxxx")

