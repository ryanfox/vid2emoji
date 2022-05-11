from setuptools import setup

with open('README.md') as f:
    readme = f.read()

setup(name='vid2emoji',
      version='0.0.1',
      description='Convert videos to emoji... videos',
      long_description=readme,
      long_description_content_type='text/markdown',
      author='Ryan Fox',
      author_email='ryan@foxrow.com',
      url='https://github.com/ryanfox/vid2emoji',
      packages=['vid2emoji', 'vid2emoji.emojEncode'],
      entry_points={
          'console_scripts': ['vid2emoji=vid2emoji.encode:main',],
      },
      install_requires=[
        'moviepy==1.0.3',
        'numpy==1.22.3',
        'Pillow==9.1.0',
        'scikit-learn==1.0.2',
        'tqdm==4.64.0',],
      license='GPLv3',
      include_package_data=True,
      package_data={'vid2emoji.emojEncode': ['emojiGamutPartitioned.json']},
     )
 