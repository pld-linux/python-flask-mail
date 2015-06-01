#
# Conditional build:
%bcond_without	doc		# don't build doc
%bcond_without	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define 	module	flask-mail
Summary:	A simple interface to set up SMTP with Flask application and to send messages from your views and scripts
Summary(pl.UTF-8):	Prosty interfejs do konfiguracji SMTP w aplikacjach Flask i do wysyałnia e-mail z widoków i skryptów
# Name must match the python module/package name (as in 'import' statement)
Name:		python-%{module}
Version:	0.9.1
Release:	2
License:	BSD
Group:		Libraries/Python
Source0:	https://pypi.python.org/packages/source/F/Flask-Mail/Flask-Mail-%{version}.tar.gz
# Source0-md5:	04b35a42a44ec7aa724ec8ce55e2e08e
URL:		https://github.com/rduplain/flask-mail
BuildRequires:	rpm-pythonprov
# if py_postclean is used
BuildRequires:	rpmbuild(macros) >= 1.219
# when using /usr/bin/env or other in-place substitutions
#BuildRequires:	sed >= 4.0
# when python3 present
%if %{with python2}
BuildRequires:	python-blinker
BuildRequires:	python-setuptools > 7.0
%endif
%if %{with python3}
BuildRequires:	python3-blinker
BuildRequires:	python3-modules
BuildRequires:	python3-setuptools > 7.0
%endif
# Below Rs only work for main package (python2)
Requires:	python-blinker
Requires:	python-modules
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
%description -l pl.UTF-8
Rozszerzenie Flask-Mail dostarcza prosty interfejs do konfiguracji
SMTP w aplikacji Flask i do wysyłanie wiadomości z widoków i skryptów.

%package -n python3-%{module}
Summary:	-
Summary(pl.UTF-8):	-
Group:		Libraries/Python
Requires:	python3-blinker
Requires:	python3-modules

%description -n python3-%{module}
The Flask-Mail extension provides a simple interface to set up SMTP
with your Flask application and to send messages from your views and
scripts.

%description -n python3-%{module} -l pl.UTF-8
Rozszerzenie Flask-Mail dostarcza prosty interfejs do konfiguracji
SMTP w aplikacji Flask i do wysyłanie wiadomości z widoków i skryptów.

%package apidocs
Summary:	%{module} API documentation
Summary(pl.UTF-8):	Dokumentacja API %{module}
Group:		Documentation

%description apidocs
API documentation for %{module}.

%description apidocs -l pl.UTF-8
Dokumentacja API %{module}.

%prep
%setup -q -n Flask-Mail-%{version}


%build
%if %{with python2}
%{__python} setup.py build --build-base build-2 %{?with_tests:test}
%endif

%if %{with python3}
%{__python3} setup.py build --build-base build-3 %{?with_tests:test}
%endif

%if %{with doc}
cd docs
%{__make} -j1 html
rm -rf _build/html/_sources
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%{__python} setup.py \
	build --build-base build-2 \
	install --skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%py_postclean
%endif

%if %{with python3}
%{__python3} setup.py \
	build --build-base build-3 \
	install --skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%{py_sitescriptdir}/*.py[co]
%if "%{py_ver}" > "2.4"
%{py_sitescriptdir}/Flask_Mail-%{version}-py*.egg-info
%endif
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%{py3_sitescriptdir}/flask_mail.py
%{py3_sitescriptdir}/__pycache__/flask_mail.*.py[co]
%{py3_sitescriptdir}/Flask_Mail-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/*
%endif
