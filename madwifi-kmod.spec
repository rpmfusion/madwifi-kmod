# buildforkernels macro hint: when you build a new version or a new release
# that contains bugfixes or other improvements then you must disable the
# "buildforkernels newest" macro for just that build; immediately after
# queuing that build enable the macro again for subsequent builds; that way
# a new akmod package will only get build when a new one is actually needed
%define buildforkernels newest

%define revision r3861-20080903
%define branch   hal-0.10.5.6

Name:           madwifi-kmod
Version:        0.9.4
Release:        60.%(echo %{revision}| tr - _)%{?dist}.7
Summary:        Kernel module for Atheros 802.11 wireless devices ar5210,ar5211 or ar5212

Group:          System Environment/Kernel
License:        GPLv2
URL:            http://www.madwifi.org/
Source0:        http://snapshots.madwifi.org/madwifi-%{branch}/madwifi-%{branch}-%{revision}.tar.gz
Source11:       madwifi-kmodtool-excludekernel-filterfile
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  sharutils
%define AkmodsBuildRequires sharutils

# needed for plague to make sure it builds for i586 and i686
ExclusiveArch:  i586 i686 x86_64 ppc
# ppc64 not supported

# get the needed BuildRequires (in parts depending on what we build for)
BuildRequires:  %{_bindir}/kmodtool
%{!?kernels:BuildRequires: buildsys-build-rpmfusion-kerneldevpkgs-%{?buildforkernels:%{buildforkernels}}%{!?buildforkernels:current}-%{_target_cpu} }
BuildRequires: kernel-devel
# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu} --repo rpmfusion --kmodname %{name} --filterfile %{SOURCE11} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description
This package contains the Multiband Atheros Driver for WiFi, a linux
device driver for 802.11a/b/g universal NIC cards - either Cardbus,
PCI or MiniPCI - that use Atheros chipsets (ar5210, ar5211, ar5212).

%prep
# error out if there was something wrong with kmodtool
%{?kmodtool_check}
# print kmodtool output for debugging purposes:
kmodtool  --target %{_target_cpu}  --repo rpmfusion --kmodname %{name} --filterfile %{SOURCE11} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null
%setup -q -c -T -a 0
#(cd madwifi-%{version} ; 
#sed -i -e 's|-Werror||' Makefile.inc
#)

for kernel_version  in %{?kernel_versions} ; do
    cp -a madwifi-%{branch}-%{revision} _kmod_build_${kernel_version%%___*}
done

%build
for kernel_version  in %{?kernel_versions} ; do
    pushd _kmod_build_${kernel_version%%___*}
    make KERNELPATH="${kernel_version##*___}" KERNELRELEASE="${kernel_version%%___*}" UUDECODE=/usr/bin/uudecode modules
    popd
done


%install
rm -rf $RPM_BUILD_ROOT
for kernel_version  in %{?kernel_versions} ; do
    make -C _kmod_build_${kernel_version%%___*} KERNELPATH="${kernel_version##*___}"  KERNELRELEASE="${kernel_version%%___*}" UUDECODE=/usr/bin/uudecode DESTDIR=$RPM_BUILD_ROOT KMODPATH=%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix} install-modules 
	chmod 0755 $RPM_BUILD_ROOT/%{kmodinstdir_prefix}/*/%{kmodinstdir_postfix}/*
done

%{?akmod_install}


%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Tue Nov 18 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.9.4-60.r3861_20080903.7
- rebuild for latest Fedora kernel;

* Fri Nov 14 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.9.4-60.r3861_20080903.6
- rebuild for latest Fedora kernel;

* Sun Nov 09 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.9.4-60.r3861_20080903.5
- rebuild for latest Fedora kernel;

* Sun Nov 02 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.9.4-60.r3861_20080903.4
- rebuild for latest rawhide kernel;

* Sun Oct 26 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.9.4-60.r3861_20080903.3
- rebuild for latest rawhide kernel; enable ppc again

* Sun Oct 19 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.9.4-60.r3861_20080903.2
- rebuild for latest rawhide kernel

* Sat Oct 04 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0.9.4-60.r3861-20080903.1
- disable ppc and ppc64

* Tue Sep 30 2008 kwizart < kwizart at gmail.com > - 0.9.4-60.r3861-20080903
- Move from trunk to hal-0.10.5.6 with r3861-20080903

* Tue Sep 30 2008 kwizart < kwizart at gmail.com > - 0.9.4-50.r3867-20080924
- Update to r3867-20080924

* Tue Jul 15 2008 kwizart < kwizart at gmail.com > - 0.9.4-48.r3771-20080715
- Build for akmod

* Tue Jul 15 2008 kwizart < kwizart at gmail.com > - 0.9.4-47.r3771-20080715
- Update snapshot to r3771-20080715 and bump

* Sun May 04 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0.9.4-31
- fix typo

* Sun May 04 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0.9.4-30
- build for f9

* Sat Feb 23 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0.9.4-2
- add "AkmodsBuildRequires sharutils"; that way the akmod.rpm will 
  require sharutils, which is a BR for the kmod.srpm

* Wed Feb 13 2008 kwizart < kwizart at gmail.com > - 0.9.4-1
- Update to 0.9.4

* Sat Jan 26 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0.9.3.3-31
- rebuild for new kmodtools, akmod adjustments

* Sun Jan 20 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0.9.3.3-30
- build akmods package

* Thu Dec 20 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0.9.3.3-12
- rebuilt for 2.6.21-2952.fc8xen 2.6.23.9-85.fc8

* Mon Dec 03 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0.9.3.3-11
- rebuilt for 2.6.23.8-63.fc8 2.6.21-2952.fc8xen

* Sat Nov 10 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0.9.3.3-10
- rebuilt for 2.6.23.1-49.fc8

* Mon Nov 05 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0.9.3.3-9
- rebuilt for F8 kernels

* Wed Oct 31 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0.9.3.3-8
- rebuilt for latest kernels

* Tue Oct 30 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0.9.3.3-7
- rebuilt for latest kernels

* Sat Oct 27 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0.9.3.3-6
- rebuilt for latest kernels
- adjust to rpmfusion and new kmodtool

* Sat Oct 27 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0.9.3.3-5
- rebuilt for latest kernels

* Tue Oct 23 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0.9.3.3-4
- rebuilt for latest kernels

* Mon Oct 22 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0.9.3.3-3
- rebuilt for latest kernels

* Thu Oct 18 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0.9.3.3-2
- rebuilt for latest kernels

* Thu Oct 18 2007 kwizart < kwizart at gmail.com > - 0.9.3.3-1
- Update to 0.9.3.3
- Drop inj. patch.
- Security bugfix: http://bugzilla.livna.org/show_bug.cgi?id=1675
  CVE-2007-5448: madwifi assertion error DoS

* Thu Oct 18 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0.9.3.2-9
- rebuilt for latest kernels

* Fri Oct 12 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0.9.3.2-8
- rebuilt for latest kernels

* Thu Oct 11 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0.9.3.2-7
- rebuilt for latest kernels

* Wed Oct 10 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0.9.3.2-6
- rebuilt for latest kernels

* Tue Oct 09 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> 0.9.3.2-5
- rebuilt for latest kernels

* Sun Oct 07 2007 Thorsten Leemhuis <fedora AT leemhuis DOT info> 
- build for rawhide kernels as of today

* Wed Oct 03 2007 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0.9.3.2-3
- update for new kmod-helper stuff
- build for newest kernels

* Sun Sep 09 2007 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0.9.3.2-2
- Build for latest only

* Sun Sep 09 2007 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0.9.3.2-1
- Convert to new kmods stuff from livna for testing it
- Rebuild for F8T2 and rawhide

* Thu Jul 26 2007 Dams <anvil[AT]livna.org> - 0.9.3.1-2
- Added 2.6.22 compatibility patch

* Wed May 23 2007 Dams <anvil[AT]livna.org> - 0.9.3.1-1
- Updated to 0.9.3.1

* Mon Mar 19 2007 Dams <anvil[AT]livna.org> - 0.9.3-1
- Updated to 0.9.3
- Dropped patch0 & 1
- Added new Patch2 to make aircrack to build

* Sun Jan 21 2007 Dams <anvil[AT]livna.org> - 0.9.2.1-2
- Fixed 2.6.19 build

* Fri Dec  8 2006 Dams <anvil[AT]livna.org> - 0.9.2.1-1
- Updated to upstream 0.9.2.1

* Sat Oct 07 2006 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0.9.2-2
- sed-away the config.h include

* Sat Aug 19 2006 Dams <anvil[AT]livna.org> - 0.9.2-2
- ppc added to ExclusiveArch

* Fri Aug 18 2006 Dams <anvil[AT]livna.org> - 0.9.2-1
- Updated to 0.9.2

* Sun Jun 11 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.0.0.20060520-7
- Invoke kmodtool with bash instead of sh.

* Sat May 20 2006 Dams <anvil[AT]livna.org> - 0.0.0.20060520-6
- Updated snapshot to 20060520

* Sun May 14 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.0.0.20060317-5
- Require version >= of madwifi-kmod-common.
- Provide madwifi-kmod instead of kmod-madwifi to fix upgrade woes (#970).

* Thu Apr 27 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.0.0.20060317-4
- Provide "kernel-modules" instead of "kernel-module" to match yum's config.

* Tue Mar 27 2006 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> 0.0.0.20060317-3
- small adjustments to kmod specific tasks
- update kmodtool to 0.10.6

* Sat Mar 18 2006 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> 0.0.0.20060317-2
- disable xenU build; no wireless extensions in xenU!

* Sat Mar 18 2006 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> 0.0.0.20060317-1
- move 20060317 from release to version

* Sat Mar 18 2006 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> 0.lvn.15.20060317
- update to 20060317
- build for ppc, too; no, don't, does not build
- drop 0.lvn
- hardcode kversion

* Sat Feb 11 2006 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> 0.lvn.15.20060211
- split into packages for userland and kmod

* Sat Dec 03 2005 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> 0.lvn.11.20051130
- fix uudecode on fc3 by passing UUDECODE=/usr/bin/uudecode to make

* Sat Dec 03 2005 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> 0.lvn.10.20051130
- Update to 2005-11-30

* Sat Nov 19 2005 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> 0.lvn.9.20051114
- Update to 2005-11-14 from madwifi.org (madwifi-ng)

* Sat Nov 12 2005 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> 0.lvn.8.20051112
- Update to 2005-11-12

* Sat Sep 17 2005 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> 0.lvn.7.20050917
- Update to 2005-09-17

* Wed Jul 20 2005 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> 0.0-0.lvn.6.20050715
- Avoid the check for kernel-patch and kernel-config on i386 if we only build
  userland

* Fri Jul 15 2005 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> 0.0-0.lvn.5.20050715
- Update to 2005-07-15 (after merge of BSD branch)

* Sat Jul 09 2005 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> 0.0-0.lvn.4.20050709
- Update to 2005-07-09
- Support x86_64
- adjust kernel-build stuff to current livna scheme
- drop tools subpackage, just use the name "madwifi"

* Sun Jan 23 2005 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> 0.0-0.lvn.3.20050220
- Update to 2005-02-20
- ExclusivArch %%{ix86} for now
- Build tools also as suggested in #355 my Michael A. Peters 
  <funkyres [AT] gmail [DOT] com>  

* Sun Jan 23 2005 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> 0.0-0.lvn.3.20041229
- Update to 20041229 on recommendation by Gianluca Sforna

* Sun Jan 09 2005 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> 0.0-0.lvn.2.20041127
- BR sharutils (thanks Gianluca Sforna for catching this bug)

* Fri Nov 26 2004 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> 0.0-0.lvn.1.20041127
- Initial Version
- Applied Ville Skyttä's nameing scheme from bash-completion
- Used cvs-snapshot web-location mentioned on Homepage as source
- Cause of the issue with the included HAL I choosed livna as repo.
   For details on the HAL and its distribution see:
   http://www.mattfoster.clara.co.uk/madwifi-5.htm
