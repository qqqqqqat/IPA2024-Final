from netmiko import ConnectHandler
from pprint import pprint

device_ip = "10.0.15.184"
username = "admin"
password = "cisco"

device_params = {
    "device_type": "cisco_ios",
    "ip": device_ip,
    "username": username,
    "password": password,
}


def gigabit_status():
    ans = ""
    with ConnectHandler(**device_params) as ssh:
        up = 0
        down = 0
        admin_down = 0
        result = ssh.send_command("show ip interface brief", use_textfsm=True)
        # ตรวจสอบผลลัพธ์
        if not result:
            print("No results returned from the command.")
            return
        
        # เก็บข้อมูลสถานะของ interfaces
        interface_status = {}
        for interface in result:
            int_name = interface['interface']  # เปลี่ยนจาก 'intf' เป็น 'interface'
            int_status = interface['status']
            interface_status[int_name] = int_status
            
            # นับสถานะต่าง ๆ
            if int_status == "up":
                up += 1
            elif int_status == "down":
                down += 1
            elif int_status == "administratively down":
                admin_down += 1

        # สร้างข้อความผลลัพธ์
        ans = ', '.join([f"{intf} {status}" for intf, status in interface_status.items()])
        ans += f" -> {up} up, {down} down, {admin_down} administratively down"
        
        # แสดงผลลัพธ์
        pprint(ans)
        return ans
