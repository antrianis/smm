===================================
 Command Line Tool for Easy Lookup
===================================

Cannot remember an oneliner? Use this :).

Installation
============

Currently we have no packaging set up. So you have to clone the source and run ``python setup.py install``
or if you want to work on the model just run ``python setup.py develop`` so that the package is just a link to
your source. Since the project is in the early stage, please manually install the dependencies in a venv:
``pip install -r requirements.txt``

Data is stored in the file ```smmdbstore.json``` on the path specified under env variable ```SMMENVDBPATH```.
If ```SMMENVDBPATH``` is not set, ```smm``` uses default location ```~/.smmdbstore/```.

Autocomplete:
Copy ```etc/smm-complet
e.sh``` to your favorite destination. Add ```smm``` path to the ```PATH``` variable
(e.g. export PATH=~/venvs/smm/bin/:$PATH) and add to your ```.bashrc``` profile
```. ~/.smmdbstore/smm-complete.sh``` or ```. /path/to/smm-complete.sh ``` if you are using different location.



Usage
=====

```$ smm```                             # prints help and usage
```$ smm all```                         # prints all commands
```$ smm cmds [args]```                 # prints names of the commands on the given level
```$ smm find command [subcommands]```  # prints commands on the given level

