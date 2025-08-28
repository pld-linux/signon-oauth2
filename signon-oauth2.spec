# TODO: fix build with qt6 based signon
#
# Conditional build:
%bcond_with	qt5	# build with qt5-based signon

%if %{with qt5}
%define	qtmajor	5
%define	qt_ver	5.8
%else
%define	qtmajor	6
%define	qt_ver	6.0
%endif
Summary:	OAuth 2.0 plugin for Single Sign On daemon
Summary(pl.UTF-8):	Wtyczka OAuth 2.0 dla demona Single Sign On
Name:		signon-oauth2
Version:	0.25
Release:	1
License:	LGPL v2.1
Group:		Libraries
#Source0Download: https://gitlab.com/accounts-sso/signon-plugin-oauth2/tags?sort=updated_desc
Source0:	https://gitlab.com/accounts-sso/signon-plugin-oauth2/-/archive/VERSION_%{version}/signon-plugin-oauth2-VERSION_%{version}.tar.bz2
# Source0-md5:	8d6f21d4bcfb527dddc20129f6972d14
Patch0:		%{name}-x32.patch
Patch1:		signon-plugin-oauth2-git.patch
# from https://gitlab.com/nicolasfella/signon-plugin-oauth2/-/commits/qt6
Patch2:		signon-plugin-oauth2-qt6-git.patch
URL:		https://gitlab.com/accounts-sso/signon-plugin-oauth2
BuildRequires:	Qt%{qtmajor}Core-devel >= %{qt_ver}
BuildRequires:	Qt%{qtmajor}Network-devel >= %{qt_ver}
BuildRequires:	Qt%{qtmajor}Test-devel >= %{qt_ver}
%if %{with qt5}
BuildRequires:	Qt%{qtmajor}XmlPatterns-devel >= %{qt_ver}
%endif
BuildRequires:	libsignon-qt%{qtmajor}-devel
BuildRequires:	libstdc++-devel >= 6:7
BuildRequires:	pkgconfig
BuildRequires:	qt%{qtmajor}-build >= %{qt_ver}
BuildRequires:	qt%{qtmajor}-qmake >= %{qt_ver}
%if %{with qt5}
BuildRequires:	signon-devel >= 8.58
Requires:	signon >= 8.58
%else
BuildRequires:	signon-devel >= 8.62
Requires:	signon >= 8.62
%endif
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
Requires:	Qt%{qtmajor}Core-devel >= %{qt_ver}
# signon-plugins
%if %{with qt5}
Requires:	signon-devel >= 8.58
%else
Requires:	signon-devel >= 8.62
%endif

%description devel
Development files for Single Sign On OAuth 2.0 plugin.

%description devel -l pl.UTF-8
Pliki programistyczne wtyczki OAuth 2.0 dla usługi Single Sign On.

%prep
%setup -q -n signon-plugin-oauth2-VERSION_%{version}
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1

%build
qmake-qt%{qtmajor} signon-oauth2.pro \
	CONFIG+=make_examples \
	QMAKE_CXX="%{__cxx}" \
	QMAKE_CXXFLAGS_RELEASE="%{rpmcxxflags}" \
	QMAKE_LFLAGS_RELEASE="%{rpmldflags}" \
	
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
