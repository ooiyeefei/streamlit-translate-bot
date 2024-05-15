import streamlit as st
import boto3
import json


def translate_text(prompt):
  # Implement translation logic using Bedrock Runtime API
  bedrock_runtime = boto3.client("bedrock-runtime", region_name="us-east-1")

  # Send translation request to Bedrock Runtime
  response = bedrock_runtime.invoke_model(
    body= prompt,
    modelId= selected_model,
    )
  response_body = json.loads(response.get("body").read())


  # Handle response and extract translated text (replace with actual structure)
  if selected_model == "anthropic.claude-3-sonnet-20240229-v1:0" or selected_model == "anthropic.claude-3-haiku-20240307-v1:0":
     if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
        translated_text = response_body.get("content")
     else:
        translated_text = f"Error: {response["ResponseMetadata"]["HTTPStatusCode"]}"  # Handle errors
     print(response_body)
  elif selected_model == "mistral.mistral-7b-instruct-v0:2":
     if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
        translated_text = response_body.get("outputs")
     else:
        translated_text = f"Error: {response["ResponseMetadata"]["HTTPStatusCode"]}"  # Handle errors
     print(response_body)
  elif selected_model == "meta.llama3-70b-instruct-v1:0":
     if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
        translated_text = response_body.get("generation")
     else:
        translated_text = f"Error: {response["ResponseMetadata"]["HTTPStatusCode"]}"  # Handle errors      
     print(response_body)

  return translated_text

st.title("Text Translation with Bedrock")

source_text = st.text_input("Enter text to translate:")

# Model selection with supported Bedrock models
model_options = ["claude3_sonnet", "claude3_haiku", "mistral_7b", "llama3_70b"]
selected_model = st.selectbox("Translation Model", model_options)

# Use if statements for clarity in text manipulation based on model selection
if selected_model == "claude3_sonnet":
   selected_model = "anthropic.claude-3-sonnet-20240229-v1:0"
   # Prepare request payload
   prompt = json.dumps({
      "anthropic_version": "bedrock-2023-05-31",
      "max_tokens": 2000,
      "system": "You are an certified Medical Translator to help with translation. Your task is to translate the English source text within <org></org> into Chinese, French and malay. When translating, please follow these rules: \
        0. Maintain the original intent of the script. \
        1. Prioritize context and ensure semantic coherence and fluency. Avoid unnecessary exaggeration or embellishments. \
        2. translate these documents with ultimate precision, accuracy, and professionalism, reason being extra precise in medical translation is simple–any error or mistranslation can have life-threatening consequences for patients. \
        3. Adapt the translation style to suit the context of Medical / Healthcare discussions. Avoid using words that are not typically used in the professional context . \
        4. Retain specific proper nouns or technical terms when appropriate, ensuring consistency throughout the translation. \
        5. Reply with the translation within <result></result>. Do not include any additional content.",
      "messages": [{
         "role": "user", 
         "content": f"<org>{source_text}</org>",
         }],
      "temperature": 0.1,
      "top_p": 0.999,
      })
elif selected_model == "claude3_haiku":
   selected_model = "anthropic.claude-3-haiku-20240307-v1:0"
   # Prepare request payload
   prompt = json.dumps({
      "anthropic_version": "bedrock-2023-05-31",
      "max_tokens": 2000,
      "system": "You are an certified Medical Translator to help with translation. Your task is to translate the English source text within <org></org> into Chinese, French and malay. When translating, please follow these rules: \
        0. Maintain the original intent of the script. \
        1. Prioritize context and ensure semantic coherence and fluency. Avoid unnecessary exaggeration or embellishments. \
        2. translate these documents with ultimate precision, accuracy, and professionalism, reason being extra precise in medical translation is simple–any error or mistranslation can have life-threatening consequences for patients. \
        3. Adapt the translation style to suit the context of Medical / Healthcare discussions. Avoid using words that are not typically used in the professional context . \
        4. Retain specific proper nouns or technical terms when appropriate, ensuring consistency throughout the translation. \
        5. Reply with the translation within <result></result>. Do not include any additional content.",
      "messages": [{
         "role": "user", 
         "content": f"<org>{source_text}</org>",
         }],
      "temperature": 0.1,
      "top_p": 0.999,
      })
elif selected_model == "mistral_7b":
   selected_model = "mistral.mistral-7b-instruct-v0:2"
   # Prepare request payload
   prompt = json.dumps({
      "max_tokens": 2000,
      "prompt": f"You are an certified Medical Translator to help with translation. Your task is to translate the English source text within <org></org> into Chinese, French and malay. When translating, please follow these rules: \
        0. Maintain the original intent of the script. \
        1. Prioritize context and ensure semantic coherence and fluency. Avoid unnecessary exaggeration or embellishments. \
        2. translate these documents with ultimate precision, accuracy, and professionalism, reason being extra precise in medical translation is simple–any error or mistranslation can have life-threatening consequences for patients. \
        3. Adapt the translation style to suit the context of Medical / Healthcare discussions. Avoid using words that are not typically used in the professional context . \
        4. Retain specific proper nouns or technical terms when appropriate, ensuring consistency throughout the translation. \
        5. Reply with the translation within <result></result>. Do not include any additional content.<org>{source_text}</org>",
      "temperature": 0.1,
      "top_p": 0.999,
      })
elif selected_model == "llama3_70b":
   selected_model = "meta.llama3-70b-instruct-v1:0"
   # Prepare request payload
   prompt = json.dumps({
      "prompt": f"You are an certified Medical Translator to help with translation. Your task is to translate the English source text within <org></org> into Chinese, French and malay. When translating, please follow these rules: \
        0. Maintain the original intent of the script. \
        1. Prioritize context and ensure semantic coherence and fluency. Avoid unnecessary exaggeration or embellishments. \
        2. translate these documents with ultimate precision, accuracy, and professionalism, reason being extra precise in medical translation is simple–any error or mistranslation can have life-threatening consequences for patients. \
        3. Adapt the translation style to suit the context of Medical / Healthcare discussions. Avoid using words that are not typically used in the professional context . \
        4. Retain specific proper nouns or technical terms when appropriate, ensuring consistency throughout the translation. \
        5. Reply with the translation within <result></result>. Do not include any additional content.<org>{source_text}</org>",
      "temperature": 0.1,
      "top_p": 0.999,
      "max_gen_len": 2048,
      })
else:
    selected_model = "Model not currently supported"

if st.button("Translate"):
  translated_text = translate_text(
      prompt
  )
  st.write("Translated Text:\n", translated_text)