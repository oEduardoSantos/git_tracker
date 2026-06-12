import sys
import requests
import json
# IP -> domain name DNS
# https://api.github.com/users/{username}/events/public

def main():
    if len(sys.argv) < 2:
        input_error()
    username = sys.argv[1]
    try:
        output = requests.get(f"https://api.github.com/users/{username}/events/public")
    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
        sys.exit(1)
        
    if output.status_code != 200:
        input_error(username)
    
    data = output.json()
    if  not data:
        print(f"No public events found for user: {username}")

    for activity in data:
        act_type = activity.get("type", "UnknownEvent")
        
        repo_data = activity.get("repo", {})
        repo_name = repo_data.get("name", "Unknown Repo")
    
        payload = activity.get("payload", {})
        description = payload.get("description", "No description available")

        print(f"Type: {act_type}")
        print(f"Nome do repositório: {repo_name}")
        print(f"Descrição: {description}")
        print("-" * 40) # Clean separator for readability

def input_error(username=None):
    if not username:
        print("Usage: git_hub_activity <username>")
    else:
        print(f"username: {username}, not found :(")
    sys.exit()

if __name__ == "__main__":
    main()