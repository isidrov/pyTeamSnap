import requests
import json
import configparser
import csv

class TeamSnapAPI:

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.access_token = config['api']['access_token']
        self.headers = {
            "Authorization": f"Bearer {self.access_token}"
        }

    def find_me(self):
        API_HREF = "https://api.teamsnap.com/v3/me"
        response = requests.get(API_HREF, headers=self.headers)
        if response.status_code == 200:
            print("find_me() was successful!\n")
            parsed_json = response.json()
            user_id = parsed_json["collection"]["items"][0]["data"][00]["value"]
            return user_id
        else:
            print(f"Request failed with status code: {response.status_code}")
            print(response.text)
            return None

    # ... [Include other methods here in the same manner]
    # ...

    def get_url(self,url):

        # Obtain API specification for an endpoint given URL
        
        API_HREF = url

        response = requests.get(API_HREF, headers=headers)

        if response.status_code == 200:

            print("get_url() was successful!\n")

            parsed_json = response.json()

            return parsed_json

        else:
            print(f"Request failed with status code: {response.status_code}")
            print(response.text)

    def list_teams(self,userid):

        params = {
            'user_id': userid
        }

        API_HREF = f"https://api.teamsnap.com/v3/teams/search"

        response = requests.get(API_HREF, headers=self.headers, params=params)

        if response.status_code == 200:

            print("list_teams() was successful!\n")
            parsed_json = response.json()

            list_of_teams = []

            for team_item in parsed_json["collection"]["items"]:
                team_data = team_item["data"]
                team = {}
                for item in team_data:
                    team[item["name"]] = item["value"]

                list_of_teams.append(team)

            return list_of_teams


        else:
            print(f"Request failed with status code: {response.status_code}")
            print(response.text)
    
    def list_events(self,userid=None,teamid = None):

        params = {
            'user_id': userid,
            'team_id': teamid
        }

        API_HREF = f"https://api.teamsnap.com/v3/events/search"  # Replace with your endpoint URL

        response = requests.get(API_HREF, headers=self.headers, params=params)

        if response.status_code == 200:

            print("list_events() was successful!")
            parsed_json = response.json()

            list_of_events = []

            for item in parsed_json["collection"]["items"]:
                data = item["data"]
                event = {}
                for subitem in data:
                    event[subitem["name"]] = subitem["value"]

                list_of_events.append(event)

            return list_of_events

        else:
            print(f"Request failed with status code: {response.status_code}")
            print(response.text)
    
    def search_user(self,userid):

        params = {
            'id': userid
        }

        API_HREF = f"https://apiv3.teamsnap.com/users/search"  # Replace with your endpoint URL

        response = requests.get(API_HREF, headers=headers, params=params)

        if response.status_code == 200:

            print("search_user() was successful!\n")

            parsed_json = response.json()

            print(f"id: is {parsed_json['collection']['items'][0]['data'][0]['value']}")
            print(f"email: {parsed_json['collection']['items'][0]['data'][5]['value']}")
            print(f"First Name: {parsed_json['collection']['items'][0]['data'][8]['value']}")
            print(f"Last Name: {parsed_json['collection']['items'][0]['data'][10]['value']}\n")

        else:
            print(f"Request failed with status code: {response.status_code}")
            print(response.text)

    def create_team_member(self,member):

        API_HREF = f"https://api.teamsnap.com/v3/members"  # Replace with your endpoint URL

        response = requests.post(API_HREF, headers=headers, json=member)

        if response.status_code in (200, 201, 204):

            print(f"{response.status_code} request successful!")

        else:
            print(f"Request failed with status code: {response.status_code}")
            print(response.text)

    # https://api.teamsnap.com/v3/events/search?user_id=28819952'



    def list_members(self,team_id):

        params = {
            'team_id': team_id
        }

        API_HREF = f"https://api.teamsnap.com/v3/members/search"  # Replace with your endpoint URL

        response = requests.get(API_HREF, headers=headers, params=params)

        if response.status_code == 200:

            print("list_members() was successful!")
            parsed_json = response.json()
            print("n")

            myList = []

            for item in parsed_json["collection"]["items"]:
                data = item["data"]
                team = {}
                for subitem in data:
                    team[subitem["name"]] = subitem["value"]

                myList.append(team)

            return myList

        else:
            print(f"Request failed with status code: {response.status_code}")
            print(response.text)

    @staticmethod
    def print_list(list,variables=[]):
        
        if variables:
            for item in list:
                for variable in variables:
                    print(f"{variable}: {item[variable]}")
                print("---------------------------------------------")
        else:
            for dict in list:
                for k,v in dict.items():
                    print(f"{k}: {v}")
                print("---------------------------------------------")
                    
                
            
    @staticmethod
    def csv_to_data_dict(filename):
        """
        Convert a CSV file into a data dictionary, skipping the first row.

        Args:
        - filename (str): Path to the CSV file.

        Returns:
        - dict: The converted data dictionary.
        """

        with open(filename, 'r') as file:
            reader = csv.reader(file)

            # Skip the very first row
            next(reader)

            # Read the second row (headers) and assign to "name" keys
            headers = next(reader)

            # Store resulting data
            data_list = []

            # Read the rest of the rows (values)
            for row in reader:
                for header, value in zip(headers, row):
                    if value:  # Skip cells with no value
                        data_list.append({"name": header, "value": value})

        return {
            "template": {
                "data": data_list
            }
        }

    @staticmethod
    def print_members(memberList):

        for member in memberList:
            print(f"First Name: {member['first_name']}")
            print(f"Last Name: {member['last_name']}")
            print(f"Email address: {member['email_addresses']}\n")

    @staticmethod
    def write_to_json_file(data, filename="output.json"):
        """
        Write a Python dictionary to a JSON file.

        Parameters:
        - data (dict): The dictionary to write to the file.
        - filename (str): The name of the file to which the data should be written. Defaults to "output.json".

        Returns:
        None
        """
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
