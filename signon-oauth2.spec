Summary:	OAuth 2.0 plugin for Single Sign On daemon
Summary(pl.UTF-8):	Wtyczka OAuth 2.0 dla demona Single Sign On
Name:		signon-oauth2
Version:	0.23
Release:	1
License:	LGPL v2.1
Group:		Libraries
#Source0Download: https://gitlab.com/accounts-sso/signon-plugin-oauth2/tags?page=2
# TODO: in the future use fake GET arg to force sane filename on df
#Source0:	https://gitlab.com/accounts-sso/signon-plugin-oauth2/repository/archive.tar.bz2?ref=VERSION_%{version}&fake_out=/%{name}-%{version}.tar.bz2
Source0:	archive.tar.bz2%3Fref=VERSION_%{version}
# Source0-md5:	dc1f73e6c841b5f318f1f53d29e220a1
URL:		https://gitlab.com/accounts-sso/signon-plugin-oauth2
BuildRequires:	Qt5Core-devel >= 5
BuildRequires:	Qt5Network-devel >= 5
BuildRequires:	Qt5Test-devel >= 5
BuildRequires:	Qt5XmlPatterns-devel >= 5
BuildRequires:	libsignon-qt5-devel
BuildRequires:	pkgconfig
BuildRequires:	qt5-build >= 5
BuildRequires:	qt5-qmake >= 5
# qt5-based
BuildRequires:	signon-devel >= 8.58
Requires:	signon >= 8.58
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This plugin for the Accounts-SSO SignOn daemon handles the OAuth
1.0 and 2.0 authentication protocols.

%description -l pl.UTF-8
Ta wtyczka demona Accounts-SSO SignOn obsługuje protokołu
uwierzytelniania OAuth 1.0 i 2.0.

%package devel
Summary:	Development files for Single Sign On OAuth 2.0 plugin
Summary(pl.UTF-8):	Pliki programistyczne wtyczki OAuth 2.0 dla usługi Single Sign On
Group:		Development/Libraries
# doesn't require base
Requires:	Qt5Core-devel >= 5
# signon-plugins
Requires:	signon-devel >= 8.58

%description devel
Development files for Single Sign On OAuth 2.0 plugin.

%description devel -l pl.UTF-8
Pliki programistyczne wtyczki OAuth 2.0 dla usługi Single Sign On.

%prep
%setup -q -n signon-plugin-oauth2-VERSION_%{version}-b74b5397992caddeb32a6158c9295126c55a3025

%build
qmake-qt5 signon-oauth2.pro \
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
%doc README.md
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
