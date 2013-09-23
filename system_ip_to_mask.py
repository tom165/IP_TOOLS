#=========================================================
# filename: system_ip_to_mask.py
# author: tom165   
# date: 2013/09/22
# require netaddr module (https://github.com/drkjam/netaddr)
# input: excel file   ip_system_big.xls(output from ip_manage_system)
# output: txt file  ip_system_big_with_mask.txt
# change system big ip arange(two ip with no mask) to ip with mask
# for example:  61.153.32.0  61.153.32.255  change to 61.150.32.0/24
#=========================================================
import netaddr, re, xlrd
import sys, getopt

def my_usage():
    print 'system_ip_to_mask.py Usage'
    print '-h, --help: print help message'
    print '-v, --version: print script version'
    print '-a, --input1: input MS Excle file name of system big ip list'
    print '-b, --input2: input MS Excle file name of system detail ip list'
    print '-c, --ouput1: output txt file name of ip_system_big_with_mask_date'
    print '-d, --ouput2: output txt file name of ip_system_detail_with_mask_user_date'
    print '-e, --ouput3: output txt file name of ip_system_detail_with_mask_nouser_date.txt'
    print 'for example:'
    print 'system_ip_to_mask.py -a ip_big_0922.xls -b ip_detail_0922.xls -c ip_big2mask_0922.txt -d ip_user2_0922.txt -e ip_nouser2_0922.txt'

    
def my_version():
    print 'system_ip_to_mask 1.0'
    print 'code by tom165'

def bigip_mask(input_filename):
    pattern = re.compile(r'\d{1,3}\.\d{1,3}.\d{1,3}.\d{1,3}')
    tmp_big_ip = []
    
    # open Excel file
    ipbig_workbook = xlrd.open_workbook(input_filename)
    ip_big_sheet = ipbig_workbook.sheet_by_index(0)
    nrows = ip_big_sheet.nrows

    #get ip info from excel file
    total = 0
    for rownum in range(1, nrows):
        ip_start = ip_big_sheet.cell_value(rownum, 3)
        ip_end = ip_big_sheet.cell_value(rownum, 7)
    
        cidrs = netaddr.iprange_to_cidrs(ip_start, ip_end)    #change Ip range to format with netmask
        total += cidrs[0].size  
        print cidrs[0]
        tmp_big_ip.append(str(cidrs[0]))

    print 'total ip = ' + str(total)
    return(tmp_big_ip)
    
def save_ip(ip_list, output_filename):
    #write output file    
    if len(ip_list) != 0:
        f = file(output_filename, 'w')   
        total = 0
        i = 0
        while i < len(ip_list):
            f.write(ip_list[i] + '\n')
            total += netaddr.IPNetwork(ip_list[i]).size 
            i += 1
        f.write('total ip = ' + str(total))
        f.close()
        
def detail_ip_mask(input_filename2, output_filename, output_filename2):
    pattern = re.compile(r'\d{1,3}\.\d{1,3}.\d{1,3}.\d{1,3}')
    pattern2 = re.compile('\d{4}-\d{2}-\d{2}')

    f = file(output_filename, 'w')   # open file for ouput ip with mask and user defined
    f2 = file(output_filename2, 'w')   # open file for ouput ip with mask and no user defined

    # open Excel file
    ipdetail_workbook = xlrd.open_workbook(input_filename2)
    ip_detail_sheet = ipdetail_workbook.sheet_by_index(0)
    nrows = ip_detail_sheet.nrows

    total = 0
    total2 = 0

    for rownum in range(1, nrows):
        ip_start = ip_detail_sheet.cell_value(rownum, 3)
        ip_end = ip_detail_sheet.cell_value(rownum, 6)
        #ip_user_name = ip_detail_sheet.cell_value(rownum, 10)
        #ip_user_addr = ip_detail_sheet.cell_value(rownum, 8)
        #ip_user_phone = ip_detail_sheet.cell_value(rownum, 9)
        #ip_user_city = ip_detail_sheet.cell_value(rownum, 11)
        ip_creattime = ip_detail_sheet.cell_value(rownum, 1)
        #ip_nums = ip_detail_sheet.cell_value(rownum, 7)

        if ip_creattime != '':    # if not define date  ,it is used ip
            #print t[0] + '-' + t[1]
            cidrs = netaddr.iprange_to_cidrs(ip_start, ip_end)    #change Ip range to format with netmask
            total += cidrs[0].size
        
            print cidrs[0]
            f.write(str(cidrs[0]) + '\n')
        else:                     # if not define date  ,it is unused ip
            #print t[0] + '-' + t[1]
            cidrs = netaddr.iprange_to_cidrs(ip_start, ip_end)    #change Ip range to format with netmask
            total2 += cidrs[0].size
        
            print cidrs[0]
            f2.write(str(cidrs[0]) + '\n')
  
    print 'ip of defined user  = ' + str(total)
    print 'ip of not defined user = ' + str(total2)
    print 'total ip =' + str(total + total2)

    f.write('total ip = ' + str(total))
    f2.write('total ip = ' + str(total2))
        
    f.close()
    f2.close()


def main(argv):
    input_filename = ''
    input_filename2 = ''
    output_filename = ''
    output_filename2 = ''
    output_filename3 = ''
    
    try:
        opts, args = getopt.getopt(argv[1:], 'hva:b:c:d:e:', ['help', 'version', 'input1=', 'input2=', 'output1=', 'output2=', 'output3='])
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
        elif opt in ('-b', '--input2'):
            input_filename2 = arg
        elif opt in ('-c', '--output1'):
            output_filename = arg
        elif opt in ('-d', '--output2'):
            output_filename2 = arg
        elif opt in ('-e', '--output3'):
            output_filename3 = arg
        else:
            print 'unhandled option'
            sys.exit(3)
    
    if (input_filename == ''):
        print 'input filename is empty, wrong '
        sys.exit(1)
    if (input_filename2 == ''):
        print 'input filename2 is empty, wrong '
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

    print 'Processing system big ip...'
    ip_list = bigip_mask(input_filename)  # change ip to mask
    
    print 'Please waiting, Now writing big ip with mask file... '
    save_ip(ip_list, output_filename)     # save ip info to file
    
    print 'Processing system detail ip...'
    detail_ip_mask(input_filename2, output_filename2, output_filename3)
    
    print 'Finished'
        
                
if __name__ == '__main__':
    main(sys.argv)
    
