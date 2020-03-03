# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Pinentry(AutotoolsPackage):
    """The PIN-Entry package contains a collection of simple PIN or pass-phrase
    entry dialogs which utilize the Assuan protocol as described by the Ägypten
    project. PIN-Entry programs are usually invoked by the gpg-agent daemon,
    but can be run from the command line as well. There are programs for
    various text-based and GUI environments, including interfaces designed for
    Ncurses (text-based), and for the common GTK and Qt toolkits."""

    homepage = "https://gnupg.org/related_software/pinentry/index.html"
    url = "https://www.gnupg.org/ftp/gcrypt/pinentry/pinentry-1.1.0.tar.bz2"

    maintainers = ["rubendibattista"]

    version(
        "1.1.0",
        sha256="68076686fa724a290ea49cdf0d1c0c1500907d1b759a3bcbfbec0293e8f56570",
    )

    variant("qt", default=False, description="Build the Qt GUI interface")

    depends_on("libassuan")
    depends_on("libgpg-error")
    depends_on("ncurses")

    depends_on("qt", when="+qt")

    def configure_args(self):
        spec = self.spec

        def variant_bool(feature, on="yes", off="no"):
            """Ternary for spec variant to ON/OFF string"""
            if feature in spec:
                return on
            return off

        args = [
            "--enable-pinentry-tty=yes",
            "--enable-pinentry-curses=yes"
            "--enable-pinentry-qt=%s" % variant_bool("+qt"),
            "--enable-pinentry-gnome3=no",
            "--enable-pinentry-gtk-2=no",
            "--enable-fallback-curses",
        ]

        return args
