%define name	ExEf
%define version 1.70
%define release %mkrel 3

Summary:   Real-time audio effects processor
Name:      %{name}
Version:   %{version}
Release:   %{release}
Source0:   %{name}.tar.bz2
Source1:   robots.tar.bz2
Source2:   %{name}16.png.bz2
Source3:   %{name}32.png.bz2
Source4:   %{name}48.png.bz2
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
rm -rf ${RPM_BUILD_ROOT}

%setup -T -b 0 -n %{name}-V116
%setup -T -D -a 1 -n %{name}-V116

# Make package relocatable
for FILE in ExEf ExEfDSP.c ; do

    sed "s|/usr/share|%{_datadir}| ; s|/usr/bin|%{_bindir}|" < ./${FILE} > ${FILE}.tmp
    mv ./${FILE}.tmp ${FILE}

done

gcc ExEfDSP.c ${RPM_OPT_FLAGS} -lm -o ExEfDSP

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
Comment=%{Summary}
Exec=%{_bindir}/%{name}
Icon=%{name}
Terminal=false
Type=Application
Categories=AudioVideo;Video
Encoding=UTF-8
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
