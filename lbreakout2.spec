%define levelsets	20160512

# getting latest levelset ?
%bcond_with	fetch_levels

Summary:	Breakout-style arcade game
Name:		lbreakout2
Version:	2.6.5
Release:	1
License:	GPLv2
Group:		Games/Arcade
Url:		http://lgames.sourceforge.net/
Source0:	http://download.sourceforge.net/lgames/%{name}-%{version}.tar.gz
Source1:	http://download.sourceforge.net/lgames/%{name}-levelsets-%{levelsets}.tar.gz
Source5:	%{name}-16.png
Source6:	%{name}-32.png
Source7:	%{name}-48.png
BuildRequires:	pkgconfig(SDL_mixer)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	texinfo
%if %{with fetch_levels}
BuildRequires:	wget
%endif

%description
LBreakout is a classical Breakout game and this means (if you like Breakout ;-)
it is a lot of fun to play!
If you never ever played such a game you can check out the manual for more
information, take a look at the screenshots and last but not least... play it!

%prep
%setup -q

# getting latest levelsets
%if %{with fetch_levels}
wget http://lgames.sourceforge.net/LBreakout2/levels/levelsets.tar.gz
mv levelsets.tar.gz %{SOURCE1}
%endif

%build
%configure2_5x	--bindir=%{_gamesbindir} \
		--with-libiconv-prefix=%{_prefix} \
		--without-included-gettext \
		--with-libintl-prefix=%{_prefix} \
		--localstatedir=%{_localstatedir}/lib/games
%make

%install
install -d %{buildroot}%{_localstatedir}/lib/games
%makeinstall_std

tar -xf %{SOURCE1} -C %{buildroot}%{_datadir}/%{name}/levels

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=LBreakout 2
Comment=Breakout-style arcade game
Exec=%{_gamesbindir}/%{name}
Icon=%{name}
Terminal=false
Type=Application
Categories=Game;ArcadeGame;
EOF

install -D -m644 %{SOURCE5} %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png
install -D -m644 %{SOURCE6} %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
install -D -m644 %{SOURCE7} %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png

# those docs are not wanted
rm -r %{buildroot}%{_docdir}

# remove ugly default desktop file, use our own
rm -r %{buildroot}%{_datadir}/applications/%{name}.desktop

%find_lang %{name}

%files -f %{name}.lang
%doc README TODO
%attr(2755, root, games) %{_gamesbindir}/%{name}
%attr(2755, root, games) %{_gamesbindir}/%{name}server
%config(noreplace) %attr(664, games, games) %{_localstatedir}/lib/games/*
%{_datadir}/%{name}
%{_datadir}/applications/mandriva-%{name}.desktop
%{_iconsdir}/hicolor/16x16/apps/%{name}.png
%{_iconsdir}/hicolor/32x32/apps/%{name}.png
%{_iconsdir}/hicolor/48x48/apps/%{name}.png
%{_iconsdir}/lbreakout48.gif
