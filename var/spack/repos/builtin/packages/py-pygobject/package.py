# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPygobject(AutotoolsPackage):
    """bindings for the GLib, and GObject,
       to be used in Python."""

    homepage = "https://pypi.python.org/pypi/pygobject"

    url      = "http://ftp.gnome.org/pub/GNOME/sources/pygobject/2.28/pygobject-2.28.6.tar.bz2"

    version('2.28.6', 'a43d783228dd32899e6908352b8308f3')
    version('2.28.3', 'aa64900b274c4661a5c32e52922977f9')

    extends('python')

    depends_on('pkgconfig', type=('build'))
    depends_on("libffi")
    depends_on('glib')
    depends_on('py-py2cairo', type=('build', 'run'))
    depends_on('gobject-introspection')

    patch('pygobject-2.28.6-introspection-1.patch', when='@2.28.3:2.28.6')

    # patch from https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/development/python-modules/pygobject/pygobject-2.28.6-gio-types-2.32.patch
    # for https://bugzilla.gnome.org/show_bug.cgi?id=668522
    patch('pygobject-2.28.6-gio-types-2.32.patch', when='@2.28.6')

    def install(self, spec, prefix):
        make('install', parallel=False)
