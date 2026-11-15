from rag import rebuild_index
if __name__ == "__main__":
    count = rebuild_index()
    print(f"Successfully indexed {count} chunks.")
