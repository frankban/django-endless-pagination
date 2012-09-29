from distutils.core import setup
import os

PROJECT_NAME = 'endless_pagination'
project = __import__(PROJECT_NAME)

root_dir = os.path.dirname(__file__)
if root_dir:
    os.chdir(root_dir)

data_files = []
for dirpath, dirnames, filenames in os.walk(PROJECT_NAME):
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'):
            del dirnames[i]
    if '__init__.py' in filenames:
        continue
    elif filenames:
        for f in filenames:
            data_files.append(os.path.join(
                dirpath[len(PROJECT_NAME) + 1:], f))

version = '%s.%s' % project.VERSION[:2]


def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()


setup(
    name='django-endless-pagination',
    version=version,
    description=project.__doc__,
    long_description=read('README'),
    author='Francesco Banconi',
    author_email='francesco.banconi@gmail.com',
    url='http://code.google.com/p/django-endless-pagination/',
    zip_safe=False,
    packages=[
        PROJECT_NAME,
        '{0}.templatetags'.format(PROJECT_NAME),
    ],
    package_data={PROJECT_NAME: data_files},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities'
    ],
)
