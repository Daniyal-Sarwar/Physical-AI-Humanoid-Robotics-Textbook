import chromadb
c = chromadb.PersistentClient(path='data/chroma')
col = c.get_collection('physical_ai_textbook')
print('Count:', col.count())
