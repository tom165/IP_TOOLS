#=========================================================
# filename: get_crs_route.py
# author: tom165   
# date: 2013/09/22
# require telnetlib and getpass and re module 
# require netaddr module (https://github.com/drkjam/netaddr)
# input: ip with mask txt file (ip_system_big_with_mask.txt)
# output: txt file (jh_crs_route_show_nouse.txt,jh_crs_route_show_use.txt )
# get crs detail route and list the route of no user( show route long X.X.X.X/X)   
#=========================================================
import sys, getopt
import re, telnetlib, getpass, netaddr

def my_usage():
    print 'get_crs_route.py Usage'
    print '-h, --help: print help message'
    print '-v, --version: print script version'
    print '-a, --input1: input txt file name of system big ip list'
    print '-b, --ouput1: output txt file name of crs route show log'
    print '-b, --ouput2: output txt file name of crs route of defines user'
    print '-d, --ouput3: output txt file name of crs route of undefines user'
    print 'for example:'
    print 'get_crs_route.py -a ip_big2mask_0922.txt -b jh_crs_log_0922.txt -c jh_crs_route_user_0922.txt -d jh_crs_route_nouser_0922.txt'

    
def my_version():
    print 'get_crs_route 1.0'
    print 'code by tom165'


def get_route(input_filename, output_filename, output_filename2, output_filename3):
    total = 0
    lines = ''

    f = file(output_filename, 'w')   # open file for input crs log file of run 'show route long XXXX/X' 
    f1 = file(output_filename2, 'w')   # open file for input use route
    f2 = file(output_filename3, 'w')   # open file for input not used route

    HOST_IP = 'X.X.X.X'  # host ip of jumper machine
    ROUTER_IP = 'X.X.X.X'  # ip of cisco crs router

    pattern = re.compile(r'\d{1,3}\.\d{1,3}.\d{1,3}.\d{1,3}/\d*')
    user = raw_input("Enter your remote account: ")
    password = getpass.getpass()

    tn = telnetlib.Telnet(HOST_IP)
    tn.open(HOST_IP)

    tn.read_until("username:")
    tn.write(user + "\n")
    if password:
        tn.read_until("password:")
        tn.write(password + "\n")

    tn.read_until("#")
    tn.write(ROUTER_IP + "\n")
    lines += tn.read_until("#")

    f.write(lines)
    print lines

    for line in open(input_filename):      # open file for input big ip with mask

        all_ipset = netaddr.IPSet([])
        used_ipset = netaddr.IPSet([])
        noused_ipset = netaddr.IPSet([])
        
        t = re.findall(pattern, line)
        if len(t) == 0:  break           # if end of total ip=SUM ,break
        
        all_ipset.add(netaddr.IPNetwork(line))
        
        lines = ''
        lines2 = ''
        
        strLineCommand = "show route long" + " " + line
        tn.write(strLineCommand)
        lines += tn.read_until("#")
        print lines
        f.write(lines)

        if lines.find('No matching routes found') >= 0:   #No matching routes found  
            t_splt = line.split('/')                      # delete netmask 
            tn.write('show route ' + t_splt[0] + '\n')    # show route X.X.X.X  , not include netmask
            lines2 = tn.read_until("#")
            f.write(lines2)
            if lines2.find('via Null0') >= 0:             # if exist "via Null0" , ip is not used ,otherwise ,ip is used 
                f2.write(line + '\n')                     
            else:
                f1.write(line + '\n')                     
                
        else:                                             #exist detail route 
            t = re.findall(pattern, lines)
            #print t
            if len(t) != 0:
                del t[0]            #the first element is big ip mask,need delete 
                for x in t:
                    #print x
                    f1.write(x + '\n')
                    used_ipset.add(netaddr.IPNetwork(x))
                    #print used_ipset
                
            noused_ipset = all_ipset - used_ipset    # get the no used ipset
        
            print all_ipset
            print used_ipset
            print noused_ipset

            for cidr in noused_ipset.iter_cidrs():
                print cidr
                f2.write(str(cidr) + '\n')
        
        
    f.close()
    f1.close()
    f2.close()


    

def main(argv):
    input_filename = ''
    output_filename = ''
    output_filename2 = ''
    output_filename3 = ''
    
    try:
        opts, args = getopt.getopt(argv[1:], 'hva:b:c:d:', ['help', 'version', 'input1=', 'output1=', 'output2=', 'output3='])
    except getopt.GetoptError, err:
        print str(err)
        my_usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            my_usage()
            sys.exit(1)
        elif opt in ('-v', '--version'):
            my_version()
            sys.exit(0)
        elif opt in ('-a', '--input1'):
            input_filename = arg
        elif opt in ('-b', '--output1'):
            output_filename = arg
        elif opt in ('-c', '--output2'):
            output_filename2 = arg
        elif opt in ('-d', '--output3'):
            output_filename3 = arg
        else:
            print 'unhandled option'
            sys.exit(3)
    
    if (input_filename == ''):
        print 'input filename is empty, wrong '
        sys.exit(1)

    if (output_filename == ''):
        print 'output filename is empty, wrong '
        sys.exit(1)
    if (output_filename2 == ''):
        print 'output filename2 is empty, wrong '
        sys.exit(1)
    if (output_filename3 == ''):
        print 'output filename3 is empty, wrong '
        sys.exit(1)

    print 'Processing crs route...'
    get_route(input_filename, output_filename, output_filename2, output_filename3)
    
    print 'Finished'
        
                
if __name__ == '__main__':
    main(sys.argv)
    

    
    

