---
id: "egovframework-dev-com"
title: "개발환경 메인"
version: "4.3"
category: "development"
source: "eGovFrame Wiki"
source_url: "https://www.egovframe.go.kr/wiki/doku.php?id=egovframework%3Adev%3Acom%3A%EA%B0%9C%EB%B0%9C%ED%99%98%EA%B2%BD_%EB%A9%94%EC%9D%B8"
format: "markdown"
---

## 개요
개발프레임워크 개발 환경의 개발도구에 대한 소개 및 링크 URL 정보를 관리한다.
## 설명
일반 사용자가 개발도구를 사용하기 위해서는 각 프로젝트의 개발환경에 맞게 개발도구의 링크 URL을 변경하여야 한다. 이를 변경하기 위해서는 다음의 절차를 따라야 한다.

- **관리자 로그인** 시스템 초기 배포시 admin/admin123으로 셋팅되어 있으며 로그인 후 비밀번호 변경으로 변경하여야 한다. - 메뉴 관리 각 도구에 대한 프로젝트 별 링크 URL 정보 및 활성화 여부를 수정하여 저장한다. ## 환경설정
- 개발환경 메인 Tool 설치 전자정부 프레임워크 포탈(http://www.egovframe.go.kr)을 통해 개발환경 메인 Tool을 내려받고 해당 WAS서버에 Deploy한다. - DB 스키마 생성 전자정부 프레임워크 포탈(http://www.egovframe.go.kr)을 통해 개발환경 메인 Tool의 DB Schema 생성 sql을 다운로드 받는다. DB에 접속하여 sql을 실행한다. - DB 접속정보 변경 개발환경 메인 Tool을 해당 WAS에 Deploy한 후 배포위치 하위의 WEB-INF/config/context-datasource.xml파일을 해당 프로젝트에 맞게 변경한다. 배포시 mysql 데이터베이스의 dev유저에 대해 default 셋팅되어 있다. ## 사용법
개발환경 메인의 기능에 대한 화면설명은 다음과 같다.
### 초기 화면
[이미지]
- 개발환경 개발도구의 각각의 메인페이지로 이동할 수 있다.
- 일반사용자가 사용전에 각 프로젝트 환경에 맞게 개발도구에 대한 환경설정이 되어있어야 하며, 그에 대한 링크 URL을 관리자가 수정해 주어야 한다.
### 관리자 로그인
[이미지]
- 아이디, 비밀번호를 입력한다.
- '로그인' 버튼을 클릭한다.
### 메뉴 관리
[이미지]
- 각 도구별 URL을 입력하고 활성화 여부를 선택한다.
- '저장' 버튼을 클릭한다.
