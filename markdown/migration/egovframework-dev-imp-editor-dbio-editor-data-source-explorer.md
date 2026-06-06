---
id: "egovframework-dev-imp-editor-dbio-editor-data-source-explorer"
title: "Data Source Explorer"
version: "4.3"
category: "development"
source: "eGovFrame Wiki"
source_url: "https://www.egovframe.go.kr/wiki/doku.php?id=egovframework%3Adev%3Aimp%3Aeditor%3Adbio_editor%3Adata_source_explorer"
format: "markdown"
---

# Data Source Explorer
## 개요
Data Source Explorer 는 Database Source 를 설정하고, Data Source 내의 하위 객체를 조회할 수 있도록 지원한다. 주요기능은 다음과 같다.
- Database Connection 설정
- Database 스키마 조회 및 기타 작업
- ODA DataSource 설정
## 설명
### 화면
Data Source Explorer View 의 메인 화면은 다음과 같다(<그림> 참조). Data Source 를 Category별로 분류하여 사용자의 이해를 돕고 있다. 상단에는 주로 사용되는 기능에 대해서 버튼이 생성되어 있는 데, 사용자는 이 버튼을 사용하여 새로운 Connection Profile 을 생성하거나, Connection Profile 에 대한 Import/Export와 같은 작업을 할 수 있다.

[이미지] <그림> Database Source Explorer View
### 주요 기능
#### Database Connection 설정 =
Data Source Explorer는 사용자의 Database Connection 을 생성, 추가, 수정, 삭제하는 등의 작업을 지원한다. 사용자는 하나 이상의 데이타베이스 연결을 생성할 수 있으며, 생성된 데이타베이스 연결은 작업환경 내의 모든 프로젝트에서 공유하여 사용할 수 있다.
#### Database Schema 조회 및 기타 작업 =
Database Source Explorer는 Database Connection에 대한 설정 뿐 아니라 사용자가 생성한 Database Source에 대해서 schema 를 조회하고 일련의 작업을 수행할 수 있도록 지원한다. 테이블을 정의하는 DDL 또는 테이블 데이타를 추출할 수 있고, 권한이 주어진 경우 테이블을 삭제할 수도 있다. 권한에 따라 USER, ROLE, TABLE, IDNEX, SEQUENCE 등 데이타베이스 내에 정의된 스키마를 조회하고 조작할 수 있다.
#### ODA DataSource 설정 =
ODA(Open Data Access) 구성 요소는 유연한 개방형 데이터 액세스 프레임워크이며, 이 구성 요소를 사용하는 애플리케이션에서는 표준 데이터 소스뿐 아니라 사용자 정의 데이터 소스의 데이터에도 액세스할 수 있다.
## 사용법
### 새 Database Connection 생성하기
- Data Source Explorer에 있는 "Database Connections" 위에서 마우스 오른쪽 키를 누른다.
- context menu에서 "New" 를 선택하면 "New Connection Profile" 다이얼로그 창이 오픈된다.
- 사용자는 "type filter text" 라고 제시되어 있는 Filter Text 입력항목을 사용하여 Connection Profile Type를 필터링할 수 있다.
- Connection Profile Type을 선택하고, 목록 하단에 있는 "Next" 버튼을 누른다.
- "Drivers" 선택항목에서 적절한 Driver를 선택한다.
- 선택한 Driver 에 대한 Driver Definition을 지정해야 하는 데, "Drivers" 선택항목 우측에 있는 [이미지] (New Driver Definition) 버튼과 [이미지] (Edit Driver Definition) 버튼을 상요하여 Driver Definition 을 입력한다.
- Driver Definition 에 대한 입력을 마친 후 Properties 그룹의 "General" 탭에서 필요한 Property 값을 입력한다.
- Property 를 입력한 후 Property 그룹 하단에 있는 "Test Connection" 버튼을 사용하여 연결 테스트를 할 수 있다.
- "Finish"버튼을 눌러 Database Connection 을 완료하면 Database Source Explorer 뷰에 작성한 Database Connection 이 추가된다.
### Database Schema 조회하기
- Data Source Explorer에 있는 "Database Connections" 을 확장하면 Database Connection 항목이 나타난다.
- Database Connection 항목을 선택하고 확장하면 하위 Database Schema 가 조회된다.
- 사용자는 테이블 및 컬럼, 인덱스 정보 등을 조회할 수 있다.
### 테이블 데이타 추출하기
- Data Source Explorer 에서 "Database Connections" Tree 를 확장하여 데이타베이스 테이블을 조회한다.
- 데이타베이스 테이블을 선택하고 마우스 오른쪽 키를 누르면 context menu 가 나타난다.
- context menu 에서 Data>Extract 를 선택하면 "Extract Data" 다이얼로그 창이 오픈된다.
- Output File 입력항목 우측에 있는 "Browse..." 버튼을 사용하여 파일 경로 및 파일명을 입력한다.
- "File format" 그룹에 있는 "Column delimiter"와 Charater string delimiter를 선택한다.
- "Finish" 버튼을 누르면 데이타가 추출되어 file로 저장된다.
