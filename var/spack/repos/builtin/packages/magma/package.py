# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Magma(CMakePackage):
    """The MAGMA project aims to develop a dense linear algebra library similar to
       LAPACK but for heterogeneous/hybrid architectures, starting with current
       "Multicore+GPU" systems.
    """

    homepage = "http://icl.cs.utk.edu/magma/"
    url = "http://icl.cs.utk.edu/projectsfiles/magma/downloads/magma-2.2.0.tar.gz"

    version('2.3.0', '9aaf85a338d3a17303e0c69f86f0ec52')
    version('2.2.0', '6c1ebf4cdf63eb302ff6258ff8c49217')

    variant('fortran', default=True,
            description='Enable Fortran bindings support')
    variant('shared', default=True,
            description='Enable shared library')

    depends_on('blas')
    depends_on('lapack')
    depends_on('cuda')

    conflicts('%gcc@6:', when='^cuda@:8')
    conflicts('%gcc@7:', when='^cuda@:9')

    patch('ibm-xl.patch', when='@2.2:%xl')
    patch('ibm-xl.patch', when='@2.2:%xl_r')
    patch('magma-2.3.0-gcc-4.8.patch', when='@2.3.0%gcc@:4.8')

    def cmake_args(self):
        spec = self.spec
        options = []

        options.extend([
            '-DCMAKE_INSTALL_PREFIX=%s' % prefix,
            '-DCMAKE_INSTALL_NAME_DIR:PATH=%s/lib' % prefix,
            '-DBLAS_LIBRARIES=%s' % spec['blas'].libs.joined(';'),
            # As of MAGMA v2.3.0, CMakeLists.txt does not use the variable
            # BLAS_LIBRARIES, but only LAPACK_LIBRARIES, so we need to
            # explicitly add blas to LAPACK_LIBRARIES.
            '-DLAPACK_LIBRARIES=%s' %
            (spec['lapack'].libs + spec['blas'].libs).joined(';')
        ])

        options += ['-DBUILD_SHARED_LIBS=%s' %
                    ('ON' if ('+shared' in spec) else 'OFF')]

        if '+fortran' in spec:
            options.extend([
                '-DUSE_FORTRAN=yes'
            ])
            if spec.satisfies('%xl') or spec.satisfies('%xl_r'):
                options.extend([
                    '-DCMAKE_Fortran_COMPILER=%s' % self.compiler.f77
                ])

        if spec.satisfies('^cuda@9.0:'):
            if '@:2.2.0' in spec:
                options.extend(['-DGPU_TARGET=sm30'])
            else:
                options.extend(['-DGPU_TARGET=sm_30'])

        return options

    @run_after('install')
    def post_install(self):
        install('magmablas/atomics.cuh', self.prefix.include)
        install('control/magma_threadsetting.h', self.prefix.include)
        install('control/pthread_barrier.h', self.prefix.include)
        install('control/magma_internal.h', self.prefix.include)
