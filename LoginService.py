
import Keycloak
import Send_email
import UserService
import GeneralUtils
import math,random,string
from datetime import datetime
import logging,requests
from keycloak import KeycloakOpenID
from keycloak import KeycloakAdmin

OTP_VALID_DURATION = 300000
USER_LOCKED_DURATION = 300000
EMAIL_LOCKED_DURATION = 300000

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

#generates 6 digit otp when invoked 
def generate_otp_digit():
    digits="0123456789"
    otp=""
    for i in range(6):
      otp+=digits[math.floor(random.random()*10)]
    return int(otp) 

# generates transaction id of length 50
def generate_transaction_id(length=50):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string
    
    
# function to handle the send_otp endpoint 
def generate_otp(email:str):
    
    # check if the email is valid or not !
    if not GeneralUtils.is_valid_email(email):
        return {"message":"Invalid email"}
    logging.info("OTP generation request email valid :- ", email)
    
    # store the otp and transaction id
    otp_value=generate_otp_digit()
    transaction_id=generate_transaction_id()

    try:
      if Keycloak.get_user_info(email)==None:
          logging.info("OTP generation request: email recieved first time in history" ,email)

          logging.info("OTP generation request",otp_value,email)

          # create a new user
          UserService.create_user(email)
          print("User Created Sucessfully !!!")
      else:
          print("OTP generation request: email already known",email,otp_value)
      user=Keycloak.get_user_info(email)
      print(user)

      current_time = [str(int(datetime.now().timestamp() * 1000))]
      current_time_in_millis = int(datetime.now().timestamp() * 1000)
      print("OTP generation request currentTimeInMillis:", current_time_in_millis)

      # check the OTP for 5 times !!!

      otp_entered_count=UserService.get_custom_attribute(email,"otp_entered_count")[0]
      last_otp_request_time=UserService.get_custom_attribute(email,"otp_requested_time")[0]

      if otp_entered_count!="" and last_otp_request_time!="":
         otp_entered_count_int=int(otp_entered_count)
         otp_requested_time_in_millis=int(last_otp_request_time)
         print("OTP generation request otpRequestedTimeInMillis ", otp_requested_time_in_millis)

         if(otp_requested_time_in_millis + USER_LOCKED_DURATION < current_time_in_millis):
            UserService.put_custom_attribute(email,"otp_entered_count","0")
         elif(otp_entered_count_int>=4):
            print("OTP generation request: User blocked. 5 attepmts over : Email  ",email)
            return("error"," OTP Generation blocked for sometime. 5 attepmts exhausted!")
         else:
            UserService.put_custom_attribute(email,"otp_entered_count",str(otp_entered_count_int+1))			   
      else:
         UserService.put_custom_attribute(email,"otp_entered_count","0")
         
         
      #Verify Email counts

      email_sent_count = UserService.get_custom_attribute(email,"email_sent_count")[0]
      last_email_req_time =UserService.get_custom_attribute(email,"email_requested_time")[0]

      if email_sent_count!="":
         email_sent_count_int=int(email_sent_count)
         last_email_req_time_int=int(last_email_req_time)
         print("OTP generation request emailRequestedTimeInMillis ", last_email_req_time_int)
         if email_sent_count_int>=11 and last_email_req_time_int + EMAIL_LOCKED_DURATION > current_time_in_millis:
            print("OTP generation request: Email sending blocked. Can not send more than 11 email in a min. Email ", email)
            return("error", "Email sending blocked for sometime. Can not send more than 11 email in a min")
         elif last_email_req_time_int + EMAIL_LOCKED_DURATION > current_time_in_millis:
            print("..................")
            UserService.put_custom_attribute(email,"email_sent_count",str(email_sent_count_int+1))
         else:
            UserService.put_custom_attribute(email,"email_sent_count","1")
            UserService.put_custom_attribute(email,"email_requested_time",str(current_time_in_millis))
      else:
         UserService.put_custom_attribute(email,"email_sent_count","1")
         UserService.put_custom_attribute(email,"email_requested_time",str(current_time_in_millis))

      UserService.put_custom_attribute(email,"otp",str(otp_value))
      print(UserService.get_custom_attribute(email,"otp")[0])
      print("OTP generation request: currentTime :",current_time)
      UserService.put_custom_attribute(email,"otp_requested_time",current_time)   
      Send_email.send_otp(otp_value,email)
      return {"message":"OTP sent successfully !!"}
    except:
       return None

# function to handle the verify_otp endpoint     
def verify_and_clear_otp(email:str,otp:str):
   
   #check if email is valid or not !
   if not GeneralUtils.is_valid_email(email):
      return{"Message":"This email is not valid !!"}
    
   print("OTP validation request email valid  ", email)
   result={}

   if not Keycloak.get_user_info(email):
      return{"Message":"This email does not exist !!"}
   
   user_otp=UserService.get_custom_attribute(email,"otp")[0]
   current_time_in_millis = int(datetime.now().timestamp() * 1000)
   print("OTP validation request currentTimeInMillis: ", current_time_in_millis)
   otp_requested_time_in_millis=int(UserService.get_custom_attribute(email,"otp_requested_time")[0])
   print("OTP validation request otpRequestedTimeInMillis {} ", otp_requested_time_in_millis)

   #Check for 5 continuous failures
   otp_entered_count=UserService.get_custom_attribute(email,"otp_entered_count")[0]
   otp_entered_count_int=int(otp_entered_count)
   otp_entered_count=str(otp_entered_count_int+1)

   if otp_requested_time_in_millis+OTP_VALID_DURATION<current_time_in_millis:
      print("OTP validation request: OTP has expired : Email  ", email)
      #result.put(AylaConstants.STATUS, "fail");
      #result.put("error", "OTP expired!");
      return {"message":"OTP expired !!"}
   elif otp_entered_count_int>=5:
      print("OTP validation request: 5 continuous attempt of wrong OTP : Email ", email)
      #result.put(AylaConstants.STATUS, "fail");
      #result.put("error", "5 attepmts exhausted!");
      return{"message":"5 attempts exhausted !!!"}
   elif str(user_otp)==str(otp):
      print("OTP validation request: OTP valid for email ", email)
      result=UserService.get_access_token(email)
      val=str(result["access_token"])
      print(val)
      #UserService.put_custom_attribute(email,"access_token",val)
      if UserService.get_custom_attribute(email,"first_name") == "":
         result["userStatus"]="new"
      else:
         result["userStatus"]="new"

   else:
      print("OTP validation request: OTP invalid for email  ",email)
      result["status"]="fail"
      result["error"]="OTP validation failed!"
      UserService.put_custom_attribute(email,"otp_entered_count",otp_entered_count)
   print(otp)
   print(user_otp)   
   return result    

#function to handle verify_token endpoint !   
def verify_token(token:str):
   url="http://localhost:8080/realms/First_Realm/protocol/openid-connect/userinfo"
   headers={'User-Agent': 'My User Agent',
            'Custom-Header': 'Custom Value',
            'Authorization': 'Bearer '+ token,
            }
   response = requests.get(url, headers=headers)
   print("Doing token verification !!!!")
   return response.status_code==200

#function to handle refresh_token endpoint !
def refresh_token(r_token):
   token=keycloak_openid.refresh_token(r_token)

   new_access_token=token['access_token']
   new_refresh_token=token['refresh_token']

   return {"access_token":new_access_token,
         "new_refresh_token":new_refresh_token}
   


