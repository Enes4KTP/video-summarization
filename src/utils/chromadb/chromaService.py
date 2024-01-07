import chromadb
import os
from chromadb.utils.embedding_functions import OpenCLIPEmbeddingFunction
from chromadb.utils.data_loaders import ImageLoader
from src.utils.imageSearch import ImageSearch


class ChromadbService:
    def __init__(self):
        self.client = chromadb.PersistentClient(path="src/utils/chromadb")
        self.embedding_function = OpenCLIPEmbeddingFunction()
        self.image_loader = ImageLoader()

    def storeImages(self,summarization_path):
        self.path = summarization_path
        cleaned_name = summarization_path.replace("/", "").replace("_", "")

        try:
            existing_collection = self.client.get_collection(
                name= cleaned_name,
                embedding_function=self.embedding_function,
                data_loader=self.image_loader)
        except ValueError as e:
            existing_collection = None

        if existing_collection:
            collection = existing_collection
        else:
            collection = self.client.create_collection(
                name= cleaned_name,
                embedding_function=self.embedding_function,
                data_loader=self.image_loader
                )
            folder_path = summarization_path
            file_names = [file for file in os.listdir(folder_path) if file.lower().endswith('.jpg')]
            file_names_only = [os.path.splitext(file)[0] for file in file_names]
            image_uris = [os.path.join(folder_path, file) for file in file_names]
            ids = [str(i) for i in range(len(file_names_only))]
            collection.add(ids=ids, uris=image_uris)  
            
        image_search = ImageSearch()
        image_search.search(collection)


