import logging
import json
import sys
import os
from dotenv import find_dotenv, load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from doccracker.shared.search import Search
from doccracker.models.job import Job
from doccracker.jobs.summary import AzureExtractiveSummary, ExtractiveSummary

def print_line_spacer():
    print('###################################')

def main() -> None:    
    load_dotenv(find_dotenv())
    search = Search("km")
    texts = search.get_document_texts(['aHR0cHM6Ly9zdGdoZzRodmhuZGUzanhlLmJsb2IuY29yZS53aW5kb3dzLm5ldC9kb2N1bWVudHMvMjAyMi0tMTAtMTRfTU9TQ09fODE5Mi50eHQ1', 
        'aHR0cHM6Ly9zdGdoZzRodmhuZGUzanhlLmJsb2IuY29yZS53aW5kb3dzLm5ldC9kb2N1bWVudHMvMjAyMi0tMDktMjNfTU9TQ09fNzk5NC50eHQ1', 
        'aHR0cHM6Ly9zdGdoZzRodmhuZGUzanhlLmJsb2IuY29yZS53aW5kb3dzLm5ldC9kb2N1bWVudHMvMjAyMi0tMDktMjlfTU9TQ09fODg4Ny50eHQ1'])

    #extsum = AzureExtractiveSummary(texts, summary_sentence_length=10)
    #summary, errors = extsum.summarize()

    #print("Azure Extractive Summary")
    #print_line_spacer()
    #if errors:
    #    print('errors', errors)
    #else: print('summary', summary)
    #print_line_spacer()


    local_ext_sum = ExtractiveSummary(texts)
    print('\nSBert Summary')
    print_line_spacer()
    summaries = local_ext_sum.sbertsummary()
    for summary in summaries:
        print(summary)
        print_line_spacer()


if __name__ == '__main__':
    main()