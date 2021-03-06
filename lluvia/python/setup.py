"""
    setup.py
    --------

    :copyright: 2018, Juan David Adarve Bermudez. See AUTHORS for more details.
    :license: Apache-2 license, see LICENSE for more details.
"""

import os, sys
import numpy as np
from setuptools import setup
from distutils.core import Extension

from Cython.Build import cythonize


VULKAN_SDK = os.environ['VULKAN_SDK'] if 'VULKAN_SDK' in os.environ.keys() else ''

incDirs = ['../cpp/core/include',
           os.path.join(VULKAN_SDK, 'include'),
           np.get_include()]

# path to build
libDirs = ['../../bazel-bin/lluvia/cpp/core',
           '../../bazel-bin/external/lua',
           '../../bazel-bin/external/miniz',
           os.path.join(VULKAN_SDK, 'lib')]


# common libs first, then we add per platforms
libs   = [
    'core_cc_library',
    'lua_cc_library',
    'miniz_cc_library',
]

cflags = ['-std=c++17',
          '-fPIC',
          '-Wno-unused-function',
          '-DSOL_ALL_SAFETIES_ON=1']

if sys.platform == "linux":
    libs += [
        'stdc++',
        'vulkan',
        'm',
        'dl',
    ]

if sys.platform == "win32":
    libs += [
        "vulkan-1",
    ]
    cflags = [
        "/std:c++17",
    ]


cython_directives = {'embedsignature' : True,
                     'infer_types' : True,
                     'language_level': 2}

def createExtension(name, sources):

    global incDirs
    global libDirs
    global libs

    runtimeLibDirs = libDirs
    if sys.platform == 'win32':
        runtimeLibDirs = []

    ext = Extension(name,
                    sources=sources,
                    include_dirs=incDirs,
                    library_dirs=libDirs,
                    libraries=libs,
                    runtime_library_dirs=runtimeLibDirs,
                    language='c++',
                    extra_compile_args=cflags)

    return ext

# list of extension modules
extensions = list()

#################################################
# PURE PYTHON PACKAGES
#################################################
py_packages = [
    'lluvia',
    'lluvia.core',
    'lluvia.core.enums',
    'lluvia.core.impl'
]

# package data include Cython .pxd files
package_data = {
    'lluvia.core': ['*.pxd', "*.so"],
    'lluvia.core.enums': ['*.pxd', "*.so"],
    'lluvia.core.impl': ['*.pxd', "*.so"]
}
package_dir = {'lluvia': 'src/lluvia'}

#################################################
# CYTHON EXTENSIONS
#################################################
cythonModules = [
    ('lluvia.core.command_buffer'    , ['src/lluvia/core/command_buffer.pyx']),
    ('lluvia.core.core_buffer'       , ['src/lluvia/core/core_buffer.pyx']),
    ('lluvia.core.duration'          , ['src/lluvia/core/duration.pyx']),
    ('lluvia.core.enums.core_object' , ['src/lluvia/core/enums/core_object.pyx']),
    ('lluvia.core.enums.image'       , ['src/lluvia/core/enums/image.pyx']),
    ('lluvia.core.enums.node'        , ['src/lluvia/core/enums/node.pyx']),
    ('lluvia.core.enums.parameter'   , ['src/lluvia/core/enums/parameter.pyx']),
    ('lluvia.core.enums.vulkan'      , ['src/lluvia/core/enums/vulkan.pyx']),
    ('lluvia.core.image'             , ['src/lluvia/core/image.pyx']),
    ('lluvia.core.impl.enum_utils'   , ['src/lluvia/core/impl/enum_utils.pyx']),
    ('lluvia.core.memory'            , ['src/lluvia/core/memory.pyx']),
    ('lluvia.core.node'              , ['src/lluvia/core/node.pyx']),
    ('lluvia.core.parameter'         , ['src/lluvia/core/parameter.pyx']),
    ('lluvia.core.program'           , ['src/lluvia/core/program.pyx']),
    ('lluvia.core.session'           , ['src/lluvia/core/session.pyx']),
]

for mod in cythonModules:
    extList = cythonize(createExtension(mod[0], mod[1]), compiler_directives=cython_directives)
    extensions.extend(extList)

# read version.txt
# FIXME
# with open('../build/version.txt', 'r') as versionFile:
#     version = versionFile.readline()
#     print('VERSION', version)
version = '0.0.1'

# call distutils setup
setup(name='lluvia',
    version=version,
    author='Juan David Adarve Bermudez',
    author_email='juanda0718@gmail.com',
    maintainer='Juan David Adarve Bermudez',
    maintainer_email='juanda0718@gmail.com',
    url='https://github.com/jadarve/lluvia',
    description='A real-time computer vision engine',
    license='Apache-2',
    packages=py_packages,
    ext_modules=extensions,
    package_data=package_data,
    package_dir=package_dir,
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'imageio']
    )
