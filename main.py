from pathlib import Path
import argparse
from command import CommandSet
from file_processor import KreportProcessor
from sankey_chart import SankeyChart


parser = argparse.ArgumentParser()

parser.add_argument("kreport_path")

parser.add_argument('-mv',
                    '--min_qtd_viruses',
                    type=int,
                    default=1,
                    help="Minimum quantity of reads or contigs fpr Viruses. Default: 1.")

parser.add_argument('-mb',
                    '--min_qtd_bacteria',
                    type=int,
                    default=1,
                    help="Minimum quantity of reads or contigs for Bacteria. Default: 1.")

parser.add_argument('-ma',
                    '--min_qtd_archaea',
                    type=int,
                    default=1,
                    help="Minimum quantity of reads or contigs for Archaea. Default: 1.")

parser.add_argument('-me',
                    '--min_qtd_eukarya',
                    type=int,
                    default=1,
                    help="Minimum quantity of reads or contigs for Eukarya. Default: 1.")

parser.add_argument('-d',
                    '--domain',
                    choices=["V", "B", "A", "E"],
                    default='-',
                    help="Domains to include: V (Viruses), B (Bacteria), A (Archaea), \
                    E (Eukarya). Default: include all domains. Example of Usage: -d V")

parser.add_argument('-e',
                    '--exclude',
                    nargs="*",
                    type=int,
                    help="One or more taxon id to be ignored (use spaces for more than one). \
                    Example of usage: -e 9606 247 -- ")

parser.add_argument('-s',
                    '--sub',
                    choices=["y", "n"],
                    default='n',
                    help="Include sub categories such as S1, G2, F1 etc. \
                    Usage: y=yes; n=no. Default: n")

parser.add_argument('-ml',
                    '--min_level',
                    choices=["D", "K", "P", "C", "O", "F", "G", "S"],
                    default='S',
                    help='Minimum level to show (D=Domain, K=Kingdom, P=Phyllum, \
                    C=Class, O=order, F=Family, G=Genus, S=Species). Default: S.')

parser.add_argument('-o',
                    '--output_path',
                    required=True,
                    help='Chart output path.')

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
                              min_reads_viruses=args.min_qtd_viruses,
                              min_reads_bacteria=args.min_qtd_bacteria,
                              min_reads_archaea=args.min_qtd_archaea,
                              min_reads_eukarya=args.min_qtd_eukarya,
                              min_level=args.min_level,
                              output_path=Path(args.output_path),
                              keep_sublevels=True if args.sub == 'y' else False)

        kreport_processor = KreportProcessor(commands)
        kreport_processor.process_kreport()

        sankey = SankeyChart(kreport_processor.kreport, commands)
        sankey.plot_sankey()

    except Exception as e:
        print(['ERROR'], e)
