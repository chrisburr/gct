Name:		globus-data-management-server
%global _name %(tr - _ <<< %{name})
Version:	6.0
Release:	1%{?dist}
Summary:	Grid Community Toolkit - Data Management Server

Group:		System Environment/Libraries
License:	ASL 2.0
URL:		http://www.globus.org/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires: globus-common-progs
Requires: globus-gfork-progs
Requires: globus-xio-pipe-driver
Requires: globus-gsi-cert-utils-progs
Requires: globus-gss-assist-progs
Requires: globus-ftp-control
Requires: globus-authz-callout-error
Requires: globus-authz
Requires: globus-usage
Requires: globus-xioperf
Requires: globus-gridftp-server-progs

%description
The Grid Community Toolkit (GCT) is an open source software toolkit used for
building grid systems and applications. It is a fork of the Globus Toolkit
originally created by the Globus Alliance. It is supported by the Grid
Community Forum (GridCF) that provides community-based support for core
software packages in grid computing.

The %{name} package contains:
Data Management Server Programs

%prep

%build

%install
rm -rf "$RPM_BUILD_ROOT"
mkdir "$RPM_BUILD_ROOT"

%files

%clean

%post

%postun

%changelog
* Mon Jul 17 2012 Joseph Bester <bester@mcs.anl.gov> - 14.7-3
- GT 5.2.2 New Metapackage
