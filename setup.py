from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()


setup(
      name='strava_training_summary',
      version='0.1',
      packages=find_packages(),
      description='Strava training summary CLI tool',
      url='https://github.com/chrisolley/strava_training_summary/',
      author='Chris Olley',
      author_email='olley.cj@gmail.com',
      license='MIT',
      install_requires=requirements,
      entry_points='''
            [console_scripts]
            strava_training_summary=strava_training_summary.cli:strava_training_summary
      '''
)
