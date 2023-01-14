# pip installed python packages
import pandas as pd

# imports from other files
try:
    from models.command import CommandSet
except ImportError as e:
   from ..models.command import CommandSet


class KreportProcessor(object):
    """Kreport file processor."""

    def __init__(self, commands: CommandSet):
        self.commands = commands
        self.kreport = None

    def process_kreport(self):
        """Process the Kraken Style Report (kreport).
        Exclude non used levels (U, R1 and R2).
        At the end, filter sublevels."""

        kreport = pd.read_csv(self.commands.kreport_file,
                              sep='\t',
                              names=['per_node',
                                     'tot_taxon',
                                     'tot_root_taxon',
                                     'level',
                                     'taxid',
                                     'taxon_name'])
        kreport['taxon_name'] = kreport['taxon_name'].apply(lambda x: x.strip())
        kreport['taxon'] = kreport['taxid'].astype(str) \
                           + '-' \
                           + kreport['taxon_name'].astype(str)
        kreport = kreport[['taxon', 'taxid', 'taxon_name', 'level', 'tot_taxon']]
        kreport.set_index('taxon', inplace=True)

        self.kreport = kreport
        self.filter_non_used_levels()

    def filter_non_used_levels(self):
        """Filter the sublevels and the unclassified level.
        Sublevels are levels followed by a number (Ex: G1) and
        unclassified is denoted by U.
        """

        regex = "[A-Z]\d+"
        self.kreport = self.kreport[self.kreport['level'] != 'U']
        self.kreport = self.kreport[~self.kreport['level'].str.contains(regex)]
