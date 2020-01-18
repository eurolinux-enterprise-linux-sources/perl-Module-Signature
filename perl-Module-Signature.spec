Name:           perl-Module-Signature
Version:        0.73
Release:        2%{?dist}
Summary:        CPAN signature management utilities and modules
Group:          Development/Libraries
# script/cpansign:  GPL+ or Artistic (bug #965126)
License:        CC0 and (GPL+ or Artistic)
URL:            http://search.cpan.org/dist/Module-Signature/
Source0:        http://search.cpan.org/CPAN/authors/id/A/AU/AUDREYT/Module-Signature-%{version}.tar.gz
Source1:        AKOENIG.pub
BuildArch:      noarch
# Module build
BuildRequires:  perl
BuildRequires:  perl(base)
BuildRequires:  perl(Config)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(ExtUtils::MM_Unix)
BuildRequires:  perl(Fcntl)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)
# Module runtime
BuildRequires:  gnupg
BuildRequires:  perl(constant)
BuildRequires:  perl(Digest::SHA)
BuildRequires:  perl(Digest::SHA1)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::Manifest)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(IO::Socket::INET)
BuildRequires:  perl(Text::Diff)
# Test suite
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(IPC::Run)
BuildRequires:  perl(lib)
BuildRequires:  perl(Pod::Usage)
BuildRequires:  perl(Test::More)
# Module runtime
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       gnupg
Requires:       perl(Digest::SHA)
Requires:       perl(Digest::SHA1)
Requires:       perl(IO::Socket::INET)
Requires:       perl(PAR::Dist)
Requires:       perl(Text::Diff)

%description
This package contains a command line tool and module for checking and creating
SIGNATURE files for Perl CPAN distributions.

%prep
%setup -q -c -n Module-Signature

# Copy up documentation for convenience with %%doc
cp -a Module-Signature-%{version}/{AUTHORS,Changes,README,*.pub} .

# Create a GPG directory for testing, to avoid using ~/.gnupg
mkdir --mode=0700 gnupghome

# Import AKOENIG key so we don't try to download it later
export GNUPGHOME=$(pwd)/gnupghome
gpg --import %{SOURCE1}

%build
export GNUPGHOME=$(pwd)/gnupghome
cd Module-Signature-%{version}
perl Makefile.PL INSTALLDIRS=vendor --skipdeps </dev/null
make %{?_smp_mflags}
cd -

%install
make -C Module-Signature-%{version} pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
%{_fixperms} %{buildroot}

%check
export GNUPGHOME=$(pwd)/gnupghome
make -C Module-Signature-%{version} test TEST_SIGNATURE=1

%files
%doc AUTHORS Changes README *.pub
%{_bindir}/cpansign
%{perl_vendorlib}/Module/
%{_mandir}/man1/cpansign.1*
%{_mandir}/man3/Module::Signature.3pm*

%changelog
* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 0.73-2
- Mass rebuild 2013-12-27

* Mon Jul 29 2013 Petr Pisar <ppisar@redhat.com> - 0.73-1.2
- Specify all dependencies

* Wed Jun 26 2013 Petr Pisar <ppisar@redhat.com> - 0.73-1.1
- Correct the license and modernize the spec file

* Fri Jun  7 2013 Paul Howarth <paul@city-fan.org> - 0.73-1
- Update to 0.73
  - Constrain the user-specified digest name to /^\w+\d+$/
  - Only allow loading Digest::* from absolute paths in @INC (CVE-2013-2145)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.70-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Nov 28 2012 Paul Howarth <paul@city-fan.org> - 0.70-1
- Update to 0.70
  - Don't check gpg version if gpg does not exist

* Fri Nov  2 2012 Paul Howarth <paul@city-fan.org> - 0.69-1
- Update to 0.69
  - Support for gpg under these alternate names: gpg gpg2 gnupg gnupg2
- This release by AUDREYT -> update source URL
- BR:/R: perl(Text::Diff)
- Include Andreas Koenig's GPG key in the SRPM and import it in %%prep so
  that we don't need to get it from a keyserver in %%check

* Thu Nov  1 2012 Petr Pisar <ppisar@redhat.com> - 0.68-7
- Make building non-interactive
- Specify all dependencies

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.68-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Paul Howarth <paul@city-fan.org> - 0.68-5
- BR: perl(constant), perl(Data::Dumper) and perl(lib)
- Don't need to remove empty directories from the buildroot
- Drop %%defattr, redundant since rpm 4.4

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 0.68-4
- Perl 5.16 rebuild

* Thu Jan 12 2012 Paul Howarth <paul@city-fan.org> - 0.68-3
- BR: perl(Exporter) and perl(ExtUtils::Manifest)
- Use %%{_fixperms} macro rather than our own chmod incantation

* Fri Jun 24 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.68-2
- Perl mass rebuild

* Fri May 13 2011 Paul Howarth <paul@city-fan.org> - 0.68-1
- Update to 0.68
  - Fix breakage introduced by 0.67 (CPAN RT#68150)

* Thu Apr 21 2011 Paul Howarth <paul@city-fan.org> - 0.67-3
- Pseudo-merge EPEL-5/EPEL-6/Fedora versions

* Tue Apr 19 2011 Ville Skyttä <ville.skytta@iki.fi> - 0.67-2
- Appease rpmbuild >= 4.9

* Tue Apr 19 2011 Ville Skyttä <ville.skytta@iki.fi> - 0.67-1
- Update to 0.67

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.66-2
- Rebuild to fix problems with vendorarch/lib (#661697)

* Tue Sep  7 2010 Ville Skyttä <ville.skytta@iki.fi> - 0.66-1
- Update to 0.66 (#630714)

* Tue Sep  7 2010 Ville Skyttä <ville.skytta@iki.fi> - 0.65-1
- Update to 0.65 (#630714)

* Wed Jun 30 2010 Ville Skyttä <ville.skytta@iki.fi> - 0.64-2
- Rebuild

* Sun May  9 2010 Ville Skyttä <ville.skytta@iki.fi> - 0.64-1
- Update to 0.64 (#590385)

* Mon May 03 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.63-2
- Mass rebuild with perl-5.12.0

* Fri Apr 23 2010 Ville Skyttä <ville.skytta@iki.fi> - 0.63-1
- Update to 0.63
- Sync with current rpmdevtools spec template

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.61-2
- Rebuild against perl 5.10.1

* Thu Nov 19 2009 Ville Skyttä <ville.skytta@iki.fi> - 0.61-1
- Update to 0.61 (#538780)

* Tue Nov 17 2009 Ville Skyttä <ville.skytta@iki.fi> - 0.60-1
- Update to 0.60 (#538043); license changed from MIT to CC0

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.55-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.55-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Mar  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.55-3
- Rebuild for new perl

* Tue Apr 17 2007 Ville Skyttä <ville.skytta@iki.fi> - 0.55-2
- BuildRequire perl(ExtUtils::MakeMaker) and perl(Test::More)

* Tue Aug 22 2006 Ville Skyttä <ville.skytta@iki.fi> - 0.55-1
- 0.55
- Make PAR::Dist dependency a Requires(hint)

* Fri May 12 2006 Ville Skyttä <ville.skytta@iki.fi> - 0.54-1
- 0.54, license changed to MIT

* Wed Feb  1 2006 Ville Skyttä <ville.skytta@iki.fi> - 0.53-1
- 0.53

* Fri Jan 20 2006 Ville Skyttä <ville.skytta@iki.fi> - 0.52-1
- 0.52
- Run non-live tests during build and make live ones optional, enabled
  when building with "--with livetests"

* Mon Jan  2 2006 Ville Skyttä <ville.skytta@iki.fi> - 0.51-1
- 0.51

* Mon Aug 22 2005 Ville Skyttä <ville.skytta@iki.fi> - 0.50-1
- 0.50

* Wed Aug 10 2005 Ville Skyttä <ville.skytta@iki.fi> - 0.45-1
- 0.45

* Thu Apr  7 2005 Ville Skyttä <ville.skytta@iki.fi> - 0.44-2
- Drop Epoch: 0 and 0.fdr. release prefix

* Fri Dec 17 2004 Ville Skyttä <ville.skytta@iki.fi> - 0:0.44-0.fdr.1
- Update to 0.44

* Sun Nov 21 2004 Ville Skyttä <ville.skytta@iki.fi> - 0:0.42-0.fdr.1
- Update to 0.42

* Tue Jul  6 2004 Ville Skyttä <ville.skytta@iki.fi> - 0:0.41-0.fdr.2
- Require perl(Digest::SHA1) (bug 1606)

* Mon Jul  5 2004 Ville Skyttä <ville.skytta@iki.fi> - 0:0.41-0.fdr.1
- Update to 0.41

* Fri Jul  2 2004 Ville Skyttä <ville.skytta@iki.fi> - 0:0.40-0.fdr.1
- Update to 0.40

* Fri Jun 18 2004 Ville Skyttä <ville.skytta@iki.fi> - 0:0.39-0.fdr.1
- Update to 0.39

* Mon May 31 2004 Ville Skyttä <ville.skytta@iki.fi> - 0:0.38-0.fdr.4
- Really use pure_install (bug 1606)
- Fix build with older mktemp versions which require a template (bug 1606)

* Mon May 31 2004 Ville Skyttä <ville.skytta@iki.fi> - 0:0.38-0.fdr.3
- Fix build in setups which do not generate debug packages (bug 1606)
- Require perl >= 1:5.6.1 for vendor install dir support
- Use pure_install to avoid perllocal.pod workarounds

* Sun Apr 25 2004 Ville Skyttä <ville.skytta@iki.fi> - 0:0.38-0.fdr.2
- Require perl(:MODULE_COMPAT_*)

* Sat Mar 27 2004 Ville Skyttä <ville.skytta@iki.fi> - 0:0.38-0.fdr.1
- First build
