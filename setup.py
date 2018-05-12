from setuptools import setup

setup(name='hsl',
      version='0.1',
      description='Converts colors from HSL (as specified in CSS) to RGB and back.',
      url='http://github.com/crowsonkb/hsl',
      author='Katherine Crowson',
      author_email='crowsonkb@gmail.com',
      license='MIT',
      packages=['hsl'],
      include_package_data=True,
      zip_safe=False,
      entry_points={
          'console_scripts': ['hslconvert=hsl.cli:main'],
      })
