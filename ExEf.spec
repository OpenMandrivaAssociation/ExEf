Summary:   Real-time audio effects processor
Name:      ExEf
Version:   1.70
Release:   10
Source0:   %{name}.tar.bz2
Source1:   robots.tar.bz2
Source2:   %{name}16.png.bz2
Source3:   %{name}32.png.bz2
Source4:   %{name}48.png.bz2
Patch0:    ExEf-fix-str-fmt.patch
License:   GPL
Group:     Sound
URL:	   https://twinstar.hobby.cz/exef/
Requires:  tcl, tk
Requires:  pulseaudio-utils

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

gcc ExEfDSP.c %{optflags} -lm -o ExEfDSP.bin
mv ExEf ExEf.bin

%install
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_datadir}/ExEf

install -m 755 ExEf.bin ExEfDSP.bin %{buildroot}%{_bindir}
cp -f ExEflogo.gif .ExEfrc %{buildroot}%{_datadir}/ExEf
cp -R configs %{buildroot}%{_datadir}/ExEf
cp -f robots/* %{buildroot}%{_datadir}/ExEf/configs

#
# Icons
install -d %{buildroot}{%{_miconsdir},%{_liconsdir}}
bzcat %{SOURCE2} > %{buildroot}%{_miconsdir}/%{name}.png
bzcat %{SOURCE3} > %{buildroot}%{_iconsdir}/%{name}.png
bzcat %{SOURCE4} > %{buildroot}%{_liconsdir}/%{name}.png

# Wrappers to launch real application binaries using 'padsp'
cat > %{buildroot}%{_bindir}/ExEf << EOF
#!/bin/bash

padsp /usr/bin/ExEf.bin
EOF

cat > %{buildroot}%{_bindir}/ExEfDSP << EOF
#!/bin/bash

padsp /usr/bin/ExEfDSP.bin
EOF

chmod a+x %{buildroot}%{_bindir}/ExEfDSP %{buildroot}%{_bindir}/ExEf

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/rosa-%{name}.desktop << EOF
[Desktop Entry]
Name=ExEf
Name[ru]=ExEf
Comment=Real-time audio effects processor
Comment[ru]=Гитарный процессор реального времени
Exec=%{_bindir}/%{name}
Icon=%{name}
Terminal=false
Type=Application
Categories=AudioVideo;Audio;
EOF

%files
%defattr(-,root,root,755)
%doc COPYING
%{_bindir}/*
%dir %{_datadir}/ExEf
%{_datadir}/ExEf/*
%{_datadir}/ExEf/.ExEfrc
%{_datadir}/applications/rosa-%{name}.desktop
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png


