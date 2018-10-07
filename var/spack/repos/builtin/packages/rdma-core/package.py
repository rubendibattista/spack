# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RdmaCore(CMakePackage):
    """RDMA core userspace libraries and daemons"""

    homepage = "https://github.com/linux-rdma/rdma-core"
    url      = "https://github.com/linux-rdma/rdma-core/releases/download/v17.1/rdma-core-17.1.tar.gz"

    version('20', sha256='bc846989f807cd2b03643927d2b99fbf6f849cb1e766ab49bc9e81ce769d5421')
    version('17.1', sha256='7f5ca9715dce922404851f6ca648399d3dfc3fc2789296f27e94bd2299c68aff')
    version('13', sha256='e5230fd7cda610753ad1252b40a28b1e9cf836423a10d8c2525b081527760d97')

    depends_on('pkgconfig', type='build')
    depends_on('libnl')
    conflicts('platform=darwin', msg='rdma-core requires FreeBSD or Linux')
    conflicts('%intel', msg='rdma-core cannot be built with intel (use gcc instead)')

    def cmake_args(self):
        cmake_args = ["-DCMAKE_INSTALL_SYSCONFDIR=" +
                      self.spec.prefix.etc]
        return cmake_args
