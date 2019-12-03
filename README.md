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
- /?company=__"company name"__: list all websites from __"company name"__
- /?company=__"company name"__&url=__"url"__: all info of __"url"__
- /?scan=__true__: scan all
- /?scan=__true__&company=__"company name"__: scan all websites from __"company name"__
- /?scan=__true__&company=__"company name"__&url=__"url"__: scan __"url"__

## Example:

```cpp
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
