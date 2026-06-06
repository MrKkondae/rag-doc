---
id: "egovframework-dev-imp-editor-ide"
title: "IDE"
version: "4.3"
category: "development"
source: "eGovFrame Wiki"
source_url: "https://www.egovframe.go.kr/wiki/doku.php?id=egovframework%3Adev%3Aimp%3Aeditor%3Aide"
format: "markdown"
---

# IDE
## 개요
eGovFrame기반의 어플리케이션 개발 시 개발자 편의성을 위하여 eclipse기반의 Perspective, Menu, 프로젝트 생성 마법사 등을 제공한다.
## 설명
기본 Eclipse IDE 에 eGovFramework기반의 어플리케이션 개발을 위한 View 초기세트와 LayOut, 메뉴, 프로젝트 생성 마법사 등을 추가했고, 상세는 다음과 같다.
##### Perspective
eGovFrame기반의 어플리케이션 개발을 위한 최적의 View 초기 세트와 레이아웃을 제공한다.
##### Menu
eGovFrame Perspective에서만 활성화 되는 메뉴로 eclipse내에서 분산되어 있는 플러그인들의 기능(eGovFrame에서 필히 사용되어지는 기능)을 빠르게 접근할 수 있는 통합 메뉴를 제공한다.
##### 프로젝트 생성 마법사
eGovFrame기반의 어플리케이션을 빌드하기 위한 소스 코드 및 관련 파일의 구조와 빌더 설정을 담고 있는 프로젝트 생성 마법사를 제공한다.
- Core Project : 비즈니스 서비스 개발을 위한 프로젝트로 Model, Vo, DAO, Service등을 개발 한다.
- Web Project : 웹 어플리케이션의 UI 개발을 위한 프로젝트로 Web Application설정 및 Controller, JSP, Css, JavaScript등을 개발 한다.
## 사용법
#### 1. eGovFramework Pespective
- Workbench 오른쪽 위의 바로가기 표시줄에 있는 **Open Perspective**단추 [이미지]를 클릭한다. 메뉴 표시줄의 **_W_indows** > **_O_pen Perspective** 메뉴와 동일한 기능을 제공한다.
- 전체 Perspective 목록을 보려면 드롭 다운 메뉴에서 **_O_ther...**를 선택한다.
- **eGovFramework** Perspective를 선택한다.
- 제목 표시줄이 변경되어 **eGovFramwork**이 표시된다.

[이미지]

[이미지]
#### 2. eGovFramework Menu
Perspective를 eGovFramework으로 변경하면 메뉴 표시줄에 **e_G_ovFramework** 메뉴가 표시된다.

[이미지]

| 구분 | 메뉴 | 설명 |
| --- | --- | --- |
| _S_tart | New _C_ore Project | New eGovFramework Core Project 생성 마법사 실행 |
|  | New _W_eb Project | New eGovFramework Web Project 생성 마법사 실행 |
| _A_nalysis | New _U_secase Diagram | New Usecase Diagram 생성 마법사 실행 |
| _D_esign | New _E_R Diagram | New ER Diagram 생성 마법사 실행 |
|  | New _C_lass Diagram | New Class Diagram 생성 마법사 실행 |
| _I_mplementation | New SQL Map Config | New SQLMap Config 생성 마법사 실행 |
|  | New SQL Map | New SQLMap 생성 마법사 실행 |
|  | Show DBIO Search View | DBIO Search View 표시 |
#### 3. eGovFramework 프로젝트 생성 마법사
##### 3.1. Core Project 생성 마법사
- 메뉴 표시줄에서 **_F_ile** > **_N_ew** > **eGovFramework Core Project**를 선택한다. (단 eGovFramework Perspective내에서) 또는, **Ctrl+N** 단축키를 이용하여 새로작성 마법사를 실행한 후 **eGovFramework** > **eGovFramework Core Project**을 선택하고 **_N_ext**를 클릭한다. [이미지]
- 프로젝트명과 메이븐 설정에 필요한 값들을 입력하고 **Next**를 클릭한다. [이미지]
- 예제 소스 파일 생성 여부를 체크하고 **Finish**를 클릭한다. [이미지]

** Create a eGovFramework Core Project 페이지 **
| 옵션 | 설명 | 기본값 |
| --- | --- | --- |
| Project Name | 새 프로젝트 이름을 입력한다. | 공백 |
| 컨텐츠 | Use default Workspace location체크시 기본 작업공간에 프로젝트 명으로 프로젝트 디렉토리가 생성된다. 임의의 디렉토리 선택시 옵션을 해제하고 **Brows_e_**버튼을 클릭하여 위치를 선택한다. | Use default Workspace location |
| Group Id | Maven에서의 Group Id를 입력한다. | 공백 |
| Artifact Id | Maven에서의 Artifact Id를 입력한다. | 공백 |
| Version | Maven에서의 버젼을 입력한다. | 0.0.1-SNAPSHOT |


** Generate Example 페이지 **
| 옵션 | 설명 | 기본값 |
| --- | --- | --- |
| Generate Example | 프로젝트 생성시 예제 소스 포함 여부를 선택한다. | false |
##### 3.2. Web Project 생성 마법사
- 메뉴 표시줄에서 **_F_ile** > **_N_ew** > **eGovFramework Web Project**를 선택한다. (단 eGovFramework Perspective내에서) 또는, **Ctrl+N** 단축키를 이용하여 새로작성 마법사를 실행한 후 **eGovFramework** > **eGovFramework Web Project**을 선택하고 **_N_ext**를 클릭한다. [이미지]
- 프로젝트명과 메이븐 설정에 필요한 값들을 입력하고 **Next**를 클릭한다. [이미지]
- 예제 소스 파일 생성 여부를 체크하고 **Finish**를 클릭한다.
** Create a eGovFramework Web Project 페이지 **
| 옵션 | 설명 | 기본값 |
| --- | --- | --- |
| Project Name | 새 프로젝트 이름을 입력한다. | 공백 |
| 컨텐츠 | Use default Workspace location체크시 기본 작업공간에 프로젝트 명으로 프로젝트 디렉토리가 생성된다. 임의의 디렉토리 선택시 옵션을 해제하고 **Brows_e_**버튼을 클릭하여 위치를 선택한다. | Use default Workspace location |
| Target Runtime | 웹 어플리케이션을 실행할 타겟 서버를 선택한다. | <none> |
| Dynamic Web Module Version | 동적 웹 모듈 버젼을 선택한다. | 2.5 |
| Artifact Id | Maven에서의 Artifact Id를 입력한다. | 공백 |
| Version | Maven에서의 버젼을 입력한다. | 0.0.1-SNAPSHOT |


** Generate Example 페이지 **
| 옵션 | 설명 | 기본값 |
| --- | --- | --- |
| Generate Example | 프로젝트 생성시 예제 소스 포함 여부를 선택한다. | false |

**※ 프로젝트 생성 후 pom.xml파일의 레파지토리 정보를 각 프로젝트의 개발환경 정보로 변경한다.**
### = 참고자료
