from typing import List, Tuple
from sentence_transformers import SentenceTransformer

from agent.models.agentbase import AgentBase
from agent.models.context import Context
from agent.models.input import EmbeddingModelInput
from agent.models.mcpstep import ROLE
from agent.models.output import  FileBaseOutput
from agent.tools.chromadb import ChromaDB


class EmbeddingModel(AgentBase[EmbeddingModelInput, FileBaseOutput]):
    def __init__(self):
        self.agent_name: str = "EmbeddingModel"
        self.role: ROLE = ROLE.EMBEDDING
        self.tool: ChromaDB = ChromaDB()
        self.purpose: str = "Creates Embedding of the files to story or query in the vector database"
        self.__model = SentenceTransformer('BAAI/bge-large-en')
        pass
    
    def run(self, input_data: EmbeddingModelInput, context: Context) -> Tuple[FileBaseOutput, Context, int]:
        self.context = context
        queries = input_data.queries
        
        embeddings = []
        
        for query in queries:           
            embedding = self.__model.encode(query)
            embeddings.append(embedding.tolist())
            
        results = self.tool.execute(workflow=context.workflow, inputs=embeddings, context=context, conditionals=input_data.conditionals)      
        files = [result.convert_to_file_class(context) for result in results]
        
        self.context.retrieved_files.extend(files)
                    
        return files, self.context, 1
