import distutils
import os
import subprocess

from pkg_resources import parse_requirements
from setuptools import Command, find_packages, setup

module_name = 'db_cinema_project'


class CompileUI(Command):
    description = "Compile all UI files"
    user_options = []

    def run(self):
        ui_dir = os.path.join(module_name, 'ui')
        for file in os.listdir(ui_dir):
            if file.endswith('.ui'):
                full_name = os.path.join(ui_dir, file)
                full_name_out = os.path.join(ui_dir, file.replace('.ui', '.py'))
                command = ['pyuic5', full_name, '-o', full_name_out]
                self.announce(
                    'Compile UI file: {}'.format(full_name), level=distutils.log.INFO
                )
                subprocess.check_call(command)

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass


def load_requirements(filename: str) -> list:
    requirements = []
    with open(filename, 'r') as f:
        for requirement in parse_requirements(f.read()):
            extras = '[{}]'.format(
                ','.join(requirement.extras)) if requirement.extras else ''
            requirements.append(
                '{}{}{}'.format(requirement.name, extras, requirement.specifier)
            )
    return requirements


with open('README.md', 'rt') as f:
    long_description = f.read()

setup(
    name=module_name,
    version='0.1.1',
    description='DB project for cinema',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/goo-goo-goo-joob/hse_db_project',
    author='goo-goo-goo-joob (Mariia Samodelkina)',
    author_email='samodelkina-m-v@yandex.ru',
    license='MIT',
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'Operating System :: MacOS',
    ],
    keywords=['python python3 qt database mysql'],
    packages=find_packages(exclude=['tests']),
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            '{0} = {0}.__main__:main'.format(module_name),
        ],
    },
    cmdclass={
        'compile_ui': CompileUI,
    },
    include_package_data=True,
    zip_safe=False,
    install_requires=load_requirements('requirements.txt'),

)
