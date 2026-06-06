---
id: "egovframework-dev"
title: "개발환경 가이드"
version: "4.3"
category: "development"
source: "eGovFrame Wiki"
source_url: "https://www.egovframe.go.kr/wiki/doku.php?id=egovframework%3Adev"
format: "markdown"
---

## 개발프레임워크 개발환경
개발프레임워크 개발 환경 개요 개발 프레임워크의 목표, 제공 서비스 및 환경설정 관련한 도구(JDK, WAS, DB, OpenSource)의 스펙 정보 등을 안내한다.
- eGovframework:DEV:COM:개발환경 메인 개발프레임워크 개발 환경의 개발도구에 대한 소개 및 링크 URL 정보를 관리한다.
### Implementation Tool
- eGovframework:DEV:IMP:Editor eGov Framework Editor는 전자정부 개발 도구 통합을 위한 개방형 플랫폼으로, IDE(Integrated Development Environment) 기반으로 Edit 기능을 제공한다.
- eGovframework:DEV:IMP:editor:IDE eGovFrame기반의 어플리케이션 개발 시 개발자 편의성을 위하여 eclipse기반의 Perspective, Menu, 프로젝트 생성 마법사 등을 제공한다.
- eGovframework:DEV:IMP:editor:SourceCode Editor eGov Framework SourceCode Editor는 전자정부 개발 도구 통합을 위한 개방형 플랫폼으로, IDE(Integrated Development Environment) 기반으로 Edit 기능을 제공한다.
- eGovframework:DEV:IMP:editor:UML Editor UML 작성도구로써 Activity/Class/Sequence/UseCase Diagram 작성을 지원한다.
- eGovframework:DEV:IMP:editor:UML Editor:Use Case Diagram Editor
- eGovframework:DEV:IMP:editor:UML Editor:Class Diagram Editor
- eGovframework:DEV:IMP:editor:UML Editor:Sequence Diagram Editor
- eGovframework:DEV:IMP:editor:UML Editor:Activity Diagram Editor
- eGovframework:DEV:IMP:editor:ERD Editor 통합개발환경에서 ER 의 물리모델 작성을 지원하는 Editor이다.
- eGovframework:DEV:IMP:editor:DBIO Editor DataBase 접근에 관한 표준적인 방법을 제공하는 Editor 이다.
- eGovframework:DEV:IMP:editor:DBIO Editor:SQL Map Config Editor SQL Maps Config File 작성을 지원하는 Editor 이다.
- eGovframework:DEV:IMP:editor:DBIO Editor:SQL Map Editor SQLMap Editor는 SQL Map File 작성을 지원하는 Editor 이다.
- eGovframework:DEV:IMP:editor:DBIO Editor:Data Source Explorer Database Source 를 설정하고, Data Source 내의 하위 객체를 조회할 수 있도록 지원한다.
- eGovframework:DEV:IMP:editor:DBIO Editor:DBIO Search View SQL Map 파일 내에 있는 Query Id를 검색하는 기능을 제공한다.
- eGovframework:DEV:IMP:editor:WebFlow Editor Spring WebFlow 설정 파일의 유효성 검사 및 에디팅을 위한 유용한 기능을 제공한다.
- Code Generation 분석/설계 과정에서 작성된 각종 모델 산출물 또는 소스 코드가 아닌 간단한 모델링 또는 설정을 통하여 실제 소스 코드 또는 Skeleton 코드를 생성하는 기능을 제공한다.
- 템플릿 기반 Code Gen.  DB Table 기반 Code Gen. 기능과 Configuration 파일 생성 기능
- 모델 기반 Code Gen. 분석/설계 단계의 개념 모델을 UML 2.0의 Execute Model 기법을 통해 소스 코드로 변환 생성하는 기능
- Code Inspection 정의된 규칙을 기반으로 개발자가 작성한 소스 코드를 검사하여, 오류 및 위험 요인을 식별하여 알려 주는 기능을 제공한다. Code Inspection 도구에 대한 개요와 설치, 업데이트 방법에 대하여 설명한다.
- Inspection 도구활용 전자정부 표준프레임워크에서 제공하는 Code Inspection 도구의 기본 사용법에 대하여 설명한다.
- Inspection 사용자정의 룰 활용 전자정부 표준프레임워크에서 제공하는 표준 Inspection 룰 이외에, 사용자가 직접 룰을 작성하고 적용하는 방법에 대하여 설명한다.
- eGovframework:DEV:IMP:Debug
- eGovframework:DEV:IMP:Debug:Local Debug 로컬 디버거는 프로그램과 동일한 시스템에서 수행 중인 프로그램에 대한 디버깅 기능을 제공한다.
- eGovframework:DEV:IMP:Debug:Remote Debug 원격 컴퓨터의 WAS(Jboss, JEUS, WebLogic)에서 실행되는 어플리케이션에 대한 디버깅 기능을 제공한다.
### Test Tool
- eGovframework:DEV:TST:Unit Test 개발한 대상 코드에 대해 테스트하고자 개발자가 작성한 테스트를 위한 코드로서의 Unit Test 에 대해 가이드한다.
- eGovframework:DEV:TST:Test Case JUnit 을 이용하여 Unit Test Case 를 작성하고 실행하는 방법을 안내한다.
- eGovframework:DEV:TST:Mock Support 단위테스트 클래스 작성 시 Mock 객체 (모의 객체)를 사용하는 방법에 대해 가이드한다.
- eGovframework:DEV:TST:DB Support 데이터베이스 관련 단위 테스트를 수행하기 위한 Test Case 를 작성하고 실행하는 방법을 안내한다.
- eGovframework:DEV:TST:Test Automation 개발자가 작성한 다수의 단위테스트 클래스를 자동으로 테스트하고 그 결과 리포트를 생성하는 기능에 대해 설명한다.
- eGovframework:DEV:TST:Write TestSuite 작성된 다수의 테스트 클래스들을 한데 묶어 테스트 자동화를 하기 위한 준비를 한다.
- eGovframework:DEV:TST:Run TestSuite 단위테스트 클래스의 테스트를 한꺼번에 수행하고 자동화한다.
- eGovframework:DEV:TST:Test Reporting 테스트 수행 결과를 Text, XML, HTML, Excel 형태의 리포트를 생성한다.
- eGovframework:DEV:TST:Test Coverage 개발자가 작성한 코드에 대해 테스트 코드가 있는지 그 커버하는 정도를 알려주고 그 결과를 리포팅하는 것에 대해 설명한다.
### Deployment Tool
- eGovframework:DEV:DEP:Build Tool 개발자 PC에서 이루어지는 개인 빌드 및 개발 서버에서 이루어지는 통합 빌드에 대해 설명한다.
- eGovframework:DEV:DEP:Build Tool:개인빌드 개발자 PC에서 이루어지는 소프트웨어 빌드 개념 및 빌드 도구인 Maven 기반의 빌드에 대해 설명한다.
- eGovframework:DEV:DEP:Build Tool:개인빌드:빌드 LifeCycle 소프트웨어 빌드 LifeCycle에 대한 개요 및 Maven 기반의 빌드 명령에 대해 설명한다.
- eGovframework:DEV:DEP:Build Tool:개인빌드:빌드 레퍼지토리 라이브러리 관리를 위한 레퍼지토리에 대해 설명한다.
- eGovframework:DEV:DEP:Build Tool:개인빌드:구현도구 플러그인 이클립스 기반의 개인빌드를 위한 Maven 플러그인 사용법에 대해 설명한다.
- eGovframework:DEV:DEP:Build Tool:통합빌드 Continuous Integration 개념을 적용한 소프트웨어의 지속적인 통합에 대해 설명한다.
- eGovframework:DEV:DEP:Nexus Nexus는 Maven repository manager로 프로젝트 또는 기업에서 필요로 하는 내부 레퍼지토리 구성을 위한 도구이다.
- eGovframework:DEV:DEP:서버 이관 빌드 후 패키징 된 모듈에 대해 Target 서버로의 이관 및 WAS 기동/중지 기능을 제공한다.
### Configuration & Change Management
- eGovframework:DEV:SCM:Configuration Management 형상관리도구(소스관리도구)의 개념과 특징, 종류에 대하여 설명한다.
- eGovframework:DEV:SCM:소스관리도구 서버환경 운영 소스관리도구인 Subversion의 서버환경 운영에 대하여 설명한다.
- eGovframework:DEV:SCM:소스관리도구 클라이언트환경 사용 Subversion 클라이언트의 한 종류인 Subversive Eclipse IDE 플러그인의 사용법을 설명한다.
- eGovframework:DEV:ISU:Change Management Change Management의 개요 및 설치, 기능에 대하여 설명한다.
- eGovframework:DEV:ISU:기능:이슈관리 사용자가 이슈를 등록하고, 담당자가 해당 이슈 처리결과를 업데이트 하여 이슈를 처리하는 방법을 설명한다.
- eGovframework:DEV:ISU:기능:이슈검색 등록 및 삭제된 이슈를 검색하는 기능을 설명한다.
- eGovframework:DEV:ISU:기능:대시보드 스페이스별로 등록된 이슈 건수를 한눈에 조회하는 대시보드를 설명한다.
- eGovframework:DEV:ISU:기능:스페이스관리 스페이스 및 롤, 상태, 필드 등 이슈가 관리될 수 있는 범위를 관리하는 기능에 대해 설명한다.
- eGovframework:DEV:ISU:기능:사용자관리 사용자의 기본정보를 관리하는 기능을 설명한다.
- eGovframework:DEV:ISU:기능:통계 스페이스별 이슈 통계를 설명한다.
- eGovframework:DEV:ISU:기능:설정관리 Change Managemet에서 사용하는 환경설정을 변경하는 내용을 설명한다.
### Getting Started
- eGovframework:DEV:GettingStarted
### 구현도구 운영 가이드
- eGovframework:DEV:operator guide
