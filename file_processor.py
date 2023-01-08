import pandas as pd
from utils.command import CommandSet
from tree import Tree
from utils.constants import LEVEL_ORDER, DOMAINS, ROOT_LEVEL

class KreportProcessor(object):

    def __init__(self, commands: CommandSet):
        self.commands = commands
        self.kreport = None

    def process_kreport(self):
        kreport = pd.read_csv(self.commands.kreport_file,
                              sep='\t',
                              names=['per_node',
                                     'tot_taxon',
                                     'tot_root_taxon',
                                     'level',
                                     'taxid',
                                     'taxon_name'])
        # exclude non used levels
        kreport = kreport[kreport['level'] != 'U']
        kreport = kreport[kreport['level'] != 'R1']
        kreport = kreport[kreport['level'] != 'R2']
        kreport['taxon_name'] = kreport['taxon_name'].apply(lambda x: x.strip())
        kreport['taxon'] = kreport['taxid'].astype(str) \
                           + '-' \
                           + kreport['taxon_name'].astype(str)
        kreport = kreport[['taxon', 'taxid', 'taxon_name', 'level', 'tot_taxon']]
        kreport.set_index('taxon', inplace=True)
        self.kreport = kreport
        self.filter_sublevels()

    def filter_sublevels(self):
        if not self.commands.keep_sublevels:
            self.kreport = self.kreport[~self.kreport['level'].str.contains("[A-Z]\d+")]

    def filter_sublevels(self):
        if not self.commands.keep_sublevels:
            self.kreport = self.kreport[~self.kreport['level'].str.contains("[A-Z]\d+")]
