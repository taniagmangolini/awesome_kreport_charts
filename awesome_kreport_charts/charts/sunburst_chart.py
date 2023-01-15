# Default python packages
import logging

# pip installed python packages
import plotly.graph_objects as go

# imports from other files
try:
    from utils.tree_processor import TreeProcessor
except ImportError as e:
    from ..utils.tree_processor import TreeProcessor


class SunBurstChart(object):
    """SunBurst chart processor."""

    def __init__(self, kreport, commands):
        self.commands = commands
        self.tree_processor = TreeProcessor(kreport, commands)

    def plot(self):
        """Generate the SunBurst Chart and export to a HTML file in the
        output path."""

        labels, sources, targets, _ = self.tree_processor.prepare_nodes(self.commands.domain)
        sources_labels = [labels[source] for source in sources]
        targets_labels = [labels[target] for target in targets]

        logging.info(f'sources_labels, {len(sources_labels)}, \
                     targets_labels, {len(targets_labels)}')

        fig = go.Figure()

        fig.add_trace(go.Sunburst(
            ids=targets_labels,
            labels=targets_labels,
            parents=sources_labels,
            domain=dict(column=0)
        ))

        fig.update_layout(
            grid = dict(columns=2, rows=1),
            margin = dict(t=0, l=0, r=0, b=0)
        )

        fig.write_html(self.commands.output_path)
