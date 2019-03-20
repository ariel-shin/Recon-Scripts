# Recon-Scripts

## arinscript 
arinscript takes a company name e.g. Google and outputs Net Range, CIDR, and Customer/Organization name for the child and parent networks. 

### Running arinscript
Currently, ARIN only supports the terminal command line. To run the script, simply type the scriptname and the company name. 

*./arinscript Google*

ARIN utilizes wildcard queries so substitute an asterisk for the alphanueric character that you want to leave off at the beginning of the query term. For example if you want The Google Company, type

*./arinscript \*Google\**

For more details, visit https://www.arin.net/resources/services/whois_guide.html

Note: arinscript has not been extensively tested. Since a lot of commands are based on the exact format of the limited tests I have run, some wonky output may appear. 

## shodanScraper.py
shodanScraper.py takes a list of IP addresses and creates a csv file with the shodan output. 

This script is modified from https://scooby.blog/2018/01/11/shodan-search-multiple-ip-addresses-with-python-script/

### Running shodanScraper.py
To get shodanscript running, you must have a) python installed b) shodan installed


To install shodan on Windows, download python then follow these steps

*py -m easy_install shodan* 


Most likely, you will get a lot of errors saying packages are missing. A few packages that might be missing are: urllib3, chardet, certifi, idna, and click
*py -m easy_install packageThatIsMissing*


Log on to your Shodan account and copy your API key on the top right bar

*py -m shodan init yourAPIkey*


To **finally** run the package

*py .\shodanscript.py .\iplist.txt*

// iplist.txt is the list of ip in a text file



