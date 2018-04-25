from os.path import isfile, isdir
from os import getcwd, listdir
import inspect
from subprocess import Popen, call, PIPE, STDOUT
from ipywidgets import widgets

class SLURMSubmitter(widgets.VBox):
    """
    """

    def __init__(self, simex_calc, time='00:10:00', partition="all"):
        
        widgets.VBox.__init__(self, layout=widgets.Layout(width='100%'))
        
        self.verbose = False        
        self.simex_calc = simex_calc
        #self.nodes_widget = widgets.IntSlider(min=1, max=10, value=nnodes)
        #self.task_widget = widgets.IntSlider(min=1, max=100,
        #                                     value=tasks_per_node)
        self.time_widget = widgets.Text(value=time)
        self.submit_widget = widgets.Button(description="Submit job", button_style="success")
        self.submit_widget.on_click(self.submit_job)
        #self.parallelism_widget = widgets.Dropdown(
        #    options=["mpirun", "CUDA"], value=parallelism)
        self.partition_widget = widgets.Dropdown(options=["all",
                                                         "maxwell",
                                                         "cfel",
                                                         "exfel"], 
                                                 value=partition)
        # ui representation
        self.children = [
            widgets.HBox([widgets.Label("Partition"), self.partition_widget]),
            #widgets.HBox([widgets.Label("Nodes"), self.nodes_widget]),
            #widgets.HBox([widgets.Label("Tasks"), self.task_widget]),
            widgets.HBox([widgets.Label("Time"), self.time_widget]),
            #widgets.HBox([widgets.Label("parallelism"),
            #              self.parallelism_widget]),
            self.submit_widget
        ]
        
        temp_prefix = '''#!/bin/sh
#SBATCH --partition={0}
#SBATCH --time={1}
#SBATCH --nodes={2}
#SBATCH --cpus-per-task={3}
#SBATCH --output={4}'''
        
        temp_suffix = '''
export MODULEPATH=$MODULEPATH:$HOME/simex_dev_workshop/modulefiles
module load python3/3.4
module load simex

python3 {5} {6}
'''

        if self.simex_calc.parameters.gpus_per_task:
            temp_prefix += '\n#SBATCH --constraint=GPU\n'
        self.batch_template = temp_prefix + temp_suffix

    def submit_job(self, b=None):
        # create a dill file from the simex_calculator
        classname = type(self.simex_calc).__name__
        dfile = classname + '.dill'
        self.simex_calc.dumpToFile(dfile)

        # get the path to the module from which the simex_calc is an instance of
        path_to_module = inspect.getfile(type(self.simex_calc))
        
        final_script = self.batch_template.format(
            self.partition_widget.value, 
            self.time_widget.value, 
            self.simex_calc.parameters.nodes_per_task,
            self.simex_calc.parameters.cpus_per_task,
            getcwd() + "/" + classname + '_%A.out', 
            #self.parallelism_widget.value, 
            #self.task_widget.value, 
            path_to_module, 
            dfile)

        if self.verbose:
            print("Would submit the following script:\n", final_script)

        fname = 'batch.sh'
        with open(fname, 'w') as ffile:
            ffile.write(final_script)
        
        slurm = Popen(['sbatch', fname], stdout=PIPE, stderr=STDOUT)
        print(slurm.stdout.read().strip().decode('utf-8'))
