import setuptools
"""
打包成一个 可执行模块
"""
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="AppiumRunner",
    version="0.0.1",
    author="hctestedu.com",
    author_email="zhangfeng0103@live.com",
    description="app ui 自动化测试工具",
    license="GPLv3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
        "Contact Us": "http://www.hctestedu.com",
    },

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
    ],
    # 需要安装的依赖
    install_requires=[
        "pytest~=6.2.5",
        "pytest-html",
        "selenium~=3.141.0",
        "Appium-Python-Client~=1.2.0",
        "py~=1.10.0",
        "xlrd~=2.0.1",
        "ruamel.yaml"
    ],
    # package_dir={"root": "src/appiumrunner"},
    # packages=setuptools.find_packages(where="appiumrunner"),
    packages=["appiumrunner"],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            'appiumrun=appiumrunner.cli:main'
        ]
    },
    zip_safe=False
)