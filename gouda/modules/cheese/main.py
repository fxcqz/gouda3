from bs4 import BeautifulSoup

from gouda.utils.web import get_page_contents


commands = ['cotd', 'cotdinfo']

def cotd(*args, **kwargs):
    writer = kwargs.pop('writer')
    data = get_page_contents("http://www.cheese.com/")
    try:
        soup = BeautifulSoup(data, "html.parser")
        cotd = soup.find('div', attrs={'class': 'top-offer'}).a.get('href').replace('/', '')
        if kwargs.get('suppress', None):
            # return the cotd rather that writing it
            return cotd
        writer("The cheese of the day is %s." % cotd.replace('-', ' ').title())
    except AttributeError:
        # no cheesy
        pass


def cotdinfo(*args, **kwargs):
    writer = kwargs.pop('writer')
    cheese = cotd(suppress=True, writer=None)
    data = get_page_contents("http://www.cheese.com/%s/" % cheese)
    try:
        soup = BeautifulSoup(data, "html.parser")
        info = soup.find('div', attrs={'class': 'summary'}).find('p', attrs={'style': 'text-align: justify;'}).text
        writer('. '.join(info.split('. ')[:2]))
    except:
        pass
