from ml.data.get_images import return_images_links_by_gender
from db import global_init
from .image_to_trend import generate_trend_summary
from langchain_core.documents import Document
from langchain_community.document_loaders import TextLoader

def summaries_by_gender( gender: str ) -> list[Document]:
    ref_images = return_images_links_by_gender()
    docs = []
    for url in ref_images[gender]:
        try:
            trend_summary = generate_trend_summary(url)
            docs.append(Document(
                            page_content = trend_summary.message.content,
                            metadata = {"source": url}
                        ))
        except Exception as e:
            print(f"Failed to generate trend summary for {url}: {e}")
            continue
    return docs



