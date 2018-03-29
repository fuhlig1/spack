##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
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
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install fairsoft
#
# You can edit this file again by typing:
#
#     spack edit fairsoft
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *
import platform
#import os
#import sys


class Fairsoft(Package):
    """Meta package to install all dependencies which are needed to properly install 
       and run FairRoot. No url or homepage is defined, only all packages whcih are
       needed are defined as dependencies. """


    homepage = ""
    url      = "https://github.com/fuhlig1/fairsoft_description/archive/17.10.tar.gz"

    # Development versions
    version('17.10', 'd3aee3525b04e1c70ccd4d5be5bf7fbf')

    # Add all dependencies here.
    if self.spec.satisfies('@17.10'):
        depends_on('cmake@3.9.4', type='build')
        depends_on('gsl@1.16')
        depends_on('googletest@1.7.0')

        depends_on('boost@1.64.0 clanglibcpp=True', when=(platform == 'darwin'))
        depends_on('boost@1.64.0', when=(platform != 'darwin'))

        depends_on('pythia6@428-alice1')
        depends_on('hepmc')


    def install(self, spec, prefix):
        # touch a file in the installation directory
        touch('%s/this-is-a-bundle.txt' % prefix)

