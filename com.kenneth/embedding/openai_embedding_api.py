from sentence_transformers import SentenceTransformer, util
from fastapi import FastAPI, Body
import uvicorn
from pydantic import BaseModel
from typing import List
from enum import Enum

EMBEDDING_MODEL_BASE_PATH = "/Users/kenneth/Developer/python/models"
EMBEDDING_MODELS = {
    "bge-large-zh": {
        "path": f"{EMBEDDING_MODEL_BASE_PATH}/bge-large-zh-v1.5"
    }
}


class EncodingFormat(str, Enum):
    FLOAT = "float",
    BASE64 = "base64"


class EmbeddingRequest(BaseModel):
    input: str | List[str]
    model: str
    encoding_format: EncodingFormat = EncodingFormat.FLOAT
    # 唯一标识符，监控
    user: str = None


class EmbeddingReposeData(BaseModel):
    object: str = "embedding"
    embedding: List[float]
    index: int


class Usage(BaseModel):
    prompt_tokens: int = 0
    total_tokens: int = 0


class EmbeddingRepose(BaseModel):
    object: str = "list"
    data: List[EmbeddingReposeData] = None
    model: str = None
    usage: Usage = None


app = FastAPI()


class EmbeddingAPI:

    @staticmethod
    def get_embedding(model_path, sentence):
        model = SentenceTransformer(model_path)
        embeddings = model.encode(sentence, normalize_embeddings=True)
        return embeddings

    @staticmethod
    def get_embedding_at_openai(model_name, sentence) -> EmbeddingRepose:
        embedding_model = EMBEDDING_MODELS.get(model_name)
        if embedding_model.get("path") is None:
            raise Exception(f"{model_name} embedding model not found.")

        embeddings = EmbeddingAPI.get_embedding(model_path=embedding_model.get("path"), sentence=sentence)
        # 格式化成openai的格式
        response = EmbeddingRepose()
        response.model = model_name
        embeddings_data = list()
        if isinstance(sentence, list):
            for index, embedding in enumerate(embeddings):
                embeddings_data.append(EmbeddingReposeData(embedding=embedding, index=index))

        else:
            embeddings_data.append(EmbeddingReposeData(embedding=embeddings, index=0))

        response.data = embeddings_data
        # 构建usage
        return response

    @app.post("/v1/embedding", response_model=EmbeddingRepose)
    async def get_embedding_at_rest(embedding_request: EmbeddingRequest = Body(...)):
        embedding_api = EmbeddingAPI()
        embeddings_openai = embedding_api.get_embedding_at_openai(embedding_request.model,
                                                                  sentence=embedding_request.input)
        return embeddings_openai


if __name__ == '__main__':
    # model_path = "/Users/kenneth/Developer/python/models/bge-large-zh-v1.5"
    # sentence = "我是中国人"
    # embedding_api = EmbeddingAPI()
    # embeddings = embedding_api.get_embedding(model_path=model_path, sentence=sentence)
    # embeddings_openai = embedding_api.get_embedding_at_openai("bge-large-zh", sentence=sentence)
    #
    # print(embeddings_openai)

    uvicorn.run(app, host="0.0.0.0", port=8080, workers=1)

