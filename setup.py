from setuptools import setup, Extension
import numpy as np
import os
import platform
if platform.system() == "Windows":
    CFLAGS="/std:c++20"
else:
    CFLAGS="-std=c++17"

data_files = [
    ('murt-assets', [
        'assets/poznan.obj',
     'assets/components/cube.obj', 'assets/components/cube.mtl',
     'assets/components/house.obj', 'assets/components/house.mtl',
     'assets/components/ground.obj', 'assets/components/ground.mtl'])
]


def install():
    core_module = Extension('murt.core',
                            sources=['murt/core/core.cpp'],
                            include_dirs=[np.get_include()],
                            language='c++',
                            extra_compile_args=[CFLAGS])

    calculator_module = Extension('murt.calculator',
                                  sources=['murt/core/calculator.cpp'],
                                  language='c++',
                                  extra_compile_args=[CFLAGS])
    setup(
        name="murt",
        version="0.0.8",
        author="Supawat Tamsri",
        python_requires='>=3.7.10',
        author_email="contact@supawat.dev",
        description="Python Library for Multipath Ray Tracing",
        long_description=open('README.md').read(),
        long_description_content_type="text/markdown",
        license="MIT",
        keywords=['Telecommunications', 'Radio', 'Ray Tracing', 'Simulation'],
        packages=['murt', 'murt.utils', 'murt.apps',
                  'murt.engine', 'murt.window'],
        ext_modules=[core_module, calculator_module],
        data_files=data_files,
        include_package_data=True,
        options={'bdist_wheel':{'universal':'1'}},
         install_requires=["pandas", "pyglet", "pywavefront"]
    )


if __name__ == "__main__":
    install()
