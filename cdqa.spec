%define gcj_support 1

%define	name	cdqa
%define	oname	CDQA
%define	jarname	cdqa
%define	version	20070201
%define	release	%mkrel 5
%define	jarlibs	axis gemo-utilities gnu.regexp

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	%{oname}
License:	LGPL
Group:		Development/Java
Url:		http://forge.objectweb.org/projects/activexml/
# from cvs
Source0:	%{name}-%{version}.tar.lzma
BuildRequires:	lzma
BuildRequires:	jpackage-utils java-devel ant %{jarlibs}
Requires:	%{jarlibs}
Provides:	%{oname} = %{version}-%{release}
%if %{gcj_support}
Requires(post):	java-gcj-compat
Requires(postun):	java-gcj-compat
BuildRequires:	java-gcj-compat-devel
%else
BuildArch:      noarch
%endif
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
CDQA is part of ActiveXML framework code and implements a query 
processor for XML using X-OQL. X-OQL is a query language for XML.
The X-OQL language is used to let the user define Web services as X-OQL 
queries (with parameters) similar to XQuery.

%package	javadoc
Summary:	Javadoc for %{oname}
Group:		Development/Java

%description	javadoc
Javadoc for %{oname}.

%prep
%setup -q -n %{oname}
#make sure that we don't use precompiled java package if shipped
rm -rf lib

%build
CLASSPATH=$(build-classpath %{jarlibs}) \
ant -f cdqa_build.xml jar javadoc -DDSTAMP=%{version}
jar -i build/lib/%{jarname}-%{version}.jar

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_javadir}
install -m644 build/lib/%{jarname}.jar -D %{buildroot}%{_javadir}/%{jarname}-%{version}.jar
for jarname in \
	%{buildroot}%{_javadir}/%{name}.jar \
	%{buildroot}%{_javadir}/%{oname}{,-%{version}}.jar
do ln -s %{jarname}-%{version}.jar $jarname
done

install -d %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -r build/api %{buildroot}%{_javadocdir}/%{name}-%{version}

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_javadir}/*.jar
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*
%endif

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}

