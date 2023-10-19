from pymilvus import connections, FieldSchema, DataType, CollectionSchema, Collection
from text2vec import SentenceModel
import random
import numpy as np

milvus_connect = connections.connect(host='192.168.48.10', port='19530')


def create_collection(collection_name):
    """
      创建集合
    :return:
    """
    stock_code = FieldSchema(
        name="stock_code",
        dtype=DataType.VARCHAR,
        is_primary=True,
        max_length=6
    )

    content = FieldSchema(
        name="embedding",
        dtype=DataType.FLOAT_VECTOR,
        dim=768
    )
    schema = CollectionSchema(
        fields=[stock_code, content],
        description="测试集合"
    )

    collection = Collection(
        name=collection_name,
        schema=schema,
        using="default",
        shards_num=2,
        consistency_level="Strong"
    )


def create_index(collection_name):
    """
      创建索引
    :return:
    """
    collection = Collection(collection_name)
    index_params = {
        "index_type": "IVF_FLAT",
        "metric_type": "L2",
        "params": {
            "nlist": 1024
        }
    }
    collection.create_index(
        field_name="embedding",
        index_params=index_params,
        index_name="idx_embedding"
    )


def build_data():
    data = [
        [str(i) for i in range(20)],
        [np.random.rand(768).tolist() for i in range(20)]
    ]
    return data


def build_embedding(sentences=[]):
    """
    构建embedding
    :param sentences:
    :return:
    """
    model = SentenceModel(model_name_or_path="/Users/kenneth/Developer/python/datas/text2vec-base-chinese",
                          device="mps")
    embeddings = model.encode(sentences)
    return embeddings


if __name__ == "__main__":
    collection_name = "test2"
    # 创建集合
    # create_collection(collection_name=collection_name)

    # 创建索引
    # create_index(collection_name=collection_name)

    collection = Collection(collection_name)

    # 加载集合
    # collection.load()

    # 插入数据
    # collection.insert(build_data())

    collection.flush()



