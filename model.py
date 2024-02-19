# Load model directly
import re
from langchain_core.prompts import PromptTemplate
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from PyPDF2 import PdfReader
from langchain.llms import HuggingFacePipeline
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.llms import HuggingFaceHub
from langchain.vectorstores import FAISS
from langchain.chains import LLMChain
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
import os
os.environ["HUGGINGFACEHUB_API_TOKEN"] = ""

model_name="TinyLlama/TinyLlama-1.1B-Chat-v1.0"
model = AutoModelForCausalLM.from_pretrained(
    model_name,
)
tokenizer = AutoTokenizer.from_pretrained(model_name)

text_generation_pipeline = pipeline(
    model=model,
    tokenizer=tokenizer,
    task="text-generation",
    temperature=0.2,
    repetition_penalty=1.1,
    return_full_text=True,
    max_new_tokens=1000,
)
llm = HuggingFacePipeline(pipeline=text_generation_pipeline)

doc_reader = PdfReader("ChatGPT_API.pdf")
print(doc_reader)

raw_text = ''
for i, page in enumerate(doc_reader.pages):
    text = page.extract_text()
    if text:
        raw_text += text

print(len(raw_text),raw_text[:100])

text_splitter = CharacterTextSplitter(
    separator = "\n",
    chunk_size = 1000,
    chunk_overlap  = 200,
    length_function = len,
)

texts = text_splitter.split_text(raw_text)
embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-mpnet-base-v2')
print("EE")
docsearch = FAISS.from_texts(texts, embeddings)
print("INPUT:")
query=input()
context = docsearch.similarity_search(query)[0]
context=context.page_content.replace("\n"," ")

sys_prompt: PromptTemplate = PromptTemplate(
    input_variables=[],
    template=""" answer the questions, If you don't know the answer, just say that you don't know, don't try to make up an answer."""
)

system_message_prompt = SystemMessagePromptTemplate(prompt=sys_prompt)

userPromtTemplate: PromptTemplate = PromptTemplate(
    input_variables=["query", "context"],
    template="Based upon the this context: ```{context}``` Answer the following query: ```{query}```"
)

user_message_promt = HumanMessagePromptTemplate(prompt=userPromtTemplate)

chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, user_message_promt])
chain=LLMChain(llm=llm, prompt=chat_prompt)
print(chain.invoke({"context":context,"query":query}))
