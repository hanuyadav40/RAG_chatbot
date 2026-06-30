from dotenv import load_dotenv
load_dotenv()
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.runnables import RunnableLambda
import os
from chroma_utils import vectorstore

retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

output_parser = StrOutputParser()

contextualize_q_system_prompt = (
    "Given a chat history and the latest user question "
    "which might reference context in the chat history, "
    "formulate a standalone question which can be understood "
    "without the chat history. Do NOT answer the question, "
    "just reformulate it if needed and otherwise return it as is."
)

contextualize_q_prompt = ChatPromptTemplate.from_messages([
    ("system", contextualize_q_system_prompt),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
])

qa_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant. Use the following context to answer the user's question."),
    ("system", "Context: {context}"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")
])

def _format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def _convert_chat_history(history):
    messages = []
    for msg in history:
        if msg["role"] == "human":
            messages.append(HumanMessage(content=msg["content"]))
        else:
            messages.append(AIMessage(content=msg["content"]))
    return messages

def get_rag_chain(model="nvidia/nemotron-3-ultra-550b-a55b:free"):
    llm = ChatOpenAI(
        model=model,
        openai_api_key=os.environ["OPENROUTER_API_KEY"],
        openai_api_base="https://openrouter.ai/api/v1",
    )

    contextualize_q_chain = contextualize_q_prompt | llm | output_parser

    def run_chain(inputs):
        chat_history = _convert_chat_history(inputs.get("chat_history", []))
        question = inputs["input"]

        if chat_history:
            question = contextualize_q_chain.invoke({
                "input": question,
                "chat_history": chat_history,
            })

        docs = retriever.invoke(question)
        context = _format_docs(docs)

        answer = (qa_prompt | llm | output_parser).invoke({
            "input": inputs["input"],
            "context": context,
            "chat_history": chat_history,
        })

        return {"answer": answer}

    return RunnableLambda(run_chain)
