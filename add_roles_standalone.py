#!/opt/local/bin/python3
import requests

def get_api_data(url, params=None):
    
    try:
        
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        print(response.text)
        return None


if __name__ == "__main__":
    #oauth_token = "01ab-7ae13326-63e6-4b6d-ba99-158c71e05a46" # OAuth token, should be changed to the one that NOC uses
    oauth_token = "01ab-7ae13326-63e6-4b6d-ba99-158c71e05a46" # OAuth token, should be changed to the one that NOC uses
    headers = { "Accept": "application/json", "content-type": "application/json", "authorization": f"Bearer {oauth_token}"}
    api_url_roles = "https://api.thousandeyes.com/v7/roles" # API URL 
    api_url_agent_tests= "https://api.thousandeyes.com/v7/tests/agent-to-server" # API URL for tests 
    account_group_id = []   

name = input("What is the customer name?")
account_group_url = "https://api.thousandeyes.com/v7/account-groups"
response = requests.get(account_group_url, headers=headers)
if response.ok:
    account_groups = response.json()
    for group in account_groups["accountGroups"]:
        if group["accountGroupName"] == name:
            account_group_id = group["aid"]
            print(f"Account Group ID: {account_group_id}")    

            


def create_roles():
    roles = [
        {"name": "AAD_Elisa_Tutka_orgadmin", "permissions": ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36","37","39","43","44","45","46","47","48","49","50","51","53","54","55","56","57","58","59","60","61","62","63","64","65","66","67","68","69","70","71","72","74","75","76","84","85","86","87","88","89","90","91","92","93","94","95","96","97","98","99","100","101","102","103","104","105","106","107","111","112","114","115"]},
        {"name": "AAD_Elisa_Tutka_accountadmin", "permissions": ["1","2","3","4","6","7","8","9","11","12","14","16","17","20","21","22","23","24","25","26","27","28","29","30","31","32","33","32","44","46","53","54","57","58","59","60","61","64","65","66","67","68","71","74","75","84","85","86","87","88","89","90","91","93","94","95","96","97","98","99","100","101","102","104","105","106","107","111","112","114","115","116","117","118","119","120","121","122","123","124","125","126","128","130"]},
        {"name": "AAD_Elisa_Tutka_noc", "permissions": ["1","2","5","6","7","8","9","10","11","13","15","16","20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36","42","44","45","48","50","53","54","55","56","58","59","60","61","62","63","64","65","66","67","68","69","70","71","72","74","75","76","84","85","86","87","88","89","90","91","93","94","95","96","99","100","101","102","104","105","106","107","111","112","114","115"]},
        {"name": "AAD_Elisa_Tutka_sd", "permissions": ["1","2","3","6","8","10","11","12","15","16","20","22","26","27","28","29","30","31","33","36","37","42","45","46","47","48","50","54","55","60","61","62","65","67","68","69","70","71","72","74","75","76","84","85","87","89","91","92","93","94","95","98","99","101","106","107","114"]},
        {"name": "AAD_Elisa_Tutka_user", "permissions": ["5","8","10","11","13","15","16","20","22","26","28","30","32","33","35","53","55","56","62","63","65","67","70","74","75","84","85","87","89","91","93","94","95","99","101","104","106","107","111","114"]}
    ]
    return roles

roles = create_roles()
for role in roles:
        response = requests.post(api_url_roles,json=role, headers=headers, params={"aid": account_group_id}) 
#check if roles were added successfully
data = get_api_data(api_url_roles, params=None)
if data:
        #print(data)
        print("Role Data received successfully")
else:
        print("An error occurred")
