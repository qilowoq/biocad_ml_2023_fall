import streamlit as st
from transformers import pipeline
import torch
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Annoy
import textwrap

title_placeholder = st.empty()
title_placeholder.title("Загружаются модели...")
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

progress_bar = st.progress(0)
title_placeholder.title("Загружается модель для поиска ответа на вопрос в тексте... ~1.1 GB")
model_for_answering_name = "timpal0l/mdeberta-v3-base-squad2"
qa_pipeline = pipeline("question-answering", 
                       model=model_for_answering_name, 
                       tokenizer=model_for_answering_name,
                       device=device)

progress_bar.progress(50)
title_placeholder.title("Загружается модель для поиска похожих документов... ~70 MB")
model_name = "cointegrated/rubert-tiny2"
model_kwargs = {'device': 'cuda:0'}
encode_kwargs = {'normalize_embeddings': False}
embeddings_function = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)

progress_bar.progress(75)
title_placeholder.title("Загружается база данных...")
db = Annoy.load_local('train_db', embeddings_function)

progress_bar.progress(100)
title_placeholder.title("Поиск ответа на вопрос в тексте. Стажировка Biocad - ML")
progress_bar.empty()

with st.sidebar:
    with st.form(key='my_form'):
        query = st.sidebar.text_area(
            label="Вопрос для поиска",
            max_chars=100,
            key="query"
            )
        context = st.sidebar.text_area(
            label="Контекст для поиска. Можно оставить пустым.",
            key="context",
            max_chars=3000,
            )
        submit_button = st.form_submit_button(label='Найти ответ')

if query and context:
    ans = qa_pipeline(question=query, context=context)
    st.subheader("Ответ:")
    st.text(textwrap.fill(ans['answer'].strip().capitalize() + ".", width=85))
elif query:
    docs = db.similarity_search(query, k=5)
    context = " ".join([d.page_content for d in docs])
    ans = qa_pipeline(question=query,  context=context)
    st.subheader("Ответ:")
    st.text(textwrap.fill(ans['answer'].strip().capitalize() + ".", width=85))
else:
    st.text(textwrap.fill("Пожалуйста введите вопрос", width=85))