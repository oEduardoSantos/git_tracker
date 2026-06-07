import sys

def main():
    user_input = sys.argv[1]
    if user_input == "git_hub_activity":
        git_hub_user = sys.argv[2]
        
    else:
        input_error(sys.argv[2])

def input_error(username):
    if not username:
        print("Usage: git_hub_activity <username>")
    else:
        print(f"username: {username}, not found :(")

main()