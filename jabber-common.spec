Summary:	Common enviroment for Jabber services
Summary(pl):	Wspólne ¶rodowisko dla us³ug Jabbera
Name:		jabber-common
Version:	0
Release:	1
License:	GPL
Group:		Applications/Communications
Requires(post):	/usr/bin/perl
Requires(pre):	/usr/bin/getgid
Requires(pre):	/bin/id
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Conflicts:	jabber
Obsoletes:	jabber-irc-transport
Obsoletes:	jabber-conference
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package prepares common environment for Jabber services.

%description -l pl
Ten pakiet przygotowywuje wspólne ¶rodowisko dla us³ug Jabbera.

%prep

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/var/run/jabber,/etc/jabber}

touch $RPM_BUILD_ROOT%{_sysconfdir}/jabber/secret

%clean
rm -rf $RPM_BUILD_ROOT

%pre
if [ "$1" = 1 ] ; then
	if [ ! -n "`getgid jabber`" ]; then
		/usr/sbin/groupadd -f -g 74 jabber
	fi
	if [ ! -n "`id -u jabber 2>/dev/null`" ]; then
		/usr/sbin/useradd -g jabber -d /var/lib/jabber -u 74 -s /bin/false jabber 2>/dev/null
	fi
fi

%post
if [ ! -f /etc/jabber/secret ] ; then
        echo "Generating Jabberd component authentication secret..."
        umask 066
        perl -e 'open R,"/dev/urandom"; read R,$r,16;
                 printf "%02x",ord(chop $r) while($r);' > /etc/jabber/secret
fi

%preun
rm -f /var/run/jabberd/* || :

%postun
if [ "$1" = "0" ]; then
      /usr/sbin/userdel jabber 2>/dev/null
      /usr/sbin/groupdel jabber 2>/dev/null
fi

%files
%defattr(644,root,root,755)
%dir %{_sysconfdir}/jabber
%dir %attr(775,root,jabber) /var/run/jabber
%attr(600,root,root) %ghost %{_sysconfdir}/jabber/secret
