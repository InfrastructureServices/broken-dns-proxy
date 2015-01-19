#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple DNS Proxy for simulating DNS issues
# Copyright (C) 2014-2015  Red Hat, Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Authors:

import subprocess
import os

try:
    from setuptools import setup, Command
except ImportError:
    from distutils.core import setup, Command


class PyTest(Command):
    user_options = [('test-runner=',
                     't',
                     'test runner to use; by default, multiple py.test runners are tried')]
    command_consumes_arguments = True

    def initialize_options(self):
        self.test_runner = None
        self.args = []

    def finalize_options(self):
        pass

    def runner_exists(self, runner):
        syspaths = os.getenv('PATH').split(os.pathsep)
        for p in syspaths:
            if os.path.exists(os.path.join(p, runner)):
                return True

        return False

    def run(self):
        # only one test runner => just run the tests
        supported = ['2.7', '3.3']
        potential_runners = ['py.test-' + s for s in supported]
        if self.test_runner:
            potential_runners = [self.test_runner]
        runners = [pr for pr in potential_runners if self.runner_exists(pr)]

        for runner in runners:
            if len(runners) > 1:
                print('\n' * 2)
                print('Running tests using "{0}":'.format(runner))

            cmd = [runner]
            for a in self.args:
                cmd.append(a)
            cmd.append('-v')
            cmd.append('test')
            t = subprocess.Popen(cmd)
            t.wait()

        raise SystemExit(t.returncode or 0)


install_requires = []
version = '0.1'

setup(
    name='Broken DNS Proxy',
    version=version,
    description='Simple DNS proxy for simulating DNS issues',
    keywords='simulating issues dns proxy',
    url='https://github.com/thozza/broken-dns-proxy',
    license='GPLv3+',
    packages=['broken_dns_proxy'],
    include_package_data=True,
    entry_points={'console_scripts': ['bdp=bdp.run']},
    install_requires=install_requires,
    setup_requires=[],
    classifiers=['Development Status :: 4 - Beta',
                 'Environment :: Console',
                 'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
                 'Operating System :: POSIX :: Linux',
                 'Programming Language :: Python',
                 ],
    cmdclass={'test': PyTest}
)
