# modified from url 
# https://scooby.blog/2018/01/11/shodan-search-multiple-ip-addresses-with-python-script/
from sys import argv, exit
import time

try:
    import shodan
    from shodan.cli.helpers import get_api_key
except ImportError:
    print("Please install the shodan libary")
    exit()

if len(argv) != 2:
    print ("Usage: python list_test.py ")
    exit()

api_key = get_api_key()
api = shodan.Shodan(api_key)

input_file = argv[1]
file_name = input_file + "-shodanoutput.csv"

#open csv file
output_csv = open(file_name, "w+")

#write header line 
output_csv.write("IP,Last_shodan_update,ORG,ISP,OS,Product,Country,City, Open_port(s), Port_header\n")

#function to iterate through ip addresses
def banaan(ip_address):
    try:
        host = api.host(ip_address)

        foundIP = "%s,%s,%s,%s,%s,%s,%s,%s," % (
            host.get('ip_str'),
            host.get('last_update' ,'n/a'),
            host.get('org' ,'n/a').replace(","," "),
            host.get('isp' ,'n/a').replace(","," "),
            host.get('os' ,'n/a'),
            host.get('product' ,'n/a'),
            host.get('country_name' ,'n/a'),
            host.get('city' ,'n/a')
        )



        output_csv.write(foundIP)

        #write first port
        output_csv.write(str(host['data'][0]['port']))
        output_csv.write("," + "\"" + str(host['data'][0]['data']).replace("\r\n", ";").replace(",","").replace("\"", "").strip() + "\"" + "\n" )

        #write / if more than one port exists
        for x in host['data'][1:]:
            output_csv.write(foundIP)
            output_csv.write(str(x['port']))
            output_csv.write("," + "\"" + str(x['data']).replace("\r\n", ";").replace(",","").replace("\"", "").strip() + "\"" + "\n")

    #print none if no results pop up    
    except Exception as e:
        output_csv.write("%s, %s,,,,,,,\n" % (ip_address, str(e)))


#open list of ip addresses
f = open(input_file ,'r')

#print to console searching for ip addresses
for x in f:
    ip = x.strip()
    # output_file.write(colored('\n' + '[*] Searching for ' + ip, 'green'))
    print('[*] Searching for ' + ip)
    banaan(ip)
    time.sleep(1)

#close the output file 
output_csv.close()
print('[*][*][*] Ouput stored as ' + file_name)

# to install shodan on windows
#py -m easy_install shodan 
# will get a bunch of errors saying a lot of packages aren't install
# py -m easy_install packageThatIsMissing

#py -m shodan init yourAPIkey
# yourAPIkey can be found on shodan.io after you make an account

#python .\shodanScript.py .\iplist.txt
#will output to shodanOutput.csv 

# other computers write
# py .\shodanScript.py .\iplist.txt
