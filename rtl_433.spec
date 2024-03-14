%global         github_owner merbanan
%global         github_name  rtl_433
%global         github_commit 3db192c458cd879571fa323a4eedec1a59e76b6a
%global         debug_package %{nil}
%define         build_timestamp %(date +"%Y%m%d")

Name:           %{github_name}
Version:        %{build_timestamp}
Release:        %{github_commit}
Summary:        Program to decode radio transmissions from devices on the ISM bands (and other frequencies)
License:        GPL-2.0-only

URL:            https://github.com/%{github_owner}/%{github_name}
Source0:        https://github.com/%{github_owner}/%{github_name}/archive/%{github_commit}/%{name}-%{github_commit}.tar.gz

BuildRequires: cmake
BuildRequires: libusb1-devel
BuildRequires: rtl-sdr-devel
BuildRequires: make
BuildRequires: gcc-c++
BuildRequires: ninja-build

Requires:      rtl-sdr-devel

%description
Program to decode radio transmissions from devices on the ISM bands (and other frequencies)

%prep
%setup -n %{name}-%{github_commit}

%build
cmake -DFORCE_COLORED_BUILD:BOOL=ON -GNinja -B build
cmake --build build -j 4

%install
# The do_build.sh does not output to _bindir.
install -p -D -m 755 ./build/src/rtl_433 %{buildroot}%{_bindir}/rtl_433

%files
%license COPYING
%doc AUTHORS README.md
%{_bindir}/rtl_433

%changelog
* Sat Apr 11 2020 Thomas Vassilian <tvassili@redhat.com> - 1-1
- initial build for fc31

* Jeu mar 14 2024 Thomas Vassilian <thomas.vassilian@gmail.com> - 1-2
- included build steps as script is now removed
