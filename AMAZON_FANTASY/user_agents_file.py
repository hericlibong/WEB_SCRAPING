import requests

data = requests.get('https://raw.githubusercontent.com/tamimibrahim17/List-of-user-agents/master/Chrome.txt')
data = data.content
data = str(data).split('\\n')
#user_agents = data[3: len(data)-1]
user_agents = data[3:]
user_agents = user_agents[:len(user_agents)-1]

print(user_agents)
