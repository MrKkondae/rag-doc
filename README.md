# rag-docs

전자정부프레임워크 4.3 Wiki 기반 RAG 데이터셋 생성 프로젝트

## 기능

- Wiki 수집
- Markdown 변환
- Chunk 생성
- BGE-M3 임베딩 생성
- 유사도 검색

## 실행순서

1. collect_egov_wiki.py
2. convert_wiki_to_markdown.py
3. create_chunks.py
4. build_embeddings.py
5. search_chunks.py

# TODO

## RAG 품질 개선

[ ] Parent Heading(Heading Path) 적용
[ ] Chunk Metadata 표준화
[ ] Hybrid Search(Vector + Keyword) 개선
[ ] 검색 결과 Re-ranking 검토

## 전환 지식베이스 확장

[ ] migration-policy 문서 추가
[ ] dao-analysis 결과 추가
[ ] sqlmap-analysis 결과 추가
[ ] spring-context-analysis 결과 추가
[ ] compile-log-analysis 결과 추가

## AI 전환 연계

[ ] RAG Prompt Generator 구현
[ ] 변환 프롬프트와 RAG 연계
[ ] 검증 프롬프트와 RAG 연계

## Knowledge Base

[ ] eGovFrame 4.3 Wiki 추가
[ ] migration-policy 추가
[ ] analysis 결과 추가
[ ] conversion 결과 추가
[ ] validation 결과 추가
[ ] 전환 사례(Knowledge Case) 축적