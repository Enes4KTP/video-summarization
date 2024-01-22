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

    def storeImages(self,summarization_path,scene_list,frameRate):
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
            name=cleaned_name,
            embedding_function=self.embedding_function,
            data_loader=self.image_loader
            )
            folder_path = summarization_path
            file_names = [file for file in os.listdir(folder_path) if file.lower().endswith('.jpg')]
            file_names_only = [os.path.splitext(file)[0] for file in file_names]
            file_names_sorted = [file_names[i] for i in sorted(range(len(file_names)), key=lambda k: int(file_names[k].split('.')[0]))]
            image_uris = [os.path.join(folder_path, file) for file in file_names_sorted]
            ids = [str(i) for i in range(len(file_names_only))]

            scene_info = []
            for i, scene in enumerate(scene_list):
                start_time = max(0, (round((scene.starting_index / frameRate()))))
                end_time = max(0, (round((scene.ending_index / frameRate()))))
                scene_info.append({"scene_id": i, "start_time": start_time, "end_time": end_time})
                print(f"Sahne {i} - Başlangıç: {start_time} s, Bitiş: {end_time} s")

            collection.add(
                ids=ids,
                uris=image_uris,
                metadatas=[
                    {"start_time": scene_info[i]["start_time"], "end_time": scene_info[i]["end_time"]}
                    for i in range(len(ids))
                ]
            )
            
        image_search = ImageSearch()
        image_search.search(collection)


