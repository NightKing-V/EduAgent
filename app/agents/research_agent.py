from app.llm.mistral_client import get_llm
from langchain.prompts import ChatPromptTemplate

llm = get_llm()

def summarize_paper(chunks):
    content = "\n\n".join(chunks)
    prompt = ChatPromptTemplate.from_template("""
        You are a research assistant. Summarize the following academic paper text.
        Make sure to include key contributions, methodology, and conclusions.

        PAPER:
        {content}
    """)
    return llm.invoke(prompt.format(content=content))

def answer_question(query):
    context = query_chunks(query)
    prompt = ChatPromptTemplate.from_template("""
        You are a helpful academic research assistant. Use the context below to answer the user's question.

        CONTEXT:
        {context}

        QUESTION:
        {query}
    """)
    return llm.invoke(prompt.format(context=context, query=query))
