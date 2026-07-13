import requests
import create_agent_to_server_test_payload
import create_dashboard_payload
import create_roles_payload
import create_http_test_payload
import create_dns_server_payload
import create_page_load_test_payload

def get_api_data(url, params=None):
    
    try:
        
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        print(response.text)
        return None
#def get account group ():
#def get agent id(aid):
#def add roles(aid):
#def add tests(aid, agent_id):
#def add dashboard and widgets(aid, test_id):
if __name__ == "__main__":
    oauth_token = "01ab-7ae13326-63e6-4b6d-ba99-158c71e05a46" # OAuth token
    headers = { "Accept": "application/json", "content-type": "application/json", "authorization": f"Bearer {oauth_token}"}
    api_url_roles = "https://api.thousandeyes.com/v7/roles" # API URL for roles with Timo's Sandbox account ID
    api_url_agent_tests= "https://api.thousandeyes.com/v7/tests/agent-to-server" # API URL for tests 
    api_url_http_tests= "https://api.thousandeyes.com/v7/tests/http-server" # API URL for tests 
    api_url_dns_server_tests= "https://api.thousandeyes.com/v7/tests/dns-server" # API URL for tests
    api_url_page_load_tests= "https://api.thousandeyes.com/v7/tests/page-load" # API URL for tests
    
    api_url_dashboards = "https://api.thousandeyes.com/v7/dashboards" # API URL for dashboards with Timo's Sandbox account ID
    account_group_id = []

#get account group id
name = input("What is the customer name?")
account_group_url = "https://api.thousandeyes.com/v7/account-groups"
response = requests.get(account_group_url, headers=headers)
if response.ok:
    account_groups = response.json()
    for group in account_groups["accountGroups"]:
        if group["accountGroupName"] == name:
            account_group_id = group["aid"]
            print(f"Account Group ID: {account_group_id}")

#get agent id
agents_url = "https://api.thousandeyes.com/v7/agents"
response = requests.get(agents_url, headers=headers, params={"aid": account_group_id})
agent_list = []
if response.ok:
      agents = response.json()
      for agent in agents["agents"]:
          if agent["agentType"] == "enterprise":
              agent_id = agent["agentId"]
              print(f"Agent ID: {agent_id}")
              agent_list.append(agent_id)


#get test label id

# response = requests.get(api_url_tests, headers=headers, params={"aid": account_group_id})
# label_list = []
# if response.ok:
#       labels = response.json()
#       for label in labels["TestLabels"]:
#           if label["name"] == "MSTeams":
#               label_id = label["labelId"]
#               print(f"Label ID: {label_id}")
#               label_list.append(label_id)        


#i is for testing only REMOVE BEFORE GOING LIVE
#i=19


#add roles
roles= create_roles_payload.create_roles()
for role in roles:
        response = requests.post(api_url_roles,json=role, headers=headers, params={"aid": account_group_id}) 
#check if roles were added successfully
data = get_api_data(api_url_roles, params=None)
if data:
        #print(data)
        print("Role Data received successfully")
else:
        print("An error occurred")


#add agent tests 
#test_ids = {}
tests = create_agent_to_server_test_payload.create_agent_tests(agent_list)
for test in tests:
        response = requests.post(api_url_agent_tests,json=test, headers=headers,params={"aid": account_group_id})
        #test_ids[response.json().get("testId")] = test["testName"]
    
#check if tests were added successfully
data = get_api_data(api_url_agent_tests, params=None)
if data:
        #print(data)
        print("Agent-to-Server Test Data received successfully")
else:
        print("An error occurred")


#add http tests
test_ids = {}
tests = create_http_test_payload.create_http_tests(agent_list)
for test in tests:
        response = requests.post(api_url_http_tests,json=test, headers=headers,params={"aid": account_group_id})
        test_ids[response.json().get("testId")] = test["testName"]
    
#check if tests were added successfully
data = get_api_data(api_url_http_tests, params=None)
if data:
        #print(data)
        print("HTTP Server Test Data received successfully")
else:
        print("An error occurred")


#add dns-server tests
test_ids = {}
tests = create_dns_server_payload.create_dns_server_tests(agent_list)
for test in tests:
        response = requests.post(api_url_dns_server_tests,json=test, headers=headers,params={"aid": account_group_id})
        test_ids[response.json().get("testId")] = test["testName"]
    
#check if tests were added successfully
data = get_api_data(api_url_dns_server_tests, params=None)
if data:
        #print(data)
        print("DNS Server Test Data received successfully")
else:
        print("An error occurred")

#add page load tests
test_ids = {}
tests = create_page_load_test_payload.create_page_load_tests(agent_list)
for test in tests:
        response = requests.post(api_url_page_load_tests,json=test, headers=headers,params={"aid": account_group_id})
        test_ids[response.json().get("testId")] = test["testName"]
    
#check if tests were added successfully
data = get_api_data(api_url_page_load_tests, params=None)
if data:
        #print(data)
        print("Page Load Test Data received successfully")
else:
        print("An error occurred")

#add dashboard and widgets
dashboards= create_dashboard_payload.create_dashboards(test_ids)
for dashboard in dashboards:
        response = requests.post(api_url_dashboards,json=dashboard, headers=headers,params={"aid": account_group_id}) 

#check if dashboard was added successfully
data = get_api_data(api_url_dashboards, params=None)
if data:
    #print(data)
    print("Dashboard Data received successfully")
else:
        print("An error occurred")
