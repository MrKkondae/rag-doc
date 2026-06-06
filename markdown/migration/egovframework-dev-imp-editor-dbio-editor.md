---
id: "egovframework-dev-imp-editor-dbio-editor"
title: "DBIO Editor"
version: "4.3"
category: "development"
source: "eGovFrame Wiki"
source_url: "https://www.egovframe.go.kr/wiki/doku.php?id=egovframework%3Adev%3Aimp%3Aeditor%3Adbio_editor"
format: "markdown"
---

# DBIO Editor
## 개요
DBIO는 DataBase Input/Output의 약자로 개발환경에서 제공하는 데이터베이스 접근에 관한 표준적인 방법이다.
데이터베이스를 쉽고 일관된 API로 접근할수 있도록 해주며 업무컴포넌트 개발시에 데이터베이스 벤더에 관계없이 코딩할수 있도록 해준다.
eGovFrameWork 의 DBIO Editor 는 DBIO 를 쉽게 가공할 수 있도록 유용한 기능을 제공한다.

주요기능은 다음과 같다.
- **SQL MAP Config File 편집기** : DB 접속정보와 SQL MAP File 목록 정보를 편집하는 기능
- **SQL MAP File 편집기** : Query정보, Parameter 와 Result 의 처리방법을 편집하는 기능
- **Data Source Explorer** : Database Source 를 설정하고, Data Source 내의 하위 객체를 조회할 수 있는 기능
- **DBIO Search View** : SQL Map 파일 내에 있는 Query Id를 검색하는 기능
## 환경설정
사용자가 DBIO Editor를 사용하기 위해서는 사용자의 eclipse 개발환경에 eGovFrameWork DBIO 를 업데이트해야 한다. 업데이트하는 방법은 다음과 같다.
- 사용자의 eclipse 개발환경에서 메뉴 > Help > Software Updates 를 클릭한다. [이미지]
- "Software Updates and Add-ons" 다이얼로그 창에서 Available Software 탭을 클릭한다.
- "Available Software" 목록 우측에 있는 "Add Site..." 버튼을 클릭한다. [이미지]
- "Add Site" 다이얼로그 창에 있는 Location 입력 항목에 "http://www.egovframe.go.kr/update" 를 입력하고 "OK" 버튼을 클릭한다. [이미지]
- "Available Software" 목록에 입력한 Url 이 추가된다.
- 입력된 항목 또는 하위 트리의 모든 항목을 선택한다.
- "Available Software" 목록 우측에 있는 "Install..." 버튼을 클릭한다. [이미지]
