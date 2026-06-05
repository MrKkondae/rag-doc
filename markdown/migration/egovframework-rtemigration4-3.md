---
id: "egovframework-rtemigration4-3"
title: "실행환경 업그레이드 가이드 4.2 to 4.3"
version: "4.3"
category: "migration"
source: "eGovFrame Wiki"
source_url: "https://www.egovframe.go.kr/wiki/doku.php?id=egovframework%3Artemigration4.3"
format: "markdown"
---

# 실행환경 Migration 가이드 (4.2 -> 4.3)
표준프레임워크 4.3은 Spring Framework 5.3.37 버전을 지원가능하게 업그레이드를 진행하였으나,
전체 오픈소스SW 업그레이드에 따라 일부 변경이 필요합니다. 또한, 각 프로젝트의 상황 및 환경에 따라서 버전 업그레이드에 따른
충돌, 버그, 불안정성이 발생할 수도 있으니 충분한 테스트 후 진행하시기 바랍니다.
## 업그레이드 개요
표준프레임워크 4.3는 JDK 1.8, Servlet 3.1이 필요합니다.
이에 따라 우선 관련된 WAS 등 적용되어 있는 SW 등이 JDK 1.8, Servlet 3.1를 지원하는지 확인하고 필요 시 업그레이드를 수행하십시오.
## 업그레이드 방법
### 1. 실행환경 library 변경
#### 1-1. Maven을 사용하는 경우
Maven을 사용하는 경우 프로젝트에서 사용하는 pom.xml 파일을 수정하여 업그레이드를 진행할 수 있습니다.
기본적으로 표준프레임워크 실행환경에서 사용되는 오픈소스 라이브러리들만을 업그레이드 하고자 하는 경우
pom.xml 파일에서 패키지명을 org.egorframe.rte로 변경하고 버전은 4.3.0으로 업그레이드 하기 바랍니다.

변경 전 (예)
```xml
<dependency>
     <groupId>org.egovframe.rte</groupId>
     <artifactId>org.egovframe.rte.psl.dataaccess</artifactId>
     <version>4.2.0</version>
</dependency>
```

변경 후 (예)
```xml
<dependency>
     <groupId>org.egovframe.rte</groupId>
     <artifactId>org.egovframe.rte.psl.dataaccess</artifactId>
     <version>4.3.0</version>
</dependency>
```

만약 표준프레임워크의 버전을 property를 사용하여 일괄적으로 관리하는 경우 property에서 변경합니다.
property의 이름은 프로젝트에 따라 다를 수 있습니다.

변경 전 (예)
```xml
<properties>
     <spring.maven.artifact.version>5.3.27</spring.maven.artifact.version>
     <org.egovframe.rte.version>4.2.0</org.egovframe.rte.version>
</properties>
```

변경 후 (예)
```xml
<properties>
     <spring.maven.artifact.version>5.3.37</spring.maven.artifact.version>
     <org.egovframe.rte.version>4.3.0</org.egovframe.rte.version>
</properties>
```

또한 표준프레임워크 Maven Reposieoty를 HTTP를 사용한 설정에서 HTTPS를 사용하는 설정을 변경하시기 바랍니다.
변경 전
```xml
http://maven.egovframe.go.kr/maven/
http://maven.egovframe.kr:8080/maven/
http://www.egovframe.go.kr/maven/
```

변경 후
```xml
https://maven.egovframe.go.kr/maven/
```
#### 1-2. 실행환경 패키지명 변경
표준프레임워크 4.0.x 버전부터 실행환경의 패키지명을 org.egovframe.rte로 변경하였으므로, 실행환경을 import한 소스에 변경된 패키지명을 사용하시기 바랍니다.
표준프레임워크 개발환경에서 Search 기능에서 기존의 패키지명인 egovframework.rte 로 검색한 후,
변경할 패키지명인 org.egovframe.rte로 일괄로 변경하여 사용할 수 있습니다.

[이미지]
#### 1-3. context-common.xml 설정 변경
context-common.xml 파일의 다국어처리를 위한 Bean 설정에 실행환경의 ID Generation, Property 라이브러리 경로 설정을 패키지명 변경에 맞춰 수정하시기 바랍니다.
변경 전
```xml
<list>
	<value>classpath*:egovframework/message/com/**/*</value>
	<value>classpath:/egovframework/rte/fdl/idgnr/messages/idgnr</value>
	<value>classpath:/egovframework/rte/fdl/property/messages/properties</value>
	<value>classpath:/egovframework/egovProps/globals</value>
</list>
```

변경 후
```xml
<list>
	<value>classpath*:egovframework/message/com/**/*</value>
	<value>classpath:/org/egovframe/rte/fdl/idgnr/messages/idgnr</value>
	<value>classpath:/org/egovframe/rte/fdl/property/messages/properties</value>
	<value>classpath:/egovframework/egovProps/globals</value>
</list>
```
#### = 2. 간소화 서비스 설정 변경
표준프레임워크에서 제공하는 간소화 서비스인 Spring Security 설정 간소화, Session 방식 접근제어, Crypto 간소화를 업그레이드 하시는 경우 변경된 내용을 확인하시기 바랍니다.
#### 2-1. Spring Security 설정 간소화 변경 사항
Spring Security 설정 간소화 변경 사항에 대한 상세한 내용은 다음을 참고하시기 바랍니다.

스키마정의(XSD) 파일명 변경 전
```xml
http://www.springframework.org/schema/security/spring-security.xsd
  http://maven.egovframe.go.kr/schema/egov-security/egov-security-4.2.0.xsd
```

스키마정의(XSD) 파일명 변경 후
```xml
http://www.springframework.org/schema/security/spring-security.xsd
  http://maven.egovframe.go.kr/schema/egov-security/egov-security-4.3.0.xsd
```
#### 2-2. Session 방식 접근제어 변경 사항
Session 방식 접근제어 변경 사항에 대한 상세한 내용은 다음을 참고하시기 바랍니다.

스키마정의(XSD) 파일명 변경 전
```xml
http://maven.egovframe.go.kr/schema/egov-access/egov-access-4.2.0.xsd
```

스키마정의(XSD) 파일명 변경 후
```xml
http://maven.egovframe.go.kr/schema/egov-access/egov-access-4.3.0.xsd
```
#### 2-3. Crypto 간소화 변경 사항
Crypto 간소화 변경 사항에 대한 상세한 내용은 다음을 참고하시기 바랍니다.

스키마정의(XSD) 파일명 변경 전
```xml
http://maven.egovframe.go.kr/schema/egov-crypto/egov-crypto-4.2.0.xsd
```

스키마정의(XSD) 파일명 변경 후
```xml
http://maven.egovframe.go.kr/schema/egov-crypto/egov-crypto-4.3.0.xsd
```

위 설정으로 4.2 버전에서 4.3 버전으로 변경하면 **StringEscapeUtils 클래스 초기화 오류가 발생**할 수 있습니다.
이럴 경우 해당 프로젝트의 pom.xml 파일에 commons-lang3 라이브러리가 정의되어 있다면
**commons-lang3 라이브러리를 제거**하거나 **commons-lang3 라이브러리 버전을 3.14.0으로 변경**하여 주시기 바랍니다.
### 3. Local Library 설정 변경
Maven Repository에 없는 로컬 jar 파일을 Maven 프로젝트에 추가하기 위해 <dependency> 의 <scope>, <systemPath> 노드 설정을 이용하여 프로젝트에 포함된 jar 파일을 지정하였으나,
Maven 빌드 시 해당 jar 파일이 포함되지 않기 때문에 Local Repository를 활용하는 방법을 사용한다.
WEB-INF/lib 아래에 포함된 jar 파일을 WEB-INF/lib/project 폴더를 구성하고 해당 폴더 아래에 [gropupId]/[artifaceId] 형식의 폴더를 구성하여 사용한다.

변경 전 (예)
```java
<dependency>
	<groupId>onepass-client</groupId>
	<artifactId>onepass-client</artifactId>
	<version>2.0.0</version>
	<scope>system</scope>
	<systemPath>${basedir}/src/main/webapp/WEB-INF/lib/onepass-client-2.0.0.jar</systemPath>
</dependency>
```

변경 후 (예)
```java
<repositories>
......
	<repository>
		<id>projectRepository</id>
		<name>Project Repository</name>
		<url>file://${project.basedir}/src/main/webapp/WEB-INF/lib</url>
	</repository>
</repositories>

......

<dependency>
	<groupId>project</groupId>
	<artifactId>onepass</artifactId>
	<version>2.0.0</version>
</dependency>
```
### 4. log4j 설정 추가
표준프레임워크 실행환경의 패키지명이 org.egovframe.rte로 변경됨에 따라 실행환경에서 발생하는 로그를 확인하기 위해
로깅 환경설정 파일인 log4j2.xml 파일에 다음과 같은 설정 추가가 필요합니다.

설정 추가 (예)
```java
<Logger name="egovframework" level="DEBUG" additivity="false">
        <AppenderRef ref="console" />
</Logger>
<Logger name="org.egovframe.rte" level="DEBUG" additivity="false">
        <AppenderRef ref="console" />
</Logger>
```
## 기타 알 수 없는 충돌이 발생하는 경우
프로젝트에 따라서 기존에 사용하던 라이브러리, 코드, WAS, DB 등과의 충돌이 발생할 수 있습니다.
알 수 없는 충돌이 발생하고 해결이 어려운 경우 표준프레임워크센터에 프로젝트의 환경 및 에러메시지를 포함하여 문의를 주시기 바랍니다.
