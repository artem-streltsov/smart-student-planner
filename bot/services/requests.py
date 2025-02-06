from curl_cffi import requests
from bs4 import BeautifulSoup


def get_archive(url: str):
    with open(url[-5:], "w") as file:
        r = requests.get(
            url,
            impersonate="chrome120",
        )
        print(r.status_code)
        soup = BeautifulSoup(r.text)
        file.write(soup.prettify())


# get_archive(url)
