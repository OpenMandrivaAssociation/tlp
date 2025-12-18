Name:		tlp
Version:	1.9.0
Release:	1
Source0:	https://github.com/linrunner/tlp/archive/%{version}/TLP-%{version}.tar.gz
Summary:	Optimize Linux Laptop Battery Life
URL:		https://github.com/linrunner/tlp
License:	GPL-2.0-or-later
Group:		System/Utils
BuildRequires:	make
BuildRequires:	systemd
BuildRequires:	pkgconfig
BuildRequires:	pkgconfig(appstream-glib)
Requires:	hdparm
Requires:	gawk
Requires:	grep
Requires:	iw
Requires:	pciutils
Requires:	rfkill
Requires:	sed
Requires:	udev
Requires:	usbutils
Requires:	util-linux
Recommends:	ethtool
Recommends:	smartmontools
Recommends:	dkms-tp_smapi
###################################
Conflicts:	auto-cpufreq
Conflicts:	laptop-mode-tools
Conflicts:	power-profiles-daemon
Conflicts:	tuned
###################################
BuildArch:	noarch

%description
TLP is a feature-rich command line utility for Linux, saving laptop
battery power without the need to delve deeper into technical details.

TLP’s default settings are already optimized for battery life.

TLP is able to be customized to meet your specific requirements.

Settings are organized into two profiles, enabling you to adjust between
savings and performance independently for battery (BAT) and AC operation.

%package rdw
Summary:	Radio Device Wizard for tlp
Requires:	%{name} = %{version}-%{release}
Requires:	networkmanager
BuildArch:	noarch

%description rdw
The Radio Device Wizard provides the capability to enable or disable
builtin Bluetooth, Wi-Fi and WWAN devices triggered by certain events.

%prep
%autosetup -p1 -n TLP-%{version}

%build
%make_build

%install
%make_install \
    TLP_SBIN=%{_sbindir} \
    TLP_BIN=%{_bindir} \
    TLP_ULIB=%{_udevrulesdir}/../ \
    TLP_NMDSP=%{_prefix}/lib/NetworkManager/dispatcher.d \
    TLP_CONFUSR=%{_sysconfdir}/tlp.conf \
    TLP_CONFDIR=%{_sysconfdir}/tlp.d \
    TLP_CONFDEF=%{_datarootdir}/tlp/defaults.conf \
    TLP_CONFREN=%{_datarootdir}/tlp/rename.conf \
    TLP_CONFDPR=%{_datarootdir}/tlp/deprecated.conf \
    TLP_CONF=%{_sysconfdir}/default/tlp \
    TLP_SYSD=%{_unitdir} \
    TLP_SDSL=%{_unitdir}/../system-sleep \
    TLP_SHPL=%{_datarootdir}/bash-completion/completions \
    TLP_ZSHCPL=%{_datarootdir}/zsh/site-functions \
    TLP_FISHCPL=%{_datarootdir}/fish/vendor_completions.d \
    TLP_WITH_SYSTEMD=1 \
    TLP_NO_INIT=1 \
    TLP_WITH_ELOGIND=0 \

#########################################
# make and install man pages in buildroot
make install-man-tlp DESTDIR=%{buildroot}
make install-man-rdw DESTDIR=%{buildroot}


%files
%{_bindir}/bluetooth
%{_bindir}/nfc
%{_bindir}/run-on-ac
%{_bindir}/run-on-bat
%{_bindir}/%{name}
%{_bindir}/%{name}-pd
%{_bindir}/%{name}-stat
%{_bindir}/%{name}ctl
%{_bindir}/wifi
%{_bindir}/wwan
%exclude %{_bindir}/tlp-rdw
%config(noreplace) %{_sysconfdir}/tlp.conf
%config(noreplace) %{_sysconfdir}/tlp.d/00-template.conf
%config(noreplace) %{_sysconfdir}/tlp.d/README
%{_datadir}/tlp
%{_datadir}/bash-completion/completions/*
%exclude %{_datadir}/bash-completion/completions/tlp-rdw
%{_datadir}/fish/vendor_completions.d/*
%exclude %{_datadir}/fish/vendor_completions.d/tlp-rdw.fish
%{_datadir}/zsh/site-functions/*
%exclude %{_datadir}/zsh/site-functions/_tlp-radio-device
%exclude %{_datadir}/zsh/site-functions/_tlp-rdw
%{_udevrulesdir}/85-tlp.rules
%{_udevrulesdir}/../tlp-usb-udev
%{_unitdir}/*.service
%{_unitdir}/../system-sleep
%{_datadir}/metainfo/de.linrunner.tlp.metainfo.xml
%doc %{_mandir}/man*/*
%exclude %{_mandir}/man8/tlp-rdw*
%{_datadir}/dbus-1/system-services/org.freedesktop.UPower.PowerProfiles.service
%{_datadir}/dbus-1/system-services/net.hadess.PowerProfiles.service
%{_datadir}/dbus-1/system.d/org.freedesktop.UPower.PowerProfiles.conf
%{_datadir}/dbus-1/system.d/net.hadess.PowerProfiles.conf
%{_datadir}/polkit-1/actions/tlp-pd.policy
%{_localstatedir}/lib/tlp
%doc AUTHORS README.rst changelog
%license LICENSE COPYING

%changelog


%files  rdw
%doc AUTHORS README.rst changelog
%license LICENSE COPYING
%{_bindir}/tlp-rdw
%{_datadir}/bash-completion/completions/tlp-rdw
%{_datadir}/fish/vendor_completions.d/tlp-rdw.fish
%{_datadir}/zsh/site-functions/_tlp-radio-device
%{_datadir}/zsh/site-functions/_tlp-rdw
%{_mandir}/man8/tlp-rdw*.8*
%{_prefix}/lib/NetworkManager/dispatcher.d/99tlp-rdw-nm
%{_udevrulesdir}/85-tlp-rdw.rules
%{_udevrulesdir}/../tlp-rdw-udev

%post
%systemd_post tlp.service
if [ $1 -eq 2 ] ; then
    systemctl unmask systemd-rfkill.service
    systemctl unmask power-profiles-daemon.service
fi

%preun
%systemd_preun tlp.service

%postun
%systemd_postun_with_restart tlp.service
