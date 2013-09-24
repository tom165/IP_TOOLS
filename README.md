IP地址考核取数工具：
使用方法：

1、IP管理系统里的“首页-地址管理-专线地址管理-专线地址规划”导出所有的大段IP地址的表格，命名为ip_big_date.xls

2、IP管理系统里的“首页-地址管理-专线地址管理-专线地址明细”导出所有的明细IP地址的表格，命名为ip_detail_date.xls((用户信息包含：客户地址，联系电话1，客户名称（中），所属县市4个字段))

3、把ip_big_date.xls 转换为掩码格式的IP段文本文件，把ip_detail_date.xls 转换为掩码格式的IP段文本文件(分已定义用户和未定义用户2个文件)
如：python system_ip_to_mask.py -a ip_big_0922.xls -b ip_detail_0922.xls -c ip_big2mask_0922.txt -d ip_user2_0922.txt -e ip_nouser2_0922.txt

4、自动登陆CRS设备，读取iip_big2mask_0922.txt，生成IP段的未用明细路由文件，三个生成文件为：
jh_crs_log_0922  log记录
jh_crs_route_user_0922 已用的IP
jh_crs_route_nouser_0922   未用的IP

如：python get_crs_route.py -a ip_big2mask_0922.txt -b jh_crs_log_0922.txt -c jh_crs_route_user_0922.txt -d jh_crs_route_nouser_0922.txt

5、用现成工具比较出差异的Ip清单
如：ip_compare.exe -i1 jh_noroute_detail.txt -i2 jh_sys_detail.txt -o1 jh_noroute_out.txt -o2 jh_sys_out.txt

ip_compare.exe -i1 jh_crs_route_nouser_0922.txt -i2 ip_nouser2_0922.txt -o1 jh_noroute_out.txt -o2 jh_sys_out.txt
其中：
jh_noroute_detail.txt  ---CRS上未用的Ip段（即jh_crs_route_nouser_0922.txt）
jh_sys_detail.txt  ---IP管理系统上没有用户的Ip段(即ip_nouser2_0922.txt)

6、给有问题的IP匹配上用户信息或使用县市：
如：get_wrong_ip_info.py -a jh_noroute_out.txt -b jh_sys_out.txt -c ip_detail_0922.xls -d ip_big_0922.xls -e jh_noroute_out.csv -f jh_sys_out.csv




