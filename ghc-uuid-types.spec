#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	uuid-types
Summary:	Type definitions for Universally Unique Identifiers
Name:		ghc-%{pkgname}
Version:	1.0.3
Release:	2
License:	BSD
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/uuid-types
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	8eb681871f48a2f7fd739fad9e91c341
Patch0:		hashable-1.3.patch
URL:		http://hackage.haskell.org/package/uuid-types
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-hashable
BuildRequires:	ghc-random
%if %{with prof}
BuildRequires:	ghc-prof
BuildRequires:	ghc-hashable-prof
BuildRequires:	ghc-random-prof
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
%requires_eq	ghc
Requires(post,postun):	/usr/bin/ghc-pkg
Requires:	ghc-hashable
Requires:	ghc-random
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
This library contains type definitions for Universally Unique
Identifiers and basic conversion functions.
See http://en.wikipedia.org/wiki/UUID for the general idea.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-hashable-prof
Requires:	ghc-random-prof

%description prof
Profiling %{pkgname} library for GHC.  Should be installed when
GHC's profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%prep
%setup -q -n %{pkgname}-%{version}
%patch0 -p1

%build
runhaskell Setup.hs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build
runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc CHANGES %{name}-%{version}-doc/*
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.so
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.a
%exclude %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a

%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/UUID
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/UUID/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/UUID/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/UUID/Types
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/UUID/Types/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/UUID/Types/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/UUID/Types/Internal
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/UUID/Types/Internal/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/UUID/Types/Internal/*.dyn_hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/UUID/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/UUID/Types/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/UUID/Types/Internal/*.p_hi
%endif
