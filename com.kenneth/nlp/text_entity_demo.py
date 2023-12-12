import spacy

nlp = spacy.load("zh_core_web_trf")

sentence1 = "这里是第一句话的内容。"
sentence2 = "这里是第二句话的内容。"

doc1 = nlp(sentence1)
doc2 = nlp(sentence2)

print("第一句话的实体：", [ent.text for ent in doc1.ents])
print("第二句话的实体：", [ent.text for ent in doc2.ents])

entities1 = {ent.text for ent in doc1.ents}
entities2 = {ent.text for ent in doc2.ents}

common_entities = entities1.intersection(entities2)

if common_entities:
    print("相同的实体有：", common_entities)
else:
    print("没有相同的实体。")

