import os
import requests
from github import Github

WAKATIME_API_KEY = os.getenv('WAKATIME_API_KEY')
GH_TOKEN = os.getenv('GH_TOKEN')
g = Github(GH_TOKEN)
user = g.get_user()

# Get Wakatime stats
r = requests.get('https://wakatime.com/api/v1/users/current/stats/last_7_days', headers={'Authorization': 'Bearer ' + WAKATIME_API_KEY})
data = r.json()

languages = []
for language in data['data']['languages']:
    languages.append(f"{language['name']} {language['text']}")

# Update README
readme = user.get_repo(user.login).get_readme()
readme_content = readme.content.decode("base64")
readme_content = readme_content.replace(
    readme_content.split("<!--START_SECTION:waka-->")[1].split("<!--END_SECTION:waka-->")[0],
    "```text\n" + "\n".join(languages) + "\n```\n"
)
readme.edit(readme_content, "Updated Wakatime stats.")
