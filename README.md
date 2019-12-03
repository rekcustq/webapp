# WEB APP API

Detect defacement of a website(s)

## Requirement

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirements

```bash
pip install flask, flask_restful, sqlalchemy
pip install apscheduler
pip install selenium
```

Download [Chrome Driver](https://chromedriver.chromium.org/downloads) for selenium webdriver

## Features

- Scan a url
- Scan multiple urls
- Auto scan every 15 minutes

## Usage

- /: list all websites
- /?company="company name": list all websites from \"company name\"
- /?company="company name"&url="url": all info of \"url\"
- /?scan=true: scan all
- /?scan=true&company="company name": scan all websites from \"company name\"
- /?scan=true&company="company name"&url="url": scan \"url\"

## Example:

```python
"https://google.com": [              [1]
    {
        "Meta": "Normal",    [2]
        "Strings": "Normal"  [3]
    },
    "Company: google"        [4]
]

[1]: Url and protocol of website
[2]: Meta tag info: {Changed, Normal}
[3]: Check illegal String: {Illegal, Normal}
[4]: Company name
```
