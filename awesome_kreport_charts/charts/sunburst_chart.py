# Default python packages
import logging

# pip installed python packages
import plotly.graph_objects as go

# imports from other files
try:
    from charts.chart import Chart
    from utils.tree_processor import TreeProcessor
    from utils.constants import SUNBURST_VALUES, DOMAINS, EUKARYOTA
except ImportError:
    from ..charts.chart import Chart
    from ..utils.tree_processor import TreeProcessor
    from ..utils.constants import SUNBURST_VALUES, DOMAINS, EUKARYOTA


class SunBurstChart(Chart):
    """SunBurst chart processor."""

    def __init__(self, kreport, commands):
        self.commands = commands
        self.tree_processor = TreeProcessor(kreport, commands)

    def add_root(self, sources_labels, targets_labels, values):
        """Add root if chart should include all domains."""
        for domain in [*DOMAINS, *[EUKARYOTA]]:
            if domain in sources_labels:
                sources_labels = [*['root'], *sources_labels]
                targets_labels = [*[domain], *targets_labels]
                for node in self.tree_processor.nodes:
                    if node.name == domain:
                        values = [*[node.lvl_reads], *values]
                        break
        return sources_labels, targets_labels, values

    def plot(self):
        """Generate the SunBurst Chart and export to a HTML file in the
        output path."""

        labels, sources, targets, values = self.tree_processor\
            .prepare_nodes(self.commands.domain)

        sources_labels = [labels[source] for source in sources]
        targets_labels = [labels[target] for target in targets]

        if self.commands.domain is None:
            sources_labels, targets_labels, values = self.add_root(
                sources_labels,
                targets_labels,
                values)

        logging.info(f'sources_labels, {len(sources_labels)}, \
                     targets_labels, {len(targets_labels)}')

        fig = go.Figure()

        if self.commands.chart_type == SUNBURST_VALUES:
            fig.add_trace(go.Sunburst(
                ids=targets_labels,
                labels=targets_labels,
                parents=sources_labels,
                values=values,
                domain=dict(column=0),
            ))
        else:
            fig.add_trace(go.Sunburst(
                ids=targets_labels,
                labels=targets_labels,
                parents=sources_labels,
                domain=dict(column=0),
            ))

        fig.update_layout(
            grid=dict(columns=2, rows=1),
            margin=dict(t=0, l=0, r=0, b=0)
        )

        fig.write_html(self.commands.output_path)
