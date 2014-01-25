#
# Conditional build:
%bcond_with	qt5	# use Qt5 instead of Qt4
#
Summary:	OAuth 2.0 plugin for Single Sign On daemon
Summary(pl.UTF-8):	Wtyczka OAuth 2.0 dla demona Single Sign On
Name:		signon-oauth2
Version:	0.19
Release:	1
License:	LGPL v2.1
Group:		Libraries
#Source0Download: http://code.google.com/p/accounts-sso/downloads/list
Source0:	http://accounts-sso.googlecode.com/files/%{name}-%{version}.tar.bz2
# Source0-md5:	32aa3b93b5d08c15a8e077d73bda61fa
URL:		http://code.google.com/p/accounts-sso/
BuildRequires:	pkgconfig
%if %{with qt5}
BuildRequires:	Qt5Core-devel >= 5
BuildRequires:	Qt5Network-devel >= 5
BuildRequires:	Qt5Test-devel >= 5
BuildRequires:	Qt5XmlPatterns-devel >= 5
BuildRequires:	libsignon-qt5-devel
BuildRequires:	qt5-build >= 5
BuildRequires:	qt5-qmake >= 5
%else
BuildRequires:	QtCore-devel >= 4
BuildRequires:	QtNetwork-devel >= 4
BuildRequires:	QtTest-devel >= 4
BuildRequires:	QtXmlPatterns-devel >= 4
BuildRequires:	libsignon-qt-devel
BuildRequires:	qjson-devel
BuildRequires:	qt4-build >= 4
BuildRequires:	qt4-qmake >= 4
%endif
Requires:	signon
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
OAuth 2.0 plugin for Single Sign On daemon.

%description -l pl.UTF-8
Wtyczka OAuth 2.0 dla demona Single Sign On.

%package devel
Summary:	Development files for Single Sign On OAuth 2.0 plugin
Summary(pl.UTF-8):	Pliki programistyczne wtyczki OAuth 2.0 dla usługi Single Sign On
Group:		Development/Libraries
# doesn't require base
%if %{with qt5}
Requires:	Qt5Core-devel >= 5
%else
Requires:	QtCore-devel >= 4
%endif
# signon-plugins
Requires:	signon-devel

%description devel
Development files for Single Sign On OAuth 2.0 plugin.

%description devel -l pl.UTF-8
Pliki programistyczne wtyczki OAuth 2.0 dla usługi Single Sign On.

%prep
%setup -q

%build
qmake-qt4 signon-oauth2.pro \
	QMAKE_CXX="%{__cxx}" \
	QMAKE_CXXFLAGS_RELEASE="%{rpmcxxflags}" \
	QMAKE_LFLAGS_RELEASE="%{rpmldflags}"
	
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

%{__mv} $RPM_BUILD_ROOT%{_bindir}/{oauthclient,signon-oauthclient}

%{__rm} $RPM_BUILD_ROOT%{_bindir}/signon-oauth2plugin-tests
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/signon-oauth2plugin-tests

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%dir %{_sysconfdir}/signon-ui
%dir %{_sysconfdir}/signon-ui/webkit-options.d
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/signon-ui/webkit-options.d/m.facebook.com.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/signon-ui/webkit-options.d/www.facebook.com.conf
%attr(755,root,root) %{_bindir}/signon-oauthclient
%attr(755,root,root) %{_libdir}/signon/liboauth2plugin.so

%files devel
%defattr(644,root,root,755)
%{_includedir}/signon-plugins/oauth1data.h
%{_includedir}/signon-plugins/oauth2data.h
%{_pkgconfigdir}/signon-oauth2plugin.pc
