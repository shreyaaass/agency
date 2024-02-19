import json
from langchain.text_splitter import CharacterTextSplitter



def ReturnTextChunksFromJson(jsonPath, contentKey, chunkSize, chunkOverlap):
    f = open(jsonPath)
    data = json.load(f)
    textChunks=[]
    count=0
    text_splitter = CharacterTextSplitter(
        separator=" ",
        chunk_size=chunkSize,
        chunk_overlap=chunkOverlap
    )
    for i in data:
        count+=1
        if len(i[contentKey])<chunkSize:
            textChunks.append(i[contentKey])
        else:
            textChunks.extend(text_splitter.split_text(i[contentKey]))
        if count==20:
            break
    f.close()
    return textChunks