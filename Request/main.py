import requests, re

headers = {
    'Host': 'live.radiance.thatgamecompany.com',
    'User-Agent': 'Sky-Live-com.tgc.sky.android/0.23.1.234919 (samsung SM-N975F; android 30.0.0; en)',
    'Content-Type': 'application/json'
}

response = requests.post(
    'https://live.radiance.thatgamecompany.com/account/get_latest_build_version',
    headers=headers,
    data={'key': 'value'},
)
#example of sky request
print(response.status_code) 
print(response.content)


# example of request with regex
def getHtml(url):
    return requests.get(url).content.decode("utf-8")

url = 'url'
html_snippet = getHtml(url)
match = re.compile(r'regex', re.DOTALL | re.IGNORECASE).findall(html_snippet)
for url, img_url in match:
    print(f"URL: {url}\nImage URL: {img_url}")