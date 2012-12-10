%define name	ExEf
%define version 1.70
%define release %mkrel 7

Summary:   Real-time audio effects processor
Name:      %{name}
Version:   %{version}
Release:   %{release}
Source0:   %{name}.tar.bz2
Source1:   robots.tar.bz2
Source2:   %{name}16.png.bz2
Source3:   %{name}32.png.bz2
Source4:   %{name}48.png.bz2
Patch0:    ExEf-fix-str-fmt.patch
BuildRoot: %{_tmppath}/%{name}-root
License:   GPL
Group:     Sound
URL:	   http://twinstar.hobby.cz/exef/
Requires:  tcl, tk

%description
ExEf (Extreme Effect) is an extremely powerful and flexible Real Time
effect engine. It is designed to work with guitars, microphones and
other instruments. It can run both in X Window System and command line.

%prep
%setup -T -b 0 -qn %{name}-V116
%setup -T -D -a 1 -qn %{name}-V116
%patch0 -p0

# Make package relocatable
for FILE in ExEf ExEfDSP.c ; do

    sed "s|/usr/share|%{_datadir}| ; s|/usr/bin|%{_bindir}|" < ./${FILE} > ${FILE}.tmp
    mv ./${FILE}.tmp ${FILE}

done

gcc ExEfDSP.c %optflags -lm -o ExEfDSP

%install
install -d ${RPM_BUILD_ROOT}%{_bindir}
install -d ${RPM_BUILD_ROOT}%{_datadir}/ExEf

install -m 755 ExEf ExEfDSP ${RPM_BUILD_ROOT}%{_bindir}
cp -f ExEflogo.gif .ExEfrc ${RPM_BUILD_ROOT}%{_datadir}/ExEf
cp -R configs ${RPM_BUILD_ROOT}%{_datadir}/ExEf
cp -f robots/* ${RPM_BUILD_ROOT}%{_datadir}/ExEf/configs

#
# Icons
install -d ${RPM_BUILD_ROOT}{%_miconsdir,%_liconsdir}
bzcat %{SOURCE2} > ${RPM_BUILD_ROOT}%{_miconsdir}/%name.png
bzcat %{SOURCE3} > ${RPM_BUILD_ROOT}%{_iconsdir}/%name.png
bzcat %{SOURCE4} > ${RPM_BUILD_ROOT}%{_liconsdir}/%name.png


mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=ExEf
Comment=Real-time audio effects processor
Exec=%{_bindir}/%{name}
Icon=%{name}
Terminal=false
Type=Application
Categories=AudioVideo;Audio;
EOF

%clean
rm -rf ${RPM_BUILD_ROOT}

%if %mdkversion < 200900
%post
%{update_menus}
%endif

%if %mdkversion < 200900
%postun
%{clean_menus}
%endif

%files
%defattr(-,root,root,755)
%doc COPYING
%{_bindir}/*
%dir %{_datadir}/ExEf
%{_datadir}/ExEf/*
%{_datadir}/ExEf/.ExEfrc
%{_datadir}/applications/mandriva-%{name}.desktop
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png


%changelog
* Sun Dec 05 2010 Oden Eriksson <oeriksson@mandriva.com> 1.70-7mdv2011.0
+ Revision: 610402
- rebuild

* Sat May 01 2010 Funda Wang <fwang@mandriva.org> 1.70-6mdv2010.1
+ Revision: 541464
- fix str fmt

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

* Thu Jul 24 2008 Thierry Vignaud <tv@mandriva.org> 1.70-5mdv2009.0
+ Revision: 244997
- rebuild

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

* Mon Feb 18 2008 Thierry Vignaud <tv@mandriva.org> 1.70-3mdv2008.1
+ Revision: 170822
- rebuild
- fix "foobar is blabla" summary (=> "blabla") so that it looks nice in rpmdrake
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Sun Sep 16 2007 Emmanuel Andry <eandry@mandriva.org> 1.70-2mdv2008.0
+ Revision: 88675
- drop old menu
- xdg menu
- Import ExEf



* Sun Jan 22 2006 Emmanuel Andry <eandry@free.fr> 1.70-1mdk
- New release 1.70
- mkrel

* Fri May 13 2005 Nicolas Lécureuil <neoclust@mandriva.org> 1.16-3mdk
- Rebuild

* Fri Feb 20 2004 David Baudens <baudens@mandrakesoft.com> 1.16-2mdk
- Remove broken menu entry (Documentation)

* Mon Mar 10 2003 Marcel Pol <mpol@gmx.net> 1.16-1mdk
- 1.16

* Mon Mar 10 2003 Marcel Pol <mpol@gmx.net> 1.14-2mdk
- club => contrib

* Tue Dec 10 2002 Maxim Heijndijk <cchq@wanadoo.nl> 1.14-1mdk
- Initial wrap.
