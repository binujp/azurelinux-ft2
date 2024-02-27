#
# spec file for package slf4j
#
# Copyright (c) 2020 SUSE LLC
# Copyright (c) 2000-2009, JPackage Project
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.
# Please submit bugfixes or comments via https://bugs.opensuse.org/
#

Summary:        Simple Logging Facade for Java
Name:           slf4j
Version:        2.0.11
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Development/Libraries/Java
URL:            https://www.slf4j.org/
Source0:        https://github.com/qos-ch/%{name}/archive/v_%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        http://www.apache.org/licenses/LICENSE-2.0.txt
BuildRequires:  ant >= 1.6.5
BuildRequires:  ant-junit >= 1.6.5
BuildRequires:  apache-commons-lang3
BuildRequires:  apache-commons-logging
BuildRequires:  cal10n
BuildRequires:  java-devel >= 1.5.0
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  javapackages-tools
BuildRequires:  javassist >= 3.4
BuildRequires:  junit >= 3.8.2
Requires:       cal10n
Requires:       java
# this is ugly hack, which creates package which requires the same,
# however slf4j is not splitted between -api and -impl, but pom files are modeled as it was
Provides:       osgi(slf4j.api)
Provides:       mvn(org.slf4j:slf4j-api) = %{version}-%{release}
BuildArch:      noarch

%description
The Simple Logging Facade for Java or (SLF4J) is intended to serve
as a simple facade for various logging APIs allowing to the end-user
to plug in the desired implementation at deployment time. SLF4J also
allows for a gradual migration path away from
Jakarta Commons Logging (JCL).

Logging API implementations can either choose to implement the
SLF4J interfaces directly, e.g. NLOG4J or SimpleLogger. Alternatively,
it is possible (and rather easy) to write SLF4J adapters for the given
API implementation, e.g. Log4jLoggerAdapter or JDK14LoggerAdapter..

%package javadoc
Summary:        Javadoc for %{name}
License:        MIT
Group:          Documentation/HTML

%description javadoc
API documentation for %{name}.

%package manual
Summary:        Documents for %{name}
License:        MIT
Group:          Documentation/Other

%description manual
Manual for %{name}.

%package jdk14
Summary:        SLF4J JDK14 Binding
License:        MIT
Group:          Development/Libraries/Java
Requires:       mvn(org.slf4j:slf4j-api) = %{version}

%description jdk14
SLF4J JDK14 Binding.

%package jcl
Summary:        SLF4J JCL Binding
License:        MIT
Group:          Development/Libraries/Java
Requires:       mvn(commons-logging:commons-logging)
Requires:       mvn(org.slf4j:slf4j-api) = %{version}

%description jcl
SLF4J JCL Binding.

%package -n jcl-over-slf4j
Summary:        JCL 1.1.1 implemented over SLF4J
License:        ASL 2.0
Group:          Development/Libraries/Java
Requires:       mvn(org.slf4j:slf4j-api) = %{version}

%description -n jcl-over-slf4j
JCL 1.1.1 implemented over SLF4J.

%package -n log4j-over-slf4j
Summary:        Log4j implemented over SLF4J
License:        ASL 2.0
Group:          Development/Libraries/Java
Requires:       mvn(org.slf4j:slf4j-api) = %{version}

%description -n log4j-over-slf4j
Log4j implemented over SLF4J.

%prep
%setup -q -n %{name}-v_%{version}
find . -name "*.jar" | xargs rm
cp -p %{SOURCE1} APACHE-LICENSE

%pom_disable_module integration
%pom_disable_module osgi-over-slf4j
%pom_disable_module slf4j-android
%pom_disable_module slf4j-ext
%pom_disable_module slf4j-log4j12
 
# Port to maven-antrun-plugin 3.0.0
sed -i s/tasks/target/ slf4j-api/pom.xml
 
# Because of a non-ASCII comment in slf4j-api/src/main/java/org/slf4j/helpers/MessageFormatter.java
%pom_xpath_inject "pom:project/pom:properties" "
    <project.build.sourceEncoding>ISO-8859-1</project.build.sourceEncoding>"
 
# Fix javadoc links
%pom_xpath_remove "pom:links"
%pom_xpath_inject "pom:plugin[pom:artifactId[text()='maven-javadoc-plugin']]/pom:configuration" "
    <detectJavaApiLink>false</detectJavaApiLink>
    <isOffline>false</isOffline>
    <links><link>/usr/share/javadoc/java</link></links>"
 
# dos2unix
find -name "*.css" -o -name "*.js" -o -name "*.txt" | \
    xargs -t sed -i 's/\r$//'
 
# Remove wagon-ssh build extension
%pom_xpath_remove pom:extensions
 
# Disable default-jar execution of maven-jar-plugin, which is causing
# problems with version 3.0.0 of the plugin.
%pom_xpath_inject "pom:plugin[pom:artifactId='maven-jar-plugin']/pom:executions" "
    <execution>
      <id>default-jar</id>
      <phase>skip</phase>
    </execution>" slf4j-api
 
# The general pattern is that the API package exports API classes and does
# not require impl classes. slf4j was breaking that causing "A cycle was
# detected when generating the classpath slf4j.api, slf4j.nop, slf4j.api."
# The API bundle requires impl package, so to avoid cyclic dependencies
# during build time, it is necessary to mark the imported package as an
# optional one.
# Reported upstream: http://bugzilla.slf4j.org/show_bug.cgi?id=283
sed -i '/Import-Package/s/\}$/};resolution:=optional/' slf4j-api/src/main/resources/META-INF/MANIFEST.MF
 
# Source JARs for are required by Maven 3.4.0
%mvn_package :::sources: sources
 
%mvn_package :%{name}-parent __noinstall
%mvn_package :%{name}-site __noinstall
%mvn_package :%{name}-api
%mvn_package :%{name}-simple
%mvn_package :%{name}-nop
 
%build
%mvn_build -f -s -- -Drequired.jdk.version=1.8
 
%install
# Compat symlinks
%mvn_file ':%{name}-{*}' %{name}/%{name}-@1 %{name}/@1
 
%mvn_install
# manual
install -d -m 0755 $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}-manual
rm -rf target/site/{.htaccess,apidocs}
cp -pr target/site/* $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}-manual

%files -f .mfiles
%dir %{_docdir}/%{name}-%{version}
%license %{_docdir}/%{name}-%{version}/LICENSE.txt
%{_javadir}/%{name}/%{name}-api.jar
%{_javadir}/%{name}/%{name}-nop.jar
%{_javadir}/%{name}/%{name}-simple.jar

%files jdk14 -f .mfiles-jdk14
%{_javadir}/%{name}/%{name}-jdk14.jar

%files jcl -f .mfiles-jcl
%{_javadir}/%{name}/%{name}-jcl.jar

%files -n jcl-over-slf4j -f .mfiles-jcl-over-slf4j

%files -n log4j-over-slf4j -f .mfiles-log4j-over-slf4j

%files javadoc
%{_javadocdir}/%{name}

%files manual
%{_docdir}/%{name}-%{version}/site

%changelog
* Fri Mar 17 2023 Mykhailo Bykhovtsev <mbykhovtsev@microsoft.com> - 1.7.30-5
- Fixing maven provides

* Mon Jan 24 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.7.30-4
- Removing dependency on "log4j12".
- License verified.

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.7.30-3
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Fri Nov 13 2020 Ruying Chen <v-ruyche@microsoft.com> - 1.7.30-2.3
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Sat Apr 11 2020 Fridrich Strba <fstrba@suse.com>
- Don't use %%%%mvn_artifact, but %%%%add_maven_depmap for the
  sources artifacts, so that they don't suck in half of the xmvn*
  stack in order to build

* Wed Feb 26 2020 Fridrich Strba <fstrba@suse.com>
- Upgrade to upstream version 1.7.30
- Removed patch:
  * slf4j-Disallow-EventData-deserialization-by-default.patch
    + not needed any more

* Wed Dec 18 2019 Fridrich Strba <fstrba@suse.com>
- Use the source tarball from github, since the previous one is
  not accessible anymore
- Modified patches:
  * slf4j-Disallow-EventData-deserialization-by-default.patch
    + Adapt to unix line-ends
  * slf4j-commons-lang3.patch
    + Adapt to unix line-ends
    + Do not patch inexisting files

* Sat Oct  5 2019 Fridrich Strba <fstrba@suse.com>
- Remove references to parent from all pom files
- Avoid dependencies without version tag

* Tue Oct  1 2019 Fridrich Strba <fstrba@suse.com>
- Build against the compatibility log4j12-mini package
- Depend on mvn(log4j:log4j:1.2.17) provided by the compatibility
  packages

* Tue Mar 19 2019 Fridrich Strba <fstrba@suse.com>
- Fix an unexpanded ${parsedVersion.osgiVersion} variable in the
  manifests.

* Mon Mar 18 2019 Fridrich Strba <fstrba@suse.com>
- Split slf4j package into several sub-packages leaving only
  parent, api, simple and nop in the main package
- Package slf4j source jar files in a separate spec file

* Tue Feb 26 2019 Fridrich Strba <fstrba@suse.com>
- Clean up the maven pom installation

* Mon Oct 22 2018 Fridrich Strba <fstrba@suse.com>
- Upgrade to 1.7.25
- Modify the build.xml file tarball to correspond to the right
  version
- Modify slf4j-commons-lang3.patch to the new context

* Mon Oct 15 2018 Fridrich Strba <fstrba@suse.com>
- Install the maven artefacts to have mvn dependencies/provides
  generated automatically

* Fri May 18 2018 pmonrealgonzalez@suse.com
- Security fix:  [bsc#1085970, CVE-2018-8088]
  * Disallow EventData deserialization by default
  * Added slf4j-Disallow-EventData-deserialization-by-default.patch
    refreshed from Fedora [ https://src.fedoraproject.org/rpms/slf4j/
    blob/d7cd96bc7a8e8d8d62c8bc62baa7df02cef56c63/f/
    0001-Disallow-EventData-deserialization-by-default.patch ]

* Wed Oct 11 2017 fstrba@suse.com
- Adeed patch:
  * slf4j-commons-lang3.patch
    + Use apache-commons-lang3 instead of apache-commons-lang

* Sun Sep 10 2017 fstrba@suse.com
- Specify java source and target levels 1.6 in order to allow
  building with jdk9
- Disable doclint to avoid bailing out on formatting errors
- Recompress the build.xml.tar.bz2, so that it is a real tar.bz2

* Fri May 19 2017 tchvatal@suse.com
- Remove some not-needed deps

* Tue Nov 10 2015 dmacvicar@suse.de
- note:
  slf4j-pom_xml.patch was removed (not relevant anymore)

* Fri Oct 23 2015 dmacvicar@suse.de
- remove all unnecessary maven depmap metadata

* Fri Oct 23 2015 dmacvicar@suse.de
- update to version 1.7.12

* Wed Mar 18 2015 tchvatal@suse.com
- Fix build with new javapackages-tools

* Fri Aug 29 2014 coolo@suse.com
- build against log4j-mini to avoid a cycle

* Thu Sep 19 2013 mvyskocil@suse.com
- self-provide osgi(slf4j.api) symbol

* Fri Sep 13 2013 mvyskocil@suse.com
- fix build with apache-commons-lang

* Wed Sep 11 2013 mvyskocil@suse.com
- use add_maven_depmap from javapackages-tools

* Mon Sep  9 2013 tchvatal@suse.com
- Move from jpackage-utils to javapackage-tools

* Fri Apr 27 2012 mvyskocil@suse.cz
- format spec file to be suitable for Factory

* Mon Dec 12 2011 dmacvicar@suse.de
- Fix absolute path in maven-build.xml that prevented
  package task in newer versions of openSUSE
- Fix javadoc group

* Wed Jul 27 2011 dmacvicar@suse.de
- Completely remove all maven build parts. Build with ant

* Mon Jul  4 2011 dmacvicar@suse.de
- add BuildRoot tag
