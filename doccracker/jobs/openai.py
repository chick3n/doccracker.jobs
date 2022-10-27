from ast import Str
from dataclasses import dataclass
import math
import os
import requests
import json
import openai
from transformers import GPT2TokenizerFast

@dataclass
class OpenAiEngine:
    name:str
    cost:str
    token_limit:int = 2048

class OpenAi:
    models:dict = {
        'summary:4': OpenAiEngine('curie-001', '$', 2048),
        'summary:3': OpenAiEngine('summary-ada', '$$', 2048),
        'summary:2': OpenAiEngine('text-davinci-002', '$$$', 4098),
        'summary:1': OpenAiEngine('text-davinci-002', '$$$', 4098),
        '4': OpenAiEngine('curie-001', '$', 2048),
        '3': OpenAiEngine('summary-ada', '$$', 2048),
        '2': OpenAiEngine('text-davinci-002', '$$$', 4098),
        '1': OpenAiEngine('text-davinci-002', '$$$', 4098),
    }

    def __init__(self):
        self.api_key = os.environ['Cognitive_Key']
        self.api_base = os.environ['Cognitive_Endpoint']
        self.api_type = 'azure'
        self.api_version = '2022-06-01-preview'

        self.tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")

        openai.api_key = self.api_key
        openai.api_base =  self.api_base
        openai.api_type = self.api_type
        openai.api_version = self.api_version

    def deployment_model(self, cost, type) -> OpenAiEngine:
        type = type.lower() if type is not None else ''

        if f'{type}:{cost}' in self.models:
            return self.models[f'{type}:{cost}']
        
        if cost in self.models:
            return self.models[cost]

        raise Exception(f'No deployment model available for cost {cost} of type {type}')

    def summary(self, engine:OpenAiEngine, prompt, max_tokens, **kwargs):
        response = self.completion(engine, 
            prompt, max_tokens, **kwargs)
        return response['choices'][0]['text'].replace('\n', '').replace(' .', '.').strip()  # type: ignore

    def prompt(self, engine:OpenAiEngine, prompt, max_tokens, **kwargs):
        response = self.completion(engine, 
            prompt, max_tokens, **kwargs)
        return response['choices'][0]['text'].replace('\n', '').replace(' .', '.').strip()  # type: ignore

    def completion(self, engine:OpenAiEngine, prompt, max_tokens, **kwargs):
        return openai.Completion.create(engine=engine.name, 
            prompt=prompt, max_tokens=max_tokens)

    def get_num_tokens(self, sentence):
        response = self.tokenizer(sentence)['input_ids']
        return len(response)

    def prompt_tokenizer(self, sentences: list[str], max_tokens:int) -> list[str]:
        prompts = []

        prompt = sentences[0]
        for sentence in sentences[1:]:
            if(self.get_num_tokens(prompt + sentence) > max_tokens):
                prompts.append(prompt)
                prompt = sentence
            else: prompt += ' ' + sentence
        
        prompts.append(prompt)
        return prompts