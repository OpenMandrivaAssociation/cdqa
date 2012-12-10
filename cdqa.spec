%define gcj_support 1

%define oname   CDQA
%define jarname cdqa
%define jarlibs axis gemo-utilities gnu.regexp

Name:           cdqa
Version:        20070201
Release:        13
Epoch:          0
Summary:        %{oname}
License:        LGPL
Group:          Development/Java
Url:            http://forge.objectweb.org/projects/activexml/
# from cvs
Source0:        %{name}-%{version}.tar.lzma
BuildRequires:  java-rpmbuild java-devel ant %{jarlibs}
Requires:       %{jarlibs}
Provides:       %{oname} = %{epoch}:%{version}-%{release}
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildArch:      noarch
%endif
BuildRequires:    locales-en

%description
CDQA is part of ActiveXML framework code and implements a query 
processor for XML using X-OQL. X-OQL is a query language for XML.
The X-OQL language is used to let the user define Web services as X-OQL 
queries (with parameters) similar to XQuery.

%package javadoc
Summary:        Javadoc for %{oname}
Group:          Development/Java

%description javadoc
Javadoc for %{oname}.

%prep
%setup -q -n %{oname}
#make sure that we don't use precompiled java package if shipped
rm -rf lib

%build
export LC_ALL=ISO-8859-1
CLASSPATH=$(build-classpath %{jarlibs}) \
%{ant} -f cdqa_build.xml jar javadoc -DDSTAMP=%{version}
%{jar} -i build/lib/%{jarname}.jar

%install
install -d %{buildroot}%{_javadir}
install -m644 build/lib/%{jarname}.jar -D %{buildroot}%{_javadir}/%{jarname}-%{version}.jar
for jarname in \
        %{buildroot}%{_javadir}/%{name}.jar \
        %{buildroot}%{_javadir}/%{oname}{,-%{version}}.jar
do ln -s %{jarname}-%{version}.jar $jarname
done

install -d %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -r build/api %{buildroot}%{_javadocdir}/%{name}-%{version}
%{__ln_s} %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%defattr(-,root,root)
%{_javadir}/*.jar
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*
%endif

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}


%changelog
* Thu Dec 09 2010 Oden Eriksson <oeriksson@mandriva.com> 0:20070201-12mdv2011.0
+ Revision: 616978
- the mass rebuild of 2010.0 packages

* Wed Sep 02 2009 Thierry Vignaud <tv@mandriva.org> 0:20070201-11mdv2010.0
+ Revision: 424792
- rebuild

* Wed Jul 23 2008 Thierry Vignaud <tv@mandriva.org> 0:20070201-10mdv2009.0
+ Revision: 243468
- rebuild

* Fri Jan 04 2008 David Walluck <walluck@mandriva.org> 0:20070201-8mdv2008.1
+ Revision: 145453
- fix build

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

  + Anssi Hannula <anssi@mandriva.org>
    - buildrequire java-rpmbuild, i.e. build with icedtea on x86(_64)
    - remove unnecessary Requires(post) on java-gcj-compat


* Mon Feb 05 2007 Per Øyvind Karlsen <pkarlsen@mandriva.com> 20070201-5mdv2007.0
+ Revision: 116505
- complete description
- fix descriptiojn (thx Ric)
- fix permissions for gcj libraries
- to make files included for gcj built stuff conditional too
- fix cdqa.jar symlink
- be sure to use actual snapshot date as version rather than current date
  misc packaging fixes
- export CLASSPATH for real
- Import cdqa

  + David Walluck <walluck@mandriva.org>
    - add %%post and %%postun for %%gcj_support
    - aot compile

