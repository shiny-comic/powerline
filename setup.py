#!/usr/bin/env python
import os
import sys
import logging
import shlex
import subprocess

from setuptools import setup, find_packages

from powerline.version import get_version

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
try:
    README = open(os.path.join(CURRENT_DIR, 'README.md'), 'rb').read().decode('utf-8')
except IOError:
    README = ''

def compile_client():
    '''Compile the C powerline-client script.'''

    if hasattr(sys, 'getwindowsversion'):
        raise NotImplementedError()
    else:
        from distutils.ccompiler import new_compiler
        compiler = new_compiler().compiler
        cflags = os.environ.get('CFLAGS', str('-O3'))
        # A normal split would do a split on each space which might be incorrect. The
        # shlex will not split if a space occurs in an arguments value.
        subprocess.check_call(compiler + shlex.split(cflags) + ['-std=c11', 'client/powerline.c', '-o', 'scripts/powerline'])

try:
    compile_client()
    print('Using C version.')
except Exception as e:
    print('Compiling C version of powerline-client failed')
    logging.exception(e)
    # FIXME Catch more specific exceptions
    import shutil
    if hasattr(shutil, 'which'):
        which = shutil.which
    else:
        sys.path.append(CURRENT_DIR)
        from powerline.lib.shell import which
    if which('socat') and which('sed') and which('sh'):
        print('Using powerline.sh script instead of C version (requires socat, sed and sh)')
        shutil.copyfile('client/powerline.sh', 'scripts/powerline')
    else:
        print('Using powerline.py script instead of C version')
        shutil.copyfile('client/powerline.py', 'scripts/powerline')

setup(
    name='powerline-status-i3',
    version=get_version(),
    description='The ultimate statusline/prompt utility. A fork containing more features for the i3 window manager.',
    long_description=README,
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: Plugins',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    download_url='https://github.com/ph111p/powerline/archive/develop.zip',
    author='Philip Wellnitz',
    author_email='philipwellnitz@gmx.de',
    url='https://github.com/ph111p/powerline',
    license='MIT',
    entry_points={
        'console_scripts': [
            'powerline-lint=scripts.powerline_lint:main',
            'powerline-daemon=scripts.powerline_daemon:main',
            'powerline-render=scripts.powerline_render:main',
            'powerline-config=scripts.powerline_config:main',
            'powerline-lemonbar=scripts.powerline_lemonbar:main',
            'powerline-gcal-auth=scripts.powerline_gcal_auth:main',
            'powerline-globmenu=scripts.powerline_globmenu:main'
        ]
    },
    package_data={'': ['scripts/powerline', 'scripts/*.py']},
    keywords='',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[],
    extras_require={
        'i3wm segment': [
            'i3ipc'
        ],
        'randr segment': [
            'python-xlib'
        ],
        'volume segment': [
            'pyalsaaudio'
        ],
        'docs': [
            'Sphinx',
            'sphinx_rtd_theme',
        ],
        'appoints segment support, Google Calendar': [
            'google-api-python-client'
        ],
        'cpu load segment support': [
            'psutil'
        ],
        'wifi segment support': [
            'iwlib'
        ],
        'better git support in vcs segment': [
            'pygit2'
        ],
    },
)
