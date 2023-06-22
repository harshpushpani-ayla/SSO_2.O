from fastapi import APIRouter
   
from fastapi import Depends, Request
from fastapi.security import  HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import  LoginService
import  UserService
import GeneralUtils
import logging,asyncio
from keycloak import KeycloakAdmin,KeycloakOpenID


router=APIRouter()
oauth2_scheme = HTTPBearer()

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

# User class used in request body of user_update endpoint 
class User(BaseModel):
    firstName: str
    lastName: str | None = None
    email: str
    primaryPhoneNumberCountryCode: str | None = None
    primaryPhoneNumber:str
    secondaryPhoneNumberCountryCode:str
    secondaryPhoneNumber:str

# update user endpoint 
@router.put("/api/v1/users/update",tags=["Users"])
async def update_user(uuid:str,user:User,token: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    print(token)
    try:
        print("Received request to update user with UUID ", uuid)
        response_status=LoginService.verify_token(token.credentials)
        if not response_status:
            print("The response has been failed !!!")
            return {"message":"Token Verification Failed !!!"}
        return UserService.update_user(user,uuid)
    except:
        return{"message":"Opps something went wrong !!!"} 

# reset password endpoint 
@router.put("/api/v1/users/resetPassword",tags=["Users"])
async def reset_password(uuid:str,password:str,token: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    try:
         logging.info("Received request to reset password for user with UUID: ", uuid)
         response=UserService.reset_Password(uuid,password)
         if not GeneralUtils.strong_password(password):
             return {"message":"Password too weak, Please Enter a Strong Password !"}
         if response:
             return {"message":"Password Updated Sucessfully !!!"}
         else:
             return {"message":"Unable to update the password !!!"}
    except:
        return {"message":"Something went wrong !!!!"}
		
# delete user endpoint
@router.delete("/api/v1/users/delete",tags=["Users"])
def delete_user(uuid:str,token: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    print("Received request to delete a user with the given uuid ", uuid)
    try:
        user = keycloak_admin.get_user(user_id=uuid)
        if user:
                user_id = user['id']
                keycloak_admin.delete_user(user_id)
                print("User is deleted !!")
                return {"message ":"User sucessfully removed !!!"}
        else:
            print('User not found !!!!')
            return {"message":"User not found !!"}
    except:
        return {"message":"Oops Something went wrong !!!"}
    
# find_user using uuid endpoint     
@router.get("/api/v1/users/findbyUuid",tags=["Users"])
def find_by_id(uuid:str,token: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    print("Received request to findbyUuid for UUID ", uuid)
    try:
        response_status=LoginService.verify_token(token.credentials)
        user=keycloak_admin.get_user(uuid)
        if not user:
            return {"message":"Unable to find the user !!"}
        print(user)
        if response_status:
            return user
        return {"message":"Token expired, try again !!!"}
    except:
        return {"message":"Something went wrong !!!!"}

#find user by username endpoint       
@router.get("/api/v1/users/findbyUsername",tags=["Users"])
def find_username(username:str,token: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    try:
        print("Received request to findbyUsername with puser id")
        response_status=LoginService.verify_token(token.credentials)
        if response_status:
            user=UserService.get_user_info(username)
            return user
        else:
            return {"message ":"Access token has expired !!!"}
    except:
        return {"message":"Opps something went wrong"}      