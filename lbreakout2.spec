%define	name		lbreakout2
%define	version		2.6.1
%define beta 		0
%define levelsets	20091026
%define rel		1
%if %beta
%define release		%mkrel -c beta%{beta} %rel
%else
%define release		%mkrel %rel
%endif

# getting latest levelset ?
%define __fetch_levels 0
%{?_fetch_levels: %{expand: %%define __fetch_levels 1}}

Summary:	Breakout-style arcade game
Name:		%{name}
Version:	%{version}
Release:	%{release}
Url:		http://lgames.sourceforge.net/
%if %beta
Source0:	http://ftp1.sourceforge.net/lgames/%{name}-%{version}beta-%{beta}.tar.gz
%else
Source0:	http://ftp1.sourceforge.net/lgames/%{name}-%{version}.tar.gz
%endif
Source1:	http://ftp1.sourceforge.net/lgames/%{name}-levelsets-%{levelsets}.tar.gz
Source5:	%{name}-16.png
Source6:	%{name}-32.png
Source7:	%{name}-48.png
Source8: 	fr_ascii.po
License:	GPLv2
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
%if %beta
%setup -q -n %{name}-%{version}beta-%{beta}
%else
%setup -q
%endif

# getting latest levelsets
%if %{__fetch_levels}
cd %{_tmppath}
wget http://lgames.sourceforge.net/LBreakout2/levels/levelsets.tar.gz
zcat levelsets.tar.gz | bzip2 > %{SOURCE1}
rm -f levelsets.tar.gz
%endif

%build
# replace french translation file because lbreakout2 doesn't like accented letters
cp -f %SOURCE8 po/fr.po 
msgfmt po/fr.po -o po/fr.gmo

%configure2_5x	--bindir=%{_gamesbindir} \
		--with-libiconv-prefix=%{_prefix} \
		--without-included-gettext \
		--with-libintl-prefix=%{_prefix} \
		--localstatedir=%{_localstatedir}/lib/games
%make

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_localstatedir}/lib/games
%{makeinstall_std}

tar xzC $RPM_BUILD_ROOT%{_datadir}/%{name}/levels -f %SOURCE1

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=LBreakout 2
Comment=Breakout-style arcade game
Exec=%_gamesbindir/%{name}
Icon=%{name}
Terminal=false
Type=Application
Categories=Game;ArcadeGame;
EOF

install -D -m644 %SOURCE5 $RPM_BUILD_ROOT%{_iconsdir}/hicolor/16x16/apps/%{name}.png
install -D -m644 %SOURCE6 $RPM_BUILD_ROOT%{_iconsdir}/hicolor/32x32/apps/%{name}.png
install -D -m644 %SOURCE7 $RPM_BUILD_ROOT%{_iconsdir}/hicolor/48x48/apps/%{name}.png

rm -rf $RPM_BUILD_ROOT/usr/doc # those docs are not wanted

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%if %mdkversion < 200900
%post
%{update_menus}
%update_icon_cache hicolor
%endif

%if %mdkversion < 200900
%postun
%{clean_menus}
%clean_icon_cache hicolor
%endif

%files -f %{name}.lang
%defattr(-,root,root)
%doc README TODO
%{_gamesbindir}/*
%attr(664, root, games) %{_localstatedir}/lib/games/*
%{_datadir}/%{name}
%{_datadir}/applications/*
%{_iconsdir}/hicolor/16x16/apps/%{name}.png
%{_iconsdir}/hicolor/32x32/apps/%{name}.png
%{_iconsdir}/hicolor/48x48/apps/%{name}.png
%{_iconsdir}/lbreakout48.gif
