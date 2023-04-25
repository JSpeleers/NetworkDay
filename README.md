# NetworkDay

## Install

0. Open terminal in this directory
1. Create a Python virtual environment: `$ python -m venv venv`
2. Activate the virtual environment 
   - Windows: `$ venv\Scripts\activate.bat`
   - Unix & MacOS: `$ source btd6bot/bin/activate`

3. You might need to upgrade setuptools: $ pip install setuptools -U
4. Install requirements: `$ pip install -r requirements.txt`

## Run

Without email output

`python main.py -f ./examples/Formulierreacties_120p_10t_5p.csv -r 3 -p 2 -t 10`

With email output

`python main.py -f ./examples/Formulierreacties_120p_10t_5p.csv -r 3 -p 2 -t 10 --emails`

### Params

----------
| Short | Long | Description | Default          |
|-------|------|-------------|------------------|
| -f | --file | path to the preference sheet | none - mandatory | 
| -r | --rounds | number of rouds | none - mandatory | 
| -p | --preferences | minimal number of preferred topics per participants | none - mandatory |
| -t | --topics | number of topics | none - mandatory |
| -g | --generations | number of generations before stopping | 1000 |
----------
