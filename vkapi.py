import requests

headers = {"user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36"}

query = "https://api.vk.com/method/groups.get?user_id=457239356&access_token=d078a7d6779d90b802ae9c53f8c337265408957cdca017d91daf72b08bc0f504f671182866740f80847df&v=5.131"
response = requests.get(query, headers=headers)

print(response.text)


with open('page.html', 'w', encoding="UTF-8") as f:
    f.write(response.text)