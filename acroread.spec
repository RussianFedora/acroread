%define acroread_inst_dir %{_libdir}

Summary:        Adobe Reader for PDF Files
Name:           acroread
Version:        9.4.2
Release:        1%{?dist}.R

URL:            http://www.adobe.com/products/acrobat/readermain.html
License:        Any commercial
Group:          Applications/Publishing
Source0:        http://ardownload.adobe.com/pub/adobe/reader/unix/9.x/%{version}/enu/AdbeRdr%{version}-1_i486linux_enu.rpm
Source10:       acroread.desktop
Source20:       acroread.png
Source30:	reader_prefs
Source31:	adobe.conf
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Provides:       libACE.so libACE.so(VERSION) libAGM.so libAGM.so(VERSION)
Provides:       libBIB.so libBIB.so(VERSION) libBIBUtils.so libBIBUtils.so(VERSION)
Provides:       libCoolType.so libCoolType.so(VERSION) libResAccess.so
Provides:       libWRServices.so libadobelinguistic.so

Requires:	/usr/lib/gtk-2.0/modules/libcanberra-gtk-module.so
Requires:	/usr/lib/gtk-2.0/modules/libpk-gtk-module.so
Requires:	/usr/lib/gtk-2.0/modules/libatk-bridge.so
Requires:	/usr/lib/gtk-2.0/2.10.0/engines/libclearlooks.so

ExclusiveArch:  %{ix86}


%description
Acroread is a well known PDF viewer.

Adobe Reader is often the only program able to process complicated PDF
files, such as PDF forms. However, there are many bugs where we cannot
do anything about because it is proprietary binary-only software.

Please consider whether it is possible to use free PDF readers like
okular, evince, xpdf, ghostview, ... instead.


%package mozplugin
Summary:	Mozilla plugin for Adobe Reader
Group:		Applications/Internet
Requires:	%{name} = %{version}-%{release}
Requires:	install-nspluginwrapper
BuildArch:	noarch


%description mozplugin
Acroread is a well known PDF viewer.

Adobe Reader is often the only program able to process complicated PDF
files, such as PDF forms. However, there are many bugs where we cannot
do anything about because it is proprietary binary-only software.

Please consider whether it is possible to use free PDF readers like
okular, evince, xpdf, ghostview, ... instead.


%prep
%setup -q -c -T


%build


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}
pushd %{buildroot}
rpm2cpio %{SOURCE0} | cpio -idV --quiet
mv opt usr
mkdir -p usr/lib/Adobe
mv usr/Adobe/* usr/lib/Adobe
rmdir usr/Adobe
popd

mkdir -p %{buildroot}/usr/bin
pushd %{buildroot}/usr/bin
   ln -sf ../../%{acroread_inst_dir}/Adobe/Reader9/bin/acroread acroread
popd

# add a link for the browser plugin so that it can be found automatically
mkdir -p %{buildroot}%{_libdir}/mozilla/plugins
ln -sf %{acroread_inst_dir}/Adobe/Reader9/Browser/intellinux/nppdf.so %{buildroot}%{_libdir}/mozilla/plugins/nppdf.so

install -d %{buildroot}/usr/share/pixmaps
install -m644 %{SOURCE20} %{buildroot}/usr/share/pixmaps/acroread.png

install -d %{buildroot}/usr/share/applications
install -m644 %{SOURCE10} %{buildroot}/usr/share/applications
install -m644 %{SOURCE30} %{buildroot}/usr/lib/Adobe/Reader9/Reader/GlobalPrefs/

install -dD %{buildroot}/etc/ld.so.conf.d/
install -m644 %{SOURCE31} %{buildroot}/etc/ld.so.conf.d/


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%clean
rm -rf %{buildroot}


%files 
%defattr(-,root,root)
%{_bindir}/acroread
%{_sysconfdir}/ld.so.conf.d/*.conf
%{_libdir}/Adobe/*
%{_datadir}/pixmaps/acroread.png
%{_datadir}/applications/%{name}.desktop


%files mozplugin
%defattr(-,root,root)
%{_libdir}/mozilla/plugins/nppdf.so


%changelog
* Thu Jul 21 2011 Vasiliy N. Glazov <vascom2@gmail.com> - 9.4.2-1.R
- update to 9.4.2

* Fri Dec 17 2010 Arkady L. Shane <ashejn@yandex-team.ru> - 9.4-1
- update to 9.4
- do not require nspluginwrapper

* Mon Oct  4 2010 Arkady L. Shane <ashejn@yandex-team.ru> - 9.3.4-1
- update to 9.3.4
- added separate package for mozilla plugin
- added new Requires for compat with i686 on 64bit platform

* Mon Jun 29 2009 Arkady L. Shane <ashejn@yandex-team.ru> - 9.1.0-2
- update to 9.1.1

* Tue Apr 28 2009 Arkady L. Shane <ashejn@yandex-team.ru> - 9.1.0-2
- added proper config
- added more requires
- added ld config for libraries

* Wed Apr 15 2009 Arkady L. Shane <ashejn@yandex-team.ru> - 9.1.0-1
- initial build for Fedora
