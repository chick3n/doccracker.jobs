import openai
import re
import os.path
import streamlit as st
import torch
import time
from PIL import Image
from streamlit_option_menu import option_menu
import streamlit.components.v1 as html
import transformers
from transformers import AutoTokenizer, AutoModelWithLMHead, AutoModelForCausalLM, AutoModelForSeq2SeqLM, FlaxLongT5ForConditionalGeneration,pipeline, GPT2Tokenizer, BartForConditionalGeneration, BartTokenizer
from datasets import load_metric
from rouge import Rouge

t5_image = Image.open('./data/T5-diagram.png')

#GPT3-API-Key
openai.api_type = "azure"
openai.api_key = ""
openai.api_base = ""
openai.api_version = "2022-12-01"

#load models
@st.cache()
def load_cache_model(selected_model):
    model = AutoModelForSeq2SeqLM.from_pretrained(path,local_files_only=True)
    return model

metric = load_metric("rouge")
rouge = Rouge()

# Sidebar menu
with st.sidebar:
    choose = option_menu("Summarizer App", ["Purpose", "GPT3", "Open Source"],
                         icons=['house', 'robot', 'robot'],
                         menu_icon="app", default_index=0,
                         styles={
                             "container": {"padding": "5!important", "background-color": "#fafafa"},
                            "icon": {"color": "orange", "font-size": "25px"}, 
                            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px",         "--hover-color": "#eee"},
                            "nav-link-selected": {"background-color": "#02ab21"}
                            }
                        )

# Main page
if choose =="Purpose":             
    # To display the header text using css style
    st.markdown(""" <style> .font {
    font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
    </style> """, unsafe_allow_html=True)
    st.markdown('<p class="font">Purpose of this Proof of Concept</p>', unsafe_allow_html=True)    
    
    st.markdown("A summarizer app is a tool that automatically summarizes long pieces of text, such as articles or documents, into shorter versions that retain the most important information. The purpose of a summarizer app is to make it easier for users to quickly understand the main points of a text without having to read through the entire document. This can be useful for a variety of tasks, such as researching a topic, studying for an exam, or keeping up with news and current events.")
    
    st.markdown("Additionally the purpose is to let the user understand the trade off between open source models like T5 that can run on CPU and GPT3, in term of response time, model size and metrics (in this case we are using the Rouge evaluation).")
    st.image(t5_image,caption="Model Card for T5 Small")

## Open Source page
elif choose == "Open Source":
    # Title
    st.title("Summarizer using open sources models")

    # Create Text Area Widget to enable user to enter texts
    article_text = st.text_area("Enter the text you want to summarize")

    # to summarize, and display a warning if it is empty:
    if len(article_text)>100:

        selected_model = st.radio( label = "Chose the model you want to use", options= [
            #"bart-large-cnn",
            "t5-small",
            "T5-Base", 
            "T5-Large",
            #LongT5"
            ], index=0)
        path_prefix = "./preTrainedModel/"
        path = os.path.join(path_prefix, selected_model)

        #Using the cache model
        start_time = time.time()
        tokenizer = AutoTokenizer.from_pretrained(path,local_files_only=True)
        model = load_cache_model(selected_model)
        end_time = time.time()
        time_taken = end_time-start_time
    
        if model is not None:
            st.success("It took {} seconds to load the model".format(round(time_taken,2)))
            
            # Generate the summary
            if st.button("Generate Summary",type='primary'): 
                # Use open source to generate a summary of the article
                #start_time = time.time()
                inputs = tokenizer.encode(article_text, return_tensors='pt', max_length=512, truncation=True)
                n_tokens = len(tokenizer.tokenize(article_text))
                outputs = model.generate(inputs, max_length=150, min_length=20, length_penalty=5., num_beams=2,no_repeat_ngram_size=1)
                
                # Print the generated summary
                res = tokenizer.decode(outputs[0], skip_special_tokens=True)
                end_time = time.time()
                time_taken = end_time-start_time
                st.success(res)
                rouge_score = rouge.get_scores(res,article_text,avg=True)
                st.write("It took {} seconds to encode, generate and decode the text".format(round(time_taken,2)))
                st.text('Rouge Score: '+str(rouge_score['rouge-1']))
                # Give user the option to download result
                st.download_button('Download result', res)
    else:
        st.warning("Not enough words to summarize!")

# GPT3 summarizer page
elif choose == "GPT3":
    # Title
    st.title("Summarize your text with GPT3")

    # Create Text Area Widget to enable user to enter texts
    article_text = st.text_area("Enter the text you want to summarize")
    temperature_selector = st.slider("Select the Temperature",0.0,1.0,0.5)

    # Create Radio Buttons
    output_size = st.radio(label = "What kind of summary output do you want?", 
                        options= ["To-The-Point", "Concise", "Detailed"]
                        )
    if output_size == "To-The-Point":
        out_token = 50
    elif output_size == "Concise":
        out_token = 128
    else:
        out_token = 516

    if len(article_text)>100:
    # Generate the summary
        if st.button("Generate Summary",type='primary'):
    
            # Use GPT-3 to generate a summary of the article
            response = openai.Completion.create(
                                engine = "text-davinci-002",
                                prompt = "Summarize this article : "+ article_text,
                                max_tokens = out_token,
                                temperature = temperature_selector)
            # Print the generated summary
            res = response["choices"][0]["text"]
            rouge_score = rouge.get_scores(res,article_text,avg=True)
            st.success(res)
            st.text('Rouge Score: '+str(rouge_score['rouge-1']))
            # Give user the option to download result
            st.download_button('Download result', res)
    else:
        st.warning("Not enough words to summarize!")


