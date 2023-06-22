from fastapi import APIRouter
   
from fastapi import Depends
from fastapi.security import  HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import  LoginService
import  UserService
import logging
from keycloak import KeycloakAdmin,KeycloakOpenID

router=APIRouter()

oauth2_scheme = HTTPBearer()

# connection to keycloak application !!!
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


# send_otp endpoint
@router.post("/api/v1/auth/send_otp",tags=["Authentication"])
async def send_otp(email:str):
    response=LoginService.generate_otp(email)
    try:
        logging.info("OTP generation request received for username",email)
        if response==None:
            return {"message":"Some error occured !!"}
        return response
    except:
        return {
                "message":"check the code, there is some error !!"
                }

# validate otp endpoint 
@router.post("/api/v1/auth/validate_otp",tags=["Authentication"])
async def validate_otp(email:str,otp:int):
    print("OTP verification request received for username :", email)
    response=LoginService.verify_and_clear_otp(email,otp)
    try:
        return response
    except:
        return{"message":"Oops, something went wrong, check code !!!"}


#user_logout endpoint 
@router.post("/api/v1/auth/logout",tags=["Authentication"])
async def logout_user( uuid:str, token: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    try:
        print("Logout Request received for userID , sessionId ", uuid)
        if UserService.logout_user_by_id(uuid):
            return {"message":"User logged out sucessfully "}
        else:
            return {"message":"User not logged out !!"}
    except :
        return {"message":"Oops, something went wrong !!!"}    

#refresh token endpoint
@router.get("/api/v1/auth/refresh_token",tags=["Authentication"])
def refresh_token(r_token:str,token: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    try:
        print("Doing the process of refresh token !")
        return LoginService.refresh_token(r_token)
    except:
        return {"message":"Unable to generate the new token"}
    
#verification of token endpoint 
@router.get("/api/v1/auth/verify_token",tags=["Authentication"])
def verify_token(token: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    try:
        print("Token verification Request received token ", token.credentials)
        response_token=LoginService.verify_token(token.credentials)
        if response_token:
            # Verify the access token and decode it
            print("before")
            # Retrieve the user ID from the token information
            user_info = keycloak_openid.userinfo(token.credentials)
            print(user_info)
            user_id = user_info['sub']
            username=user_info['preferred_username']
            return {"uuid":user_id,
                    "username":username,
                    "message":"token verified !!"
                    }
        else:
            return {"message":"token verification failed !!!, please enter a valid token !!!"}
    except:
        return {"message":"Oops, Something went wrong !!!"}
    

