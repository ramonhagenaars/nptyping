import subprocess

_CHECK_ONLY = 'check' in COMMAND_LINE_TARGETS
_CONTINUE = 'continue' in COMMAND_LINE_TARGETS
_SUBJECT = 'nptyping'


def _exec(cmd: str) -> None:
    print('>>> {}'.format(cmd))
    exit_code = subprocess.call(cmd, shell=True)
    if exit_code != 0 and not _CONTINUE:
        print('Exiting with {}'.format(exit_code))
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
    _exec('pycodestyle {} -v --config=setup.cfg'.format(_SUBJECT))

if 'pylint' in COMMAND_LINE_TARGETS:
    _exec('pylint --rcfile=setup.cfg {}'.format(_SUBJECT))

if 'complexity' in COMMAND_LINE_TARGETS:
    _exec('radon cc {} -nc --total-average'.format(_SUBJECT))
    _exec('xenon {} --max-absolute B --max-modules A --max-average A --exclude {}/config.py'.format(_SUBJECT, _SUBJECT))


# FORMAT:

if 'autoflake' in COMMAND_LINE_TARGETS:
    cmd = 'autoflake {} --recursive --in-place --remove-unused-variables'.format(_SUBJECT)
    if _CHECK_ONLY:
        cmd += ' --check'
    _exec(cmd)

if 'isort' in COMMAND_LINE_TARGETS:
    cmd = 'isort {} --recursive --quiet'.format(_SUBJECT)
    if _CHECK_ONLY:
        cmd += ' --check'
    _exec(cmd)

Exit(0)
