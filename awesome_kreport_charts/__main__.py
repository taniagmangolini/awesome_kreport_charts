#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__autor__ = "Tania Girao Mangolini"
__credits__ = ["Tania Girao Mangolini"]
__License__ = "BSD"
__mantainer__ = "Tania Girao Mangolini"
__email__= "taniagmangolini@gmail.com"
__status__= "Development"
__version__= "0.0.2"

# Default python packages
import argparse
import logging
from pathlib import Path

# imports from other files
from utils.file_processor import KreportProcessor
from charts.sankey_chart import SankeyChart
from models.command import CommandSet


parser = argparse.ArgumentParser()

parser.add_argument("kreport_path")

parser.add_argument('-mv',
                    '--min_viruses',
                    type=int,
                    default=1,
                    help="Minimum quantity of reads or contigs for Viruses.\
                        Default: 1.")

parser.add_argument('-mb',
                    '--min_bacteria',
                    type=int,
                    default=1,
                    help="Minimum quantity of reads or contigs for Bacteria.\
                        Default: 1.")

parser.add_argument('-ma',
                    '--min_archaea',
                    type=int,
                    default=1,
                    help="Minimum quantity of reads or contigs for Archaea.\
                        Default: 1.")

parser.add_argument('-me',
                    '--min_eukarya',
                    type=int,
                    default=1,
                    help="Minimum quantity of reads or contigs for Eukarya.\
                        Default: 1.")

parser.add_argument('-d',
                    '--domain',
                    choices=["V", "B", "A", "E"],
                    help="Domains to include: V (Viruses), B (Bacteria), A (Archaea), \
                    E (Eukarya). Default: include all domains. Example of Usage: -d V")

parser.add_argument('-e',
                    '--exclude',
                    nargs="*",
                    type=int,
                    help="One or more taxon id to be ignored (use spaces for more than one). \
                    Example of usage: -e 9606 247 -- ")

parser.add_argument('-ml',
                    '--min_level',
                    choices=["D", "K", "P", "C", "O", "F", "G", "S"],
                    default='S',
                    help='Minimum level to show (D=Domain, K=Kingdom, P=Phyllum, \
                    C=Class, O=order, F=Family, G=Genus, S=Species). Default: S.')

parser.add_argument('-c',
                    '--chart_type',
                    choices=["sankey"],
                    default='sankey',
                    help='Chart type. Options: sankey. Default: sankey.')

parser.add_argument('-o',
                    '--output_path',
                    required=True,
                    help='Chart output path.')

parser.add_argument('-v',
                    '--version',
                    action='version',
                    version='%(prog)s {version}'.format(version=__version__),
                    help='Show the current version.')

args = parser.parse_args()

kreport_path = Path(args.kreport_path)

if not kreport_path.exists():
    parser.exit(1, message="[ERROR] Kreport file not found.")

if not args.output_path:
    parser.exit(1, message="[ERROR] Output path should be provided.")

if __name__ == '__main__':

    try:
        commands = CommandSet(kreport_file=Path(args.kreport_path),
                              domain=args.domain,
                              excluded_nodes=args.exclude if args.exclude else [],
                              min_viruses=args.min_viruses,
                              min_bacteria=args.min_bacteria,
                              min_archaea=args.min_archaea,
                              min_eukarya=args.min_eukarya,
                              min_level=args.min_level,
                              chart_type=args.chart_type,
                              output_path=Path(args.output_path))

        kreport_processor = KreportProcessor(commands)
        kreport_processor.process_kreport()

        sankey = SankeyChart(kreport_processor.kreport, commands)
        sankey.plot_sankey()

    except Exception as e:
        logging.error('[ERROR]', e)
