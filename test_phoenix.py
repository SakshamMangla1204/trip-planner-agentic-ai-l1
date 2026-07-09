from phoenix.otel import register
from openinference.instrumentation.langchain import LangChainInstrumentor
from langchain_ollama import ChatOllama

tracer_provider = register(project_name="phoenix-test")

LangChainInstrumentor().instrument(
    tracer_provider=tracer_provider
)

llm = ChatOllama(
    model="qwen3:8b",
    temperature=0
)

response = llm.invoke("Say hello in one sentence.")

print(response.content)