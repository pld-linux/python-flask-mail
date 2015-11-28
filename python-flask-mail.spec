#
# Conditional build:
%bcond_without	doc		# don't build doc
%bcond_without	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%if %{without python2}
# docs built using python2, this simplifies BR just to disable doc if built without py2
%undefine	with_doc
%endif

%define 	module	flask-mail
Summary:	Flask-Mail adds SMTP mail sending to your Flask applications
Summary(pl.UTF-8):	Prosty interfejs do konfiguracji SMTP w aplikacjach Flask i do wysyałnia e-mail z widoków i skryptów
Name:		python-%{module}
Version:	0.9.1
Release:	6
License:	BSD
Group:		Libraries/Python
Source0:	https://pypi.python.org/packages/source/F/Flask-Mail/Flask-Mail-%{version}.tar.gz
# Source0-md5:	04b35a42a44ec7aa724ec8ce55e2e08e
URL:		http://pythonhosted.org/Flask-Mail/
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
%if %{with python2}
BuildRequires:	python-blinker
BuildRequires:	python-flask
BuildRequires:	python-mock
BuildRequires:	python-modules
BuildRequires:	python-nose
BuildRequires:	python-setuptools
BuildRequires:	python-speaklater
%endif
%if %{with python3}
BuildRequires:	python3-blinker
BuildRequires:	python3-flask
BuildRequires:	python3-mock
BuildRequires:	python3-nose
BuildRequires:	python3-setuptools
BuildRequires:	python3-speaklater
%endif
%if %{with doc}
BuildRequires:	sphinx-pdg
%endif
Requires:	python-blinker
Requires:	python-flask
Requires:	python-modules
Requires:	python-speaklater
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Flask-Mail extension provides a simple interface to set up SMTP
with your Flask application and to send messages from your views and
scripts.

%description -l pl.UTF-8
Rozszerzenie Flask-Mail dostarcza prosty interfejs do konfiguracji
SMTP w aplikacji Flask i do wysyłanie wiadomości z widoków i skryptów.

%package -n python3-%{module}
Summary:	Flask-Mail adds SMTP mail sending to your Flask applications
Group:		Libraries/Python
Requires:	python3-blinker
Requires:	python3-flask
Requires:	python3-modules
Requires:	python3-speaklater

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
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%if %{with doc}
cd docs
%{__make} -j1 html
rm -rf _build/html/_sources
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%{py_sitescriptdir}/flask_mail.py[co]
%{py_sitescriptdir}/Flask_Mail-%{version}-py*.egg-info
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
