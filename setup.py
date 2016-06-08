from setuptools import setup

setup(
    name="vpn-porthole",
    version="0.1",
    description="Splice VPN access into your default network space",
    author="Source Simian",
    author_email='sourcesimian@users.noreply.github.com',
    url='https://github.com/sourcesimian/vpn-porthole',
    download_url="https://github.com/sourcesimian/vpn-porthole/tarball/v0.1",
    license='MIT',
    packages=['VPNPorthole'],
    entry_points={
        "console_scripts": [
            "vpn-porthole=VPNPorthole.cli:main",
        ]
    },
    install_requires=[
        'ConfigObj>=4.7.0',
        'pexpect',
    ],
    package_data={
        'VPNPorthole': ['resources/*'],
    }
)
