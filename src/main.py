import requests
from bs4 import BeautifulSoup
import math
import re


def getSource(session):
    html = session.get("https://quantbet.com/quiz/dev").text
    soup = BeautifulSoup(html, 'html.parser')
    numbers = []
    for n in soup.find_all('strong'):
        numbers.append(n.get_text())
    if len(numbers) < 2:
        raise RuntimeError(
            'Failed to fetch numbers from https://quantbet.com/quiz/dev')
    return int(numbers[0]), int(numbers[1])


def postResult(session, gcd):
    payload = {"divisor": gcd}
    response = session.post("https://quantbet.com/submit", payload)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.find(text=re.compile("Correct"))


def main():
    session = requests.Session()
    n1, n2 = getSource(session)
    gcd = math.gcd(n1, n2)
    contact = postResult(session, gcd)
    print(contact)


if __name__ == "__main__":
    main()
