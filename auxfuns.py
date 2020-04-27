import json
import os
from datetime import datetime
from git import Repo
from typing import Dict

json_keys = {"lang": "language",
             "url": "url",
             "contact": "contact",
             "name": "name"}


def pull_subtrees(repos: Dict):
    for (name, data) in repos.items():
        dir, url = data["language"] + "/" + name, data["url"]
        repo = Repo(".")
        if os.path.exists(dir):
            cmd, msg = f"git subtree pull --prefix={dir} {url} master --squash", f"Pulling {dir}\n"
        else:
            cmd, msg = f"git subtree add --prefix={dir} {url} master --squash", f"Adding {dir}\n"
        print(msg)
        repo.git.execute(cmd)


def unpack(d: Dict):
    return d[json_keys["name"]], d[json_keys["url"]], d[json_keys["contact"]]


def create_language_dictionary(repos: Dict):
    langs = [data[json_keys["lang"]] for data in repos.values()]
    d = {}
    for data in repos.values():
        d[data[json_keys["lang"]]] = []
    return d


def fill_language_dictionary(d: Dict, repos: Dict):
    for (name, data) in repos.items():
        language = data[json_keys["lang"]]
        temp = {json_keys["name"]: name,
                json_keys["url"]: data["url"],
                json_keys["contact"]: data["contact"]}
        d[language].append(temp)



def create_md_file(name: str):
    if os.path.isfile(name):
        os.remove(name)

    with open(name, "w") as file:
        file.write("# Included packages\n\n")
        file.write(
            f"The following packages---ordered by language---are included in the repository (last updated {datetime.now()}).\n")


def append_md_file(name: str, lang: str, data):
    mode = "a" if os.path.isfile(name) else "w"
    with open(name, mode) as file:
        file.write("## " + lang.upper() + "\n")
        file.write("| Package | Contact |\n")
        file.write("| --- | --- |\n")

        for d in data:
            name, url, contact = unpack(d)
            file.write(f"| [{name}]({url}) | {contact} |\n")

        file.write("\n")


def build_md_file(repos):
    langs = create_language_dictionary(repos)
    fill_language_dictionary(langs, repos)
    file = "list-of-packages.md"
    create_md_file(file)

    for lang, data in langs.items():
        append_md_file(file, lang, data)


def run_all(repos):
    pull_subtrees(repos)
    build_md_file(repos)


with open('subtree-packages.json') as json_file:
    repos = json.load(json_file)

if __name__ == "__main__":
    run_all(repos)