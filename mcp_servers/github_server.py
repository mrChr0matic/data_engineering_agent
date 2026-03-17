from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import requests
import os

load_dotenv()

mcp = FastMCP("github")

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


@mcp.tool()
def list_repos(username: str):
    url = f"https://api.github.com/users/{username}/repos"

    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}

    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        return {
            "error": "GitHub API error",
            "status": r.status_code,
            "response": r.json()
        }

    repos = r.json()

    return [repo["name"] for repo in repos]


@mcp.tool()
def read_file(owner: str, repo: str, path: str):

    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}"
    }

    r = requests.get(url, headers=headers)

    return r.json()


if __name__ == "__main__":
    mcp.run()