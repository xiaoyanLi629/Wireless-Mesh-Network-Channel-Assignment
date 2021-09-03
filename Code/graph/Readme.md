Run the following command to install required module in your python 
```bash
python -m pip install -r .\requirements.txt
```


To get the graph analysis plots, run
```bash
python main.py --plot_graph_analysis
```


To get plots of intermidiate steps of the 3 node graph, run
```bash
python main.py --plot_special_n3
```


To get plots of intermidiate steps of the 4 node graph, run
```bash
python main.py --plot_special_n4
```

To get plots of the performance by varing number of nodes, run
```bash
python main.py --plot_performance --use_base --use_sfs --min_node 5 --max_node 100
```


To get plots of the intermeditate performance for 100 nodes, run
```bash
python main.py --plot_performance --use_base --use_sfs --min_node 100 --max_node 100
```