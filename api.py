import requests
import re
from datetime import date, datetime
from fastapi import FastAPI
from collections import Counter
import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("GITHUB_TOKEN")

HEADERS = {"Authorization": f"Bearer {TOKEN}",
           "Accept": "application/vnd.github+json",
           "X-GitHub-Api-Version": "2026-03-10"}

def getUser(username):
    URL = f"https://api.github.com/users/{username}"
    print("getting users")
    user = requests.get(URL, headers=HEADERS).json()
    print("got user")
    return user

def getFollowers(data):
    URL = data["followers_url"]
    print("getting followers")
    followers = requests.get(URL, headers=HEADERS).json()
    print("got followers")
    return followers

def getFollowing(data):
    URL = data["following_url"]
    URL = re.sub(r'\{.*?\}', "", URL)
    print("getting following")
    following = requests.get(URL, headers=HEADERS).json()
    print("got following")
    return following

def getGists(data):
    URL = data["gists_url"]
    URL = re.sub(r'\{.*?\}', "", URL)
    print("getting gists")
    gists = requests.get(URL, headers=HEADERS).json()
    print("got gists")
    return gists

def getStarred(data):
    URL = data["starred_url"]
    URL = re.sub(r'\{.*?\}', "", URL)
    print("getting starred")
    starred = requests.get(URL, headers=HEADERS).json()
    print("got starred")
    return starred

def getOrgs(data):
    URL = data["organizations_url"]
    print("getting orgs")
    orgs = requests.get(URL, headers=HEADERS).json()
    print("got orgs")
    return orgs

def getEvents(data):
    URL = data["events_url"]
    URL = re.sub(r'\{.*?\}', "", URL)
    print("getting event")
    events = requests.get(URL, headers=HEADERS).json()
    print("got events")
    return events

def getRepos(data):
    URL = data["repos_url"]
    print("getting repos")
    repos = requests.get(URL, headers=HEADERS).json()
    print("got repos")
    return repos

def main(user):
    userdat = getUser(user)
    numberStarred = 0
    numberRepos = 0
    leastStars = float("inf")
    maxStars = 0
    totalStars = 0
    mostStarred = ""
    age = date.today() - datetime.strptime(userdat["created_at"], "%Y-%m-%dT%H:%M:%SZ").date()
    starred = getStarred(userdat)
    repos = getRepos(userdat)
    languages = Counter()
    for _ in starred:
        numberStarred += 1
    for repo in repos:
        numberRepos += 1
        if repo["stargazers_count"] > maxStars:
            maxStars = repo["stargazers_count"]
            mostStarred = repo["full_name"]
        if repo["stargazers_count"] < leastStars:
            leastStars = repo["stargazers_count"]
        totalStars += repo["stargazers_count"]
        lang = repo["language"]
        languages[lang] += 1
    print("starred", numberStarred)
    print("repos", numberRepos)
    print("leastStars", leastStars)
    print("maxStars", maxStars)
    print("age", age.days)
    print("moststarred", mostStarred)
    return {"numberStarred": numberStarred, "numberRepos": numberRepos, "leastStars": leastStars, "maxStars": maxStars,
            "totalStars": totalStars, "age": age.days, "mostStarred": mostStarred, "lang": languages.most_common(1)}
    
def api():   
    app = FastAPI()
    @app.get("/{identifier}")
    def root(identifier):
        return main(identifier)

    uvicorn.run(app, host="127.0.0.1", port=8000)
        

if __name__ == "__main__":
    api()