import time
import openai
import os

# LlamaIndex
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core import (
    Settings,
    VectorStoreIndex,
)
from llama_index.core.vector_stores import ExactMatchFilter, MetadataFilters, MetadataFilter
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from openai import AzureOpenAI
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.llms import azure_openai

# pinecone
from llama_index.vector_stores.pinecone import PineconeVectorStore
from pinecone import Pinecone

class RequestLLM:
    def __init__(self) -> None:
        self.pc = Pinecone(api_key="c18185b6-1bb2-45c6-9cf6-4c0b225eed91")
        self.pc_index = self.pc.Index(host="https://law-ai-kbgyolu.svc.aped-4627-b74a.pinecone.io")
    
    def request_generate(self, prompt, filter1: str="", filter2: str="", filter3: str="", filter4: str="", filter5: str=""):
        """
        Sends a request for review to the OpenAI API and returns the generated text.

        Args:
            prompt (str): The content to be reviewed.
            filter (str, optional): The title filter for the documents.

        Returns:
            str: The generated text from the OpenAI API.

        Raises:
            None
        """
        Settings.embed_model = AzureOpenAIEmbedding(
            model="text-embedding-3-large",
            deployment_name="corpu-text-embedding-3-large",
            # api_key=os.getenv("AZURE_API_KEY"),
            # azure_endpoint=os.getenv("AZURE_API_BASE"),
            # api_version="2023-05-15",
            api_key="25417b9e73574c49965cad8f28ab4dd6",  
            api_version="2024-02-01",
            azure_endpoint="https://openaitcuc.openai.azure.com/"
        )

        Settings.llm = azure_openai.AzureOpenAI(
            model="gpt-4o",
            deployment_name="corpu-text-gpt-4o",
            temperature=0.3,
            # api_key=os.getenv("AZURE_API_KEY"),
            # azure_endpoint=os.getenv("AZURE_API_BASE"),
            # api_version="2023-05-15",
            api_key="25417b9e73574c49965cad8f28ab4dd6",  
            api_version="2024-02-01",
            azure_endpoint="https://openaitcuc.openai.azure.com/"
        )
        vector_store = PineconeVectorStore(self.pc_index)

        index = VectorStoreIndex.from_vector_store(vector_store)
        while True:
            try:
                filters = []
                if filter1 != "":
                    filters.append(MetadataFilter(key="title", value=filter1))
                if filter2 != "":
                    filters.append(MetadataFilter(key="title", value=filter2))
                if filter3 != "":
                    filters.append(MetadataFilter(key="title", value=filter3))
                if filter4 != "":
                    filters.append(MetadataFilter(key="title", value=filter4))
                if filter5 != "":
                    filters.append(MetadataFilter(key="title", value=filter5))

                if not filters:
                    print("No references added, getting references")
                    retriever = VectorIndexRetriever(index=index, similarity_top_k=4)
                else:
                    print(f"references '{' + '.join(filter for filter in [filter1, filter2, filter3, filter4, filter5] if filter)}' found, adding to references")
                    filters = MetadataFilters(filters=filters, condition='or')
                    retriever = VectorIndexRetriever(index=index, similarity_top_k=4, filters=filters)

                query_engine = RetrieverQueryEngine.from_args(
                    retriever=retriever,
                )
                result = query_engine.query(prompt)
                return result
            except Exception as e:
                try:
                    print(f"Error occurred: {e}, reduce similarity top k......")
                    retriever = VectorIndexRetriever(index=index, similarity_top_k=2)
                    query_engine = RetrieverQueryEngine.from_args(
                        retriever=retriever,
                    )
                    result = query_engine.query(prompt)
                    return result
                except Exception as e:
                    print(f"Fallback error occurred: {e}, retrying after sleep...")
                    time.sleep(7)