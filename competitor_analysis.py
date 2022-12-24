import requests, re, locale
from bs4 import BeautifulSoup

locale.setlocale(locale.LC_ALL, '')

COMPETITORS = ('google.ru', 'yandex.ru', 'rambler.ru')
FILE = 'data.txt'


def analysis(sites):
    data = {}
    for site in sites:
        html = get_html(site)
        soup = BeautifulSoup(html, 'html.parser')
        element = soup.select('a[href^="https://webmaster.yandex.ru/sqi/"]')[0]
        yandex_x = re.sub('\W+', '', element.getText())
        element = soup.select(
            'a[href^="http://yandex.ru/yandsearch?text="]')[0]
        yandex_index = re.sub('\W+', '', element.getText())
        element = soup.select('a[href^="https://www.google.com/search?q="]')[0]
        google_index = re.sub('\W+', '', element.getText())
        element = soup.select(
            'div#publicStatistics tr:nth-child(2) td:nth-child(2)')[0]
        visitors_day = re.sub('\W+', '', element.getText())
        data[site] = [yandex_x, yandex_index, google_index, visitors_day]

    write_file(data)


def write_file(data):
    lines = []
    for site in data:
        lines.append(site)
        lines.append("Яндекс ИКС: " + number_to_string(data[site][0]))
        lines.append("В индексе Яндекса: " + number_to_string(data[site][1]) +
                     " стр.")
        lines.append("В индексе Google: " + number_to_string(data[site][2]) +
                     " стр.")
        lines.append("Посетителей в сутки: " + number_to_string(data[site][3]))
        lines.append("-----------------------")
    f = open(FILE, 'w')
    f.write('\n'.join(lines))
    f.close()


def number_to_string(number):
    if not number.isnumeric():
        number = 0
    return locale.format_string('%.0f', float(number), grouping=True)


def get_html(site):
    url = 'https://a.pr-cy.ru/' + site
    response = requests.get(url)
    return response.text


if __name__ == '__main__':
    analysis(COMPETITORS)
