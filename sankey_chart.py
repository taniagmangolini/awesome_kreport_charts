from tree import Tree
from constants import LEVEL_ORDER, DOMAINS, ROOT_LEVEL
import plotly.graph_objects as go

class SankeyChart(object):

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
        parent_level_id = LEVEL_ORDER[node.level] - 1 if len(node.level) == 1 else LEVEL_ORDER[node.level_adjusted]

        if node.name in DOMAINS:
            parent_level_id = 1

        for candidate_parent in list(reversed(self.nodes[:node.line_number])):
            # In case of same level with different sublevels, check if parent is higher before proceed.
            # For instance, go to next candidate if candidate parent is G2 and node is G1.
            if (len(node.level) > 1 and len(candidate_parent.level) > 1
                    and node.level[0] == candidate_parent.level[0]
                    and int(node.level[1:]) < int(candidate_parent.level[1:])):
                continue
            if (node.level != candidate_parent.level
                    and (candidate_parent.name in DOMAINS
                         or (candidate_parent.level_id <= parent_level_id
                             and node.level != candidate_parent.level))):
                node.parent = candidate_parent
                break

    def _get_children_nodes(self, node):
        if node.name != ROOT_LEVEL:
            for candidate_child in self.nodes[node.line_number:]:
                if node.taxid == candidate_child.parent.taxid:
                    node.add_child(candidate_child)

    def _get_nodes_relations(self):
        """process nodes parents and children."""
        for node in self.nodes:
            self._get_parent_node(node)
        for node in self.nodes:
            self._get_children_nodes(node)

    def _get_node_domain(self, node, previous_node=None):
        if not node or node.name == ROOT_LEVEL:
            return previous_node.name
        return self._get_node_domain(node.parent, node)

    def _set_domains(self):
        for node in self.nodes:
            if node.name != ROOT_LEVEL:
                node.domain = self._get_node_domain(node)

                if node.domain == 'Viruses':
                    self.viruses.append(node)
                elif node.domain == 'Bacteria':
                    self.bacteria.append(node)
                elif node.domain == 'Archaea':
                    self.archaea.append(node)
                else:
                    self.eukarya.append(node)

        self.all.extend(self.viruses)
        self.all.extend(self.bacteria)
        self.all.extend(self.archaea)
        self.all.extend(self.eukarya)

        print(f'viruses: {len(self.viruses)}, bacteria: {len(self.bacteria)}, \
                archaea: {len(self.archaea)}, eukarya: {len(self.eukarya)}, \
                total: {len(self.all)}')

    def _get_adjusted_level(self, level):
        level_adjusted = level if len(level) == 1 else level[0]
        return level_adjusted, LEVEL_ORDER[level_adjusted]

    def get_nodes(self):
        for line_number, line in enumerate(self.kreport.values.tolist()):
            level_adjusted, level_adjusted_id = self._get_adjusted_level(line[2])
            node = Tree(line_number=line_number,
                        taxid=line[0],
                        name=line[1],
                        level=line[2],
                        level_adjusted=level_adjusted,
                        level_id=level_adjusted_id,
                        lvl_reads=line[3])
            self.nodes.append(node)
        self._get_nodes_relations()
        self._set_domains()

    def _prepare_sankey(self, selected_nodes):
        labels = {0: 'root'}
        sources = []
        targets = []
        values = []
        index = 0

        print(f'Processing {len(selected_nodes)} nodes')
        for node in selected_nodes:
            if node == 'root' or not node.children or node.excluded:
                print(f'Excluded node {node}')
                continue

            if not node.index:
                index = index + 1
                node.index = index

            print(f'Processing {len(node.children)} children from node {node} ({node.excluded},\
                  {node.index}) (parent {node.parent}, {node.parent.excluded}): {node.lvl_reads}')

            for child in node.children:

                if child.excluded:
                    print(f'- Excluded child {child}')
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

                print(f'- Add child {child}({child.index}): {child.lvl_reads}')
        return labels, sources, targets, values

    def plot_sankey(self):
        self.get_nodes()
        labels, sources, targets, values = self._prepare_sankey(self.eukarya)
        params = {'labels': list(labels.values()),
                  'sources': sources,
                  'targets': targets,
                  'values': values}

        print(f'labels, {len(labels)}, sources, {len(sources)},\
              values, {len(values)}, targets, {len(targets)}')

        fig = go.Figure(data=[go.Sankey(
            node = dict(
                pad = 15,
                thickness = 5,
                line = dict(color = "black", width = 0.5),
                label = params['labels']
            ),
            link = dict(
                source = params['sources'],
                target = params['targets'],
                value = params['values']
            ))
        ])
        fig.update_layout(title_text="Sankey from Kraken Report", font_size=9)
        fig.write_html(self.commands.output_path)
