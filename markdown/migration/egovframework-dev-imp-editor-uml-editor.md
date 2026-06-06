---
id: "egovframework-dev-imp-editor-uml-editor"
title: "UML Editor"
version: "4.3"
category: "development"
source: "eGovFrame Wiki"
source_url: "https://www.egovframe.go.kr/wiki/doku.php?id=egovframework%3Adev%3Aimp%3Aeditor%3Auml_editor"
format: "markdown"
---

# UML Editor
## 개요
UML 작성도구로써 Activity Diagram, Class Diagram, Sequence Diagram, UseCase Diagram 작성이 가능하고 Class Diagram으로부터 정의된 클래스의 Java Code를 생성할 수 있는 기능을 제공한다.

타 UML 도구간의 호환은 Java Source Code를 통한 Class Diagram 소통이 전부 이지만(Source Code Import), 확장팩을 이용하여 더 많은 호환성을 가질 수 있다.
## 사용법
 eGovFramework 에서 제공하는 개발환경을 다운받으면 이미 설치되어 있으므로 별도로 설치하지 않아도 된다. 각각의 사용법은 다음과 같다.
- eGovframework:DEV:IMP:editor:UML Editor:Use Case Diagram Editor
- eGovframework:DEV:IMP:editor:UML Editor:Class Diagram Editor
- eGovframework:DEV:IMP:editor:UML Editor:Sequence Diagram Editor
- eGovframework:DEV:IMP:editor:UML Editor:Activity Diagram Editor
## 환경설정
- 기본설치
- AmaterasUML_xxx.zip 파일을 다운로드 한다. [ [다운로드](http://amateras.sourceforge.jp/cgi-bin/fswiki_en/wiki.cgi?page=AmaterasUML) ]
- 압축을 풀어 ECLIPSE_HOME/plugins 폴더에 복사한다.
- 확장 : XML import/export 기능을 제공하는 콤포넌트 이다. 이것은 EMF(Eclipse Modeling Framework) 와  UML2 설치가 선행되어야 한다.
- 먼저 EMF2.2.0 [ [다운로드](http://www.eclipse.org/modeling/emf/downloads/?project=emf) ]와 UML2 2.0.0 [ [다운로드](http://www.eclipse.org/modeling/mdt/downloads/?project=uml2-uml) ]를 설치한다.
- AmaterasUMLExtensionxxx.zip 파일을 다운로드 한다.
- 압축을 풀고 ECLIPSE_HOME/plugins 폴더에 복사한다.
## 참고자료(Optional)
[AmaterasUML](http://amateras.sourceforge.jp/cgi-bin/fswiki_en/wiki.cgi?page=AmaterasUML)
