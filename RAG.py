import os
import torch
from transformers import (
  AutoTokenizer, 
  AutoModelForCausalLM, 
  BitsAndBytesConfig,pipeline
)

from transformers import BitsAndBytesConfig, AutoConfig

from langchain.text_splitter import CharacterTextSplitter
from langchain.document_transformers import Html2TextTransformer
from langchain.document_loaders import AsyncChromiumLoader

from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS

from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.llms import HuggingFacePipeline
from langchain.chains import LLMChain

import nest_asyncio

model_name='TinyLlama/TinyLlama-1.1B-Chat-v1.0'

model_config =AutoConfig.from_pretrained(
    model_name,
)

tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right"
use_4bit = True

model = AutoModelForCausalLM.from_pretrained(model_name, 
                                                #  quantization_config=bnb_config, 
                                                 torch_dtype=torch.float32, 
                                                #  load_in_4bit = True,
 
                                                 device_map= "auto",
                                                 )

def print_number_of_trainable_model_parameters(model):
    trainable_model_params = 0
    all_model_params = 0
    for _, param in model.named_parameters():
        all_model_params += param.numel()
        if param.requires_grad:
            trainable_model_params += param.numel()
    return f"trainable model parameters: {trainable_model_params}\nall model parameters: {all_model_params}\npercentage of trainable model parameters: {100 * trainable_model_params / all_model_params:.2f}%"

print(print_number_of_trainable_model_parameters(model))

text_generation_pipeline = pipeline(
    model=model,
    tokenizer=tokenizer,
    task="text-generation",
    temperature=0.5,
    repetition_penalty=1.1,
    return_full_text=True,
    max_new_tokens=1000,
)

mistral_llm = HuggingFacePipeline(pipeline=text_generation_pipeline)


import nest_asyncio
nest_asyncio.apply()

# Articles to index
articles = ["https://www.bizbash.com/event-tech-virtual/event-tech-tools/media-gallery/22879160/how-did-the-walls-at-this-anniversary-event-turn-into-water"]

# Scrapes the blogs above
loader = AsyncChromiumLoader(articles)
docs = loader.load()

# Converts HTML to plain text 
html2text = Html2TextTransformer()
docs_transformed = html2text.transform_documents(docs)
print(docs_transformed)
# Chunk text
text_splitter = CharacterTextSplitter(
                                      chunk_size=800, 
                                      chunk_overlap=400)
chunked_documents = text_splitter.split_documents(docs_transformed)

# Load chunked documents into the FAISS index
db = FAISS.from_documents(chunked_documents, 
                          HuggingFaceEmbeddings(model_name='sentence-transformers/all-mpnet-base-v2'))

retriever = db.as_retriever()

# Create prompt template
prompt_template = """
### [INST] Instruction: Create a new idea for an event based on the context as given below. Here is context to help:

{context}

### Query:
{question} [/INST]
 """

# Create prompt from prompt template 
prompt = PromptTemplate(
    input_variables=["context", "question"],
    template=prompt_template,
)

# Create llm chain 
llm_chain = LLMChain(llm=mistral_llm, prompt=prompt)

rag_chain = ( 
 {"context": retriever, "question": RunnablePassthrough()}
    | llm_chain
)

response=rag_chain.invoke("A sensory experience to showcase paintings.")
print(response)
print(response['question'])
print(response['text'])