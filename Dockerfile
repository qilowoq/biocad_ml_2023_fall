FROM ubuntu:18.04
ENV PATH="/root/miniconda3/bin:${PATH}"
ARG PATH="/root/miniconda3/bin:${PATH}"
RUN apt-get update
RUN apt-get install -y wget build-essential && rm -rf /var/lib/apt/lists/*



RUN wget \
    https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && mkdir /root/.conda \
    && bash Miniconda3-latest-Linux-x86_64.sh -b \
    && rm -f Miniconda3-latest-Linux-x86_64.sh 


RUN pip install matplotlib==3.8.1 \
                pandas==2.1.3 \
                scikit_learn==1.3.2 \
                torch==2.1.0 \
                sentence_transformers==2.2.2 \
                transformers==4.35.0 \
                streamlit==1.28.2 \
                langchain==0.0.337 \
                annoy==1.17.3

# Download the models
RUN python -c "from transformers import AutoModel; AutoModel.from_pretrained('timpal0l/mdeberta-v3-base-squad2')"

RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/paraphrase-multilingual-mpnet-base-v2')"

RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('cointegrated/rubert-tiny2')"

RUN python -c "from langchain.embeddings import HuggingFaceEmbeddings; HuggingFaceEmbeddings(model_name='cointegrated/rubert-tiny2')"

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health
