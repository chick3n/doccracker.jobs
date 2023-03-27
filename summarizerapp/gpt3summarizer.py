import openai
import streamlit as st

#GPT3-API-Key
openai.api_type = "azure"
openai.api_key = ""
openai.api_base = ""
openai.api_version = "2022-12-01"

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
                            prompt = "Summarize this article in a few sentences: "+ article_text,
                            max_tokens = out_token,
                            temperature = temperature_selector)
        # Print the generated summary
        res = response["choices"][0]["text"]
        st.success(res)
        # Give user the option to download result
        st.download_button('Download result', res)
else:
    st.warning("Not enough words to summarize!")
