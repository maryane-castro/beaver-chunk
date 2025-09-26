import re


def process_PDF(documents):
    if isinstance(documents, list):
        processed_docs = []
        for doc in documents:
            processed_content = doc.page_content.replace("\n", " ")
            processed_content = re.sub(r"\s+", " ", processed_content)
            doc.page_content = processed_content
            processed_docs.append(doc)
        return processed_docs
    else:
        return documents.replace("\n", " ")
