from typing import List

from cliglue import *
from tests.asserts import MockIO, assert_cli_error
from tests.parser.actions import *


def test_param_with_2_args():
    with MockIO('--param', 'OK') as mockio:
        CliBuilder(run=print_param).has(
            parameter('--param'),
        ).run()
        assert mockio.output() == 'param: OK\n'
    with MockIO('-p', 'OK') as mockio:
        CliBuilder(run=print_param).has(
            parameter('--param', '-p'),
        ).run()
        assert mockio.output() == 'param: OK\n'


def test_param_with_2_args_with_action():
    with MockIO('run', '--param', 'OK') as mockio:
        CliBuilder().has(
            subcommand('run', run=print_param),
            parameter('param'),
        ).run()
        assert mockio.output() == 'param: OK\n'
    with MockIO('run', '-p', 'OK') as mockio:
        CliBuilder().has(
            subcommand('run', run=print_param),
            parameter('param', 'p'),
        ).run()
        assert mockio.output() == 'param: OK\n'


def test_set_param_with_equals():
    with MockIO('run', '--param=OK') as mockio:
        CliBuilder().has(
            subcommand('run', run=print_param),
            parameter('param'),
        ).run()
        assert mockio.output() == 'param: OK\n'
    with MockIO('run', '-p=OK') as mockio:
        CliBuilder().has(
            subcommand('run', run=print_param),
            parameter('param', 'p'),
        ).run()
        assert mockio.output() == 'param: OK\n'
    with MockIO('--param=OK') as mockio:
        CliBuilder(run=print_param).has(
            parameter('--param'),
        ).run()
        assert mockio.output() == 'param: OK\n'
    with MockIO('-p=OK') as mockio:
        CliBuilder(run=print_param).has(
            parameter('--param', '-p'),
        ).run()
        assert mockio.output() == 'param: OK\n'


def test_no_param():
    with MockIO() as mockio:
        CliBuilder(run=print_param).has(
            parameter('--param', '-p'),
        ).run()
        assert mockio.output() == 'param: None\n'


def test_int_type_param():
    def print_param_and_type(param):
        print(f'param: {param}, type: {type(param).__name__}')

    with MockIO('--param', '42') as mockio:
        CliBuilder(run=print_param_and_type).has(
            parameter('--param', type=int),
        ).run()
        assert mockio.output() == 'param: 42, type: int\n'


def test_missing_required_param():
    with MockIO():
        cli = CliBuilder(run=print_param, help_onerror=False, reraise_error=True).has(
            parameter('--param', required=True),
        )
        assert_cli_error(lambda: cli.run())


def test_multi_parameters():
    def sum_param(param: List[int]):
        print(f'param: {sum(param)}')

    with MockIO('--param', '800', '--param=42') as mockio:
        CliBuilder(run=sum_param).has(
            parameter('param', multiple=True, type=int),
        ).run()
        assert mockio.output() == 'param: 842\n'

    with MockIO() as mockio:
        CliBuilder(run=sum_param).has(
            parameter('param', multiple=True, type=int),
        ).run()
        assert mockio.output() == 'param: 0\n'


def test_strict_choices():
    with MockIO('--param=4'):
        cli = CliBuilder(reraise_error=True).has(
            parameter('param', choices=['42'], strict_choices=True),
        )
        assert_cli_error(lambda: cli.run())

    with MockIO('--param=42'):
        CliBuilder(reraise_error=True).has(
            parameter('param', choices=['42'], strict_choices=True),
        ).run()

    def complete():
        return ['42']

    with MockIO('--param=42'):
        CliBuilder(reraise_error=True).has(
            parameter('param', choices=complete, strict_choices=True),
        ).run()
