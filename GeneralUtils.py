import re
from keycloak import KeycloakAdmin
from pydantic import BaseModel
import temp
keycloak_admin = KeycloakAdmin(server_url="http://localhost:8080",
                               username="admin",
                               password="Lame@##@24",
                               realm_name="First_Realm",
                               client_id="harsh",
                               client_secret_key="v7KKaqYbOD4VjTvWOn89ipESFfjiw8jB",
                               verify=True)



def is_valid_email(s):
   pat = "^[a-zA-Z0-9-_.]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
   if re.match(pat,s):
      return True
   return False

def validate_phone_number(string):
    allowed_pattern_for_name = re.compile(r'[^0-9+ ]', re.IGNORECASE)
    str_matcher = allowed_pattern_for_name.search(string)
    return bool(str_matcher)


def find_special_characters(string):
    allowed_pattern_for_name = re.compile(r'[^a-z0-9 ]', re.IGNORECASE)
    str_matcher = allowed_pattern_for_name.search(string)
    return bool(str_matcher)

def strong_password(password):
     allowed_pattern_for_name = re.compile(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$', re.IGNORECASE)
     str_matcher=allowed_pattern_for_name.search(password)
     return bool(str_matcher)

def validate_phone_numbers(user):
    print(user)
    email_id=user.email
    primary_phone_code=user.primaryPhoneNumberCountryCode
    primary_phone_no=user.primaryPhoneNumber
    secondary_phone_code=user.secondaryPhoneNumberCountryCode
    secondary_phone_no=user.secondaryPhoneNumber

    if not primary_phone_code=="":
        invalid_primary=validate_phone_number(primary_phone_code)
        if invalid_primary:
            print("User creation failed, reason - Either country code or phone number not valid",email_id)
            return {"message":"Primary Phone Code Not valid "}
    if not primary_phone_code=="":
        invalid_primary=validate_phone_number(primary_phone_no)
        if invalid_primary:
            print("User creation failed, reason - Either country code or phone number not valid} ",email_id)
            return {"message":"Primary phone number Not Valid"}
    if not secondary_phone_code=="":
        invalid_secondary=validate_phone_number(secondary_phone_code)
        if invalid_secondary:
            print("User creation failed, reason - Either country code or phone number not valid",email_id)
            return {"message":"Secondary Phone Code Not valid "}    
    if not secondary_phone_code=="":
        invalid_primary=validate_phone_number(secondary_phone_no)
        if invalid_secondary:
            print("User creation failed, reason - Either country code or phone number not valid} ",email_id)
            return {"message":"Secondary phone number Not Valid"}
              

def validate_user(user):
    email_id=user.email
    #validate user's phone number !!
    validate_phone_numbers(user)

    #validate email id of the user !!
    if email_id=="" or (not is_valid_email(email_id)):
        return {"message":"Email Not Valid !!"}
    
    # validate first and last name !!
    f_name=user.firstName
    l_name=user.lastName

    if not f_name=="" and len(f_name)<3 or find_special_characters(f_name):
        print("User creation failed, reason - first name not valid} ",email_id)
        return{"message":"first name is not valid !!"}
    
    if not l_name=="" and len(f_name)<3 or find_special_characters(f_name):
        print("User creation failed, reason - last name not valid} ",email_id)
        return{"message":"last name is not valid !!"}
        
