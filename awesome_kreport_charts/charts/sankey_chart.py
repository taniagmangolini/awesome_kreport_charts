# Default python packages
import logging

# pip installed python packages
import plotly.graph_objects as go

# imports from other files
try:
    from models.tree import Tree
    from utils.constants import LEVEL_ORDER, DOMAINS, ROOT_LEVEL, VIRUSES,\
        BACTERIA, ARCHAEA, EUKARYA
except ImportError as e:
    from ..models.tree import Tree
    from ..utils.constants import LEVEL_ORDER, DOMAINS, ROOT_LEVEL, VIRUSES,\
        BACTERIA, ARCHAEA, EUKARYA


class SankeyChart(object):
    """Sankey chart processor."""

    def __init__(self, kreport, commands):
        self.commands = commands
        self.kreport = kreport
        self.nodes = []
        self.viruses = []
        self.bacteria = []
        self.archaea = []
        self.eukarya = []
        self.all = []

    def _get_parent_node(self, node):
        """Iterate backwards parting from the node position
        until find the parent node."""

        parent_level_id = LEVEL_ORDER[node.level] - 1

        if node.name in DOMAINS:
            parent_level_id = 1

        for candidate_parent in list(reversed(self.nodes[:node.line_number])):
            if (node.level != candidate_parent.level
                    and (candidate_parent.name in DOMAINS
                         or (candidate_parent.level_id <= parent_level_id
                             and node.level != candidate_parent.level))):
                node.parent = candidate_parent
                break

    def _get_children_nodes(self, node):
        """Get the child nodes for a node."""

        if node.name != ROOT_LEVEL:
            for candidate_child in self.nodes[node.line_number:]:
                if node.taxid == candidate_child.parent.taxid:
                    node.add_child(candidate_child)

    def _get_nodes_relations(self):
        """Process nodes parents and children."""

        for node in self.nodes:
            self._get_parent_node(node)
        for node in self.nodes:
            self._get_children_nodes(node)

    def _check_node_exclusion(self, node, min_quantity):
        """Mark node and node children as excluded
        if they dont pass the filters."""

        min_level = self.commands.min_level
        if node.lvl_reads < min_quantity \
            or node.taxid in self.commands.excluded_nodes \
                or LEVEL_ORDER[node.level] > LEVEL_ORDER[min_level]:
                    node.excluded = True
                    for child in node.children:
                        if child.taxid not in self.commands.excluded_nodes:
                            self.commands.excluded_nodes.append(child.taxid)
                            self._check_node_exclusion(child, min_quantity)

    def _filter_nodes(self, selected_nodes, min_reads):
        """Apply min reads, min level and taxids exclusion filters."""

        for node in selected_nodes:
            self._check_node_exclusion(node, min_reads)

    def _get_node_domain(self, node, previous_node=None):
        """Get the domain for nodes. The nodes can be in the
        following domains: Archaea, Bacteria, Viruses or Eukarya. """

        if not node or node.name == ROOT_LEVEL:
            return previous_node.name
        return self._get_node_domain(node.parent, node)

    def _set_domains(self):
        for node in self.nodes:
            if node.name != ROOT_LEVEL:
                node.domain = self._get_node_domain(node)

                if node.domain == VIRUSES:
                    self.viruses.append(node)
                elif node.domain == BACTERIA:
                    self.bacteria.append(node)
                elif node.domain == ARCHAEA:
                    self.archaea.append(node)
                else:
                    self.eukarya.append(node)

        logging.info(f'{VIRUSES}: {len(self.viruses)}, \
            {BACTERIA}: {len(self.bacteria)}, \
            {ARCHAEA}: {len(self.archaea)}, \
            {EUKARYA}: {len(self.eukarya)}, \
            total: {len(self.all)}')

    def _apply_filters(self):
        """Apply filters to domains."""

        self._filter_nodes(self.viruses, self.commands.min_viruses)
        self.all.extend(self.viruses)

        self._filter_nodes(self.bacteria, self.commands.min_bacteria)
        self.all.extend(self.bacteria)

        self._filter_nodes(self.archaea, self.commands.min_archaea)
        self.all.extend(self.archaea)

        self._filter_nodes(self.eukarya, self.commands.min_eukarya)
        self.all.extend(self.eukarya)

    def get_nodes(self):
        """Extract the hierarchy of nodes from the kreport."""

        for line_number, line in enumerate(self.kreport.values.tolist()):
            node = Tree(line_number=line_number,
                        taxid=line[0],
                        name=line[1],
                        level=line[2],
                        level_id=LEVEL_ORDER[line[2]],
                        lvl_reads=line[3])
            self.nodes.append(node)
        self._get_nodes_relations()
        self._set_domains()
        self._apply_filters()

    def _prepare_sankey(self, selected_nodes):
        """Prepare nodes data to be represented in a Sankey Chart."""

        labels = {0: ROOT_LEVEL}
        sources = []
        targets = []
        values = []
        index = 0

        logging.info(f'Processing {len(selected_nodes)} nodes')
        for node in selected_nodes:
            if node == 'root' or not node.children or node.excluded:
                logging.info(f'Excluded node {node}')
                continue

            if not node.index:
                index = index + 1
                node.index = index

            logging.info(f'Processing {len(node.children)} children from \
                         node {node}({node.index}): {node.lvl_reads}')

            for child in node.children:

                if child.excluded:
                    logging.info(f'- Excluded child {child}')
                    continue

                if node.index not in labels:
                    labels[node.index] = node.name

                sources.append(node.index)
                values.append(node.lvl_reads)

                if not child.index:
                    index = index + 1
                    child.index = index

                targets.append(child.index)

                if child.index not in labels:
                    labels[child.index] = child.name

                logging.info(f'- Add child {child}({child.index}): \
                             {child.lvl_reads}')
        return labels, sources, targets, values

    def plot_sankey(self):
        """Generate the Sankey Chart and export to a HTML file in the
        output path."""

        self.get_nodes()
        labels, sources, targets, values = self._prepare_sankey(self.all)
        params = {'labels': list(labels.values()),
                  'sources': sources,
                  'targets': targets,
                  'values': values}

        logging.info(f'labels, {len(labels)}, \
                     sources, {len(sources)}, \
                     values, {len(values)}, \
                     targets, {len(targets)}')

        fig = go.Figure(data=[go.Sankey(
            node = dict(
                pad = 15,
                thickness = 5,
                line = dict(color = "black", width = 0.5),
                label = params['labels'],
                hovertemplate = '%{label}: %{value}<extra></extra>'
            ),
            link = dict(
                source = params['sources'],
                target = params['targets'],
                value = params['values'],
                hovertemplate = '%{source.label}-> %{target.label}<extra></extra>'
            ))
        ])
        fig.update_layout(font_size=9)
        fig.write_html(self.commands.output_path)
