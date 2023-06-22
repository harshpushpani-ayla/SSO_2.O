from keycloak import KeycloakAdmin
from keycloak import KeycloakOpenIDConnection

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



def get_user_info(email:str):
  try:
    user_id=keycloak_admin.get_user_id(email)
    user_info = keycloak_admin.get_user(user_id=user_id)
    return user_info
  except:
    return None

print(get_user_info("harshpushpani1999@gmail.com"))

#print(get_custom_attribute("test_example@gmail.com","otp"))  
