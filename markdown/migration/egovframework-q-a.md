---
id: "egovframework-q-a"
title: "Q&A관리"
version: "4.3"
category: "common"
source: "eGovFrame Wiki"
source_url: "https://www.egovframe.go.kr/wiki/doku.php?id=egovframework%3Aq_a%EA%B4%80%EB%A6%AC"
format: "markdown"
---

# 공통서비스 - Q&A관리
## 개요
Q&A 내역 및 조치처리 관리기능으로 일반사용자가 Q&A내역을 등록하는 기능 및 관리자가 답변글을 등록하는 기능으로 구성되어 있다
## 설명
Q&A관리기능은 크게 일반사용자가 사용하는 **Q&A목록조회**, **Q&A상세조회**, **Q&A내역등록**, **Q&A내역수정** 기능 및 관리자가
사용하는 **Q&A답변목록조회**, **Q&A답변상세조회**, **Q&A내역답변등록**, **Q&A내역답변수정** 기능으로 분류된다.
##### 관련소스
| 유형 | 대상소스명 | 비고 |
| --- | --- | --- |
| Controller | egovframework.com.uss.olh.qna.web.EgovQnaManageController.java | Q&A관리를 위한 컨트롤러 클래스 |
| Service | egovframework.com.uss.olh.qna.service.EgovQnaManageService.java | Q&A관리를 위한 서비스 인터페이스 |
| ServiceImpl | egovframework.com.uss.olh.qna.service.impl.EgovQnaManageServiceImpl.java | Q&A관리를 위한 서비스 구현 클래스 |
| VO | egovframework.com.uss.olh.qna.service.QnaManageVO.java | Q&A관리를 위한 VO 클래스 |
|  | egovframework.com.uss.olh.qna.service.QnaManageDefaultVO.java | Q&A관리를 위한 SearchVO 클래스 |
| DAO | egovframework.com.uss.olh.qna.service.imp.QnaManageDAO.java | Q&A 관리를 위한 데이터처리 클래스 |
| JSP | /WEB-INF/jsp/egovframework/uss/olh/qna/EgovQnaListInqire.jsp | Q&A관리를 위한 목록조회 페이지 |
|  | /WEB-INF/jsp/egovframework/uss/olh/qna/EgovQnaDetailInqire.jsp | Q&A관리를 위한 상세조회 페이지 |
|  | /WEB-INF/jsp/egovframework/uss/olh/qna/EgovQnaCnRegist.jsp | Q&A관리를 위한 등록 페이지 |
|  | /WEB-INF/jsp/egovframework/uss/olh/qna/EgovQnaCnUpdt.jsp | Q&A관리를 위한 수정 페이지 |
| JSP | /WEB-INF/jsp/egovframework/uss/olh/qna/EgovQnaAnswerListInqire.jsp | Q&A관리를 위한 답변목록조회 페이지 |
|  | /WEB-INF/jsp/egovframework/uss/olh/qna/EgovQnaAnswerDetailInqire.jsp | Q&A관리를 위한 답변상세조회 페이지 |
|  | /WEB-INF/jsp/egovframework/uss/olh/qna/EgovQnaCnAnswerRegist.jsp | Q&A관리를 위한 답변등록 페이지 |
|  | /WEB-INF/jsp/egovframework/uss/olh/qna/EgovQnaCnAnswerUpdt.jsp | Q&A관리를 위한 답변수정 페이지 |
| Query XML | resources/egovframework/sqlmap/com/uss/olh/qna/EgovQnaManage_SQL.xml | Q&A관리(조회,등록,수정,삭제)를 위한 Query XML |
| Validator Rule XML | resources/egovframework/validator/validator-rules.xml | Validator Rule을 정의한 XML |
| Validator XML | resources/egovframework/validator/com/uss/olh/qna/EgovQnaManage_SQL.xml | Q&A관리를 위한 Validator XML |
| Message properties | resources/egovframework/message/message-common_ko_KR.properties | Q&A관리를 위한 Message properties |
| Idgen XML | resources/egovframework/spring/context-idgen.xml | Q&A등록을 위한 Id생성 Idgen XML |

**클래스다이어그램**

[이미지]
##### 관련테이블
| 테이블명 | 테이블명(영문) | 비고 |
| --- | --- | --- |
| QA정보 | COMTNQAINFO | 질문과 답변을 관리 |
## 관련기능
Q&A관리기능은 크게 일반사용자가 사용하는 **Q&A목록조회**, **Q&A상세조회**, **Q&A내용등록**, **Q&A내용수정** 기능 및 관리자가
사용하는 **Q&A답변목록조회**, **Q&A답변상세조회**, **Q&A내용답변등록**, **Q&A내용답변수정** 기능으로 분류된다.
### Q&A목록조회
#### 비즈니스 규칙
조회조건으로 목록조회를 할 수 있고, 등록버튼을 클릭하여 Q&A등록 화면으로 이동하여 Q&A를 등록 처리 할 수 있다.
#### 관련코드
N/A
#### 관련화면 및 수행매뉴얼
| Action | URL | Controller method | QueryID |
| --- | --- | --- | --- |
| 조회 | /uss/olh/qna/QnaListInqire.do | selectQnaList | "QnaManageDAO.selectQnaList" |
|  | /uss/olh/qna/QnaListInqire.do | selectQnaListTotCnt | "QnaManageDAO.selectQnaListTotCnt" |
| 등록 | /uss/olh/qna/QnaCnRegistView.do | insertQnaCnView |
|  | /uss/olh/qna/QnaCnRegist.do | insertQnaCn | "QnaManageDAO.insertQnaCn" |
| 목록클릭 | /uss/olh/qna/QnaDetailInqire.do | selectQnaListDetail | "QnaManageDAO.selectQnaListDetail" |

Q&A 목록은 페이지 당 10건씩 조회되며 페이징은 10페이지씩 이루어진다.
검색조건은 작성자명, Q&A제목에 대해서 수행된다. 페이지 당 검색 범위를 변경하고자 하는 경우
context-properties.xml 파일의 pageUnit, pageSize를 변경한다.(단 해당 설정은 전체 공통서비스 기능에 영향을 미친다.)

[이미지]

등록버튼 클릭 시 로그인 하지 않은 경우에는 로그인이나 실명확인 선택화면이 활성화 된다.

[이미지]

로그인선택시 아래와 같이 화면이 활성화 된다.

[이미지]

실명확인 선택 시 아래와 같은 화면이 활성화 된다

[이미지]


조회: Q&A를 조회하기 위해서는 상단의 검색조건을 선택 후 해당하는 검색문자를 입력 후 조회 버튼을 클릭한다.
등록: Q&A를 등록하기 위해서는 상단의 등록 버튼을 통해서 **Q&A등록** 화면으로 이동한다.
목록클릭: **Q&A상세조회** 화면으로 이동한다.
----
### Q&A상세조회
#### 비즈니스 규칙
Q&A목록조회에서 목록 클릭 시 이동되는 화면으로 Q&A에 대한 상세정보를 보여준다.
#### 관련코드
 N/A
#### 관련화면 및 수행매뉴얼
| Action | URL | Controller method | QueryID |
| --- | --- | --- | --- |
| 수정 | /uss/olh/qna/QnaCnUpdtView.do | updateQnaCnView |
| 삭제 | /uss/olh/qna/QnaCnDelete.do | deleteQnaCn | "QnaManageDAO.deleteQnaCn" |
| 목록 | /uss/olh/qna/QnaListInqire.do | selectQnaList | "QnaManageDAO.selectQnaList" |

Q&A 상세조회화면은 Q&A내역수정, Q&A내역삭제, Q&A목록조회를 할 수 있다.

[이미지]

수정 및 삭제 버튼 클릭 시 작성 비밀번호를 확인 후 Q&A 글을 수정 및 삭제 할 수 있도록 구성되어 있다.

[이미지]

수정: 수정버튼 클릭 시 Q&A를 수정할 수 있는 화면으로 이동한다.
삭제: 삭제버튼 클릭 시 삭제여부를 확인하는 메세지를 보여주고 삭제처리를 할 수 있다.
목록: **Q&A목록조회** 화면으로 이동한다.
----
### Q&A내역등록
#### 비즈니스 규칙
- 입력명 우측의 빨간* 표시는 반드시 입력해야할 항목을 표시한다.
- 저장처리 시 QA_ID 컬럼은 "egovframework.rte.fdl.idgnr.impl.EgovTableIdGnrService"를 통하여
  Primary Key => QA_ID(20자리) : QA__(3자리) + 일련번호(17자리)로 자동생성 부여된다.

	<bean name="egovQnaManageIdGnrService"
		class="egovframework.rte.fdl.idgnr.impl.EgovTableIdGnrService"
		destroy-method="destroy">
		<property name="dataSource" ref="dataSource" />
		<property name="strategy"   ref="qnaManageStrategy" />
		<property name="blockSize" 	value="10"/>
		<property name="table"	   	value="COMTECOPSEQ"/>
		<property name="tableName"	value="QA_ID"/>
	</bean>

	<bean name="qnaManageStrategy"
		class="egovframework.rte.fdl.idgnr.impl.strategy.EgovIdGnrStrategyImpl">
		<property name="prefix" value="QA_" />
		<property name="cipers" value="17" />
		<property name="fillChar" value="0" />
	</bean>
#### 관련코드
 N/A
#### 관련화면 및 수행매뉴얼
| Action | URL | Controller method | QueryID |
| --- | --- | --- | --- |
| 목록 | /uss/olh/qna/QnaListInqire.do | selectQnaList | "QnaManageDAO.selectQnaList" |
| 저장 | /uss/olh/qna/QnaCnRegist.do | insertQnaCn | "QnaManageDAO.insertQnaCn" |

Q&A에 관한 기본정보를 입력 저장처리한다.

[이미지]


목록: **Q&A목록조회** 화면으로 이동한다.
저장: 입력한 Q&A정보들이 저장 처리된다.
----
### Q&A내역수정
#### 비즈니스 규칙
- 입력명 우측의 빨간* 표시는 수정 시 반드시 입력해야 할 항목을 표시한다.
#### 관련코드
 N/A
#### 관련화면 및 수행매뉴얼
| Action | URL | Controller method | QueryID |
| --- | --- | --- | --- |
| 수정 | /uss/olh/qna/QnaCnUpdt.do | updateQnaCn | "QnaManageDAO.updateQnaCn" |
| 목록 | /uss/olh/qna/QnaListInqire.do | selectQnaList | "QnaManageDAO.selectQnaList" |

입력한 Q&A정보들을 저장 처리한다.

[이미지]


수정: 수정 입력한 Q&A정보들이 저장 처리된다.
목록: **Q&A목록조회** 화면으로 이동한다.
----
### Q&A답변목록조회
#### 비즈니스 규칙
관리자가 답변글을 관리하기 위한 기능으로 조회조건으로 목록조회를 할 수 있고, 등록버튼을 클릭하여 Q&A등록 화면으로 이동하여 Q&A를
등록 처리 할 수 있다.
#### 관련코드
N/A
#### 관련화면 및 수행매뉴얼
| Action | URL | Controller method | QueryID |
| --- | --- | --- | --- |
| 조회 | /uss/olh/qna/QnaAnswerListInqire.do | selectQnaAnswerList | "QnaManageDAO.selectQnaAnswerList" |
|  | /uss/olh/qna/QnaAnswerListInqire.do | selectQnaAnswerListTotCnt | "QnaManageDAO.selectQnaAnswerListTotCnt" |
| 목록클릭 | /uss/olh/qna/QnaAnswerDetailInqire.do | selectQnaAnswerListDetail | "QnaManageDAO.selectQnaAnswerDetail" |

Q&A 목록은 페이지 당 10건씩 조회되며 페이징은 10페이지씩 이루어진다.
검색조건은 작성자명, 진행상태에 대해서 수행된다. 페이지 당 검색 범위를 변경하고자 하는 경우
context-properties.xml 파일의 pageUnit, pageSize를 변경한다.(단 해당 설정은 전체 공통서비스 기능에 영향을 미친다.)

[이미지]

조회: Q&A를 조회하기 위해서는 상단의 검색조건을 선택 후 해당하는 검색문자를 입력 후 조회 버튼을 클릭한다.
목록클릭: **Q&A상세조회** 화면으로 이동한다.
----
### Q&A답변상세조회
#### 비즈니스 규칙
관리자가 작성자정보 및 답변내용상세정보를 보여준다.
#### 관련코드
 N/A
#### 관련화면 및 수행매뉴얼
| Action | URL | Controller method | QueryID |
| --- | --- | --- | --- |
| 수정 | /uss/olh/qna/QnaCnAnswerUpdtView.do | updateQnaCnAnswerView |
| 목록 | /uss/olh/qna/QnaAnswerListInqire.do | selectQnaAnswerList | "QnaManageDAO.selectQnaAnswerList" |

Q&A답변상세조회화면은 Q&A내용답변수정, Q&A답변목록조회를 할 수 있다.

[이미지]


수정: 수정버튼 클릭 시 Q&A를 수정할 수 있는 화면으로 이동한다.
삭제: 삭제버튼 클릭 시 삭제여부를 확인하는 메세지를 보여주고 삭제처리를 할 수 있다.
목록: **Q&A답변목록조회** 화면으로 이동한다.
----
### Q&A내역답변수정
#### 비즈니스 규칙
- 작성자 정보는 참고만 할 수 있고, 하단의 답변내용만 입력 가능하도록 구성되어 있습니다.
#### 관련코드
Q&A관리에서 사용되는 코드 및 그에 따른 설정 값의 반영사항은 다음과 같다.

| 코드분류 | 코드분류명 | 코드ID | 코드명 |
| --- | --- | --- | --- |
| COM028 | 질의응답처리상태 | 1 | 접수대기 |
| COM028 | 질의응답처리상태 | 2 | 접수 |
| COM028 | 질의응답처리상태 | 3 | 완료 |

- 질의응답처리상태코드를 추가하여 사용 할 수 있다.
#### 관련화면 및 수행매뉴얼
| Action | URL | Controller method | QueryID |
| --- | --- | --- | --- |
| 수정 | /uss/olp/cnm/QnaCnAnswerUpdt.do | updateQnaCnAnswer | "QnaManageDAO.updateQnaCnAnswer" |
| 목록 | /uss/olp/cnm/QnaAnswerListInqire.do | selectQnaAnswerList | "QnaManageDAO.selectQnaAnswerList" |

입력한 Q&A정보들을 저장 처리한다.

[이미지]


수정: 수정 입력한 Q&A정보들이 저장 처리된다.
목록: **Q&A목록조회** 화면으로 이동한다.
----
## 참고자료
N/A
