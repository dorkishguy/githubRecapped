import requests
import re
from datetime import date, datetime
from fastapi import FastAPI
from collections import Counter
import uvicorn

HEADERS = {"Accept": "application/vnd.github+json",
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

from collections import Counter
from datetime import date, datetime

def main(name):
    user = getUser(name)
    starred = getStarred(user)
    repos = getRepos(user)

    numberStarred = len(starred)
    numberRepos = len(repos)
    leastStars = float('inf')
    maxStars = 0
    totalStars = 0
    mostStarred = ""
    languages = Counter()
    totalForks = 0
    mostForked = ""
    maxForks = 0
    licenses = Counter()

    age = date.today() - datetime.strptime(user["created_at"], "%Y-%m-%dT%H:%M:%SZ").date()

    for repo in repos:
        stars = repo["stargazers_count"]
        forks = repo["forks_count"]

        totalStars += stars
        totalForks += forks

        if stars > maxStars:
            maxStars = stars
            mostStarred = repo["full_name"]
        if stars < leastStars:
            leastStars = stars
        if forks > maxForks:
            maxForks = forks
            mostForked = repo["full_name"]

        lang = repo["language"] or "Unknown"
        languages[lang] += 1

        lic = repo["license"]["name"] if repo["license"] else "No License"
        licenses[lic] += 1
    print("starred", numberStarred)
    print("repos", numberRepos)
    print("leastStars", leastStars)
    print("maxStars", maxStars)
    print("totalStars", totalStars)
    print("totalForks", totalForks)
    print("age", age.days)
    print("moststarred", mostStarred)
    print("mostforked", mostForked)
    print("top language", languages.most_common(1))
    print("license breakdown", licenses)
    return {"numberStarred": numberStarred, "numberRepos": numberRepos, "leastStars": leastStars, "maxStars": maxStars, "totalStars": totalStars, "totalForks": totalForks, "age": age.days, "mostStarred": mostStarred, "mostForked": mostForked, "lang": languages.most_common(1), "licenses": licenses}

def api():   
    app = FastAPI()
    @app.get("/{identifier}")
    def root(identifier):
        return main(identifier)

    uvicorn.run(app, host="127.0.0.1", port=8000)

if __name__ == "__main__":
    api()