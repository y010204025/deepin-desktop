%global   debug_package   %{nil}

%global   provider        github
%global   provider_tld    com
%global   project         BurntSushi
%global   repo            graphics-go
# https://github.com/BurntSushi/graphics-go
%global   provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}
%global   import_path     %{provider_prefix}
%global   commit          b43f31a4a96688fba0b612e25e22648b9267e498
%global   shortcommit     %(c=%{commit}; echo ${c:0:7})

Name:       golang-%{provider}-%{project}-%{repo}
Version:    0
Release:    0.1%{?dist}
Summary:    Graphics library for the Go programming language
License:    BSD
URL:        https://%{provider_prefix}
Source0:    %{url}/archive/%{commit}/%{repo}-%{shortcommit}.tar.gz

%package devel
Summary:    %{summary}
BuildArch:  noarch
Provides:   golang(%{import_path}) = %{version}-%{release}
Provides:   golang(%{import_path}/graphics) = %{version}-%{release}

%description devel
%{summary}.

This package contains library source intended for
building other packages which use import path with
%{import_path} prefix.

%description
%{summary}.

%prep
%setup -q -n %{repo}-%{commit}

%build

%install
# source codes for building projects
install -d -p %{buildroot}%{gopath}/src/%{import_path}/
echo "%%dir %%{gopath}/src/%%{import_path}/." >> devel.file-list
# find all *.go but no *_test.go files and generate devel.file-list
for file in $(find . -iname "*.go" \! -iname "*_test.go") ; do
    echo "%%dir %%{gopath}/src/%%{import_path}/$(dirname $file)" >> devel.file-list
    install -d -p %{buildroot}%{gopath}/src/%{import_path}/$(dirname $file)
    cp -pav $file %{buildroot}%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> devel.file-list
done

sort -u -o devel.file-list devel.file-list

%files devel -f devel.file-list
%doc README
%license LICENSE
%dir %{gopath}/src/%{import_path}

%changelog
* Mon Aug  7 2017 mosquito <sensor.wen@gmail.com> - 0.1-1
- Initial package build
