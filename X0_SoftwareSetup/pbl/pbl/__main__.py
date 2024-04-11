#!/usr/bin/env python3

# command-line interface (CLI) for `pbl`
#
# this is ultimately what running `pbl {command}` in the terminal does

import pbl

import argparse
import importlib.util

# returns a set of python modules based on user-supplied CLI arguments
def _calc_which_modules_to_use(args):

    # by default, run against all modules (e.g. s1, s2, l1)
    modules = pbl.all_modules
    if hasattr(args, "modules") and len(args.modules) > 0:
        # caller explicitly requested specific modules: use those
        modules = set()
        for module in args.modules:
            spec = importlib.util.find_spec(f"pbl.{module}")
            if not spec:
                raise RuntimeError(f"{module}: cannot load module")
            else:
                modules.add(spec.loader.load_module())
    if hasattr(args, "exclude"):
        # caller explicitly requested the exclusion of some modules, exclude them
        excluded_names = {f"pbl.{module}" for module in args.exclude}
        modules = [module for module in modules if module.__name__ not in excluded_names]

    return modules

def _run_install_command(args):
    modules = _calc_which_modules_to_use(args)
    pbl.install(modules)

def _run_test_command(args):
    modules = _calc_which_modules_to_use(args)
    pbl.test(modules)

def _run_hwtest_command(args):
    modules = _calc_which_modules_to_use(args)
    pbl.hwtest(modules)

def main():
    parser = argparse.ArgumentParser(prog='pbl', description='command-line interface for the PortableBalanceLab helper code')
    subparsers = parser.add_subparsers(dest='command', required=True)

    # add 'install' command
    parser_install = subparsers.add_parser("install", help="setup + install software your Raspberry Pi ready for all PortableBalanceLab practicals")
    parser_install.add_argument("modules", nargs="*")
    parser_install.add_argument("--exclude", nargs="*", help="which module(s) to exclude from installation (e.g. s1 s2)", default=[])
    parser_install.set_defaults(command=_run_install_command)

    # add 'test' command
    parser_test = subparsers.add_parser("test", help="run all unit tests")
    parser_test.add_argument("modules", nargs="*")
    parser_test.add_argument("--exclude", nargs="*", help="which module(s) to exclude from testing (e.g. s1 s2)", default=[])
    parser_test.set_defaults(command=_run_test_command)

    # add 'hardware-test' command
    parser_hwtest = subparsers.add_parser("hwtest", help="run all hardware tests")
    parser_hwtest.set_defaults(command=_run_hwtest_command)
    parser_hwtest.add_argument("modules", nargs="*")
    parser_hwtest.add_argument("--exclude", nargs="*", help="which module(s) to exclude from testing (e.g. s1 s2)", default=[])

    parsed = parser.parse_args()
    parsed.command(parsed)

if __name__ == '__main__':
    main()

