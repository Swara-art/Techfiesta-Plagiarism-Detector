import chromadb

def get_chroma_client():
    return chromadb.CloudClient(
        api_key="ck-AtF4guC5v8zdP3geoMBUBeA6XBge1spmkzV2wNFUX7WP",
        tenant="131e8c3e-b60b-4906-80e6-a4a266fe5a27",
        database="Plagiarism"
    )
