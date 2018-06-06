# ACI CLI CMD Parser

This project is to parse ACI CLIs (mainly switch's) from plain text output into categorized dictionaries.

## Getting Started

* This purpose of this project is to create functions and packages for other application.
* Depends on the raw text files, the application needs to produce the below dictionary format before using the package/functions

```
{
"vsh_lc -c 'show xxxx'":
                [
					"output_line1",
					"output_line2",
					.....
				]
"<next command>":
                [
					"output_line1",
					"output_line2",
					.....                    
                ]
}
```

* The key of the dictionary is the command itself. 
* It must be a command run under ibash mode.
* For vsh_lc, vsh or bcm commands, use:

```
"vsh_lc -c"
"vsh -c"
"bcm-shell-hw"
```
* cmd_breaker.py is one of the example.
* For demo/testing purpose, you can use init.py to call the functions for quick demo.

  
## Main packages

### bcm_cmd_parser.py
Currently supported commands:
* bcm-shell-hw 'ps'
* bcm-shell-hw 'show c all'

### ns_cmd_parser.py
Currently supported commands:
* vsh_lc -c 'show plat int counters port detail'
* vsh_lc -c 'show plat int ns counters mac asic 0 detail'

### tah_cmd_parser.py
Currently supported commands:
* vsh_lc -c 'show plat int counters port detail'
* vsh_lc -c 'show plat int hal counters usdcounters'

## Optional tools

### init.py
```
# python init.py  --help
usage: init.py [-h] [--file FILE] [--list] [--json JSON] [--raw_json]

Generate

optional arguments:
  -h, --help   show this help message and exit
  --file FILE  input file
  --list       list the supported commands
  --json JSON  parse the selected command output and export it to a given file
               in JSON format
  --raw_json   print out the raw command line output in JSON format

```

### cmd_breaker.py
* This python code is to parse the file in a format generated by Andy Gossett's script, collect_switch_internal_counters.sh
* If you have raw dictionary in above format, you don't need to use cmd_breaker.py