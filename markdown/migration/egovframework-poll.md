---
id: "egovframework-poll"
title: "온라인POLL참여"
version: "4.3"
category: "common"
source: "eGovFrame Wiki"
source_url: "https://www.egovframe.go.kr/wiki/doku.php?id=egovframework%3A%EC%98%A8%EB%9D%BC%EC%9D%B8poll%EC%B0%B8%EC%97%AC"
format: "markdown"
---

# 사용자지원 - 온라인POLL참여
## 개요
사이트에서 빈번하게 일어나는 간단한 설문 조사에 참여토록 하게 하기 위한 컴포넌트로서 온라인POLL참여자(기업회원, 일반회원)가 투표 및 통계를 확인 할수 있는 기능을 제공한다.
## 설명
온라인POLL참여기능은 크게**온라인POLL참여 목록조회**, **온라인POLL참여 등록**, **온라인POLL참여 통계** 기능으로 구성되어 있다.(관련기능 부분참조)
##### 온라인POLL 콤포넌트 구성도
[이미지: 온라인poll컴포넌트 구성도]
##### 온라인POLL 기능 흐름도
[이미지: 온라인poll참여 기능흐름도]
##### 클래스 다이어그램
[이미지: 온라인poll참여 다이어그램]
##### 관련소스
| 유형 | 대상소스명 | 비고 |
| --- | --- | --- |
| Controller | egovframework.com.uss.olp.opp.web.EgovOnlinePollPartcptnController.java | 온라인POLL참여 Controller Class |
| Service | egovframework.com.uss.olp.opp.service.EgovOnlinePollPartcptnService.java | 온라인POLL참여 Service Class |
| VO | egovframework.com.uss.olp.opp.service.OnlinePollPartcptn.java | 온라인POLL참여  VO Class |
| VO | egovframework.com.uss.olp.opp.service.OnlinePollItem.java | 온라인POLL항목  VO Class |
| VO | egovframework.com.cmm.ComDefaultVO.java | 검색 VO Class |
| ServiceImpl | egovframework.com.uss.olp.opp.service.impl.EgovOnlinePollPartcptnServiceImpl.java | 온라인POLL참여 ServiceImpl Class |
| DAO | egovframework.com.uss.olp.opp.service.impl.OnlinePollPartcptnDao.java | 온라인POLL참여 Dao Class |
| JSP | /WEB-INF/jsp/egovframework/uss/olp/opp/EgovOnlinePollPartcptnList.jsp | 온라인POLL참여 목록조회 페이지 |
| JSP | /WEB-INF/jsp/egovframework/uss/olp/opp/EgovOnlinePollPartcptnRegist.jsp | 온라인POLL참여 등록 페이지 |
| JSP | /WEB-INF/jsp/egovframework/uss/olp/opp/EgovOnlinePollPartcptnStatistics.jsp | 온라인POLL참여 통계 페이지 |
| QUERY XML | /egovframework/sqlmap/com/uss/olp/opp/EgovOnlinePollPartcptn.xml | 온라인POLL참여 QUERY XML |
| Validator Rule XML | resources/egovframework/validator/validator-rules.xml | Validator Rule을 정의한 XML |
| Validator XML | resources/egovframework/validator/com/uss/olp/opp/EgovOnlinePollPartcptn.xml | 온라인POLL참여 Validator XML |
| Message properties | resources/egovframework/message/message-common_ko_KR.properties | 온라인POLL참여 Message properties |
| Idgen XML | resources/egovframework/spring/context-idgen.xml | 온라인POLL참여 Id생성 Idgen XML |
##### ID Generation
- ID Generation Service를 활용하기 위해서 Sequence 저장테이블인  COMTECOPSEQ에 SCHDUL_ID 항목을 추가해야 한다.
 ```sql
CREATE TABLE COMTECOPSEQ ( table_name varchar(16) NOT NULL,
  		   next_id DECIMAL(30) NOT NULL,
  		   PRIMARY KEY (table_name));
  INSERT INTO COMTECOPSEQ VALUES('POLL_MGR_ID','0');

  CREATE TABLE COMTECOPSEQ ( table_name varchar(16) NOT NULL,
  		   next_id DECIMAL(30) NOT NULL,
  		   PRIMARY KEY (table_name));
  INSERT INTO COMTECOPSEQ VALUES('POLL_IEM_ID','0');

  CREATE TABLE COMTECOPSEQ ( table_name varchar(16) NOT NULL,
  		   next_id DECIMAL(30) NOT NULL,
  		   PRIMARY KEY (table_name));
  INSERT INTO COMTECOPSEQ VALUES('POLL_RUT_ID','0');
 ```
##### 관련테이블
| 테이블명 | 테이블명(영문) | 비고 |
| --- | --- | --- |
| 온라인POLL관리 | COMTNOnlinePollPartcptn | 온라인POLL을 관리 한다. |
| 온라인POLL항목 | COMTNONLINEPOLLITEM | 온라인POLL항목을 관리 한다. |
| 온라인POLL결과 | COMTNONLINEPOLLRESULT | 온라인POLL결과를 관리 한다. |
##### 관련코드
| 코드분류 | 코드분류명 | 코드ID | 코드명 |
| --- | --- | --- | --- |
| COM039 | 온라인POLL구분 | 001 | 사회 |
| COM039 | 온라인POLL구분 | 002 | 정치 |
| COM039 | 온라인POLL구분 | 003 | 경제 |
| COM039 | 온라인POLL구분 | 004 | 문화 |
| COM039 | 온라인POLL구분 | 005 | 인문 |
| COM039 | 온라인POLL구분 | 006 | 공학 |
| COM039 | 온라인POLL구분 | 007 | 기타 |
## 관련기능
온라인POLL참여기능은 크게 **온라인POLL참여 목록조회**, **온라인POLL참여 등록**, **온라인POLL참여 통계**  기능으로 구성되어 있다.
### 온라인POLL참여 목록조회
#### 비즈니스 규칙
사이트 회원이 기(記) 등록된 온라인POLL참여 정보를 리스트 형태로 조회 할 수 있고, 등록버튼을 클릭하여 등록화면으로 이동할수있다.
#### 관련코드
N/A
#### 관련화면 및 수행뉴메얼
| Action | URL | Controller method | QueryID |
| --- | --- | --- | --- |
| 등록 | /uss/olp/opp/registOnlinePollPartcptn.do | EgovOnlinePollPartcptnRegist | OnlinePollPartcptn.selectOnlinePollManage |
| 통계 | /uss/olp/opp/statisticsOnlinePollPartcptn.do | EgovOnlinePollManageStatistics | OnlinePollPartcptn.selectOnlinePollManageDetail,OnlinePollPartcptn.selectOnlinePollItem |

[이미지: 온라인poll참여 목록]


등록 클릭: 등록하기 위해서는 상단의 등록 버튼을 통해서 **온라인POLL참여 등록** 화면으로 이동한다.
목록 클릭: **온라인POLL참여 상세조회** 화면으로 이동한다.

----
### 온라인POLL참여 등록
#### 비즈니스 규칙
- 항목명은 필수로 입력한다.
- 저장처리 시 SCHDUL_ID 컬럼은 "egovframework.rte.fdl.idgnr.impl.EgovTableIdGnrService"를 통하여 Primary Key => POLLRUT_(포함 20자리) : SCHDUL_(7자리) + 일련번호(13자리)로 자동생성 부여된다.
	<!-- IdGnrService... START-->
	<bean name="egovOnlinePollResultIdGnrService"
		class="egovframework.rte.fdl.idgnr.impl.EgovTableIdGnrService"
		destroy-method="destroy">
		<property name="dataSource" ref="dataSource" />
		<property name="strategy" ref="onlinePollResultMsgtrategy" />
		<property name="blockSize" 	value="1"/>
		<property name="table"	   	value="COMTECOPSEQ"/>
		<property name="tableName"	value="POLL_RUT_ID"/>
	</bean>
	<bean name="onlinePollResultMsgtrategy"
		class="egovframework.rte.fdl.idgnr.impl.strategy.EgovIdGnrStrategyImpl">
		<property name="prefix" value="POLLRUT_" />
		<property name="cipers" value="12" />
		<property name="fillChar" value="0" />
	</bean>
	<!-- IdGnrService... END-->
#### 관련코드
N/A
#### 관련화면 및 수행메뉴얼
| Action | URL | Controller method | QueryID |
| --- | --- | --- | --- |
| 등록 | /uss/olp/opp/registOnlinePollPartcptn.do | EgovOnlinePollPartcptnRegist | OnlinePollPartcptn.insertOnlinePollPartcptn |
| 목록 | /uss/olp/opp/listOnlinePollPartcptn.do | EgovOnlinePollPartcptnList | OnlinePollPartcptn.selectOnlinePollPartcptn |

온라인POLL참여에 관한 정보를 입력 저장처리한다.

[이미지: 온라인poll참여 등록]

저장: 입력한 온라인POLL참여 정보들이 저장 처리된다.
목록: **온라인POLL참여 목록** 화면으로 이동한다.
----
### 온라인POLL참여 통계
#### 비즈니스 규칙
- 온라인POLL관리 별 온라인POLL항목을 그래프 형태로 건수로 표시한다.
#### 관련코드
N/A
#### 관련화면 및 수행메뉴얼
| Action | URL | Controller method | QueryID |
| --- | --- | --- | --- |
| 목록 | /uss/olp/opp/listOnlinePollPartcptn.do | EgovOnlinePollPartcptnList | OnlinePollPartcptn.selectOnlinePollPartcptn |


온라인POLL관리 별 온라인POLL항목을 그래프 형태로 건수로 표시한다.

[이미지: 온라인poll참여 통계]

목록: **온라인POLL참여 목록** 화면으로 이동한다.
----
## 참고자료
- 실행환경 참조 : ID Generation Service
- 배포 및 테스트 관련 : Common Component System 및 배포 패키지 구성안
