from curl_cffi import requests
from bs4 import BeautifulSoup


def get_events(url: str):
    r = requests.get(
        url,
        impersonate="chrome120",
    )
    soup = BeautifulSoup(r.text)
    parse_events(soup)


def parse_events(soup: BeautifulSoup):
    # Limit to 50 events - covers next 10 days or so
    event_items = soup.find_all("div", class_="event_item")[:50]
    for event in event_items:
        event_time = event.find("dd", class_="msl_event_time").get_text(strip=True)
        event_name = event.find("a", class_="msl_event_name").get_text(strip=True)
        event_link = event.find("a", class_="msl_event_name")["href"]
        event_description = event.find("dd", class_="msl_event_description").get_text(
            strip=True
        )
        event_types = []
        event_types_dd = event.find("dd", class_="msl_event_types")
        if event_types_dd:
            for a_tag in event_types_dd.find_all("a"):
                event_types.append(a_tag.get_text(strip=True))
        print(f"{event_name} - {event_link}")
        print(f"    {event_time}")
        print(f"    {event_description}")
        print(f"    {', '.join(event_types)}")


url = "https://www.kclsu.org/events/"
get_events(url)
