from bs4 import BeautifulSoup

from gouda.utils.web import get_page_contents


commands = ['cotd']

def cotd(*args, **kwargs):
    writer = kwargs.pop('writer')
    data = get_page_contents("http://www.cheese.com/")
    try:
        soup = BeautifulSoup(data, "html.parser")
        cotd = soup.find('div', attrs={'class': 'top-offer'}).a.get('href').replace('/', '')
        writer("The cheese of the day is %s." % cotd)
    except AttributeError:
        # no cheesy
        pass
