import requests

# Get Access Token
url, id = 'http://ec2-34-211-81-131.us-west-2.compute.amazonaws.com', '205125796'
access_token = requests.post(url + '/session', data = {'uid': id}).json()['token']
print(f"access token: {access_token}\nGame Status: {requests.get(url + '/game?token=' + access_token).json()['status']}")