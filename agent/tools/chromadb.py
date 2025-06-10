from typing import List
from chromadb import Where, chromadb, QueryResult
from agent.models.context import Context
from agent.models.embedded_file import EmbeddedFile, Metadata
from agent.tools.tool import Tool


class ChromaDB(Tool):
    def __init__(self):
        super().__init__()
        self.chroma_client = chromadb.HttpClient(host="localhost", port=8005)
        self.collection = None
        
    def execute(self, workflow, inputs: List[float], context: Context, **kwargs) -> List[EmbeddedFile]:
        repo_url = context.issue.repo_url
        repo_name = "_".join(repo_url.split("/")[-2:])
        
        self.collection = self.chroma_client.get_collection(name=repo_name) 
        
        if workflow == "issue_resolution":
            return self.query_chroma(embedding_files=inputs, conditionals=kwargs["conditionals"])
        pass
        
    def query_chroma(self, embedding_files: List[float], conditionals: List[Where]) -> List[EmbeddedFile]:
        results = []
        if conditionals is None:
            conditionals = [None] * len(embedding_files)
    
        for embedding_file, conditional in zip(embedding_files, conditionals):
            results.append(self.collection.query(
                query_embeddings=embedding_file, 
                where=conditional,
                n_results=1 ,
                include=["documents", "metadatas", "embeddings"]
            ))
        new_embedding_files = self.convert_many_query_results(results)
        return new_embedding_files
    
    def convert_many_query_results(self, results: List[QueryResult]) -> List[EmbeddedFile]:
        all_files = []
        for r in results:
            embedding_file = EmbeddedFile.convert_query_result_to_embedding(r)
            all_files.append(embedding_file)
        return all_files
    