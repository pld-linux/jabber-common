Summary:	Common enviroment for Jabber services
Summary(pl):	Wspólne ¶rodowisko dla us³ug Jabbera
Name:		jabber-common
Version:	0
Release:	5
License:	GPL
Group:		Applications/Communications
BuildRequires:	rpmbuild(macros) >= 1.202
Requires(post):	%{__perl}
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Provides:	group(jabber)
Provides:	user(jabber)
Conflicts:	jabber
Obsoletes:	jabber-irc-transport
Obsoletes:	jabber-conference
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package prepares common environment for Jabber services.

%description -l pl
Ten pakiet przygotowuje wspólne ¶rodowisko dla us³ug Jabbera.

%prep

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/var/run/jabber,/etc/jabber,/home/services/jabber}

touch $RPM_BUILD_ROOT%{_sysconfdir}/jabber/secret

%clean
rm -rf $RPM_BUILD_ROOT

%triggerpostun -- jabber-common < 0-4
if [ "`echo -n ~jabber`" = "/var/lib/jabber" -o "`echo -n ~jabber`" = "/var/lib/jabberd" ] ; then
	/usr/sbin/usermod -d /home/services/jabber jabber
fi

%pre
%groupadd -g 74 jabber
%useradd -g jabber -d /home/services/jabber -u 74 -s /bin/false jabber

%post
if [ ! -f /etc/jabber/secret ] ; then
	echo "Generating Jabberd component authentication secret..."
	umask 066
	%{__perl} -e 'open R,"/dev/urandom"; read R,$r,16;
		printf "%02x",ord(chop $r) while($r);' > /etc/jabber/secret
fi

%preun
if [ "$1" = 0 ]; then
	rm -f /var/run/jabber/* || :
fi

%postun
if [ "$1" = "0" ]; then
	%userremove jabber
	%groupremove jabber
fi

%files
%defattr(644,root,root,755)
%dir %{_sysconfdir}/jabber
%dir %attr(775,root,jabber) /var/run/jabber
%dir %attr(711,jabber,jabber) /home/services/jabber
%attr(600,root,root) %ghost %{_sysconfdir}/jabber/secret
