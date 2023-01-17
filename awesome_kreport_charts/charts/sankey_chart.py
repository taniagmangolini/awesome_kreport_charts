# Default python packages
import logging

# pip installed python packages
import plotly.graph_objects as go

# imports from other files
try:
    from charts.chart import Chart
    from utils.tree_processor import TreeProcessor
except ImportError:
    from ..charts.chart import Chart
    from ..utils.tree_processor import TreeProcessor


class SankeyChart(Chart):
    """Sankey chart processor."""

    def __init__(self, kreport, commands):
        self.commands = commands
        self.tree_processor = TreeProcessor(kreport, commands)

    def plot(self):
        """Generate the Sankey Chart and export to a HTML file in the
        output path."""

        labels, sources, targets, values = self.tree_processor.prepare_nodes(
            self.commands.domain)

        params = {'labels': list(labels.values()),
                  'sources': sources,
                  'targets': targets,
                  'values': values}

        logging.info(f'labels, {len(labels)}, \
                     sources, {len(sources)}, \
                     values, {len(values)}, \
                     targets, {len(targets)}')

        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=5,
                line=dict(color="black", width=0.5),
                label=params['labels'],
                hovertemplate='%{label}: %{value}<extra></extra>'
            ),
            link=dict(
                source=params['sources'],
                target=params['targets'],
                value=params['values'],
                hovertemplate='%{source.label}-> \
                    %{target.label}<extra></extra>'
            ))
        ])
        fig.update_layout(font_size=9)
        fig.write_html(self.commands.output_path)
