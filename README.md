# Introduction
I advocate for making for different reasons. Sometime we make to test our assumptions and test with users. This is the classic prototyping phase in Design Thinking and human centred design. And sometimes I make to communicate an idea and to make stakeholders excited. 

I find it really exciting that barrier to play with these technologies are getting lower and lower. So for me as a creative technologist, it’s really exciting times to be able to play with a version of these LLM on my own crappy machine and with no access to GPU.

In this article, I show you how to create an app to chat with your csv files locally. Why is this important?

## Note
- You can use your normal CPU powered machine, no GPU required.
- You just need max 30 minutes.
- Everything is on your local machine. So no stress about leaking secret data anywhere!


# How to get started:

## Libraries/ tools
Here are a list of tools I used:

- LangChain
- Steamlit
- Ollama
- Chroma vector store
- VSCode


To start, clone this project.

Create a virtual env and activate it:

`python -m venv .venv`

`source .venv/bin/activate`

in that virtual environment, install the required libraries by running:

`pip install -r requirements.txt`

which installs the following:

`pip instal langchain`

`pip install langchain-community`

`pip install bs4`

`pip install chromadb`

`pip install gpt4all`

`pip install steamlit`

`pip install streamlit_chat`

## Local Llamma installation

`brew update`

`brew install ollama`

`brew services start ollama`

now you will have Ollama running on port 11434

## Run the app
`streamlit run app.py`
