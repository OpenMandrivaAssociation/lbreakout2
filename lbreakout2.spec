%define	name		lbreakout2
%define	version		2.6.3
%define beta 		0
%define levelsets	20100920
%define rel		3
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
Source0:	http://download.sourceforge.net/lgames/%{name}-%{version}beta-%{beta}.tar.gz
%else
Source0:	http://download.sourceforge.net/lgames/%{name}-%{version}.tar.xz
%endif
Source1:	http://download.sourceforge.net/lgames/%{name}-levelsets-%{levelsets}.tar.gz
Source5:	%{name}-16.png
Source6:	%{name}-32.png
Source7:	%{name}-48.png
License:	GPLv2
Group:		Games/Arcade
BuildRequires:	SDL_mixer-devel
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


%changelog
* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 2.6.3-2mdv2011.0
+ Revision: 666061
- mass rebuild

* Tue Mar 08 2011 Zombie Ryushu <ryushu@mandriva.org> 2.6.3-1
+ Revision: 642959
- Upgrade to 2.6.3

* Wed Oct 06 2010 Funda Wang <fwang@mandriva.org> 2.6.2-1mdv2011.0
+ Revision: 583445
- new version 2.6.2

* Fri Dec 25 2009 Frederik Himpe <fhimpe@mandriva.org> 2.6.1-1mdv2010.1
+ Revision: 482292
- Update to new version 2.6.1

* Sat Nov 07 2009 Frederik Himpe <fhimpe@mandriva.org> 2.6-1mdv2010.1
+ Revision: 462294
- Update to new version 2.6
- Update levelsets to new version 20091026

* Thu Aug 27 2009 Samuel Verschelde <stormi@mandriva.org> 2.6-0.beta7.7mdv2010.0
+ Revision: 421721
- better french translation, still without accented letters

* Wed Aug 26 2009 Samuel Verschelde <stormi@mandriva.org> 2.6-0.beta7.6mdv2010.0
+ Revision: 421311
- remove accented letters from french translation, and fix some strings (bug #49275)

* Sat Mar 07 2009 Antoine Ginies <aginies@mandriva.com> 2.6-0.beta7.5mdv2009.1
+ Revision: 351346
- rebuild

* Fri Aug 22 2008 Funda Wang <fwang@mandriva.org> 2.6-0.beta7.4mdv2009.0
+ Revision: 275045
- move to /usr/share/data

* Thu Aug 21 2008 Funda Wang <fwang@mandriva.org> 2.6-0.beta7.3mdv2009.0
+ Revision: 274631
- fix intlbuild

* Thu Jun 12 2008 Pixel <pixel@mandriva.com> 2.6-0.beta7.2mdv2009.0
+ Revision: 218422
- rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas
- adapt to %%_localstatedir now being /var instead of /var/lib (#22312)

* Sun Jan 13 2008 Thierry Vignaud <tv@mandriva.org> 2.6-0.beta7.2mdv2008.1
+ Revision: 150438
- rebuild
- kill re-definition of %%buildroot on Pixel's request
- kill desktop-file-validate's 'warning: key "Encoding" in group "Desktop Entry" is deprecated'

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Thu Aug 23 2007 Funda Wang <fwang@mandriva.org> 2.6-0.beta7.2mdv2008.0
+ Revision: 70709
- fix comment of desktop file

* Sun Jul 15 2007 Adam Williamson <awilliamson@mandriva.org> 2.6-0.beta7.1mdv2008.0
+ Revision: 52301
- don't try and unbzip a gzip file...
- switch to fd.o icons
- drop old menu and X-Mandriva menu category
- specify GPLv2 as license
- clean spec
- update level sets
- new release 2.6 beta 7
- Import lbreakout2



* Fri Jul  7 2006 Pixel <pixel@mandriva.com> 2.6-0.beta5.2mdv2007.0
- use mkrel
- switch to XDG menu

* Wed Jan 11 2006 Pixel <pixel@mandriva.com> 2.6-0.beta5.1mdk
- for now, disable writing highscore (segfault hopefully fixed in next beta)
- new beta
- add i18n

* Wed Jan 11 2006 Pixel <pixel@mandriva.com> 2.6-0.beta.3mdk
- i don't think one should get new levels by default
  (otherwise one can't get the same resulting rpm)

* Sat Dec 31 2005 Mandriva Linux Team <http://www.mandrivaexpert.com/> 2.6-0.beta.2mdk
- Rebuild

* Fri Jul 01 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 2.6-0.beta.1mdk
- 2.6beta

* Fri Jan 14 2005 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 2.5.2-1mdk
- 2.5.2

* Thu Nov 11 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 2.5.1-1mdk
- 2.5.1

* Mon Aug 16 2004 Laurent MONTEL <lmontel@mandrakesoft.com> 2.5-2mdk
- Rebuild with new menu

* Sun Aug 08 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 2.5-1mdk
- 2.5
- cosmetics
- drop P0

* Tue Jul 15 2003 Götz Waschk <waschk@linux-mandrake.com> 2.4.1-3mdk
- move menu to the spec file
- move files to the game-specific dirs 

* Mon Jul 14 2003 Götz Waschk <waschk@linux-mandrake.com> 2.4.1-2mdk
- drop all redundant buildrequires
- buildrequires wget to fetch the levels

* Wed Apr  2 2003 Pixel <pixel@mandrakesoft.com> 2.4.1-1mdk
- new release

* Tue Dec 24 2002 Daouda LO <daouda@mandrakesoft.com> 2.4-2mdk
- rebuild against latest glibc

* Tue Dec 17 2002 Pixel <pixel@mandrakesoft.com> 2.4-1mdk
- update levelsets
- new release

* Tue Oct  8 2002 Pixel <pixel@mandrakesoft.com> 2.3.5-1mdk
- update levelsets
- new release

* Mon Aug 19 2002 Pixel <pixel@mandrakesoft.com> 2.3.2-2mdk
- disable COMM_STATS to fix Floating Point Exception (thanks to Byron Poland)

* Fri Aug 16 2002 Pixel <pixel@mandrakesoft.com> 2.3.2-1mdk
- new release

* Tue Aug 13 2002 Pixel <pixel@mandrakesoft.com> 2.3-1mdk
- new release

* Mon Aug  5 2002 Pixel <pixel@mandrakesoft.com> 2.2.2-3mdk
- add "BuildRequires: SDL_mixer-devel" so that it's always build with sound support
- update levelsets

* Mon Apr 29 2002 Pixel <pixel@mandrakesoft.com> 2.2.2-2mdk
- rebuild for new libasound (alsa)

* Fri Mar 22 2002 Pixel <pixel@mandrakesoft.com> 2.2.2-1mdk
- new release

* Mon Feb  4 2002 Pixel <pixel@mandrakesoft.com> 2.2.1-1mdk
- convert menu entries xpm's to png's
- new release

* Sun Jan 27 2002 Pixel <pixel@mandrakesoft.com> 2.2-2mdk
- add levelsets

* Sat Jan 26 2002 Pixel <pixel@mandrakesoft.com> 2.2-1mdk
- new version

* Mon Jan 21 2002 Stefan van der Eijk <stefan@eijk.nu> 2.1.2-3mdk
- BuildRequires

* Mon Jan 14 2002 Pixel <pixel@mandrakesoft.com> 2.1.2-2mdk
- fix-segfault-when-no-personal-levels-are-found patch

* Sun Jan 13 2002 Pixel <pixel@mandrakesoft.com> 2.1.2-1mdk
- new version, new versioning, and this is now lbreakout2

* Thu Sep  6 2001 Pixel <pixel@mandrakesoft.com> 010315-4mdk
- fixing rights on /var/lib/games/lbreakout.hscr

* Wed Jul 11 2001 Stefan van der Eijk <stefan@eijk.nu> 010315-3mdk
- BuildRequires:	libSDL-devel

* Mon May 14 2001 Pixel <pixel@mandrakesoft.com> 010315-2mdk
- rebuild with new SDL

* Fri Apr 27 2001 Pixel <pixel@mandrakesoft.com> 010315-1mdk
- new version

* Wed Dec 20 2000 Pixel <pixel@mandrakesoft.com> 001104-1mdk
- new version

* Tue Nov  7 2000 Pixel <pixel@mandrakesoft.com> 001022-2mdk
- rebuild
- longtitle
- capitalize summary

* Sun Oct 22 2000 Pixel <pixel@mandrakesoft.com> 001022-1mdk
- new version

* Wed Oct 18 2000 Pixel <pixel@mandrakesoft.com> 001018-1mdk
- new version

* Mon Oct  2 2000 Pixel <pixel@mandrakesoft.com> 001002-1mdk
- new version

* Fri Sep 29 2000 Pixel <pixel@mandrakesoft.com> 000928-1mdk
- initial spec
