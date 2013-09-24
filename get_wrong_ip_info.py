#=========================================================
# -*- coding: cp936 -*-
# filename: get_wrong_ip_info.py
# author: tom165   
# date: 2013/09/22
# require xlrd module for read excel
# require re
# require netaddr module (https://github.com/drkjam/netaddr)
# input: ip with mask txt file (ip_system_big_with_mask.txt)
# output: txt file (jh_crs_route_show_nouse.txt,jh_crs_route_show_use.txt )
# get crs detail route and list the route of no user( show route long X.X.X.X/X)  
#=========================================================
import re, xlrd, netaddr, csv
import sys, getopt
reload(sys)
sys.setdefaultencoding('utf-8')

def my_usage():
    print 'get_wrong_ip_info.py Usage'
    print '-h, --help: print help message'
    print '-v, --version: print script version'
    print '-a, --input1: input txt file name of no route user ip list'
    print '-b, --input2: input txt file name of no defined ip list'
    print '-c, --input3: input txt file name of ip user deltail info list'
    print '-d, --input4: input txt file name of ip big info list'
    print '-e, --ouput1: output txt file name of no route user ip detail info'
    print '-f, --ouput2: output txt file name of no defined ip detail info'
    print 'for example:'
    print 'get_wrong_ip_info.py -a jh_noroute_out.txt -b jh_sys_out.txt -c ip_detail_0922.xls -d ip_big_0922.xls -e jh_noroute_out.csv -f jh_sys_out.csv'

    
def my_version():
    print 'get_wrong_ip_info 1.0'
    print 'code by tom165'


def get_no_route_ip_info(input_filename, input_filename3, output_filename):

    pattern = re.compile(r'\d{1,3}\.\d{1,3}.\d{1,3}.\d{1,3}')

    # open Excel file
    ipdetail_workbook = xlrd.open_workbook(input_filename3)
    ip_detail_sheet = ipdetail_workbook.sheet_by_index(0)
    nrows = ip_detail_sheet.nrows

    ip_list=[]

    for rownum in range(1, nrows):
        ip_start = ip_detail_sheet.cell_value(rownum, 3)
        ip_end = ip_detail_sheet.cell_value(rownum, 6)
        ip_user_name = ip_detail_sheet.cell_value(rownum, 10)
        ip_user_addr = ip_detail_sheet.cell_value(rownum, 8)
        ip_user_phone = ip_detail_sheet.cell_value(rownum, 9)
        ip_user_city = ip_detail_sheet.cell_value(rownum, 11)
        ip_creattime = ip_detail_sheet.cell_value(rownum, 1)
        #ip_nums = ip_detail_sheet.cell_value(rownum, 7)
        
        ip_list.append(rownum)
        ip_list.append(ip_start)
        ip_list.append(ip_end)
        ip_list.append(ip_user_name)
        ip_list.append(ip_user_addr)
        ip_list.append(ip_user_phone)
        ip_list.append(ip_user_city)
        ip_list.append(ip_creattime) 
        #ip_list.append(ip_nums)
        
        
        #ip_list[ip_start] = (rownum, ip_start,ip_end, ip_user_name, ip_user_addr, ip_user_phone, ip_user_city, ip_creattime, ip_nums)
        
        print rownum, ip_start, ip_end, ip_user_name
        
        
    #f = file('jh_noroute_out.txt', 'w')   # open file for ouput 

    f = csv.writer(open(output_filename, "wb"), dialect='excel')  #, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)   # open file for ouput 
    f.writerow(['start_ip', 'end_ip', 'ip_sum', 'cust_name', 'cust_addr', 'cust_phone', 'cust_city', 'create_date'])

    for line in open(input_filename):      # open file for input 
        t = re.findall(pattern, line)
        if len(t) == 0:  break           # if end of total ip=SUM ,break

        #print(line)
        ip_user_name = " "
        ip_user_addr = " "
        ip_user_phone = " "
        ip_user_city = " "
        ip_creattime = " " 

        ip_splt = line.split('-')
        ip_start = ip_splt[0].strip()
        ip_end = ip_splt[1].strip()
        ip_nums = len(netaddr.IPRange(ip_start, ip_end))

        i = 0   
        while  i < round(len(ip_list) / 8):
            r1 = netaddr.IPRange(ip_list[i*8 + 1], ip_list[i*8 + 2]) 
            if (netaddr.IPAddress(ip_start) in r1) and (netaddr.IPAddress(ip_end) in r1): 
                ip_user_name = ip_list[i*8 + 3]
                ip_user_addr = ip_list[i*8 + 4]
                ip_user_phone = ip_list[i*8 + 5]
                ip_user_city = ip_list[i*8 + 6]
                ip_creattime = ip_list[i*8 + 7]
                break
            i += 1
            
        print ip_start, ip_end, ip_nums, ip_user_name, ip_user_addr, ip_user_phone, ip_user_city, ip_creattime
        #newline = line + ip_nums + ip_user_name + ip_user_addr + ip_user_phone + ip_user_city + ip_creattime
        #print newline
        
        #f.write(newline + '\n')
        f.writerow([ip_start, ip_end, ip_nums, ip_user_name, ip_user_addr, ip_user_phone, ip_user_city, ip_creattime])

    #f.close()

    
def get_no_user_ip_info(input_filename2, input_filename4, output_filename2):

    pattern = re.compile(r'\d{1,3}\.\d{1,3}.\d{1,3}.\d{1,3}')

    # open Excel file
    ipdetail_workbook = xlrd.open_workbook(input_filename4)
    ip_detail_sheet = ipdetail_workbook.sheet_by_index(0)
    nrows = ip_detail_sheet.nrows

    ip_list = []

    for rownum in range(1, nrows):
        ip_start = ip_detail_sheet.cell_value(rownum, 3)
        ip_end = ip_detail_sheet.cell_value(rownum, 7)
        ip_nums = ip_detail_sheet.cell_value(rownum, 9)
        ip_user_city = ip_detail_sheet.cell_value(rownum, 0)
        ip_creattime = ip_detail_sheet.cell_value(rownum, 1)

        ip_list.append(rownum)
        ip_list.append(ip_start)
        ip_list.append(ip_end)
        ip_list.append(ip_user_city)
        ip_list.append(ip_creattime) 
        ip_list.append(ip_nums)
        
        print rownum, ip_start, ip_end, ip_user_city
        
    #print ip_list
        
    #f = file('jh_sys_out.txt', 'w')   # open file for ouput 

    f = csv.writer(open(output_filename2, "wb"), dialect='excel')  #, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)   # open file for ouput 
    f.writerow(['start_ip', 'end_ip', 'ip_sum', 'cust_city', 'create_date'])

    for line in open(input_filename2):      # open file for input 
        t = re.findall(pattern, line)
        if len(t) == 0:  break           # if end of total ip=SUM ,break

        #print(line)
        ip_user_city = " "
        ip_creattime = " " 

        ip_splt = line.split('-')
        ip_start = ip_splt[0].strip()
        ip_end = ip_splt[1].strip()
        ip_sum = len(netaddr.IPRange(ip_start, ip_end))
        
        i = 0   
        while  i < round(len(ip_list) / 6):
            r1 = netaddr.IPRange(ip_list[i*6 + 1], ip_list[i*6 + 2]) 
            if (netaddr.IPAddress(ip_start) in r1) and (netaddr.IPAddress(ip_end) in r1): 
                ip_user_city = ip_list[i*6 + 3]
                ip_creattime = ip_list[i*6 + 4] 
                break
            i += 1
            
        print i, ip_start, ip_end, ip_sum, ip_user_city, ip_creattime
        #newline = line + ip_nums + ip_user_name + ip_user_addr + ip_user_phone + ip_user_city + ip_creattime
        #print newline
        
        #f.write(newline + '\n')
        f.writerow([ip_start, ip_end, ip_sum, ip_user_city, ip_creattime])

    #f.close()


def main(argv):
    input_filename = ''
    output_filename = ''
    output_filename2 = ''
    output_filename3 = ''
    
    try:
        opts, args = getopt.getopt(argv[1:], 'hva:b:c:d:e:f:', ['help', 'version', 'input1=', 'input2=', 'input3=', 'input4=', 'output1=', 'output2='])
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
        elif opt in ('-c', '--input3'):
            input_filename3 = arg
        elif opt in ('-d', '--input3'):
            input_filename4 = arg
        elif opt in ('-e', '--output1'):
            output_filename = arg
        elif opt in ('-f', '--output2'):
            output_filename2 = arg
        else:
            print 'unhandled option'
            sys.exit(3)
    
    if (input_filename == ''):
        print 'input filename is empty, wrong '
        sys.exit(1)
    if (input_filename2 == ''):
        print 'input filename2 is empty, wrong '
        sys.exit(1)
    if (input_filename3 == ''):
        print 'input filename3 is empty, wrong '
        sys.exit(1)
    if (input_filename4 == ''):
        print 'input filename3 is empty, wrong '
        sys.exit(1)

    if (output_filename == ''):
        print 'output filename is empty, wrong '
        sys.exit(1)
    if (output_filename2 == ''):
        print 'output filename2 is empty, wrong '
        sys.exit(1)

    print 'Processing wrong ip1 of no route...'
    get_no_route_ip_info(input_filename, input_filename3, output_filename)

    print 'Processing wrong ip2 of no user...'
    get_no_user_ip_info(input_filename2, input_filename4, output_filename2)
    
    print 'Finished'
        
                
if __name__ == '__main__':
    main(sys.argv)

    
