# WEB APP API

Detect defacement of a website(s)

## Requirement

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirements

```bash
pip install flask, flask_restful, sqlalchemy
pip install apscheduler
pip install selenium
```

Download [Chrome Driver](https://chromedriver.chromium.org/downloads) to open selenium webdriver

## Features

Auto scan every 15 minutes

- /: list all websites
- /<company name>: list all websites from <company name>
- /<company name>/<url>: all info of <url>
- /check: scan all
- /check/<company name>: scan all websites from <company name>
- /check/<company name>/<url>: scan <url>

## Example:

```json
    "google.com": [              [1]
        {
            "Meta": "Normal",    [2]
            "Strings": "Normal"  [3]
        },
        "Company: google"        [4]
    ]
```
    [1]: Url of website
    [2]: Meta tag info: {Changed, Normal}
    [3]: Check illegal String: {Illegal, Normal}
    [4]: Company name
