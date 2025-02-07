from curl_cffi import requests
from bs4 import BeautifulSoup
from bot.config import config


def get_events(url: str):
    r = requests.get(
        url,
        impersonate="chrome120",
    )
    soup = BeautifulSoup(r.text)
    events = parse_events(soup)
    return events


def get_event_time(url: str):
    r = requests.get(
        url,
        impersonate="chrome120",
    )
    soup = BeautifulSoup(r.text)
    paragraphs = soup.select("p:has(i.fa-clock-o)")
    if len(paragraphs) > 0:
        return paragraphs[0].get_text(strip=True)
    else:
        return None


def parse_events(soup: BeautifulSoup):
    # Limit to 50 events - covers next 10 days or so
    event_items = soup.find_all("div", class_="event_item")[:1]
    events = []
    for event in event_items:
        event_date = event.find("dd", class_="msl_event_time").get_text(strip=True)
        event_name = event.find("a", class_="msl_event_name").get_text(strip=True)
        event_link = event.find("a", class_="msl_event_name")["href"]
        event_link = config["events"]["url"] + event_link
        event_location = event.find("dd", class_="msl_event_location").get_text(
            strip=True
        )
        event_description = event.find("dd", class_="msl_event_description").get_text(
            strip=True
        )
        event_types = []
        event_types_dd = event.find("dd", class_="msl_event_types")
        if event_types_dd:
            for a_tag in event_types_dd.find_all("a"):
                event_types.append(a_tag.get_text(strip=True))
        event_time = get_event_time(event_link)
        events.append(
            {
                "name": event_name,
                "link": event_link,
                "date": event_date,
                "location": event_location,
                "description": event_description,
                "types": event_types,
                "time": event_time if event_time else None,
            }
        )
    return events
