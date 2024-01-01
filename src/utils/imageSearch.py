from matplotlib import pyplot as plt
import requests

class ImageSearch:
    def search(collection):
        user_queries = input("Lütfen arama terimlerini virgülle ayırarak yazın: ")
        query_terms = [query.strip() for query in user_queries.split(",")]
        images, labels = [], []

        for query in query_terms:
            try:
                retrieved = collection.query(query_texts=[query], include=['data'], n_results=1)
                
                for result in retrieved['data']:
                    frame = 12
                    time = frame / 3

                    minutes = int(time // 60)
                    seconds = int(time % 60)
                    formatted_time = f"{minutes:02d}:{seconds:02d}"

                    for img in result:
                        images.append(img)
                        labels.append({"label": query, "time": formatted_time})
                        
            except requests.exceptions.ConnectionError as e:
                # Bağlantı hatası durumunda bir hata oluştuğunu belirt
                print("Hata: Bağlantı hatası oluştu, PostHog'a erişilemiyor.")

        fig, axs = plt.subplots(1, len(images), figsize=(18, 6))

        for i, (image, label) in enumerate(zip(images, labels)):
            ax = axs if len(images) == 1 else axs[i]
            ax.imshow(image)
            ax.set_title(f"{label['label']}\n{label['time']}")
            ax.axis("off")

        plt.show()