#!/usr/bin/env python3

# command-line interface (CLI) for `pbl`
#
# this is ultimately what running `pbl {command}` in the terminal does

import pbl.install
import pbl.test

import argparse


def main():
    parser = argparse.ArgumentParser(prog='pbl', description='command-line interface for the PortableBalanceLab helper code')
    subparsers = parser.add_subparsers(dest='command', required=True)

    # add 'install' command
    parser_install = subparsers.add_parser("install", help="setup + install software your Raspberry Pi ready for all PortableBalanceLab practicals")
    parser_install.set_defaults(command=pbl.install.install)

    # add 'test' command
    parser_test = subparsers.add_parser("test", help="run all unit tests")
    parser_test.set_defaults(command=pbl.test.test)

    parsed = parser.parse_args()
    parsed.command()

if __name__ == '__main__':
    main()
