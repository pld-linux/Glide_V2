#
# Conditional build:
%bcond_with	glide_sdk	# build glide2/glide3 SDKs
#
Summary:	Glide runtime for 3Dfx Voodoo2 boards
Summary(pl.UTF-8):	Biblioteki Glide do kart 3Dfx Voodoo2
Name:		Glide_V2
Version:	2.53
Release:	7
Group:		Libraries
License:	3DFX GLIDE Source Code General Public License
Source0:	GlideV2.tar.gz
# Source0-md5:	a7110232c3d4d888580aaff7919017d2
Patch0:		glide-gcc4.patch
Patch1:		glide-gasp.patch
Patch2:		glide-cpp.patch
Patch3:		glide-link.patch
URL:		http://glide.sourceforge.net/
%ifarch %{ix86}
BuildRequires:	/usr/bin/gasp
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This library allows the user to use a 3dfx Interactive Voodoo2 card
under Linux.

%description -l pl.UTF-8
Ta biblioteka pozwala używać kart 3dfx Interactive Voodoo2 pod
Linuksem.

%package -n Glide2x_SDK
Summary:	Development libraries for Glide 2.x
Summary(pl.UTF-8):	Część Glide 2.x przeznaczona dla programistów
Group:		Development/Libraries
Conflicts:	Glide_SDK

%description -n Glide2x_SDK
This package includes the header files and test files necessary for
developing applications that use any of the 3D accelerators in the
3Dfx Interactive Voodoo line utilizing Glide 2.x interface.

%description -n Glide2x_SDK -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe i pliki testowe potrzebne do
tworzenia aplikacji korzystających z akceleratorów 3D serii 3Dfx
Interactive Voodoo przy użyciu interfejsu Glide 2.x.

%package -n Glide3x_SDK
Summary:	Development libraries for Glide 3.x
Summary(pl.UTF-8):	Część Glide 3.x przeznaczona dla programistów
Group:		Development/Libraries
Conflicts:	Glide_SDK

%description -n Glide3x_SDK
This package includes the header files and test files necessary for
developing applications that use any of the 3D accelerators in the
3Dfx Interactive Voodoo line utilizing Glide 3.x interface.

%description -n Glide3x_SDK -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe i pliki testowe potrzebne do
tworzenia aplikacji korzystających z akceleratorów 3D serii 3Dfx
Interactive Voodoo przy użyciu interfejsu Glide 3.x.

%prep
%setup -q -n GlideV2
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
chmod +x swlibs/include/make/ostype
%{__rm} glide3x/cvg/init/*.{o,a}

ln glide2x/README README.glide2x
ln glide3x/README README.glide3x

%build
# Make sure we build for Voodoo2
export FX_GLIDE_HW=cvg
%{__make} V2 \
	CC="%{__cc}" \
	CNODEBUG="%{rpmcflags} %{!?debug:-fomit-frame-pointer -funroll-loops} \
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
# (X driver used to dlopen by libglide2x.so name)
ln -sf libglide.so.2.53 $RPM_BUILD_ROOT%{_libdir}/libglide2x.so

######################################################################
# Install the Glide3X libraries
######################################################################
install glide3x/cvg/lib/libglide3.so.3.01 \
	$RPM_BUILD_ROOT%{_libdir}/libglide3.so.3.01

# Create symlinks
ln -sf libglide3.so.3 $RPM_BUILD_ROOT%{_libdir}/libglide3.so

# Create a compatibility link for the old name
# (X driver used to dlopen by libglide3x.so name)
ln -sf libglide3x.so.3.01 $RPM_BUILD_ROOT%{_libdir}/libglide3x.so

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

%if %{with glide_sdk}
### SDK
install -d $RPM_BUILD_ROOT%{_includedir}/{glide,glide3}
install -d $RPM_BUILD_ROOT%{_examplesdir}/{glide2x-%{version}/{tests,texus/examples},glide3x-%{version}/tests}

# glide2x headers
install swlibs/include/3dfx.h $RPM_BUILD_ROOT%{_includedir}/glide
install swlibs/include/linutil.h $RPM_BUILD_ROOT%{_includedir}/glide
install swlibs/include/texus.h $RPM_BUILD_ROOT%{_includedir}/glide
install glide2x/cvg/include/glide.h $RPM_BUILD_ROOT%{_includedir}/glide
install glide2x/cvg/include/glidesys.h $RPM_BUILD_ROOT%{_includedir}/glide
install glide2x/cvg/include/glideutl.h $RPM_BUILD_ROOT%{_includedir}/glide
install glide2x/cvg/include/sst1vid.h $RPM_BUILD_ROOT%{_includedir}/glide
install glide2x/cvg/include/gump.h $RPM_BUILD_ROOT%{_includedir}/glide

# glide2x examples
install glide2x/cvg/glide/tests/makefile.distrib $RPM_BUILD_ROOT%{_examplesdir}/glide2x-%{version}/tests/makefile
install glide2x/cvg/glide/tests/*.3df $RPM_BUILD_ROOT%{_examplesdir}/glide2x-%{version}/tests
install glide2x/cvg/glide/tests/test??.c $RPM_BUILD_ROOT%{_examplesdir}/glide2x-%{version}/tests
install glide2x/cvg/glide/tests/tldata.inc $RPM_BUILD_ROOT%{_examplesdir}/glide2x-%{version}/tests
install glide2x/cvg/glide/tests/tlib.[ch] $RPM_BUILD_ROOT%{_examplesdir}/glide2x-%{version}/tests

# texus examples
install swlibs/texus/examples/makefile.distrib $RPM_BUILD_ROOT%{_examplesdir}/glide2x-%{version}/texus/examples/makefile
install swlibs/texus/examples/*.c $RPM_BUILD_ROOT%{_examplesdir}/glide2x-%{version}/texus/examples

# glide3x headers
install swlibs/include/3dfx.h $RPM_BUILD_ROOT%{_includedir}/glide
install swlibs/include/linutil.h $RPM_BUILD_ROOT%{_includedir}/glide
install swlibs/include/texus.h $RPM_BUILD_ROOT%{_includedir}/glide
install glide3x/cvg/include/glide.h $RPM_BUILD_ROOT%{_includedir}/glide
install glide3x/cvg/include/glidesys.h $RPM_BUILD_ROOT%{_includedir}/glide
install glide3x/cvg/include/glideutl.h $RPM_BUILD_ROOT%{_includedir}/glide
install glide3x/cvg/include/sst1vid.h $RPM_BUILD_ROOT%{_includedir}/glide

# glide3x examples
install glide3x/cvg/glide3/tests/makefile.distrib $RPM_BUILD_ROOT%{_examplesdir}/glide3x-%{version}/tests/makefile
install glide3x/cvg/glide3/tests/*.3df $RPM_BUILD_ROOT%{_examplesdir}/glide3x-%{version}/tests
install glide3x/cvg/glide3/tests/test??.c $RPM_BUILD_ROOT%{_examplesdir}/glide3x-%{version}/tests
install glide3x/cvg/glide3/tests/tldata.inc $RPM_BUILD_ROOT%{_examplesdir}/glide3x-%{version}/tests
install glide3x/cvg/glide3/tests/tlib.[ch] $RPM_BUILD_ROOT%{_examplesdir}/glide3x-%{version}/tests
%endif

/sbin/ldconfig -n $RPM_BUILD_ROOT%{_libdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.glide2x README.glide3x glide_license.txt
%attr(755,root,root) %{_bindir}/texus
%attr(755,root,root) %{_bindir}/test3Dfx
%attr(755,root,root) %{_bindir}/testGlide3x
%attr(755,root,root) %{_bindir}/testGlide2x
%attr(755,root,root) %{_libdir}/libglide.so.2.53
%attr(755,root,root) %ghost %{_libdir}/libglide.so.2
%attr(755,root,root) %{_libdir}/libglide.so
%attr(755,root,root) %{_libdir}/libglide2x.so
%attr(755,root,root) %{_libdir}/libglide3.so.3.01
%attr(755,root,root) %ghost %{_libdir}/libglide3.so.3
%attr(755,root,root) %{_libdir}/libglide3.so
%attr(755,root,root) %{_libdir}/libglide3x.so
%attr(755,root,root) %{_libdir}/libtexus.so.1.1
%attr(755,root,root) %ghost %{_libdir}/libtexus.so.1
%attr(755,root,root) %{_libdir}/libtexus.so

%if %{with glide_sdk}
%files -n Glide2x_SDK
%defattr(644,root,root,755)
%{_includedir}/glide
%{_examplesdir}/glide2x-%{version}

%files -n Glide3x_SDK
%defattr(644,root,root,755)
%{_includedir}/glide3
%{_examplesdir}/glide3x-%{version}
%endif
