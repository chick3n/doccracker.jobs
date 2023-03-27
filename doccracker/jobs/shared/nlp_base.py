import spacy
from spacy.tokens import Span

class NlpBase:
    def __init__(self):
        self.nlp = spacy.load('en_core_web_lg')

    def sentence_extraction(self, text):
        if text is None:
            return []
        doc = self.nlp(text)
        sentences = []
        for sent in doc.sents:
            if self.is_sentence(sent):
                sentences.append(sent.text)
        return sentences
        
    def is_sentence(self,sent:Span):
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