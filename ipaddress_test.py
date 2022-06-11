import ipaddress



log_result = ['10.1.1.3', '10.1.1.13', '10.2.1.3', '10.39.1.4', '10.1.1.200', '10.1.10.13', '10.6.1.58', '10.1.1.29','10.2.1.29']
counter = 0
ip_list = []
subnet_list = []


def validate(ip, net):
    var  = ip in net
    return var
def list_intersection(list1, list2):
    for i in list2:
        list1.remove(i)
    return list1


while len(log_result) >= 3:
    iface = ipaddress.ip_interface(log_result[0] +'/24')
    for ip in log_result:
        subnet = iface.network
        ip_addr = ipaddress.ip_address(ip)
        if validate(ip_addr, subnet) == True:
            counter = counter + 1
            ip_list.append(ip)
    if counter >=3:
        subnet_list.append(subnet.with_prefixlen)
    list_intersection(log_result, ip_list)
    print(ip_list)
    counter = 0 
    ip_list.clear()
    print(log_result)
    print(subnet_list)
   


