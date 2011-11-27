%global spec_ver 3.0
%global spec_name geronimo-interceptor_%{spec_ver}_spec

Name:             geronimo-interceptor
Version:          1.0.1
Release:          6
Summary:          Java EE: Interceptor API v3.0
Group:            Development/Java
License:          ASL 2.0
URL:              http://geronimo.apache.org/

# svn export http://svn.apache.org/repos/asf/geronimo/specs/tags/geronimo-interceptor_3.0_spec-1.0.1/
# tar czf geronimo-interceptor_3.0_spec-1.0.1.tar.gz geronimo-interceptor_3.0_spec-1.0.1/
Source0:          %{spec_name}-%{version}.tar.gz
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:        noarch

BuildRequires:    java-devel >= 0:1.6.0
BuildRequires:    jpackage-utils
BuildRequires:    maven2 >= 2.2.1
BuildRequires:    geronimo-parent-poms
BuildRequires:    maven-resources-plugin

Requires:         java >= 0:1.6.0
Requires:         jpackage-utils
Requires(post):   jpackage-utils
Requires(postun): jpackage-utils

Provides:         interceptor_api = %{spec_ver}

%description
Contains annotations and interfaces for defining interceptor methods, 
interceptor classes and for binding interceptor classes to target classes.

%package javadoc
Group:            Development/Java
Summary:          Javadoc for %{name}
Requires:         jpackage-utils

%description javadoc
This package contains the API documentation for %{name}.


%prep
%setup -q -n %{spec_name}-%{version}

%build
export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mvn-jpp \
        -e \
        -Dmaven2.jpp.mode=true \
        -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
        install javadoc:javadoc

%install
rm -rf %{buildroot}

# jars
install -d -m 0755 %{buildroot}%{_javadir}
install -m 644 target/%{spec_name}-%{version}.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
ln -s %{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar
ln -s %{name}-%{version}.jar %{buildroot}%{_javadir}/interceptor.jar

# poms
install -d -m 0755 %{buildroot}%{_mavenpomdir}
install -pm 644 pom.xml %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom
%add_to_maven_depmap org.apache.geronimo.specs %{spec_name} %{version} JPP %{name}
%add_to_maven_depmap org.apache.geronimo.specs geronimo-interceptor_1.1_spec 1.0 JPP %{name}

# javadoc
install -d -m 0755 %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -pr target/site/api*/* %{buildroot}%{_javadocdir}/%{name}-%{version}/
ln -s %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}


%post
%update_maven_depmap

%postun
%update_maven_depmap

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc LICENSE.txt
%{_javadir}/*
%{_mavenpomdir}/*
%{_mavendepmapfragdir}/*

%files javadoc
%defattr(-,root,root,-)
%doc LICENSE.txt
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}

