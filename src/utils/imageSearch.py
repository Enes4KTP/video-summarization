from matplotlib import pyplot as plt

class ImageSearch:
    def calculator(self,scene_list,getFrameRate):
        for i, scene in enumerate(scene_list):
            print(f"Sahne {i} - Başlangıç: {scene.starting_index / getFrameRate()} s, Bitiş: {scene.ending_index / getFrameRate()} s")
        self.scene = scene
        
    def search(collection):
        images, labels = [], []

        user_queries = input("Lütfen arama terimlerini virgülle ayırarak yazın: ")
        query_terms = [query.strip() for query in user_queries.split(",")]

        for query in query_terms:
            retrieved = collection.query(query_texts=[query], include=['data'], n_results=3)

            time = 12

            minutes = int(time // 60)
            seconds = int(time % 60)
            formatted_time = f"{minutes:02d}:{seconds:02d}"

            for img in retrieved['data'][0]:
                images.append(img)
                labels.append({"label": query, "time": formatted_time})

        fig, axs = plt.subplots(1, len(images), figsize=(18, 6))

        for i, (image, label) in enumerate(zip(images, labels)):
            ax = axs if len(images) == 1 else axs[i]
            ax.imshow(image)
            ax.set_title(f"{label['label']}\n{label['time']}")
            ax.axis("off")

        plt.show()
