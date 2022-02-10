import setuptools

setuptools.setup(
        name = 'mopumopu',
        version = '0.1.0',
        packages = setuptools.find_packages(),
        install_requires = ['numpy', 'torch'],
        entry_points = {
            'console_scripts':[
                'mopumopu = mopumopu.main:main']})

