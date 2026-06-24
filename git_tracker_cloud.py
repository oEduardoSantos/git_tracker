import sys
import urllib.request
import urllib.error
import json


def main():
    if len(sys.argv) < 2:
        print("Usage: github-activity <username>")
        sys.exit(1)

    username = sys.argv[1]
    data = fetch_events(username)

    if not data:
        print(f"No public events found for user: {username}")
        sys.exit(0)

    for activity in data:
        print(f"- {format_event(activity)}")


def fetch_events(username):
    url = f"https://api.github.com/users/{username}/events/public"
    try:
        with urllib.request.urlopen(url) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"Error: User '{username}' not found.")
        else:
            print(f"HTTP error: {e.code} {e.reason}")
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Network error: {e.reason}")
        sys.exit(1)


def format_event(activity):
    act_type = activity.get("type", "UnknownEvent")
    repo_name = activity.get("repo", {}).get("name", "Unknown Repo")
    payload = activity.get("payload", {})

    if act_type == "PushEvent":
        count = len(payload.get("commits", []))
        return f"Pushed {count} commit(s) to {repo_name}"

    elif act_type == "IssuesEvent":
        action = payload.get("action", "interacted with")
        return f"{action.capitalize()} an issue in {repo_name}"

    elif act_type == "IssueCommentEvent":
        return f"Commented on an issue in {repo_name}"

    elif act_type == "WatchEvent":
        return f"Starred {repo_name}"

    elif act_type == "ForkEvent":
        return f"Forked {repo_name}"

    elif act_type == "CreateEvent":
        ref_type = payload.get("ref_type", "resource")
        ref = payload.get("ref", "")
        if ref:
            return f"Created a {ref_type} '{ref}' in {repo_name}"
        return f"Created a {ref_type} in {repo_name}"

    elif act_type == "DeleteEvent":
        ref_type = payload.get("ref_type", "resource")
        ref = payload.get("ref", "")
        return f"Deleted {ref_type} '{ref}' in {repo_name}"

    elif act_type == "PullRequestEvent":
        action = payload.get("action", "interacted with")
        return f"{action.capitalize()} a pull request in {repo_name}"

    elif act_type == "PullRequestReviewEvent":
        return f"Reviewed a pull request in {repo_name}"

    elif act_type == "PullRequestReviewCommentEvent":
        return f"Commented on a pull request in {repo_name}"

    elif act_type == "ReleaseEvent":
        action = payload.get("action", "published")
        tag = payload.get("release", {}).get("tag_name", "")
        if tag:
            return f"{action.capitalize()} release {tag} in {repo_name}"
        return f"{action.capitalize()} a release in {repo_name}"

    elif act_type == "PublicEvent":
        return f"Made {repo_name} public"

    elif act_type == "MemberEvent":
        action = payload.get("action", "updated")
        member = payload.get("member", {}).get("login", "someone")
        return f"{action.capitalize()} {member} as a collaborator in {repo_name}"

    else:
        return f"{act_type} in {repo_name}"


if __name__ == "__main__":
    main()
