---
id: "egovframework-let4-0-configration"
title: "경량환경 구성 및 환경설정"
version: "4.3"
category: "rte43"
source: "eGovFrame Wiki"
source_url: "https://www.egovframe.go.kr/wiki/doku.php?id=egovframework%3Alet4.0%3Aconfigration"
format: "markdown"
---

# 경량환경 템플릿 구성 및 환경설정(configration)
아래 설정 사항들은 엔터프라이즈 및 포털 사이트에 관련된 내용들이다.
  1. 템플릿 소스의 웹환경 관련 설정은 아래 3곳의 위치에 정의되어 사용된다.
- web.xml
- classpath*:egovframework/spring/com/context-*.xml
- /WEB-INF/config/egovframework/springmvc/*.xml
  2. 템플릿 소스의 DB관련 설정은 globlas.properties에 정의되어 사용된다.


심플 홈페이지는 아래 github 안내 페이지를 참고하도록 한다.
[심플홈페이지 BackEnd](https://github.com/eGovFramework/egovframe-template-simple-backend/blob/main/README.md)
[심플홈페이지 FrontEnd](https://github.com/eGovFramework/egovframe-template-simple-react/blob/main/README.md)
## web.xml 주요 설정
- *.do로 호출되는 경우 기본 화면에 출력되는 encoding은 utf-8로 필터링 되도록 설정하여 특수문자에 의한 크로스사이트 스크립트를 방지한다. HTMLTagFilter를 설정하면 파라미터로 전달되는 값 자체를 변환하는 방식의 사용도 가능하다. 템플릿 소스에서는 화면을 통해 입력하는 값을 변환하지 않고 출력하는 시점에 encoding처리하는 방식을 기본으로 사용한다.
```xml
<filter>
        <filter-name>encodingFilter</filter-name>
        <filter-class>org.springframework.web.filter.CharacterEncodingFilter</filter-class>
        <init-param>
            <param-name>encoding</param-name>
            <param-value>utf-8</param-value>
        </init-param>
    </filter>
    <filter-mapping>
        <filter-name>encodingFilter</filter-name>
        <url-pattern>*.do</url-pattern>
    </filter-mapping>

    <!-- 템플릿 소스에서는 아래의 필터사용 대신 JSP 출력시 <c:out> 태그를 사용하는 것을 기본정책으로 한다  -->
    <!-- org.egovframe.rte.ptl.mvc.filter.HTMLTagFilter egovframework.com.cmm.filter.HTMLTagFilter-->
    <!--
    <filter>
        <filter-name>HTMLTagFilter</filter-name>
        <filter-class>org.egovframe.rte.ptl.mvc.filter.HTMLTagFilter</filter-class>
    </filter>
    <filter-mapping>
        <filter-name>HTMLTagFilter</filter-name>
        <url-pattern>*.do</url-pattern>
    </filter-mapping>
    -->
```
- spring context관련 환경설정정보 파일 위치를 등록한다.
```xml
<context-param>
        <param-name>contextConfigLocation</param-name>
        <param-value>classpath*:egovframework/spring/com/context-*.xml</param-value>
    </context-param>
```
- spring mvc를 위한 Listener, DispatcherServlet설정과 mvc관련 관련 추가 환경설정정보 파일위치를 등록한다.
```xml
<listener>
        <listener-class>org.springframework.web.context.ContextLoaderListener</listener-class>
    </listener>

    <servlet>
        <servlet-name>action</servlet-name>
        <servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
        <init-param>
            <param-name>contextConfigLocation</param-name>
            <param-value>/WEB-INF/config/egovframework/springmvc/*.xml</param-value>
        </init-param>
        <load-on-startup>1</load-on-startup>
    </servlet>
    <servlet-mapping>
        <servlet-name>action</servlet-name>
        <url-pattern>*.do</url-pattern>
    </servlet-mapping>
```
- spring security 를 사용하는 경우 포함되는 설정(내부업무, 포털사이트 템플릿만 포함됨)
```xml
<filter>
        <filter-name>springSecurityFilterChain</filter-name>
        <filter-class>org.springframework.web.filter.DelegatingFilterProxy</filter-class>
    </filter>
    <filter-mapping>
        <filter-name>springSecurityFilterChain</filter-name>
        <url-pattern>/*</url-pattern>
    </filter-mapping>

    <listener>
        <listener-class>org.springframework.security.web.session.HttpSessionEventPublisher</listener-class>
    </listener>
```
## egovframework/spring/com/context-*.xml 주요 설정
   추가 설정 파일들은 템플릿 프로젝트 소스의 각 resource/egovframework/spring/com/폴더 아래에 위치한다.
   anontation, aop, schedule, validation, security, id-generation, mapper, transaction 관련 설정정보가 등록된다.(템플릿 종류별로 차이 있음)
- context-aspect.xml의 ExceptionTransfer 설정(템플릿 서비스 임플 클래스에서 발생하는 경우는 Exception에 대한 개별 로그를 출력)
```xml
<!-- 내부업무의 기능 작동과정에서 Exception 발생 시 후처리를 위한 AOP설정  -->
    <aop:config>
        <aop:pointcut id="serviceMethod" expression="execution(* egovframework.let..impl.*Impl.*(..)) or execution(* egovframework.com..impl.*Impl.*(..))" />

        <aop:aspect ref="exceptionTransfer">
            <aop:after-throwing throwing="exception" pointcut-ref="serviceMethod" method="transfer" />
        </aop:aspect>
    </aop:config>
    ...
```
- context-common.xml의 egovMessageSource 설정(프로퍼티 파일에 등록된 메시지 활용), leavaTrace 설정(Exception 발생 시 개별 Trace 출력)
```xml
<!-- 메시지소스 빈 설정 -->
    <bean id="egovMessageSource" class="egovframework.com.cmm.EgovMessageSource">
        <property name="reloadableResourceBundleMessageSource">
            <ref bean="messageSource" />
        </property>
    </bean>
    ...

    <!-- Exception 발생 시 후처리용 별도 작업을 위해 실행환경의 LeveaTrace를 활용하도록 설정 -->
    <bean id="leaveaTrace" class="org.egovframe.rte.fdl.cmmn.trace.LeaveaTrace">
        <property name="traceHandlerServices">
            <list>
                <ref bean="traceHandlerService" />
            </list>
        </property>
    </bean>
    ...

    <!-- 소스 내에서 egovMessageSource의 사용 예
        @Resource(name="egovMessageSource")
        EgovMessageSource egovMessageSource;
        String message = egovMessageSource.getMessage("fail.common.login");
    -->
    <!-- 소스 내에서 사용 예(템플릿에서는 특별한 후속 처리 없으므로 로그아웃 시에 샘플 소스만 적용함)
    @Resource(name="leaveaTrace")
    LeaveaTrace leaveaTrace;
    ...
    } catch (ArithmeticException athex) {
        // TraceHandler에서 메시지에 따른 후속조치 등을 처리할 수 있다.
        leaveaTrace.trace("fail.common.msg", this.getClass());
    }
    ...
    -->
```
- context-datasource.xml의 datasource 설정
```xml
<!-- 환경설정 기본정보를 globals.properties 에서 참조하도록 propertyConfigurer 설정  -->
    <bean id="propertyConfigurer"
        class="org.springframework.beans.factory.config.PropertyPlaceholderConfigurer">
        <property name="locations">
            <list>
                <value>classpath:/egovframework/egovProps/globals.properties</value>
                <!-- value>file:/product/jeus/egovProps/globals.properties</value-->
            </list>
        </property>
    </bean>

    <!-- datasource 설정(propertyConfigurer 활용) -->
    <alias name="dataSource-${Globals.DbType}" alias="dataSource" />
    <alias name="dataSource-${Globals.DbType}" alias="egov.dataSource" />

    <!-- mysql -->
    <bean id="dataSource-mysql" class="org.apache.commons.dbcp2.BasicDataSource" destroy-method="close">
        <property name="driverClassName" value="${Globals.DriverClassName}"/>
        <property name="url" value="${Globals.Url}" />
        <property name="username" value="${Globals.UserName}"/>
        <property name="password" value="${Globals.Password}"/>
    </bean>
    ...

    <!-- DB 5개 종류에 대한 정의 샘플이 존재한다. -->
    <!-- 홈페이지 템플릿 globals.properties의 dbtype을 hsql로 변경후 아래 설정을 사용하여 간단한 테스트가 가능하다. -->
    <bean id="dataSource-hsql" class="org.apache.commons.dbcp2.BasicDataSource" destroy-method="close">
	<property name="driverClassName" value="net.sf.log4jdbc.DriverSpy"/>
	<property name="url" value="jdbc:log4jdbc:hsqldb:hsql://localhost/sampledb"/>
	<property name="username" value="sa"/>
    </bean>
```
- context-idgen.xml의 업무 별 일련번호 생성 서비스 설정
```xml
<!-- 시스템에서 업무 별로 레코드 신규발생 시 일련번호를 생성하는 bean 클래스 설정 -->
    <!-- 첨부파일 ID Generation  Config-->
    <bean name="egovFileIdGnrService"
        class="org.egovframe.rte.fdl.idgnr.impl.EgovTableIdGnrServiceImpl"
        destroy-method="destroy">
        <property name="dataSource" ref="dataSource-${Globals.DbType}" />
        <property name="strategy" ref="fileStrategy" />
        <property name="blockSize"  value="10"/>
        <property name="table"      value="IDS"/>
        <property name="tableName"  value="FILE_ID"/>
    </bean>
    <!-- 첨부파일 ID Generation  Strategy Config -->
    <bean name="fileStrategy"
        class="org.egovframe.rte.fdl.idgnr.impl.strategy.EgovIdGnrStrategyImpl">
        <property name="prefix" value="FILE_" />
        <property name="cipers" value="15" />
        <property name="fillChar" value="0" />
    </bean>
    ...

    <!-- 소스 내 사용 예
       ...
    @Resource(name = "egovFileIdGnrService")
    private EgovIdGnrService idgenService;
    ...
    String newId = idgenService.getNextStringId();
    ...
    -->
```
- context-properties.xml의 프로퍼티 값 설정
```xml
<!-- 프로퍼티 정보 설정 -->
    <bean name="propertiesService" class="org.egovframe.rte.fdl.property.impl.EgovPropertyServiceImpl" destroy-method="destroy">
        <property name="properties">
            <map>
                <entry key="pageUnit" value="10"/>
                <entry key="pageSize" value="10"/>
                <entry key="posblAtchFileSize" value="5242880"/>
                <entry key="Globals.fileStorePath" value="/user/file/sht/"/>
                <entry key="Globals.addedOptions" value="false"/>
            </map>
        </property>
    </bean>

    <!-- 소스 내 사용 예
    @Resource(name = "propertiesService")
    protected EgovPropertyService pService;
    ...
    String savePath = pService.getString("Globals.fileStorePath");
    ...
    -->
```
- context-mapper.xml의 프로퍼티 값 설정
```xml
<!-- 소스 내 DAO에서 사용할 쿼리문의 위치정보를 확인 bean 설정으로 Dao 클래스에서 extends하는 EgovAbstractMapper 내부에 포함하여 사용 -->
    <!-- configLocations properties 항목에 쿼리문 위치정보 파일들을 등록(각 위치정보 파일 내에 실제 쿼리문들이 포함된 파일들의 위치정보가 존재) -->
	<!-- Mybatis setup for Mybatis Database Layer -->
	<bean id="sqlSession" class="org.mybatis.spring.SqlSessionFactoryBean">
		<property name="dataSource" ref="dataSource"/>
		<property name="configLocation" value="classpath:/egovframework/mapper/config/mapper-config.xml" />

		<property name="mapperLocations">
			<list>
				<value>classpath:/egovframework/mapper/let/**/*_${Globals.DbType}.xml</value>
			</list>
		</property>
	</bean>
    ...

    <!-- 소스 내 사용 예 (DAO 클래스 정의 시 extends를 통해 자동으로 사용 -->
    <!-- com.sqlMapClient 와 같이 새로 지정한 후 EgovAbstractMapper를 재정의하여 사용할 수도 있음(소스 내 설정 참고) -->
    @Repository("BBSAttributeManageDAO")
    public class BBSAttributeManageDAO extends EgovAbstractMapper {
    ...

```

* context-transaction.xml의 트랜잭션 설정
```xml
<!-- transaction 설정 -->
    <bean id="txManager" class="org.springframework.jdbc.datasource.DataSourceTransactionManager">
      <property name="dataSource" ref="dataSource"/>
    </bean>

    <tx:advice id="txAdvice" transaction-manager="txManager">
        <tx:attributes>
            <tx:method name="*" rollback-for="Exception"/>
        </tx:attributes>
    </tx:advice>

    <aop:config>
        <aop:pointcut id="requiredTx" expression="execution(* egovframework.let..impl.*Impl.*(..)) or execution(* egovframework.com..*Impl.*(..))"/>
        <aop:advisor advice-ref="txAdvice" pointcut-ref="requiredTx" />
    </aop:config>

        <!-- 템플릿에서는 서비스 임플 클래스 내의 함수 내에서 트랜잭션을 처리한다.(Exception 발생 시 임플 클래스의 함수 내에서 호출된 DAO 함수들의 처리결과가 모두 롤백됨) -->
```

* context-validator.xml의 Vaildator설정
```xml
<!-- Integration Apache Commons Validator by Spring Modules -->
    <bean id="beanValidator" class="org.springmodules.validation.commons.DefaultBeanValidator">
    	<property name="validatorFactory" ref="validatorFactory"/>
    </bean>

    <bean id="validatorFactory" class="org.springmodules.validation.commons.DefaultValidatorFactory">
	    <property name="validationConfigLocations">
	        <list>
	            <!-- 경량환경 템플릿 밸리데이터 설정 -->
	            <value>classpath:/egovframework/validator/validator-rules-let.xml</value>
	            <value>classpath:/egovframework/validator/let/**/*.xml</value>
	        </list>
	    </property>
    </bean>

    <!-- validationConfigLocations 프로퍼터로 등록된 xml파일 내에 validation시 사용될 함수와 validation의 대상이 되는 form 정보가 등록된다. -->
    <!-- classpath:/egovframework/validator/validator-rules-let.xml 내용 예
        ...
        <validator name="required"
        ...
        <javascript><![CDATA[
            function validateRequired(form) {
                var isValid = true;
                ...
    -->
    <!-- classpath:/egovframework/validator/let/*.xml 내용 예
        ...
        <validator name="required"
        ...
        <javascript><![CDATA[
            function validateRequired(form) {
                var isValid = true;
                ...
    -->
    <!--
        <formset>
		    <form name="boardMaster">
			    <field property="bbsNm" depends="required">
        		    <arg0 key="cop.bbsNm" />
        		</field>
            ...
    -->
```

* context-security.xml의 스프링 시큐리티 설정 (내부업무 템플릿, 포털사이트 템플릿 해당)
- 실행환경의 시큐리티 간소화 부분을 참고하세요.
- context-excel.xml의 excel파일 컨트롤 설정(내부업무 템플릿 해당)
```xml
<bean id="excelZipService" class="org.egovframe.rte.fdl.excel.impl.EgovExcelServiceImpl">
		<property name="mapClass" value="egovframework.let.sym.ccm.zip.service.impl.EgovCcmExcelZipMapping" />
		<property name="sqlSessionTemplate" ref="egov.sqlSessionTemplate" />
	</bean>
    <!-- 소스 내 사용 예 (엑셀 컬럼 정보를 설정한 후 정보 설정한 후 (템플릿의 EgovCcmExcelZipMapping 클래스 참조) 엑셀업로드 시 uploadExcel 함수 사용)
           ...
           excelZipService.uploadExcel("ZipManageDAO.insertExcelZip", file, 2, (long) 5000);
      ...
    -->
```

* context-scheduling-sym-log-lgm.xml의 일 단위 접속통계 스케쥴링 설정(내부업무 템플릿 해당)
```xml
<!-- 시스템 로그 요약  -->
	<bean id="sysLogging" class="org.springframework.scheduling.quartz.MethodInvokingJobDetailFactoryBean">
		<property name="targetObject" ref="egovSysLogScheduling" />
		<property name="targetMethod" value="sysLogSummary" />
		<property name="concurrent" value="false" />
	</bean>

	<!-- 시스템 로그 요약  트리거-->
	<bean id="sysLogTrigger" class="org.springframework.scheduling.quartz.SimpleTriggerFactoryBean">
		<property name="jobDetail" ref="sysLogging" />
		<!-- 시작하고 1분후에 실행한다. (milisecond) 60000-->
		<property name="startDelay" value="30000" />
		<!-- 매 24시간마다 실행한다.864000000 (milisecond) -->
		<property name="repeatInterval" value="864000000" />
	</bean>

	<!-- 시스템 로그 요약 스케줄러 -->
	<bean id="sysLogScheduler" class="org.springframework.scheduling.quartz.SchedulerFactoryBean">
		<property name="triggers">
			<list>
				<ref bean="sysLogTrigger" />
			</list>
		</property>
	</bean>

    <!-- 서버가동후 1분후 시점을 기준으로 일단위로 egovSysLogScheduling서비스의 sysLogSummary()를 실행  -->
```

* context-syslogaop.xml의 aop를 사용한 로그 기록 설정(내부업무 템플릿 해당)
```xml
<!--  System Log Aspect -->
	<bean id="logManage" class="egovframework.let.sym.log.clg.service.EgovLoginLogAspect" />

	<aop:config>
		<aop:aspect id="logManageAspect" ref="logManage">
		  <!--  로그인 Method -->
	      <aop:before pointcut="execution(public * egovframework.let.uat.uia.service.EgovLoginService.actionLogin(..))" method="logLogin" />
	      <!--  로그아웃 Method
	      <aop:before pointcut="execution(public * egovframework.let.uat.uia.web.EgovLoginController.actionLogout(..))" method="logLogout" />
	       -->
		</aop:aspect>
	</aop:config>

    <!-- 로그인 관련 서비스 클래스 내에서 actionLogin으로 시작하는 함수 동작 시 logManage를 통해 접속로그 등록 -->
```
## /WEB-INF/config/egovframework/springmvc/*.xml
   추가설정파일들은 템플릿 프로젝트 소스의 각 WEB-INF/config/egovframework/springmvc 폴더 아래에 위치한다.
   exception, view, error-page 관련 설정 정보가 등록된다.
- auto detect를 위한 mvc 설정
```xml
<context:component-scan base-package="egovframework">
        <context:include-filter type="annotation" expression="org.springframework.stereotype.Controller"/>
        <context:exclude-filter type="annotation" expression="org.springframework.stereotype.Service"/>
        <context:exclude-filter type="annotation" expression="org.springframework.stereotype.Repository"/>
    </context:component-scan>
```
- exception 발생시 이동할 오류페이지 설정
```xml
<bean class="org.springframework.web.servlet.handler.SimpleMappingExceptionResolver">
        <property name="defaultErrorView" value="cmm/error/egovError"/>
        <property name="exceptionMappings">
            <props>
                <prop key="org.springframework.dao.DataAccessException">cmm/error/dataAccessFailure</prop>
                <prop key="org.springframework.transaction.TransactionException">cmm/error/transactionFailure</prop>
                <prop key="egovframework.rte.fdl.cmmn.exception.EgovBizException">cmm/error/egovError</prop>
                <prop key="org.springframework.security.AccessDeniedException">cmm/error/accessDenied</prop>
            </props>
        </property>
    </bean>
```
- 화면처리용 JSP 파일명의  prefix, suffix 처리에 대한 설정
```xml
<bean class="org.springframework.web.servlet.view.UrlBasedViewResolver" p:order="1"
    p:viewClass="org.springframework.web.servlet.view.JstlView"
    p:prefix="/WEB-INF/jsp/" p:suffix=".jsp"/>
```
- 로그인이 필요한 URL을 체크하는 필터설정(홈페이지 템플릿만 사용하고 다른 템플릿은 시큐리티 권한 적용)
```xml
<!--홈페이지 템플릿은 로그인한 관리자에게 허용되는 URL에 대한 제약이 필터설정과 함께 Controller클래스내에서 접근체크함수를 통해서도 체크한다.-->
    <!--필터설정이 해제되어도 소스내에서 체크로직이 존재하므로 제약 변경시 해당 Request Mapping(***.do)에 해당하는 Controller내의 소스 수정요함 -->
    <bean id="selectAnnotaionMapper"
        class="egovframework.rte.ptl.mvc.handler.SimpleUrlAnnotationHandlerMapping"
        p:order="1">
        <property name="interceptors">
            <list>
                <ref local="authenticInterceptor" />
            </list>
        </property>
        <property name="urls">
            <set>
                 <!-- 게시판 생성, 템플릿 생성은 로그인후 사용 가능하다. 관리자만 사용가능  -->
                 <value>/cop/com/*.do</value>
                 <value>/cop/bbs/*Master*.do</value>
                 <value>/uat/uia/*.do</value>
            </set>
        </property>
    </bean>

    <bean id="authenticInterceptor" class="egovframework.com.cmm.interceptor.AuthenticInterceptor" >
	    <!-- 로그인 체크 인터셉터의 접근허용 URL 리스트-->
            <property name="permittedURL">
            <set>
                <value>/uat/uia/actionLogin.do</value>
                <value>/uat/uia/egovLoginUsr.do</value>
            </set>
	    </property>
    </bean>
```
## datasource관련 설정
- globals.properties 주요 설정정보(datasource.xml의 설정 정보로 적용)
```xml
databse 종류, databse dirver, databse 계정/암호 등을 설정한다.
  템플릿 3종 모두 동일하게 적용되는데 홈페이지의 경우는 Hsql DB를 사용할 수 있는 설정이 추가로 포함되어 있다.
  # DB서버 타입(mysql,oracle,altibase,tibero) - datasource 및 sqlMap 파일 지정에 사용됨
    Globals.DbType = mysql
  # DB 사용자 계정
  Globals.UserName=ebt
  # DB 사용자 암호
  Globals.Password=ebt01
  # driver 정보l
  Globals.DriverClassName=net.sf.log4jdbc.DriverSpy
  # DB 연결 정보
  Globals.Url=jdbc:log4jdbc:mysql://127.0.0.1:3306/ebt
```
