from summarizer.sbert import SBertSummarizer
import spacy
from spacy.tokens import Span
from spacy.lang.en import English
from typing import List, Tuple
import os

from doccracker.models.job import JobOptionEntity

class ExtractiveSummaryOptions:
    def __init__(self, options:dict={}):
        if options:
            self.__from_dict(options)

    max_sentences: int = 3
    
    def __from_dict(self, options:dict):
        if options is not None:
            for option, value in options.items():
                if option == 'max_sentences':
                    try:
                        self.max_sentences = int(value)
                    except: pass

class ExtractiveSummary:
    def __init__(self, **kwargs):
        self.nlp = spacy.load('en_core_web_lg')
        self.options = ExtractiveSummaryOptions(kwargs.pop('options', {}))

    def sbertsummary(self, text, model='paraphrase-MiniLM-L6-v2') -> str:
        model = SBertSummarizer(model)
        sentences = self.__sentence_extraction(text)
        return model(' '.join(sentences), num_sentences=self.options.max_sentences)

    def __sentence_extraction(self, text):
        if text is None:
            return []
        doc = self.nlp(text)
        sentences = []
        for sent in doc.sents:
            if self.__is_sentence(sent):
                sentences.append(sent.text)
        return sentences
        
    def __is_sentence(self,sent:Span):
        if sent[0].is_title and sent[-1].is_punct:
            has_noun = 2
            has_verb = 1
            for token in sent:
                if token.pos_ in ["NOUN", "PROPN", "PRON"]:
                    has_noun -= 1
                elif token.pos_ == "VERB":
                    has_verb -= 1
            if has_noun < 1 and has_verb < 1:
                return True
        return False

    def sentence_cleaning(self, text):
        return text.replace('\t', '').replace('\n', '')
