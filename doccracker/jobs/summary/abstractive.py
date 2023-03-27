import spacy
from spacy.tokens import Span
from doccracker.jobs.openai import OpenAi
from doccracker.jobs.shared.nlp_base import NlpBase

class AbstractiveSummaryOptions:
    def __init__(self, options:dict={}):
        if options:
            self.__from_dict(options)

    max_sentences: int = 3
    cost: str = '$'
    
    def __from_dict(self, options:dict):
        if options is not None:
            for option, value in options.items():
                if option == 'max_sentences':
                    try:
                        self.max_sentences = int(value)
                    except: pass
                elif option == 'cost':
                    self.cost = str(value)

class AbstractiveSummary(NlpBase):
    def __init__(self, **kwargs):
        super().__init__()
        self.options = AbstractiveSummaryOptions(kwargs.pop('options', {}))

    def openaisummary(self, text) -> str:
        openai = OpenAi()

        engine = openai.deployment_model(self.options.cost, 'summary')
        sentences = self.sentence_extraction(text)
        prompt_request = '\n\ntldr;'
        prompt_tokens = openai.get_num_tokens(prompt_request)
        token_limit = engine.token_limit - prompt_tokens - (self.options.max_sentences * 15)
        packages = openai.prompt_tokenizer(sentences, token_limit)
        summary = []

        for prompt in packages:
            prompt_text  = prompt+str(prompt_request)
            max_token_limit = engine.token_limit - openai.get_num_tokens(prompt_text)
            sum = openai.summary(engine, prompt_text, max_token_limit)
            summary.append(sum)

        return ' '.join(summary)
        
