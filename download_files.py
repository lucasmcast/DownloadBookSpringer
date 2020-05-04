"""
Modulo responsável por fazer o download dos livros que foram
disponibilizados pela Springer de forma gratuita devido
a pandemia do covid19
"""
from describe_books import get_books_describe
from urllib.parse import urljoin, quote_plus
from urllib.request import urlretrieve
import os.path
from progress_bar import printProgressBar
import argparse
import sys
import signal


def main(books, path_download):
    """Recebendo todas os livros em um lista de dicionario contendo as informações do livro"""

    path_url = '/content/pdf/'

    url = urljoin(BASE_URL, path_url)
    l = len(books)

    print("\nExecutando Downloads dos Livros")
    printProgressBar(0, l, prefix="Progress", suffix="Complete", length=50)

    for i, book in enumerate(books):
        title = book['title']
        path_book = book['url_book']
        path_book = path_book[6:]
        data = quote_plus(path_book)+'.pdf'
        url_full = urljoin(url, data)
        
        file_name = title+'.pdf'
        file_name = file_name.replace('/', '-')
        if os.path.exists(os.path.join(path_download, file_name)):
            continue 
        
        urlretrieve(url_full, os.path.join(path_download, file_name))

        printProgressBar(i + 1, l, prefix='Progress:', suffix='Complete', length=50)

def signal_handler(signal, frame):
    response = input("\nDeseja realmente sair, y(SIM) ou n(NÃO): ")
    try:
        if response == 'y':
            sys.exit(0)
    except KeyboardInterrupt:
        print("exiting...")
    

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--path", required=True, help="Path to save books")
    args = vars(ap.parse_args())

    path_download = args["path"]

    if not os.path.exists(path_download):
        print(f"download: Não foi possivel encontrar {path_download} : Path not exist")
        sys.exit(0)

    # store the original SIGINT handler
    signal.signal(signal.SIGINT, signal_handler)

    BASE_URL = 'https://link.springer.com/'

    books = get_books_describe(BASE_URL)

    main(books, path_download)
