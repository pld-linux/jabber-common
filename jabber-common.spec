Summary:	Common environment for Jabber services
Summary(pl.UTF-8):	Wspólne środowisko dla usług Jabbera
Name:		jabber-common
Version:	0
Release:	9
License:	GPL
Group:		Applications/Communications
Source0:	%{name}.tmpfiles
BuildRequires:	rpmbuild(macros) >= 1.202
Requires(post):	%{__perl}
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Provides:	group(jabber)
Provides:	user(jabber)
Obsoletes:	jabber-conference
Obsoletes:	jabber-irc-transport
Conflicts:	jabber
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package prepares common environment for Jabber services.

%description -l pl.UTF-8
Ten pakiet przygotowuje wspólne środowisko dla usług Jabbera.

%prep

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/var/run/jabber,/etc/jabber,/home/services/jabber} \
	$RPM_BUILD_ROOT/usr/lib/tmpfiles.d

install %{SOURCE0} $RPM_BUILD_ROOT/usr/lib/tmpfiles.d/jabber.conf

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
/usr/lib/tmpfiles.d/jabber.conf
%dir %attr(775,root,jabber) /var/run/jabber
%dir %attr(711,jabber,jabber) /home/services/jabber
%attr(600,root,root) %ghost %{_sysconfdir}/jabber/secret
