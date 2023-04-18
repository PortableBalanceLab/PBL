#!/usr/bin/env python3

# command-line interface (CLI) for `pbl`
#
# this is ultimately what running `pbl {command}` in the terminal does

import pbl.setup

import argparse


def main():
    parser = argparse.ArgumentParser(prog='pbl', description='command-line interface for the PortableBalanceLab helper code')
    subparsers = parser.add_subparsers(dest='command', required=True)

    # add 'setup' command
    parser_setup = subparsers.add_parser("setup", help="setup your Raspberry Pi ready for all PortableBalanceLab practicals")
    parser_setup.set_defaults(command=pbl.setup.setup)

    parsed = parser.parse_args()
    parsed.command()

if __name__ == '__main__':
    main()
