import os
from dotenv import load_dotenv
from typing import TypedDict, Annotated, Sequence
from langgraph.graph import StateGraph, END
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage, ToolMessage
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_core.tools import tool
import feedparser

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

urls = [
    "https://news.ycombinator.com/rss",
    "https://ai-techpark.com/category/ai/feed",
    "https://knowtechie.com/category/ai/feed/",
    "https://www.theguardian.com/technology/artificialintelligenceai/rss",
    "https://machinelearningmastery.com/blog/feed",
    "https://www.vox.com/rss/index.xml",
]

documents = []
seen_links = set()

for url in urls:
    try:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            link = entry.get("link", "")
            if link in seen_links:
                 continue  
            seen_links.add(link)

            title = entry.get("title", "")
            page_content = title
            if "content" in entry and isinstance(entry["content"], list):
                page_content += "\n" + "\n".join([c.get("value", "") for c in entry["content"]])
            if "summary" in entry:
                page_content += "\n" + entry["summary"]

            categories = ", ".join([t["term"] for t in entry.get("tags", []) if "term" in t])

            doc = Document(
                page_content=page_content,
                metadata={"link": link, "categories": categories}
            )
            documents.append(doc)
        print(f"Loaded {len(feed.entries)} entries from {url}")
    except Exception as e:
        print(f"Error processing {url}: {e}")


persist_directory = "Agents_db"
collection_name = "rss_data"

if not os.path.exists(persist_directory):
    os.makedirs(persist_directory)

try:
    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=persist_directory,
        collection_name=collection_name
    )
    print(f"Created ChromaDB vector store with {len(documents)} documents!")
except Exception as e:
    print(f"Error setting up ChromaDB: {str(e)}")
    raise

retriver = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 5}
)

@tool
def retriever_tool(query: str) -> str:
    """This tool searches and returns the information from the articles."""
    docs = retriver.invoke(query)

    if not docs:
        return "I found no relevant information in the articles"
    
    return docs

tools = [retriever_tool]
llm = llm.bind_tools(tools)

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

def should_continue(state: AgentState):
    """Check if the last message contains tool calls."""
    result = state["messages"][-1]
    return hasattr(result, 'tool_calls') and len(result.tool_calls) > 0

system_prompt = """
You are an intelligent AI assistant who answers questions about articles based on the RSS data loaded into your knowledge base.
Use the retriever tool avaible to answer questions about articles data. You can make multiple calls if needed.
If you need to look up some information before asking a follow up question, you are allowed to do that!
Please always cite the specific parts of the documents you use in your answers.
"""

tools_dict = {our_tool.name: our_tool for our_tool in tools}

def call_llm(state: AgentState):
    """Function to call LLM with the current state."""
    messages = list(state["messages"])
    messages = [SystemMessage(content=system_prompt)] + messages
    message = llm.invoke(messages)
    return {"messages": [message]}

def take_action(state: AgentState) -> AgentState:
    """Execute tool calls from the LLM's response."""
    tool_calls = state["messages"][-1].tool_calls
    results = []
    for t in tool_calls:
        print(f"Calling Tool: {t['name']} with query: {t['args'].get('query','No query provided')}")
        if not t['name'] in tools_dict:
            print(f"\n Tool: {t['name']} doesn't exist.")
            result = "Incorrect Tool Name, Please Retry and Select tool from List of Available tools."
        else:
            result = tools_dict[t['name']].invoke(t['args'].get('query',''))
            print(f"Result length: {len(str(result))}")
        results.append(ToolMessage(tool_call_id=t['id'], name=t['name'], content=str(result)))
    print("Tools Execution Complete. Back to the model!")
    return {"messages": results}

graph = StateGraph(AgentState)
graph.add_node("llm", call_llm)
graph.add_node("retriever_agent", take_action)

graph.add_conditional_edges(
    "llm",
    should_continue,
    {
        True: "retriever_agent", 
        False: END,
    }
)

graph.add_edge("retriever_agent", "llm")
graph.set_entry_point("llm")

rag_agent = graph.compile()

def running_agent():
    print("\n ------ RAG AGENT -------")
    while True:
        user_input = input("\n What is your question: ")
        if user_input.lower() in ['exit', 'quit']:
            break
        messages = [HumanMessage(content=user_input)]
        result = rag_agent.invoke({"messages": messages})
        print("\n ------ ANSWER -------")
        print(result["messages"][-1].content)

running_agent()
