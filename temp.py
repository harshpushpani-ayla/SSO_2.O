
# class named User for creating a custom attributes 
class User:
    def __init__(self):
        self.first_name=""
        self.last_name=""
        self.username=""
        self.uuid=""
        self.password="1234567"
        self.primary_phone_number_country_code=""
        self.primary_phone_number=""
        self.secondary_phone_number_country_code=""
        self.secondary_phone_number=""
        self.otp_requested_time=""
        self.otp_entered_count=""
        self.otp=""
        self.email_sent_count=""
        self.email_requested_time=""
    
    # function to fetch all the attributes 
    def fetch_all_attributes(self):
        return {
            "uuid":self.uuid,
            "first_name":self.first_name,
            "last_name":self.last_name,
            "username": self.username,
            "password": self.password,
            "primary_phone_number_country_code":self.primary_phone_number_country_code,
            "primary_phone_number": self.primary_phone_number,
            "secondary_phone_number_country_code": self.secondary_phone_number_country_code,
            "secondary_phone_number": self.secondary_phone_number,
            "otp_requested_time": self.otp_requested_time,
            "otp_entered_count":  self.otp_entered_count,
            "otp": self.otp,
            "email_sent_count":  self.email_sent_count,
            "email_requested_time": self.email_requested_time
        }
    
    # function to put values into attributes 
    def put_attribute(self,attribute,value):
        try:
            setattr(self,attribute,value)
            print(getattr(self,attribute))
            return True
        except:
            print("Something went wrong in updating the attribute: ",attribute)
            return False

    def get_attribute(self,attribute):
        try:
            return getattr(self,attribute)
        except:
            return None
        
               



        
        