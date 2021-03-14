import subprocess

_CHECK_ONLY = 'check' in COMMAND_LINE_TARGETS
_CONTINUE = 'continue' in COMMAND_LINE_TARGETS
_SUBJECT = 'nptyping'


def _exec(cmd: str) -> None:
    print(f'>>> {cmd}')
    exit_code = subprocess.call(cmd, shell=True)
    if exit_code != 0 and not _CONTINUE:
        print(f'Exiting with {exit_code}')
        Exit(exit_code)


# COMBINATIONS:

if 'all' in COMMAND_LINE_TARGETS:
    COMMAND_LINE_TARGETS += ['format', 'quality']

if 'quality' in COMMAND_LINE_TARGETS:
    COMMAND_LINE_TARGETS += ['test', 'doctest', 'coverage', 'pycodestyle', 'pylint', 'complexity']

if 'format' in COMMAND_LINE_TARGETS:
    COMMAND_LINE_TARGETS += ['autoflake', 'isort']


# QUALITY:

if 'test' in COMMAND_LINE_TARGETS:
    _exec('python -m unittest discover tests')

if 'doctest' in COMMAND_LINE_TARGETS:
    _exec('python -m doctest README.md')

if 'coverage' in COMMAND_LINE_TARGETS:
    _exec('coverage run -m unittest discover .')
    _exec('coverage report -m --fail-under=100')

if 'pycodestyle' in COMMAND_LINE_TARGETS:
    _exec(f'pycodestyle {_SUBJECT} -v --config=setup.cfg')

if 'pylint' in COMMAND_LINE_TARGETS:
    _exec(f'pylint --rcfile=setup.cfg {_SUBJECT}')

if 'complexity' in COMMAND_LINE_TARGETS:
    _exec(f'radon cc {_SUBJECT} -nc --total-average')
    _exec(f'xenon {_SUBJECT} --max-absolute B --max-modules A --max-average A --exclude nptyping/config.py')


# FORMAT:

if 'autoflake' in COMMAND_LINE_TARGETS:
    cmd = f'autoflake {_SUBJECT} --recursive --in-place --remove-unused-variables'
    if _CHECK_ONLY:
        cmd += ' --check'
    _exec(cmd)

if 'isort' in COMMAND_LINE_TARGETS:
    cmd = f'isort {_SUBJECT} --recursive --quiet'
    if _CHECK_ONLY:
        cmd += ' --check'
    _exec(cmd)

Exit(0)
