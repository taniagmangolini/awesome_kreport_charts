# Awesome Kreport Charts

Create awesome charts for kreports (kraken-style reports).
The following charts are available:

* sankey
* sunburst_no_values
* sunburst_values

There are some chart examples at samples_files folder.

It is possible to show all domains, or select some domain to show (Viruses, Bacteria, Archaea or Eukarya).
You can also apply filters such as minimum reads/contigs and exclude taxons.

To know more about kreports: https://ccb.jhu.edu/software/kraken/MANUAL.html#output-format

#### Multi Kreport File

It is possible to generate a consolidate kreport file from multiple samples using the following script:

https://github.com/jenniferlu717/KrakenTools/blob/master/combine_kreports.py

Example of usage:

Download the merging script at https://raw.githubusercontent.com/jenniferlu717/KrakenTools/master/combine_kreports.py and run the following command (adapt the command to your sample files):

```python combine_kreports.py --only-combined  --no-headers --report-files sample1.kreport sample_2.kreport sample_3.kreport -o merged.kreport```

The consolidated kreport can be used as input for awesome_kreports_charts tool.


#### Instalation

##### Install with pip:

```pip install awesome-kreport-charts```

More info: https://pypi.org/project/awesome-kreport-charts/1.1.0/

##### Install from source:

```git clone https://github.com/taniagmangolini/awesome-kreport-charts.git```

```cd awesome_kreport_charts```

```python3 setup.py install```


#### Help

Use the following command to see all the options:

```python main.py --helṕ```


#### History

* 0.0.1: first release
* 0.0.2: add project info
* 1.0.0: add sunburst chart
* 1.1.0: add sunburst_values and sunburst_no_values charts, fix sunburst values to child values and all domains.
* 1.1.1: style fixes
* 1.1.2: add chart abstract class and merging kreports option.

#### Usage as a command line tool

```python3 awesome_kreport_charts -mb 1000 -mv 5 --exclude 9606 8959 -o sample_files/sankey-all.html -- sample_files/sample.kreport```

```python3 awesome_kreport_charts --min_bacteria 10  --chart sunburst_no_values -o sample_files/sunburst__no_values_all.html -- sample_files/sample.kreport```

```python3 awesome_kreport_charts --min_bacteria 10  --chart sunburst_values -o sample_files/sunburst__values_all.html -- sample_files/sample.kreport```


#### Import as a package

You can import it to your own project and generate the charts as the example below:

```
from awesome_kreport_charts.models.command import CommandSet
from awesome_kreport_charts.utils.file_processor import KreportProcessor
from awesome_kreport_charts.charts.sankey_chart import SankeyChart
from awesome_kreport_charts.charts.sunburst_chart import SunBurstChart


commands = CommandSet(kreport_file='sample_files/sample.kreport',
                      domain=None,
                      excluded_nodes=[],
                      min_viruses=1,
                      min_bacteria=100,
                      min_archaea=1,
                      min_eukarya=1,
                      min_level='S',
                      chart_type='sankey',
                      output_path='sample_files/sample.html')

kreport_processor = KreportProcessor(commands)
kreport_processor.process_kreport()

if commands.chart_type == 'sankey':
    chart = SankeyChart(kreport_processor.kreport, commands)
if commands.chart_type == 'sunburst':
    chart = SunBurstChart(kreport_processor.kreport, commands)
chart.plot()
```