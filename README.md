IP��ַ����ȡ�����ߣ�
ʹ�÷�����

1��IP����ϵͳ��ġ���ҳ-��ַ����-ר�ߵ�ַ����-ר�ߵ�ַ�滮���������еĴ��IP��ַ�ı������Ϊip_big_date.xls

2��IP����ϵͳ��ġ���ҳ-��ַ����-ר�ߵ�ַ����-ר�ߵ�ַ��ϸ���������е���ϸIP��ַ�ı������Ϊip_detail_date.xls((�û���Ϣ�������ͻ���ַ����ϵ�绰1���ͻ����ƣ��У�����������4���ֶ�))

3����ip_big_date.xls ת��Ϊ�����ʽ��IP���ı��ļ�����ip_detail_date.xls ת��Ϊ�����ʽ��IP���ı��ļ�(���Ѷ����û���δ�����û�2���ļ�)
�磺python system_ip_to_mask.py -a ip_big_0922.xls -b ip_detail_0922.xls -c ip_big2mask_0922.txt -d ip_user2_0922.txt -e ip_nouser2_0922.txt

4���Զ���½CRS�豸����ȡiip_big2mask_0922.txt������IP�ε�δ����ϸ·���ļ������������ļ�Ϊ��
jh_crs_log_0922  log��¼
jh_crs_route_user_0922 ���õ�IP
jh_crs_route_nouser_0922   δ�õ�IP

�磺python get_crs_route.py -a ip_big2mask_0922.txt -b jh_crs_log_0922.txt -c jh_crs_route_user_0922.txt -d jh_crs_route_nouser_0922.txt

5�����ֳɹ��߱Ƚϳ������Ip�嵥
�磺ip_compare.exe -i1 jh_noroute_detail.txt -i2 jh_sys_detail.txt -o1 jh_noroute_out.txt -o2 jh_sys_out.txt

ip_compare.exe -i1 jh_crs_route_nouser_0922.txt -i2 ip_nouser2_0922.txt -o1 jh_noroute_out.txt -o2 jh_sys_out.txt
���У�
jh_noroute_detail.txt  ---CRS��δ�õ�Ip�Σ���jh_crs_route_nouser_0922.txt��
jh_sys_detail.txt  ---IP����ϵͳ��û���û���Ip��(��ip_nouser2_0922.txt)

6�����������IPƥ�����û���Ϣ��ʹ�����У�
�磺get_wrong_ip_info.py -a jh_noroute_out.txt -b jh_sys_out.txt -c ip_detail_0922.xls -d ip_big_0922.xls -e jh_noroute_out.csv -f jh_sys_out.csv




