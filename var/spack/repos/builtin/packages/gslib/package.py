##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *


class Gslib(Package):
    """Highly scalable Gather-scatter code with AMG and XXT solvers"""

    homepage = "https://github.com/gslib/gslib"
    url      = "https://github.com/gslib/gslib"

    version('1.0.1', git='https://github.com/gslib/gslib.git',
        commit='d16685f24551b7efd69e58d96dc76aec75239ea3')
    version('1.0.0', git='https://github.com/gslib/gslib.git',
        commit='9533e652320a3b26a72c36487ae265b02072cd48')

    variant('mpi', default=True, description='Build with MPI')
    variant('mpiio', default=True, description='Build with MPI I/O')
    variant('blas', default=False, description='Build with BLAS')

    depends_on('mpi', when="+mpi")
    depends_on('mpi', when="+mpiio")
    depends_on('blas', when="+blas")

    conflicts('~mpi', when='+mpiio')

    def install(self, spec, prefix):
        srcDir = 'src'
        libDir = 'lib'
        libname = 'libgs.a'

        if self.version == Version('1.0.1'):
            makeFile = 'Makefile'
        else:
            makeFile = 'src/Makefile'

        CC  = self.compiler.cc

        if '+mpiio' not in spec:
            filter_file(r'MPIIO.*?=.*1', 'MPIIO = 0', makeFile)

        if '+mpi' in spec:
            CC  = spec['mpi'].mpicc
        else:
            filter_file(r'MPI.*?=.*1', 'MPI = 0', makeFile)
            filter_file(r'MPIIO.*?=.*1', 'MPIIO = 0', makeFile)

        makeCmd = "CC=" + CC

        if '+blas' in spec:
            filter_file(r'BLAS.*?=.*0', 'BLAS = 1', makeFile)
            blas = spec['blas'].libs
            ldFlags = blas.ld_flags
            filter_file(r'\$\(LDFLAGS\)', ldFlags, makeFile)

        if self.version == Version('1.0.1'):
            make(makeCmd)
            make('install')
            install_tree(libDir, prefix.lib)
        elif self.version == Version('1.0.0'):
            with working_dir(srcDir):
                make(makeCmd)
                mkdir(prefix.lib)
                install(libname, prefix.lib)

        # Should only install the headers (this will
        # be fixed in gslib on future releases.
        install_tree(srcDir, prefix.include)
