from sentence_transformers import SentenceTransformer

print("모델 로딩 시작")

model = SentenceTransformer("BAAI/bge-m3")

print("모델 로딩 완료")

text = """
전자정부프레임워크 4.3에서는
패키지명이 org.egovframe.rte 로 변경되었다.
"""

embedding = model.encode(text)

print(f"Vector Dimension : {len(embedding)}")

print(embedding[:10])