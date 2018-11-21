#
#  Licensed to the Apache Software Foundation (ASF) under one or more
#  contributor license agreements.  See the NOTICE file distributed with
#  this work for additional information regarding copyright ownership.
#  The ASF licenses this file to You under the Apache License, Version 2.0
#  (the "License"); you may not use this file except in compliance with
#  the License.  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
%define timestamp           %(date +%Y%m%d%H%M)
%define version             %{?_version}%{!?_version:UNKNOWN}
%define full_version        %{version}%{?_prerelease}
%define prerelease_fmt      %{?_prerelease:.%{_prerelease}}
%define vendor_version      %{?_vendor_version}%{!?_vendor_version: UNKNOWN}
%define url                 http://janusgraph.org/
%define base_name           janusgraph
%define name                %{base_name}-%{vendor_version}
%define versioned_app_name  %{base_name}-%{version}
%define buildroot           %{_topdir}/BUILDROOT/%{versioned_app_name}-root
%define installpriority     %{_priority} # Used by alternatives for concurrent version installs
%define __jar_repack        %{nil}

%define janusgraph_root         %{_prefix}/%{base_name}
%define janusgraph_home         %{janusgraph_root}/%{full_version}

%define _binaries_in_noarch_packages_terminate_build   0

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Name:           %{base_name}
Version:        %{version}
Release:        %{timestamp}%{prerelease_fmt}
BuildRoot:      %{buildroot}
BuildArch:      noarch
Summary:        JanusGraph provides a highly scalable graph database
License:        ASL 2.0
Group:          Applications/Internet
URL:            %{url}
Provides:       janusgraph = %{version}
Source0:        janusgraph-%{full_version}-hadoop2.zip
Requires(pre): /usr/sbin/useradd, /usr/bin/getent
Requires(postun): /usr/sbin/userdel

%description
JanusGraph provides a highly scalable graph database

%prep
rm -rf %{_rpmdir}/%{buildarch}/%{versioned_app_name}*
rm -rf %{_srcrpmdir}/%{versioned_app_name}*

%build
rm -rf %{_builddir}
mkdir -p %{_builddir}/%{versioned_app_name}

%clean
rm -rf %{buildroot}
rm -rf %{_builddir}/*

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{janusgraph_home}

# copy source files and untar
unzip %{SOURCE0} -x 'janusgraph-%{version}-hadoop2/javadocs/*' 'janusgraph-%{version}-hadoop2/elasticsearch/*' 'janusgraph-%{version}-hadoop2/examples/*' 'janusgraph-%{version}-hadoop2/log/*'
mv janusgraph-%{version}-hadoop2/* %{buildroot}%{janusgraph_home} && rmdir janusgraph-%{version}-hadoop2
rm %{buildroot}%{janusgraph_home}/bin/*.bat

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

%files          

%defattr(-,root,root,755)
%dir %{janusgraph_root}
%dir %{janusgraph_home}
%dir %{janusgraph_home}/bin
%dir %{janusgraph_home}/conf
%dir %{janusgraph_home}/data
%dir %{janusgraph_home}/ext
%dir %{janusgraph_home}/lib
%dir %{janusgraph_home}/scripts
%dir %{janusgraph_home}/conf/cassandra
%dir %{janusgraph_home}/conf/solr
%dir %{janusgraph_home}/conf/solr/lang
%dir %{janusgraph_home}/conf/gremlin-server
%dir %{janusgraph_home}/conf/hadoop-graph

%attr(0755,janusgraph,janusgraph) %{janusgraph_home}/bin/*.sh
%attr(0755,janusgraph,janusgraph) %{janusgraph_home}/bin/nodetool
%attr(0755,janusgraph,janusgraph) %{janusgraph_home}/bin/cassandra
%attr(0644,janusgraph,janusgraph) %{janusgraph_home}/lib/*
%attr(0644,janusgraph,janusgraph) %{janusgraph_home}/conf/*
%attr(0644,janusgraph,janusgraph) %{janusgraph_home}/data/*
%attr(0644,janusgraph,janusgraph) %{janusgraph_home}/ext/*
%attr(0644,janusgraph,janusgraph) %{janusgraph_home}/LICENSE.txt
%attr(0644,janusgraph,janusgraph) %{janusgraph_home}/NOTICE.txt
%attr(0644,janusgraph,janusgraph) %{janusgraph_home}/upgrade.adoc
%attr(0644,janusgraph,janusgraph) %{janusgraph_home}/changelog.adoc
%attr(0644,janusgraph,janusgraph) %{janusgraph_home}/scripts/empty-sample.groovy

%pre
/usr/bin/getent group janusgraph > /dev/null || /usr/sbin/groupadd -r janusgraph
/usr/bin/getent passwd janusgraph > /dev/null || /usr/sbin/useradd -r -d /usr/janusgraph/ -s /sbin/nologin -g janusgraph janusgraph

%postun
/usr/sbin/userdel janusgraph

%changelog
* Tue Nov 20 2018 Simon Elliston Ball <simon@simonellistonball.com> - 0.2.2
- First packaging
