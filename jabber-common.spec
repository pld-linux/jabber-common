Summary:	Common enviroment for Jabber services
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
Conflicts:	jabber
Obsoletes:	jabber-irc-transport
Obsoletes:	jabber-conference
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package prepares common environment for Jabber services.

%prep

%build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/var/run/jabber,/etc/jabber}
touch $RPM_BUILD_ROOT%{_sysconfdir}/jabber/secret

%clean
rm -rf $RPM_BUILD_ROOT

%pre
if [ "$1" = 1 ] ; then
	if [ ! -n "`getgid jabber`" ]; then
		%{_sbindir}/groupadd -f -g 74 jabber
	fi
	if [ ! -n "`id -u jabber 2>/dev/null`" ]; then
		%{_sbindir}/useradd -g jabber -d /var/lib/jabber -u 74 -s /bin/false jabber 2>/dev/null
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
# If package is being erased for the last time.
if [ "$1" = "0" ]; then
      %{_sbindir}/userdel jabber 2> /dev/null
      %{_sbindir}/groupdel jabber 2> /dev/null
fi

%files
%defattr(644,root,root,755)
%dir %{_sysconfdir}/jabber
%dir %attr(775,root,jabber) /var/run/jabber
%attr(600,root,root) %ghost %{_sysconfdir}/jabber/secret
