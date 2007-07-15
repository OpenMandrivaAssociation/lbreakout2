%define	name		lbreakout2
%define	version		2.6
%define	real_version	2.6beta-5
%define release		%mkrel 0.beta5.2

# getting latest levelset ?
%define __fetch_levels 0
%{?_fetch_levels: %{expand: %%define __fetch_levels 1}}

Summary:	Breakout-style arcade game
Name:		%{name}
Version:	%{version}
Release:	%{release}
Url:		http://lgames.sourceforge.net/
Source0:	http://ftp1.sourceforge.net/lgames/%{name}-%{real_version}.tar.bz2
Source1:	levelsets.tar.bz2
Source5:	%{name}-16.png
Source6:	%{name}-32.png
Source7:	%{name}-48.png
#Patch0:	lbreakout2-2.3.2-fix-FPE.patch.bz2
License:	GPL
Group:		Games/Arcade
BuildRequires:	SDL_mixer-devel
BuildRequires:	esound-devel
BuildRequires:	libpng-devel
BuildRequires:	texinfo
%if %__fetch_levels
BuildRequires:	wget
%endif
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
LBreakout is a classical Breakout game and this means (if you like Breakout ;-)
it is a lot of fun to play!
If you never ever played such a game you can check out the manual for more
information, take a look at the screenshots and last but not least... play it!

%prep
%setup -q -n %{name}-%{real_version}
#%patch0 -p1

# getting latest levelsets
%if %{__fetch_levels}
cd %{_tmppath}
wget http://lgames.sourceforge.net/LBreakout2/levels/levelsets.tar.gz
zcat levelsets.tar.gz | bzip2 > %{SOURCE1}
rm -f levelsets.tar.gz
%endif

%build
%configure	--bindir=%{_gamesbindir} \
		--datadir=%{_gamesdatadir} \
		--localstatedir=%{_localstatedir}/games
%make

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_localstatedir}/games
%{makeinstall_std}

mv $RPM_BUILD_ROOT%{_gamesdatadir}/locale $RPM_BUILD_ROOT%{_datadir}

tar xjC $RPM_BUILD_ROOT%{_datadir}/games/%{name}/levels -f %SOURCE1

mkdir -p $RPM_BUILD_ROOT%{_menudir}/
cat > %buildroot%{_menudir}/%{name} <<EOF
?package(%name):needs=x11 section="More Applications/Games/Arcade" \
title="LBreakout 2" longtitle="Breakout-style arcade game" \
command="%{_gamesbindir}/lbreakout2" icon="lbreakout2.png" xdg="true"
EOF

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Encoding=UTF-8
Name=LBreakout 2
Comment=%{summary}
Exec=%_gamesbindir/%{name}
Icon=%{name}
Terminal=false
Type=Application
Categories=Game;ArcadeGame;X-MandrivaLinux-MoreApplications-Games-Arcade;
EOF

install -D -m644 %SOURCE6 $RPM_BUILD_ROOT%{_iconsdir}/%{name}.png
install -D -m644 %SOURCE5 $RPM_BUILD_ROOT%{_miconsdir}/%{name}.png
install -D -m644 %SOURCE7 $RPM_BUILD_ROOT%{_liconsdir}/%{name}.png

rm -rf $RPM_BUILD_ROOT/usr/doc # those docs are not wanted

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{update_menus}

%postun
%{clean_menus}

%files -f %{name}.lang
%defattr(-,root,root)
%doc README TODO
# %attr(2755, root, games) 
%{_gamesbindir}/*
%attr(664, root, games) %{_localstatedir}/games/*
%{_gamesdatadir}/%{name}
%{_datadir}/applications/*
%{_menudir}/%{name}
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
