# MGPro

MGPro is a Python Interactive command line toolbox for processing geomagnetic and gravity data

## Installation
### Install MGPro via Pypi

```
pip install mgpro
```

### Install MGPro via source codes
We recommend this way for general user.

1. Download source codes from github

```
git clone https://github.com/xumi1993/MGPro.git
```

2. Install in command line

```
cd /path/to/MGPro
python setup.py install
```

## What does MGPro contain?
### MGPro client
Just enter `mgpro` in command line to run MGPro client. the MGPro interface is shown as follows:

```bash
$ mgpro
MGPro>?

Documented commands (type help <topic>):
========================================
continuation  gradient  help  quit  read  write

Undocumented commands:
======================
dt2za

MGPro>
```

MGPro include functions as follows. Please enter `help cmd` for more details:

- read (r): read a raw data file with 3 columns (x, y, value)
- continuation (c): Calculate continuation and derivative for the data read
- gradient (g): Calculare horizontal gradient or the module
- write (w): Write any result to a txt file

