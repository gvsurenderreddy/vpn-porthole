from setuptools import setup

setup(
    name="vpnporthole",
    version="0.0.1",
    download_url="https://github.com/sourcesimian/pyVpnPorthole/tarball/v0.0.1",
    url='https://github.com/sourcesimian/pyVpnPorthole',
    description="Splice VPN access into your default network space",
    author="Source Simian",
    author_email='sourcesimian@users.noreply.github.com',
    license='MIT',
    packages=['vpnporthole'],
    entry_points={
        "console_scripts": [
            "vpnp=vpnporthole.cli:main",
        ]
    },
    install_requires=[
        'ConfigObj>=4.7.0',
        'pexpect',
        'docker-py',
    ],
    package_data={
        'vpnporthole': ['resources/*'],
    }
)
