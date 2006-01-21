Summary:	Glide runtime for 3Dfx Voodoo2 boards
Summary(pl):	Biblioteki Glide do kart 3Dfx Voodoo2
Name:		Glide_V2
Version:	2.53
Release:	7
Group:		Libraries
License:	GPL
Vendor:		3Dfx Interactive Inc.
Source0:	GlideV2.tar.gz
# Source0-md5:	a7110232c3d4d888580aaff7919017d2
URL:		http://www.3dfx.com/
%ifarch %{ix86}
BuildRequires:	/usr/bin/gasp
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This library allows the user to use a 3dfx Interactive Voodoo2 card
under Linux.

%description -l pl
Ta biblioteka pozwala u¿ywaæ kart 3dfx Interactive Voodoo2 pod
Linuksem.

%prep
%setup -q -n GlideV2
chmod +x swlibs/include/make/ostype

%build
# Make sure we build for Voodoo2
export FX_GLIDE_HW=cvg
%{__make} V2 CNODEBUG="%{rpmcflags} %{!?debug:-fomit-frame-pointer -funroll-loops} \
	%{!?debug:-fexpensive-optimizations -ffast-math -DBIG_OPT}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_bindir}}

######################################################################
# Install the Glide2x libraries
######################################################################

install glide2x/cvg/lib/libglide.so.2.53 \
	$RPM_BUILD_ROOT%{_libdir}/libglide.so.2.53

# Create symlinks
ln -sf libglide.so.2 $RPM_BUILD_ROOT%{_libdir}/libglide.so

# Create a compatibility link for the old name
ln -sf libglide.so.2.53 $RPM_BUILD_ROOT%{_libdir}/libglide2x.so.2
ln -sf libglide2x.so $RPM_BUILD_ROOT%{_libdir}/libglide2x.so

######################################################################
# Install the Glide3X libraries
######################################################################
install glide3x/cvg/lib/libglide3.so.3.01 \
	$RPM_BUILD_ROOT%{_libdir}/libglide3.so.3.01

# Create symlinks
ln -sf libglide3.so.3 $RPM_BUILD_ROOT%{_libdir}/libglide3.so

# Create a compatibility link for the old name
ln -sf libglide3.so.3.01 $RPM_BUILD_ROOT%{_libdir}/libglide3x.so.3
ln -sf libglide3x.so.3 $RPM_BUILD_ROOT%{_libdir}/libglide3x.so

######################################################################
# Install Texus
######################################################################
install -m 755 glide2x/swlibs/lib/libtexus.so.1.1 \
    $RPM_BUILD_ROOT%{_libdir}

ln -sf libtexus.so.1 $RPM_BUILD_ROOT%{_libdir}/libtexus.so

install swlibs/bin/texus $RPM_BUILD_ROOT%{_bindir}

######################################################################
# Install the Test Programs
######################################################################
# Make two copies so that the old test3Dfx is still there and
# we now have a consisten testGlide2x, testGlide3x
install glide2x/cvg/glide/tests/test00 \
	$RPM_BUILD_ROOT%{_bindir}/test3Dfx
install glide2x/cvg/glide/tests/test00 \
	$RPM_BUILD_ROOT%{_bindir}/testGlide2x
install glide3x/cvg/glide3/tests/test00 \
	$RPM_BUILD_ROOT%{_bindir}/testGlide3x

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc glide2x/glide_license.txt
%attr(755,root,root) %{_bindir}/texus
%attr(755,root,root) %{_bindir}/test3Dfx
%attr(755,root,root) %{_bindir}/testGlide3x
%attr(755,root,root) %{_bindir}/testGlide2x
%attr(755,root,root) %{_libdir}/libglide.so.2.53
%attr(755,root,root) %{_libdir}/libglide.so
%attr(755,root,root) %{_libdir}/libglide2x.so
%attr(755,root,root) %{_libdir}/libglide2x.so.2
%attr(755,root,root) %{_libdir}/libglide3.so.3.01
%attr(755,root,root) %{_libdir}/libglide3.so
%attr(755,root,root) %{_libdir}/libglide3x.so
%attr(755,root,root) %{_libdir}/libglide3x.so.3
%attr(755,root,root) %{_libdir}/libtexus.so.1.1
%attr(755,root,root) %{_libdir}/libtexus.so
