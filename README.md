# Awesome Kreport Charts

Create awesome charts for kreports (kraken-style reports):

To know more about kreports: https://ccb.jhu.edu/software/kraken/MANUAL.html#output-format


#### Instalation

##### Install with pip:

```pip install awesome-kreport-charts==0.0.2```

More info: https://pypi.org/project/awesome-kreport-charts/0.0.2/

##### Install from source:

```git clone https://github.com/taniagmangolini/awesome-kreport-charts.git```

```cd awesome_kreport_charts```

```python3 setup.py install```


#### Help

```python main.py --helṕ```


#### History

* 0.0.1: first release
* 0.0.2: add project info


#### Usage as a command line tool

```python3 awesome_kreport_charts -mb 10000 --exclude 9606 8959 -o sample_files/sankey.html -- sample_files/sample.kreport```

#### Import as a package

You can import it to your own project and generate the charts as the example below:

```
from awesome_kreport_charts.models.command import CommandSet
from awesome_kreport_charts.utils.file_processor import KreportProcessor
from awesome_kreport_charts.charts.sankey_chart import SankeyChart

commands = CommandSet(kreport_file='sample_files/sample.kreport',
                      domain='V',
                      excluded_nodes=[],
                      min_viruses=1,
                      min_bacteria=10000,
                      min_archaea=1,
                      min_eukarya=1,
                      min_level='S',
                      chart_type='sankey',
                      output_path='sample_files/sample2.html')

kreport_processor = KreportProcessor(commands)
kreport_processor.process_kreport()

sankey = SankeyChart(kreport_processor.kreport, commands)
sankey.plot_sankey()```

