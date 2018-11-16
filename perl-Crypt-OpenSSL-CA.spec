# Conditional build:
%bcond_with	tests		# do perform "make test"

%include	/usr/lib/rpm/macros.perl
%define		pdir	Crypt
%define		pnam	OpenSSL-CA
Summary:	Crypt::OpenSSL::CA - The crypto parts of an X509v3 Certification Authority
Name:		perl-Crypt-OpenSSL-CA
Version:	0.24
Release:	1
# same as perl
License:	GPL v1+ or Artistic
Group:		Development/Languages/Perl
Source0:	http://www.cpan.org/modules/by-module/Crypt/%{pdir}-%{pnam}-%{version}.tar.gz
# Source0-md5:	0b290daa5b9287d603ebf5bb21ea4d78
URL:		http://search.cpan.org/dist/Crypt-OpenSSL-CA/
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm-perlprov >= 4.1-13
BuildRequires:	perl(Devel::Mallinfo)
%if %{with tests}
BuildRequires:	perl(Devel::Leak)
BuildRequires:	perl(File::Slurp)
BuildRequires:	perl(Inline) >= 0.4
BuildRequires:	perl(Inline::C)
BuildRequires:	perl(Module::Build)
BuildRequires:	perl(Module::Build::Compat)
BuildRequires:	perl(Parse::RecDescent)
BuildRequires:	perl(Test::Group)
BuildRequires:	perl-Convert-ASN1 >= 0.2
BuildRequires:	perl-IPC-Run
BuildRequires:	perl-Net-SSLeay >= 1.25
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This module performs the cryptographic operations necessary to issue
X509 certificates and certificate revocation lists (CRLs).  It is
implemented as a Perl wrapper around the popular OpenSSL library.

Crypt::OpenSSL::CA is an essential building block to create an
X509v3 Certification Authority or CA, a crucial part of an X509
Public Key Infrastructure (PKI). A CA is defined by RFC4210 and
friends (see Crypt::OpenSSL::CA::Resources) as a piece of software
that can (among other things) issue and revoke X509v3 certificates.
To perform the necessary cryptographic operations, it needs a private
key that is kept secret (currently only RSA is supported).

Despite the name and unlike the openssl ca command-line tool,
Crypt::OpenSSL::CA is not designed as a full-fledged X509v3
Certification Authority (CA) in and of itself: some key features are
missing, most notably persistence (e.g. to remember issued and revoked
certificates between two CRL issuances) and security-policy based
screening of certificate requests.  Crypt::OpenSSL::CA mostly does
``just the crypto'', and this is deliberate: OpenSSL's features such
as configuration file parsing, that are best implemented in Perl, have
been left out for maximum flexibility.

%prep
%setup -q -n %{pdir}-%{pnam}-%{version}

%build
%{__perl} Build.PL \
	destdir=$RPM_BUILD_ROOT \
	installdirs=vendor
./Build

%{?with_tests:./Build test}

%install
rm -rf $RPM_BUILD_ROOT

./Build install

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Changes README
%{perl_vendorarch}/Crypt/OpenSSL/*.pm
%{perl_vendorarch}/Crypt/OpenSSL/CA
%dir %{perl_vendorarch}/auto/Crypt/OpenSSL/CA
%dir %{perl_vendorarch}/auto/Crypt/OpenSSL/CA/CONF
%attr(755,root,root) %{perl_vendorarch}/auto/Crypt/OpenSSL/CA/CONF/CONF.so
%dir %{perl_vendorarch}/auto/Crypt/OpenSSL/CA/PrivateKey
%attr(755,root,root) %{perl_vendorarch}/auto/Crypt/OpenSSL/CA/PrivateKey/PrivateKey.so
%dir %{perl_vendorarch}/auto/Crypt/OpenSSL/CA/PublicKey
%attr(755,root,root) %{perl_vendorarch}/auto/Crypt/OpenSSL/CA/PublicKey/PublicKey.so
%dir %{perl_vendorarch}/auto/Crypt/OpenSSL/CA/X509
%attr(755,root,root) %{perl_vendorarch}/auto/Crypt/OpenSSL/CA/X509/X509.so
%dir %{perl_vendorarch}/auto/Crypt/OpenSSL/CA/X509V3_EXT
%attr(755,root,root) %{perl_vendorarch}/auto/Crypt/OpenSSL/CA/X509V3_EXT/X509V3_EXT.so
%dir %{perl_vendorarch}/auto/Crypt/OpenSSL/CA/X509_CRL
%attr(755,root,root) %{perl_vendorarch}/auto/Crypt/OpenSSL/CA/X509_CRL/X509_CRL.so
%dir %{perl_vendorarch}/auto/Crypt/OpenSSL/CA/X509_NAME
%attr(755,root,root) %{perl_vendorarch}/auto/Crypt/OpenSSL/CA/X509_NAME/X509_NAME.so
%{_mandir}/man3/*
%dir %{_examplesdir}/%{name}-%{version}
%attr(755,root,root) %{_examplesdir}/%{name}-%{version}/*.pl
