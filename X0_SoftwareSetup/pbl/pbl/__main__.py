#!/usr/bin/env python3

# command-line interface (CLI) for `pbl`
#
# this is ultimately what running `pbl {command}` in the terminal does

import pbl
import pbl.test

import argparse
import importlib.util

def _install_cli_wrapper(args):
    if hasattr(args, "modules") and len(args.modules) > 0:
        loaded_modules = set()
        for module in args.modules:
            spec = importlib.util.find_spec(f"pbl.{module}")
            if not spec:
                raise RuntimeError(f"{module}: cannot load module")
            else:
                loaded_modules.add(spec.loader.load_module())
        pbl.install(loaded_modules)
    else:
        pbl.install()

def main():
    parser = argparse.ArgumentParser(prog='pbl', description='command-line interface for the PortableBalanceLab helper code')
    subparsers = parser.add_subparsers(dest='command', required=True)

    # add 'install' command
    parser_install = subparsers.add_parser("install", help="setup + install software your Raspberry Pi ready for all PortableBalanceLab practicals")
    parser_install.add_argument("modules", nargs="*")
    parser_install.set_defaults(command=_install_cli_wrapper)

    # add 'test' command
    parser_test = subparsers.add_parser("test", help="run all unit tests")
    parser_test.set_defaults(command=lambda args: pbl.test.test())

    parsed = parser.parse_args()
    parsed.command(parsed)

if __name__ == '__main__':
    main()
