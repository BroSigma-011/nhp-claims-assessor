from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='nhp-claims-assessor',
    version='2.0.0',
    author='NHP Claims Assessment Team',
    description='Namibian medical-aid claims assessment with AI chatbot and workflow automation',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/BroSigma-011/nhp-claims-assessor',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Healthcare Industry',
        'Topic :: Office/Business :: Financial',
    ],
    python_requires='>=3.9',
    install_requires=[
        'pandas>=1.5.3',
        'numpy>=1.24.3',
        'plotly>=5.14.0',
        'rapidfuzz>=2.15.1',
        'openpyxl>=3.10.8',
        'pydantic>=2.0.0',
        'requests>=2.31.0',
        'python-dotenv>=1.0.0',
        'transformers>=4.30.2',
    ],
    extras_require={
        'dev': [
            'pytest>=7.4.0',
            'pytest-cov>=4.1.0',
            'black>=23.0.0',
            'flake8>=6.0.0',
            'mypy>=1.0.0',
        ],
        'notebook': [
            'jupyter>=1.0.0',
            'ipywidgets>=8.0.7',
            'gTTS>=2.3.2',
            'duckduckgo-search>=3.9.1',
            'deep-translator>=1.11.4',
        ],
        'web': [
            'fastapi>=0.100.0',
            'uvicorn>=0.23.0',
        ],
    },
)
