---
id: "egovframework-rss"
title: "RSS태그관리"
version: "4.3"
category: "common"
source: "eGovFrame Wiki"
source_url: "https://www.egovframe.go.kr/wiki/doku.php?id=egovframework%3Arss%ED%83%9C%EA%B7%B8%EA%B4%80%EB%A6%AC"
format: "markdown"
---

# 사용자지원 - RSS태그관리
## 개요
**RSS태그관리**는 번번히 게시물이 자주 생겨나거나 업데이트가 자주 일어나는 웹사이트에서, 필요한 정보를 쉽게 사용자들에게 제공하기 위한 서비스로 RSS태그관리 정보를 관리하는 기능을 제공하디.
## 설명
- **RSS태그관리**는 RSS를 등록하기 위한 목적으로 RSS태그 정보를 등록, 수정, 삭제, 조회, 목록조회의 기능을 수반한다.
- **RSS태그관리** 등록/수정시 테이블 컬럼정보는 #테이블컬럼명# 형태로 입력되는 RSS본문정보(본문TITLE,본문LINK, 본문DESCRIPTION)와 RSS서비스를 매핑하기 위한 정보이다.

    ① RSS태그관리 목록 : RSS태그관리 정보를 최근 등록 순서대로 조회하고, 그 결과 목록을 화면에 반영한다.
    ② RSS태그관리 등록 : RSS태그관리 정보를 등록하고, 등록 결과를 조회한다.
    ③ RSS태그관리 수정 : 기 등록된 RSS태그관리 정보의 항목들을 수정한다.
    ④ RSS태그관리 삭제 : 기 등록된 RSS태그관리 정보를 삭제한다.
    ⑤ RSS태그관리 상세조회 : 등록된 RSS태그관리 정보를 상세정보를 조회한다.
#### 관련소스
| 유형 | 대상소스명 | 비고 |
| --- | --- | --- |
| Controller | egovframework.com.uss.ion.rss.web.EgovRssTagManageController.java | RSS태그관리 정보 관리를 위한 컨트롤러 클래스 |
| Service | egovframework.com.uss.ion.rss.service.EgovRssTagManageService.java | RSS태그관리 정보 관리를 위한 서비스 인터페이스 |
| ServiceImpl | egovframework.com.uss.ion.rss.service.impl.EgovRssTagManageServiceImpl.java | RSS태그관리 정보 관리를 관리를 위한 서비스 구현 클래스 |
| DAO | egovframework.com.uss.ion.rss.service.impl.RssTagManageDao.java | RSS태그관리 정보 관리를 위한 데이터처리 클래스 |
| Model | egovframework.com.uss.ion.rss.service.RssManage.java | RSS태그 정보 관리를 위한 Model 클래스 |
| JSP | /WEB-INF/jsp/egovframework/uss/ion/rss/EgovRssTagManageList.jsp | RSS태그관리 정보를 목록조회 하기 위한 jsp페이지 |
| JSP | /WEB-INF/jsp/egovframework/uss/ion/rss/EgovRssTagManageDetail.jsp | RSS태그관리 정보를 성세조회 하기 위한 jsp페이지 |
| JSP | /WEB-INF/jsp/egovframework/uss/ion/rss/EgovRssTagManageRegist.jsp | RSS태그관리 정보를 등록 하기 위한 jsp페이지 |
| JSP | /WEB-INF/jsp/egovframework/uss/ion/rss/EgovRssTagManageUpdt.jsp | RSS태그관리 수정을  위한 jsp페이지 |
| JSP | /WEB-INF/jsp/egovframework/uss/ion/rss/EgovRssTagManageTableColumnList.jsp | RSS태그관리 정보를 등록/수정 할때 컬럼목록을 조회 하기 위한 jsp페이지 |
| XML | /egovframework/sqlmap/com/uss/ion/rss/EgovRssTagManage_SQL_*.xml | RSS태그관리  QUERY XML |
#### 클래스 다이어그램
[이미지]
#### 관련테이블
| 테이블명 | 테이블명(영문) | 비고 |
| --- | --- | --- |
| RSS관리 | COMTNRSS | RSS관리정보를 관리하기 위한 속성정보를 정의하고, 관리한다. |
#### ID Generation
- ID Generation Service를 활용하기 위해서 Sequence 저장테이블인  COMTECOPSEQ에 **RSS_ID** 항목을 추가한다.

 ```sql
INSERT INTO COMTECOPSEQ VALUES('RSS_ID','0');
 ```
## 관련화면 및 수행메뉴얼
#### RSS태그관리 목록조회
| Action | URL | Controller method | QueryID |
| --- | --- | --- | --- |
| 목록조회 | /uss/ion/rss/listRssTagManage.do | EgovRssTagManageList | "RssTagManage.selectRssTagManage" |
|  |  |  | "RssTagManage.selectRssTagManageCnt" |
| 삭제 | /uss/ion/rss/listRssTagManage.do | EgovRssTagManageList | "RssTagManage.deleteRssTagManage" |

RSS태그관리 목록조회는 페이지당 10건씩 조회되며 페이징은 10페이지씩 이루어진다.

[이미지]
조회 : 기 등록된 RSS태그의 목록을 조회한다.
삭제 : 목록에 선택된 RSS태그정보를 삭제한다.
등록 : 신규 RSS태그를 등록하기 위해서는 상단의 등록 버튼을 통해서 **RSS태그관리 등록** 화면으로 이동한다.
목록 대상서비스명/대상테이블명 클릭 :  **RSS태그관리 상세조회** 화면으로 이동한다.
----
#### RSS태그관리 상세조회
| Action | URL | Controller method | QueryID |
| --- | --- | --- | --- |
| 상세조회 | /uss/ion/rss/detailRssTagManage.do | EgovRssTagManageDetail | "RssTagManage.selectRssTagManageDetail" |
| 삭제 | /uss/ion/rss/detailRssTagManage.do | EgovRssTagManageDetail | "RssTagManage.deleteRssTagManage" |

[RSS태그관리 목록조회]에서 선택한 RSS태그관리 정보의 상세조회를 제공합니다.

[이미지]

수정 : RSS태그관리 수정 화면으로 이동한다.
삭제 : 기 등록된  RSS태그 정보를 삭제한다.
목록 : RSS태그관리 목록조회 화면으로 이동한다.
----
#### RSS태그관리 등록
| Action | URL | Controller method | QueryID |
| --- | --- | --- | --- |
| 등록 | /uss/ion/rss/registRssTagManage.do | EgovRssTagManageRegist | "RssTagManage.insertRssTagManage" |

RSS태그관리 등록 화면을 제공합니다.
**대상테이블명**은 등록된 테이블 목록이 출력되어 사용자가 직접 선택할 수 있습니다.
**대상테이블명** 클릭시 해당 태이블 컬럼정보가 **컬럼**에 자동 출력 된다.
**본문**정보(본문TITLE,본문LINK, 본문DESCRIPTION) 입력시 컬럼추가 버튼을 이용하여 추가하거나 #컬럼명# 형태로 입력한다.
[이미지]

저장 : 신규로 작성된 RSS태그 정보를 저장한다.
목록 : RSS태그관리 목록조회 화면으로 이동한다.
----
#### RSS태그관리수정
| Action | URL | Controller method | QueryID |
| --- | --- | --- | --- |
| 수정 | /uss/ion/rss/updtRssTagManage.do | EgovRssTagManageModify | "RssTagManage.updateRssTagManage |

RSS태그관리 수정 화면을 제공합니다.
**대상테이블명**은 등록된 테이블 목록이 출력되어 사용자가 직접 선택할 수 있습니다.
**대상테이블명** 클릭시 해당 태이블 컬럼정보가 **컬럼**에 자동 출력 된다.
**본문**정보(본문TITLE,본문LINK, 본문DESCRIPTION) 입력시 컬럼추가 버튼을 이용하여 추가하거나 #컬럼명# 형태로 입력한다.
[이미지]

저장 : 수정된 RSS태그 정보를 저장한다.
목록 : RSS태그관리 목록조회 화면으로 이동한다.
----
