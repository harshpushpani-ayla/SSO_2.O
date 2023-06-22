from keycloak import KeycloakAdmin
from keycloak import KeycloakOpenIDConnection
from keycloak import KeycloakOpenID
import GeneralUtils
import temp
from pydantic import BaseModel

# Initialize KeycloakOpenID instance
keycloak_openid = KeycloakOpenID(server_url="http://localhost:8080",
                                 client_id="harsh",
                                 realm_name="First_Realm",
                                 client_secret_key="v7KKaqYbOD4VjTvWOn89ipESFfjiw8jB")


keycloak_admin = KeycloakAdmin(server_url="http://localhost:8080",
                               username="admin",
                               password="Lame@##@24",
                               realm_name="First_Realm",
                               client_id="harsh",
                               client_secret_key="v7KKaqYbOD4VjTvWOn89ipESFfjiw8jB",
                               verify=True)

keycloak_connection = KeycloakOpenIDConnection(server_url="http://localhost:8080",  
username='admin',
 password='Lame@##@24', 
 realm_name="First_Realm", 
 user_realm_name="First_Realm", 
 client_id="harsh", 
 client_secret_key="v7KKaqYbOD4VjTvWOn89ipESFfjiw8jB", 
 verify=True) 

#constant value (initially provided )
old_password="1234567"
uuid=""
username=""

#function provides the information about the user !!
def get_user_info(email:str):
  global uuid
  try:
    user_id=keycloak_admin.get_user_id(email)
    user_info = keycloak_admin.get_user(user_id=user_id)
    return user_info
  except:
    return None

#function to create a new user !!!
def create_user(email: str):
    # creating an instance of KeylcloakAdmin
    keycloak_admin_instance = KeycloakAdmin(connection=keycloak_connection, server_url="http://localhost:8080")
    
    global uuid
    global username
    user=temp.User()
    user_data = {
        "username": email,
        "email": email,
        "enabled": True,
        "credentials": [
            {
                "type": "password",
                "value": "1234567",
                "temporary": False
            }
        ],
        "attributes":user.fetch_all_attributes() 
    }

    try:
        new_user = keycloak_admin_instance.create_user(user_data)
        print(new_user)
        uuid=new_user
        username=email
        return new_user
    except:
        print("Something went wrong!")
        return None


#function to get values of custom attribute   
def get_custom_attribute(username:str,attribute:str):

  user_info=get_user_info(username)
  custom_attribute=user_info.get("attributes",{})
  try:
    print("Sucess of get !!!")
    #print(custom_attribute)
    return custom_attribute[attribute]
  except:
    return None

#function to put values into the custom attribute   
def put_custom_attribute(username: str, attribute: str, value: str):
    user_id = keycloak_admin.get_user_id(username)
    user = keycloak_admin.get_user(user_id)
    try:
      user["attributes"][attribute] = value
      keycloak_admin.update_user(user_id, {"attributes": user["attributes"]})
      print("Success of put !")
      return True
    except:
       print("Failure !")
       return False
    
# function to logout the user
def logout_user_by_id(id):
   try:
     user_sessions = keycloak_admin.get_sessions(user_id=id)
     for session in user_sessions:
        keycloak_admin.logout_user_session(session['id'])
     return True   
   except:
      return False

#function to get the access_token          
def get_access_token(email:str):
# Get access token for user
  username = email
  password = "1234567"
  token_response = keycloak_openid.token(username=username, password=password)
  user_id=keycloak_admin.get_user_id(email)
  result = {}
  result["access_token"] = token_response["access_token"]
  result["expires_in"] = token_response["expires_in"]
  result["refresh_token"] = token_response["refresh_token"]
  result["refresh_token_expires_in"] = token_response["refresh_expires_in"]
  result["token_type"] = token_response["token_type"]
  result["uuid"] = user_id
  result["session_id"] = token_response["session_state"]

  return result
    
#function to update user using uuid 
def update_user(user,user_id:str):

  GeneralUtils.validate_user(user)
  user_=keycloak_admin.get_user(user_id)
  
  email=user_["email"]
  

  # all the necessary attributes for user 
  primary_phone_code=user.primaryPhoneNumberCountryCode
  primary_phone_no=user.primaryPhoneNumber
  secondary_phone_code=user.secondaryPhoneNumberCountryCode
  secondary_phone_no=user.secondaryPhoneNumber
  f_name=user.firstName
  l_name=user.lastName
  u_email=user.email
  
  try:
     
     if not primary_phone_code=="string":
        put_custom_attribute(email,"primary_phone_number_country_code",primary_phone_code)
     else:
        primary_phone_code=""  

     if not primary_phone_no=="string":
        put_custom_attribute(email,"primary_phone_number",primary_phone_no)
     else:
        primary_phone_no=""  

     if not secondary_phone_code=="string":
        put_custom_attribute(email,"secondary_phone_number_country_code",secondary_phone_code)
     else:
        secondary_phone_code=""


     if not secondary_phone_no=="string":
        put_custom_attribute(email,"secondary_phone_number",secondary_phone_no)
     else:
        secondary_phone_no=""  

     if not f_name=="string":
        put_custom_attribute(email,"first_name",f_name)
     else:
        f_name=""  

     if not l_name=="string":
        put_custom_attribute(email,"last_name",l_name)
     else:
        l_name=""
     if not u_email=="string" and GeneralUtils.is_valid_email(u_email):
        changed_user=keycloak_admin.get_user(user_id)
        changed_user["email"]=u_email
        keycloak_admin.update_user(user_id,changed_user)
        print("Email changed successfully !!!")
     else:
        u_email=email
              


     print(keycloak_admin.get_user(user_id))
     return {
        "firstName": f_name,
        "lastName": l_name,
        "email": u_email,
        "primaryPhoneNumberCountryCode": primary_phone_code,
        "primaryPhoneNumber": primary_phone_no,
        "secondaryPhoneNumberCountryCode": secondary_phone_code,
        "secondaryPhoneNumber": secondary_phone_no
     }
  
  except:
     return {"message":"User updation failed !!!"}  

  
#function to reset the password of the user !!
def reset_Password(uuid:str,password:str):
   try:
      user=keycloak_admin.get_user(uuid)
      username=user["username"]
      print(username)
      print(user)
      print("-----------")
      keycloak_admin.set_user_password(uuid,password)
      put_custom_attribute(username,'password',password)
      return True
   except:
      print("Something went wrong !!!")
      return False   

#function return the credentials of the user !!
def get_credentials():
   return {"uuid":uuid,
           "username":username,
           "password":old_password
           }
                    
