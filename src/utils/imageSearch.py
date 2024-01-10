from matplotlib import pyplot as plt
import mpld3

class ImageSearch:
    def search(self,collection):
        while True:
            images, labels, metadata = [], [], []

            user_queries = input("Lütfen arama terimlerini virgülle ayırarak yazın: (Çıkmak için q yazınız.)")
            query_terms = [query.strip() for query in user_queries.split(",")]

            if user_queries.lower() == 'q':
                break

            for query in query_terms:
                retrieved = collection.query(query_texts=[query], include=['data', 'metadatas'], n_results=1)

                for img, meta in zip(retrieved['data'][0], retrieved['metadatas'][0]):
                    images.append(img)
                    labels.append({"label": query})
                    metadata.append({"start_time": meta["start_time"]})

            fig, axs = plt.subplots(1, len(images), figsize=(18, 6))

            for i, (image, label, meta) in enumerate(zip(images, labels, metadata)):
                ax = axs if len(images) == 1 else axs[i]
                ax.imshow(image)
                ax.text(
                    0.5,  # x koordinatı
                    1.05,  # y koordinatı (negatif, altta olacak şekilde)
                    f"{label['label']} - Başlangıç Süresi: {meta['start_time']} s",
                    fontsize=12,  # Metin boyutu
                    ha="center",  # Yatay hizalama: 'center'
                    va="center",  # Dikey hizalama: 'center'
                    transform=ax.transAxes  # Koordinat sistemini belirtme
                )
                ax.axis("off")

            mpld3.show()

        print("Program Sonlandırıldı!")
