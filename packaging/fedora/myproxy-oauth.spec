%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

Name:           myproxy-oauth
%global _name %(echo %{name} | tr - _)
Version:        1.1
Release:        1%{?dist}
Summary:        MyProxy OAuth Delegation Serice

Group:          System Environment/Libraries
License:        %{?suse_version:Apache-2.0}%{!?suse_version:ASL 2.0}
URL:            https://github.com/gridcf/gct/
Source:         %{_name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  python
BuildArch:      noarch

Requires:       pyOpenSSL

%if 0%{?suse_version} == 0
Requires:       mod_ssl
Requires:       mod_wsgi
Requires(pre):  shadow-utils
%else
# Available from http://download.opensuse.org/repositories/Apache/SLE_11_SP3/Apache.repo
Requires:       apache2 >= 2.4
# Available from http://download.opensuse.org/repositories/Apache:/Modules/Apache_SLE_12_SP1/Apache:Modules.repo
Requires:       apache2-mod_wsgi
Requires(pre):  shadow
%endif

%if 0%{?rhel} != 0
Requires:       python-crypto
Requires:       m2crypto
%else
%if 0%{?suse_version} > 0
Requires:       python-crypto
Requires:       python-m2crypto
%else
Requires:       python-crypto >= 2.2
%endif
%endif

%description
The Grid Community Toolkit (GCT) is an open source software toolkit used for
building grid systems and applications. It is a fork of the Globus Toolkit
originally created by the Globus Alliance. It is supported by the Grid
Community Forum (GridCF) that provides community-based support for core
software packages in grid computing.

The %{name} package contains:
MyProxy OAuth Delegation Service

%prep
%setup -q -n %{_name}-%{version}

%build
:

%install
python setup.py install \
    --install-lib /usr/share/%{name} \
    --install-scripts /usr/share/%{name} \
    --install-data %{_pkgdocdir} \
    --root $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_pkgdocdir}
cp README.md $RPM_BUILD_ROOT%{_pkgdocdir}/README.txt
mkdir -p $RPM_BUILD_ROOT/%{_sbindir}
pythonpath="/usr/share/%{name}"
cat > $RPM_BUILD_ROOT%{_sbindir}/myproxy-oauth-setup <<EOF
#! /bin/sh
if [ "\$(id -u)" = 0 ]; then
    idarg="-i \$(id -u myproxyoauth)"
fi
exec /usr/bin/env PYTHONPATH="$pythonpath" python /usr/share/%{name}/myproxy-oauth-setup "\$@" \${idarg}
EOF
chmod a+x $RPM_BUILD_ROOT%{_sbindir}/myproxy-oauth-setup
%if 0%{?fedora} >= 18 || 0%{?rhel} >= 7
mkdir -p $RPM_BUILD_ROOT/etc/httpd/conf.d
cp $RPM_BUILD_ROOT%{_pkgdocdir}/apache/myproxy-oauth-2.4 \
   $RPM_BUILD_ROOT/etc/httpd/conf.d/wsgi-myproxy-oauth.conf
%else
%if 0%{?suse_version} > 0
mkdir -p $RPM_BUILD_ROOT/etc/apache2/conf.d
cp $RPM_BUILD_ROOT%{_pkgdocdir}/apache/myproxy-oauth-2.4 \
   $RPM_BUILD_ROOT/etc/apache2/conf.d/wsgi-myproxy-oauth.conf
%else
mkdir -p $RPM_BUILD_ROOT/etc/httpd/conf.d
cp $RPM_BUILD_ROOT%{_pkgdocdir}/apache/myproxy-oauth \
   $RPM_BUILD_ROOT/etc/httpd/conf.d/wsgi-myproxy-oauth.conf
%endif
%endif

mkdir -p "$RPM_BUILD_ROOT/var/lib/myproxy-oauth"

%pre
getent group myproxyoauth >/dev/null || groupadd -r myproxyoauth
getent passwd myproxyoauth >/dev/null || \
    useradd -r -g myproxyoauth -d /usr/share/myproxy-oauth -s /sbin/nologin \
        -c "MyProxy Oauth Daemon" myproxyoauth

%if 0%{?suse_version} != 0
mkdir -p /srv/www/run
%endif

exit 0

%files
%defattr(-,root,root,-)
%if %{?suse_version}%{!?suse_version:0}
%dir %{_sysconfdir}/apache2
%dir %{_sysconfdir}/apache2/conf.d
%endif
%dir %{_pkgdocdir}
%doc %{_pkgdocdir}/README.txt
%dir %{_pkgdocdir}/apache
%doc %{_pkgdocdir}/apache/*
%config(noreplace) /etc/*/conf.d/wsgi-myproxy-oauth.conf
%dir %attr(0700,myproxyoauth,myproxyoauth) /var/lib/myproxy-oauth
/usr/share/%{name}

%{_sbindir}/myproxy-oauth-setup

%changelog
* Mon May 14 2018 Globus Toolkit <support@globus.org> - 1.1-1
- Allow newer TLS versions

* Tue Apr 03 2018 Mattias Ellert <mattias.ellert@physics.uu.se> - 1.0-1
- First Grid Community Toolkit release

* Mon Dec 18 2017 Globus Toolkit <support@globus.org> - 0.27-1
- Revert

* Mon Mar 13 2017 Globus Toolkit <support@globus.org> - 0.26-1
- Move apache config file deployment into setup script

* Thu Nov 10 2016 Globus Toolkit <support@globus.org> - 0.25-1
- Python exception handling workaround for 2.5-3.x

* Wed Nov 09 2016 Globus Toolkit <support@globus.org> - 0.24-1
- Verify all paths yield proper response or error response

* Fri Nov 04 2016 Globus Toolkit <support@globus.org> - 0.23-1
- Fix indent issue

* Tue Oct 18 2016 Globus Toolkit <support@globus.org> - 0.22-1
- Catch exceptions and return "400 Bad Request"

* Wed Aug 31 2016 Globus Toolkit <support@globus.org> - 0.21-4
- Updates for SLES 12

* Thu Mar 10 2016 Globus Toolkit <support@globus.org> - 0.21-1
- Fix redirect when callback_uri contains a query

* Thu Oct 29 2015 Globus Toolkit <support@globus.org> - 0.20-1
- Use setsebool if it is installed and semanage is not available

* Tue Nov 11 2014 Globus Toolkit <support@globus.org> - 0.18-1
- Run selinux commands as root, run database commands as myproxyoauth

* Wed Nov 05 2014 Globus Toolkit <support@globus.org> - 0.16-1
- Remove httplib2 dependent code which is not used

* Mon Aug 04 2014 Globus Toolkit <support@globus.org> - 0.15-2
- Fix error in scriptlet to create wsgi socket dir on SLES 11

* Thu Jul 31 2014 Globus Toolkit <support@globus.org> - 0.15-1
- Update to 0.15 for EC2-public hostname awareness
- Create wsgi socket dir on SLES 11

* Tue Jul 29 2014 Globus Toolkit <support@globus.org> - 0.14-3
- EL7 requires Apache 2.4 configuration file

* Fri Jul 25 2014 Globus Toolkit <support@globus.org> - 0.14-2
- EL7 doesn't require python-sqlite2

* Mon Jan 20 2014 Globus Toolkit <support@globus.org> - 0.14-1
- move to globus repo

* Wed Sep 04 2013 Globus Toolkit <support@globus.org> - 0.13-1
- Fix regression on python path setting

* Wed Sep 04 2013 Globus Toolkit <support@globus.org> - 0.12-1
- Fall back to pysqlite2 when sqlite3 is not available

* Wed Sep 04 2013 Globus Toolkit <support@globus.org> - 0.11-1
- Remove dependency on sql alchemy

* Fri Aug 23 2013 Globus Toolkit <support@globus.org> - 0.10-1
- Remove dependency on jinja2

* Wed Mar 27 2013 Globus Toolkit <support@globus.org> - 0.0-1
- Initial packaging
