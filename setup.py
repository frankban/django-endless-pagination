from distutils.core import setup
import os

root_dir = os.path.dirname(__file__)
if root_dir:
    os.chdir(root_dir)

data_files = []
for dirpath, dirnames, filenames in os.walk('endless_pagination'):
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'): del dirnames[i]
    if '__init__.py' in filenames:
        continue
    elif filenames:
        for f in filenames:
            data_files.append(os.path.join(dirpath[len("endless_pagination")+1:], f))
            
version = "%s.%s" % __import__('endless_pagination').VERSION[:2]

setup(name='django-endless-pagination',
    version=version,
    description='Ajax pagination tools for Django.',
    author='Francesco Banconi',
    author_email='francesco.banconi@gmail.com',
    url='http://code.google.com/p/django-endless-pagination/',
    zip_safe=False,
    packages=[
        'endless_pagination', 
        'endless_pagination.templatetags',
    ],
    package_data={'endless_pagination': data_files},
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
