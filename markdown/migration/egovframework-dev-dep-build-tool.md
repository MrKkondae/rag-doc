---
id: "egovframework-dev-dep-build-tool"
title: "통합빌드"
version: "4.3"
category: "development"
source: "eGovFrame Wiki"
source_url: "https://www.egovframe.go.kr/wiki/doku.php?id=egovframework%3Adev%3Adep%3Abuild_tool%3A%ED%86%B5%ED%95%A9%EB%B9%8C%EB%93%9C"
format: "markdown"
---

## 개요
각 개발자들이 개인 빌드 과정을 거쳐 작성한 코드들을 통합하여 실행 가능한 산출물로 만들어 내는 일련의 과정을 통합 빌드라 하며 지속적이고 자동화된 통합을 위하여
CI를 사용하며 Continous Integration이란 여러 명으로 구성된 팀이 작업한 것을 자주-각 팀원이 하루에 한 번 이상, 매일 여러 번-통합하는 것을 가리키는 소프트웨어 개발 Practice를 말한다.
## 설명
CI 효과와 특징
- 효과
- 흔히 발생하는 일반적인 위험을 줄여준다.
- 에러를 초기에 발견할 수 있다. 자주 통합할수록 에러가 발생하는 범위가 좁아 에러를 잡는 것이 수월해진다.
- 잘 동작하고 에러가 거의 없는 S/W를 유지할 수 있다.
- 언제 어느 때라도 배포할 수 있는 S/W를 생성해낸다.
- 반복적인 수작업을 줄여준다.
- 프로젝트 가시성을 좋게 해준다.
- 개발 팀이 S/W 제품에 대해 보다 큰 자신감을 갖게 해준다.
- 특징
- 소스 코드 일관성 유지 : 소스 관리 시스템이 필요하다.
- 자동 빌드 : 빌드는 CI 툴에 의해 자동으로 이루어져야 한다.
- 자동 테스트 : 소스 검증과 함께 기능/비기능 테스팅을 매번 검증함으로써 코드의 품질을 높일 수 있다.
- 일일 체크아웃과 빌드 : 빌드 주기가 길어질수록 개발자 소스의 오류 발생 확률이 높아지고 그 만큼 시간을 낭비하게 된다. CI(Continuous Integration)는 개발자, 버전 관리 저장소, CI시스템, 빌드 스크립트, 의사소통 장치, 통합 빌드 머신 등으로 구성 된다.
[이미지]
CI 서버는 형상관리 서버로부터 개발자들이 commit 한 소스 코드를 check out 받아 CI 서버의 로컬 파일 시스템에 저장하고
그 코드를 바탕으로 빌드를 실행 후 동작하는 코드 산출물(WAR, JAR 등의 working 패키지)을 생성해 낸다.
### 오픈소스 CI서버: Hudson
Hudson은 오픈 소스 CI 서버로 소스와 빌드 스크립트를 사용한 자동 빌드 및 빌드 결과를 개발자에게 피드백 하는 메커니즘을 제공한다. **Hudson의 특징 및 주요 기능**
#### Hudson 특징
- 쉬운 Installation : hudson.war 형태로 servlet container에 배포
- 웹 기반 UI를 통한 쉬운 설정 및 즉각적인 피드백
- 플러그인 기반의 확장성 제공
- 깔끔하고 잘 정의된 문서 및 API
#### Hudson 주요 기능
- 소프트웨어 자동 빌드
- 빌드 주기에 따른 일일 빌드 또는 주간 빌드 기능 제공
- 지속적이고 자동화된 빌드 검증
- SCM 폴링(polling) 기능을 통한 최신 코드 기반의 빌드 수행
- 지속적이고 자동화된 빌드 테스트
- 테스트 슈트 실행을 통한 코드 품질 검증
- 빌드 후속 절차 자동화
- 컴파일 된 코드의 패키징 및 테스트 리포팅 기능 제공
## 환경 설정
### Hudson 설치
1. hudson.war을 다운로드 받는다.
[Hudson 다운로드](https://hudson.dev.java.net/servlets/ProjectDocumentList?folderID=2761&expandFolder=2761&folderID=0)
[이미지]
2. hudson.zip 파일로 받은 파일의 확장자를 .war로 변경한다.
3. 톰캣의 webapp 디렉터리 밑에 다운 받은 hudson.war 파일을 위치시킨다.
[이미지]

4. startup.bat 파일로 톰캣 서버를 구동시킨다.  ### Hudson 시스템 설정
- Configure System 메뉴를 통해 소프트웨어 빌드 작업 및 피드백 작업을 시작하기 위한 JDK 및 Ant, Maven 등의 인스톨 위치를 지정한다.
[이미지]
기본 설정으로 JDK, Maven, Ant, 빌드 결과 피드백 메커니즘 설정을 한다.
1. JDK Home 설정
[이미지]
2. Maven Home 설정
Maven 빌드를 위한 Maven Home 위치 지정
[이미지]
3. Ant Home 설정
Ant 작업 수행을 위한 Ant Home 위치 지정
[이미지]
4. 피드백 설정을 위한 E-mail Notification 설정
SMTP 서버, Hudson 시스템 Admin 이메일 주소, 설치된 Hudson의 URL
[이미지]
## 사용법
### Hudson 대시보드 (dashboard)
   Hudson은 빌드 결과 및 테스트 결과등을 보여주는 대시보드 기능을 제공하고 있다.
[이미지]
### Hudson 프로젝트 메뉴
   Hudson은 등록된 프로젝트의 소스 코드 변경 내용 추적을 위한 메뉴와 수동 빌드 메뉴 그리고 프로젝트 빌드 상태를
   보여주는 메뉴 등을 제공하고 있다.
[이미지]
### Hudson - JUnit 테스트 연동
   Hudson은 기본 설정으로 빌드 스크립트를 이용해 생성한 JUnit 테스트 리포트를 브라우저에 출력해 주는 기능을 제공하고 있으며
   테스트의 Progress 누적 그래프를 Hudson 프로젝트의 초기 화면에 보여주는 기능을 제공한다.
[이미지]
### Hudson - 코드 인스펙션 도구 연동
   Hudson은 코드 인스펙션 도구인 PMD 플러그인을 제공하며 빌드 스크립트를 통해 수행한 PMD 결과 리포트를 PMD 플러그인 연동을 통해
   Hudson 화면에 보여주는 기능을 제공한다.
[이미지]
프로젝트의 Configure 메뉴 선택 후 PMD 설정
[이미지]
Hudson 화면에서 PMD 결과 확인
### Hudson에 소프트웨어 프로젝트 작업 등록하기
#### 1. 설정 전제 조건
- 접근 가능한 소스 코드 저장소(Repository)가 존재해야 한다.
- 저장소는 등록하려고 하는 작업(프로젝트)의 소스 코드를 담고 있어야 한다.
- 프로젝트는 소스 자동 빌드를 위한 스크립트를 반드시 포함하고 있어야 한다.
#### 2. 작업 등록 시나리오
- 등록할 작업명을 입력한다.
- Build a maven2 project를 선택한다. (전자정부 표준 프레임워크는 메이븐 프로젝트를 기본으로 함)
- OK 버튼을 클릭 후 Hudson 작업을 생성한다.
[이미지]
#### 3. 등록된 작업 설정
 3.1 등록한 작업(프로젝트)의 이름 확인 및 프로젝트 요약 설명 작성한다.
[이미지]
 3.2 프로젝트의 코드가 보관된 SCM(저장소)를 선정한다.
- 프로젝트에서 사용중인 SCM을 선택한다. - CVS 또는 SVN 등
- 전자정부 표준 프레임워크에서는 SVN을 개발환경의 도구로 제공하고 있다.
 3.3 SCM 종류 선택 후 Hudson 서버에 등록할 프로젝트가 저장된 저장소(repository) URL을 설정한다.
- URL은 repository에 등록된 프로젝트 name 레벨까지 적어준다.
- 예) http://192.168.100.11:8090/svn/eGovFramework/DEV/egovframework-dev-com
[이미지]
 3.4 주기적 통합을 위한 자동 빌드 주기를 설정한다.
- Hudson은 cron expression 기반의 스케쥴링을 제공하고 있다
- 예) 매일 21시에 빌드 실행 - 0 21 * * *
[이미지]
 3.5 빌드를 설정한다.
- Root POM - Maven 프로젝트의 정보를 담고 있는 pom.xml을 입력한다.
- Maven 빌드 생명 주기 단계 및 option 사항을 입력한다.
- 예) clean install pmd:pmd emma:emma

 3.6 빌드 피드백 매커니즘을 설정한다.
[이미지]
 3.7 빌드 후 인스펙션 도구인 pmd 및 emma 커버리지 리포트 생성 설정을 한다.
[이미지]
## 참고자료
[Martin Fowler - Continous Integration](http://martinfowler.com/articles/continuousIntegration.html#AutomateDeployment)
[Hudson Home](https://hudson.dev.java.net/)
