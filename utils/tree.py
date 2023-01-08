class Tree(object):
    """This class represents the nodes extracted from the Kreport."""

    def __init__(self, name,
                 taxid,
                 level,
                 level_id,
                 lvl_reads,
                 line_number,
                 index=None,
                 color=None,
                 parent=None,
                 domain=None,
                 excluded=False,
                 sublevel=0):

        self.name = name
        self.taxid = taxid
        self.index = index
        self.line_number = line_number
        self.level = level
        self.sublevel = sublevel
        self.level_id = level_id
        self.lvl_reads = lvl_reads
        self.color = color,
        self.children = []
        self.parent = parent
        self.domain = domain
        self.excluded = excluded

    def add_child(self, node):
        self.children.append(node)

    def __str__(self):
        return f'{self.taxid}-{self.name}-{self.level}-{self.index}'

    def __eq__(self, other):
        return isinstance(other, type(self)) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(tuple(self.__dict__[k] for k in sorted(self.__dict__)))
