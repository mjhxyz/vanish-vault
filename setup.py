from setuptools import setup, find_packages

setup(
    name='vanishvault',
    version='0.0.1',
    author='mjhxyz',
    author_email='mjhxyz@foxmail.com',
    description='Flask-built, open-source project like Pastebin. Upload encrypted, self-deleting short messages. Emphasizes message security and ephemerality, suitable for sensitive information transmission without leaving traces.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/mjhxyz/vanish-vault',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Flask>=2.2.3',
        'PyCryptodome>=3.10',
        'redis>=4.5.4',
        'Flask-SQLAlchemy>=3.0.3',
        'cymysql>=0.9.18',
        'WTForms>=3.0.1',
        'email-validator>=2.0.0',
    ],
    entry_points={
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
