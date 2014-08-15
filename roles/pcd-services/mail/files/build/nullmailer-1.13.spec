Name: nullmailer
Summary: Simple relay-only mail transport agent - Ported to CentOS + initscripts
Version: 1.13
Release: 2
License: GPL
Group: System Environment/Daemons 
Source: http://untroubled.org/nullmailer/archive/%{version}/nullmailer-%{version}.tar.gz
BuildRoot: /tmp/nullmailer-root
URL: http://untroubled.org/nullmailer/
Packager: Brice Burgess @iceburg_net 
Provides: smtpdaemon
Provides: nullmailer
Provides: sendmail
Provides: MTA
Provides: /usr/sbin/sendmail
Provides: server(smtp)
Conflicts: sendmail
Conflicts: qmail
Requires: initscripts 
Requires: gnutls
BuildRequires: gnutls-devel

%description
Nullmailer is a mail transport agent designed to only relay all its
messages through a fixed set of "upstream" hosts.  It is also designed
to be secure.

%prep
%setup

%build
CFLAGS="$RPM_OPT_FLAGS" CXXFLAGS="$RPM_OPT_FLAGS" \
./configure --prefix=/usr --sysconfdir=/etc --localstatedir=/var --enable-tls

make

%install
rm -fr $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/etc
mkdir -p $RPM_BUILD_ROOT/etc/init.d
mkdir -p $RPM_BUILD_ROOT/usr/lib
mkdir -p $RPM_BUILD_ROOT/var/log/nullmailer

make DESTDIR=$RPM_BUILD_ROOT install-strip
ln -s ../sbin/sendmail $RPM_BUILD_ROOT/usr/lib/sendmail
cp scripts/nullmailer.init $RPM_BUILD_ROOT/etc/init.d/nullmailer

%clean
rm -rf $RPM_BUILD_ROOT

%pre
PATH="/sbin:/usr/sbin:$PATH" export PATH
if [ "$1" = 1 ]; then
	# pre-install instructions
	grep ^nullmail: /etc/group >/dev/null || groupadd -r nullmail
	grep ^nullmail: /etc/passwd >/dev/null || useradd -d /etc/nullmailer -g nullmail -M -r -s /bin/true nullmail
fi

%post
if ! [ -s /etc/nullmailer/me ]; then
	/bin/hostname --fqdn >/etc/nullmailer/me
fi
if ! [ -s /etc/nullmailer/defaultdomain ]; then
	/bin/hostname --domain >/etc/nullmailer/defaultdomain
fi
chkconfig nullmailer on

%preun

%postun
if [ "$1" = 0 ]; then
	# post-erase instructions
	/usr/sbin/userdel nullmail
	/usr/sbin/groupdel nullmail
fi

%files
%defattr(-,nullmail,nullmail)
%doc AUTHORS BUGS ChangeLog COPYING INSTALL NEWS README TODO
%dir /etc/nullmailer
%attr(04711,nullmail,nullmail) /usr/bin/mailq
/usr/bin/nullmailer-inject
/usr/bin/nullmailer-smtpd
/usr/lib/sendmail
%dir /usr/libexec/nullmailer
/usr/libexec/nullmailer/*
%{_mandir}/*/*
%attr(04711,nullmail,nullmail) /usr/sbin/nullmailer-queue
/usr/sbin/nullmailer-send
/usr/sbin/sendmail
%dir /var/log/nullmailer
/var/nullmailer
%defattr(755,root,root)
/etc/init.d/nullmailer
