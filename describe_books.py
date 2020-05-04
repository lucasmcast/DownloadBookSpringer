__autor__ = "Lucas Martins de Castro"
"""Modulo é responsável por buscar as informações de cada livro"""

from urllib.request import urlopen as uReq, Request
from urllib.error import HTTPError
from bs4 import BeautifulSoup as soup
import urllib.parse
from progress_bar import printProgressBar


def get_books_describe(base_url):
    """Faz a busca de todos os livros e retorna uma lista com as descrições de cada um"""
    headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'
    }

    BASE_URL = urllib.parse.urljoin(base_url, 'search/page/')

    #Quantidade de paginas para ser percorrido 
    qtd_pages = 20
    
    #lista de paginas para ser adicionado na url
    num_pages = [str(num) for num in range(1,qtd_pages+1)]
    
    values = {
        'facet-language' : 'En',
        'facet-content-type' : 'Book',
        'package' : 'mat-covid19_textbooks',
        'sortOrder' : 'newestFirst',
        'showAll' : 'false'
    }
    
    data = urllib.parse.urlencode(values)
    #print(data)
    url_list = []
    
    for i in range(0, qtd_pages):
        url_with_num = BASE_URL+num_pages[i]+'?'
        url = url_with_num+ data
        #print(url)
        url_list.append(url)
    
    books_list = []
    l = len(url_list)

    print("Fazendo Busca de todos os livros")
    #Barra de progresso do prompt
    printProgressBar(0, l, prefix="Progress", suffix="Complete", length=50)

    for i, url in enumerate(url_list):
        req = Request(url=url, headers=headers)

        try:
            uclient = uReq(req)
            page_html = uclient.read()
            uclient.close()

            page_soup = soup(page_html, "html.parser")
            #print(page_soup)

            #Busca a lista de livros da pagina
            content_list = page_soup.find("ol", class_="content-item-list")
            books = content_list.findAll('li')

            for book in books:
                divs = book.findAll("div")
                title = divs[1].find("h2").text.strip()
                url_book = divs[1].find("a").get('href')
                p = divs[1].findAll("p")
                subtitle = p[0].text.strip()
                span = p[1].findAll("span")
                autor = span[0].text.strip()
                year = span[1].text.strip()

                #print(title)
                book_data = {
                    'title': title,
                    'url_book' : url_book,
                    'subtitle' : subtitle,
                    'autor' : autor,
                    'year' : year
                }

                books_list.append(book_data)
        
        except HTTPError as e:
            print(e.reason, " ", e.code)

        printProgressBar(i + 1, l, prefix='Progress:', suffix='Complete', length=50)
    
    return books_list
