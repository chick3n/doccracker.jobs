import logging
import json
import sys
import os
from dotenv import find_dotenv, load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from doccracker.shared.search import Search
from doccracker.models.job import Job

def main() -> None:    
    load_dotenv(find_dotenv())
    search = Search("km")
    texts = search.get_document_texts(['aHR0cHM6Ly9zdGdoZzRodmhuZGUzanhlLmJsb2IuY29yZS53aW5kb3dzLm5ldC9kb2N1bWVudHMvMjAyMi0tMTAtMTRfTU9TQ09fODE5Mi50eHQ1', 
        'aHR0cHM6Ly9zdGdoZzRodmhuZGUzanhlLmJsb2IuY29yZS53aW5kb3dzLm5ldC9kb2N1bWVudHMvMjAyMi0tMDktMjNfTU9TQ09fNzk5NC50eHQ1', 
        'aHR0cHM6Ly9zdGdoZzRodmhuZGUzanhlLmJsb2IuY29yZS53aW5kb3dzLm5ldC9kb2N1bWVudHMvMjAyMi0tMDktMjlfTU9TQ09fODg4Ny50eHQ1'])

    if len(texts) > 0:
        print('\n'.join(map(lambda text: text[0:100], texts)))
    else:
        print('no texts found.')



if __name__ == '__main__':
    main()