import stanza
import sys
import os
import spacy
from spacy.cli import download
    
#stanza
root = os.path.dirname(os.path.dirname(__file__))
stanza.download('en', model_dir=f'{root}/tmodels')

#spacy
try:
    spacy.load('en_core_web_lg')
except:
    download('en')