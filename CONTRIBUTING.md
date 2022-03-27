<a href='https://https://pypi.org/project/nptyping/'>
  <img src='https://github.com/ramonhagenaars/nptyping/raw/master/resources/logo.png' />
</a> 

# *Contributing*

* [Introduction](#Introduction)
* [Bug reporting](#Bug-reporting)
* [Pull requests](#Pull-requests)
* [Development](#Development)

## Introduction
Thank you for showing interest in contributing to this library. This document is intended to be a guideline to make any
contribution as smooth as possible.

## Bug reporting
When reporting a bug, please first check if it has been reported already in the list of 
[issues](https://github.com/ramonhagenaars/nptyping/issues). Also check the 
[closed ones](https://github.com/ramonhagenaars/nptyping/issues?q=is%3Aissue+is%3Aclosed).

If your bug was not specified earlier, please [open a new issue](https://github.com/ramonhagenaars/nptyping/issues/new).
When describing your bug, try to be as clear as possible. At least provide:

* the Python version you used
* the `nptyping` version you used
* the Operating system you were on

If applicable and possible, provide a complete stacktrace of the error.

## Pull requests
You are free to open pull requests: this is highly appreciated! To avoid any waste of valuable developer time, it is
recommended to first [open a new issue](https://github.com/ramonhagenaars/nptyping/issues/new) describing the 
feature/fix that you propose. This is not mandatory though. 

A pull request can be merged when:
* all [checks](https://github.com/ramonhagenaars/nptyping/actions) are green
* the content is deemed an improvement
* the code is deemed acceptable

## Development
Prerequisites:
* A Python version within the `nptyping` [supported range](https://github.com/ramonhagenaars/nptyping/blob/master/nptyping/package_info.py)
* An IDE to your liking

### Step 1: clone this repository
Clone this repo in a space on your machine that you have sufficient rights on. For more info on cloning, please refer to
the [Github Docs](https://docs.github.com/en/get-started/getting-started-with-git/about-remote-repositories#cloning-with-https-urls).

### Step 2: install invoke
The build tool `invoke` is used in this repository. It is recommended to install it in your global python setup:
```
pip install invoke
```

### Step 3: setup a ready-to-go virtual environment
Make sure you cd to the directory of this repo that contains `tasks.py`. Then you can execute the following:
```
invoke venv install
```

When done, you can check all available build options by executing:
```
invoke --list
```

#### Optional: different Python versions
Optionally, you can create multiple virtual environments for different Python versions. To do so, make sure you have
`invoke` installed on that Python version, then use that specific Python interpreter to create a virtual environment.
Here is an example of how that command would look like on a Windows machine:
```
C:\Users\guidovanrossum\AppData\Local\Programs\Python\Python38\python -m invoke venv
```
If you now invoke the tests, it will by default execute them using multiple virtual environments. this lets you check
compatibility with different Python versions.

### Step 4: start developing
You are now ready to go. You might want to point your IDEs interpreter to the Python executable in the created virtual 
environment.

While you develop, it is a good idea to run the following tasks every now and then:
```
invoke format qa coverage
```

Happy coding!
