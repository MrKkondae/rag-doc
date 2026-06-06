---
id: "egovframework-dev-imp-codegen-model"
title: "모델 기반 Code Gen."
version: "4.3"
category: "development"
source: "eGovFrame Wiki"
source_url: "https://www.egovframe.go.kr/wiki/doku.php?id=egovframework%3Adev%3Aimp%3Acodegen%3Amodel"
format: "markdown"
---

# 모델 기반 Code Gen.
## 개요
분석/설계 단계의 개념 모델을 UML 2.0의 Execute Model 기법을 통해 소스 코드로 변환 생성하는 기능으로 구현도구의 UML Editor를 통해 Class Diagram을 설계하고 이를 Code Gen. 기능을 통해 eGovFrame 실행 환경 기반 소스코드를 생성한다.
eGovFramework 의 개발환경의 구현도구에서는 다음과 같은 모델 기반 Code Generation 기능을 제공한다.
## 설명
타 UML 모델링 툴에서 제공하는 Code Generation 기능에 비하여 다음과 같은 특장점을 갖는다. - 전자정부 프레임워크 Based Code Generaion 기능
- Spring Annotation 자동생성 : Model, Service, ServiceImpl, Controller, Vo, Dao 등의 스테레오 타입을 지원하여 모델간 관계에 따른 Spring Annotation 을 자동생성
| StereoType | 내용 |
| Model | attribute 정보로 자동으로 getter, setter 메소드 생성 |
| Service | Realization 관계에 있는 ServiceImpl 이 있을 때 사용 |
| ServiceImpl | eGovFramework 기본 import 구문 생성, Relation 으로 연결된 Service, Dao 에 대한 @Service, @Resource 자동 생성 |
| Dao | eGovFramework 기본 import 구문 생성, @Repository Annotation 추가 |
| Controller | @Controller Annotation 추가 |
| Vo | attribute 정보로 자동으로 getter, setter 메소드 생성 |
- 타 UML 모델링 도구에서 작성한 XMI에 대한 호환성 제공. (UML 2.1, XMI 2.1 버전에 한함)
- UML 2.1  http://www.omg.org/technology/documents/modeling_spec_catalog.htm#UML
- XMI 2.1  http://www.omg.org/technology/documents/modeling_spec_catalog.htm#XMI
## 사용법
- 구현도구의 UML 클래스 다이어그램을 사용한 코드 자동 생성
- XMI 파일을 이용한 코드 자동 생성
- 구현도구의 UML 클래스 다이어그램을 XMI 파일로 Export하는 기능
