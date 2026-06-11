import sys
import requests
import json
# IP -> domain name DNS
# https://api.github.com/users/{username}/events/public
def main():
    try:
        username = sys.argv[1]
    except:
        input_error()
    
    output = requests.get(f"https://api.github.com/users/{username}/events/public")
    if output.status_code == 200:
        data = output.json()
    else:
        input_error(username)
    
    for activity in data:
        print(f"Type:{activity["type"]}\nNome do repositório: {activity["repo"]["name"]}\nDescrição: {activity["payload"]["description"]}\n")

def input_error(username):
    if not username:
        print("Usage: git_hub_activity <username>")
    else:
        print(f"username: {username}, not found :(")
    sys.exit()

main()