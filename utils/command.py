class CommandSet(object):
    """This class represents the input line commands."""

    def __init__(self,
                 kreport_file,
                 output_path,
                 excluded_nodes,
                 domain,
                 min_viruses,
                 min_bacteria,
                 min_archaea,
                 min_eukarya,
                 min_level,
                 chart_type):

        self.kreport_file = kreport_file
        self.domain = domain
        self.output_path = output_path
        self.excluded_nodes = excluded_nodes
        self.min_viruses = min_viruses
        self.min_bacteria = min_bacteria
        self.min_archaea = min_archaea
        self.min_eukarya = min_eukarya
        self.min_level = min_level
        self.chart_type = chart_type
