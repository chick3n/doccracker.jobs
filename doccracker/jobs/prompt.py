from email.mime import base
import spacy
from spacy.tokens import Span
from doccracker.jobs.openai import OpenAi
from doccracker.jobs.shared.nlp_base import NlpBase

class PrompterOptions:
    def __init__(self, options:dict={}):
        if options:
            self.__from_dict(options)

    max_sentences: int = 3
    cost: str = '$'
    prompt: str = ''
    
    def __from_dict(self, options:dict):
        if options is not None:
            for option, value in options.items():
                if option == 'max_sentences':
                    try:
                        self.max_sentences = int(value)
                    except: pass
                elif option == 'cost':
                    self.cost = str(value)
                elif option == 'prompt':
                    self.prompt = str(value).strip()

class Prompter(NlpBase):
    def __init__(self, **kwargs):
        super().__init__()
        self.options = PrompterOptions(kwargs.pop('options', {}))

    def openaisummary(self, text) -> str:
        openai = OpenAi()

        engine = openai.deployment_model(self.options.cost, 'prompt')
        sentences = self.sentence_extraction(text)
        prompt_request = f'{self.options.prompt}\n\n'
        prompt_tokens = openai.get_num_tokens(prompt_request)
        token_limit = engine.token_limit - prompt_tokens - (self.options.max_sentences * 30)
        packages = openai.prompt_tokenizer(sentences, token_limit)
        summary = []

        for prompt in packages:
            prompt_text  = str(prompt_request)+prompt
            max_token_limit = engine.token_limit - openai.get_num_tokens(prompt_text)
            sum = openai.prompt(engine, prompt_text, max_token_limit)
            summary.append(sum)

        return ' '.join(summary)

    
        
    
