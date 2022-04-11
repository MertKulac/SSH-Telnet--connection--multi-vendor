import sys
import time
import paramiko  ###SSH LIBRARY###
from paramiko_expect import \
    SSHClientInteraction  ###TAKES AN ACTION ACCORDING TO INPUT CODE AND PROVIDES STOP THE CODE (expect)###
import telnetlib
from queue import Queue
import threading
from termcolor import colored

line_break = "\r\n"
line_end = "\r"
vrp_cli_length = "screen-length 0 tempo"


#### Both HUAWEI&CISCO CPE's via Telnet&SSH via LDAP ######
##new features : Aware that CPE is Cisco or Huawei besides via Telnet or SSH and sends to appropriate commands.###

def connectionkapici(ip):
    kapici_prompt = '.*\$ '
    bash_prompt = "[tc137553@tcellsconn3 ~]$ "
    telnet_prompt = ".*:"
    configure_prompt = '.*)#'
    user_prompt = '.*sername:'
    pass_prompt = '.*assword: '
    huawei_sys_prompt = '.*]'
    cpe_prompt = ".*>"
    enable_prompt = ".*#"
    ssh_prompt = ".*? "
    Username = "admin"
    Password = "admin*"
    kapici = "admin"
    SSH = paramiko.SSHClient()
    SSH.load_system_host_keys()
    SSH.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    telnet = telnetlib.Telnet()
    # remote_connection = SSH.invoke_shell()

    ldap_user = 'admin'
    ldap_pass = 'admin'
    file1 = open("Connection_Output_10.txt", "a")

    try:
        SSH.connect(hostname=kapici, username=Username, password=Password, port=22)
        with SSHClientInteraction(SSH, timeout=10, display=False, buffer_size=65535) as command:
            command.expect(kapici_prompt, timeout=1)
            command.send('bash')
            command.expect(kapici_prompt)
            command.send('telnet ' + ip)  ###at first trying telnet
            print(ip)
            command.expect([user_prompt, kapici_prompt])
            if command.last_match == kapici_prompt:  # continue with ssh
                command.send('ssh {}@{}'.format(ldap_user, ip))
                print(ip + ' via SSH')
                command.expect(ssh_prompt)
                command.send("yes")
                command.expect(pass_prompt)

                if pass_prompt == command.last_match:
                    print("###########Router is reachable.###########")
                    # file1.write(ip + "successful access\n")
                    command.send(ldap_pass)
                    command.expect([cpe_prompt, enable_prompt])
                    # command.expect(cpe_prompt) or command.expect(enable_prompt)
                    if command.last_match == cpe_prompt:
                        print(colored("###########Connection to Huawei Router was established.###########", "red"))
                        file1.write(ip + " Huawei" + " SSH" + " successful access\n")  ####test if connection to router exactly##
                        time.sleep(0.5)

                    elif command.last_match == enable_prompt:
                        print("###########Connection to Cisco Router was established.###########")
                        file1.write(ip + " Cisco" + " SSH" + " successful access\n")  ####test if connection to router exactly##
                        time.sleep(0.5)

                    else:
                        print("###########CPE is uncreachable via LDAP,please check your user,pass info.(might be tellcom.)")
                        file1.write(ip + " CPE is unreachable via LDAP\n")

                else:
                    print("###########CPE is uncreachable.###########")  ###cannot access via telnet or ssh
                    file1.write(ip + " CPE is unreachable\n")

            elif command.last_match == user_prompt:  # continue with telnet
                print(ip + ' via Telnet')
                command.send(ldap_user)
                command.expect(pass_prompt)
                command.send(ldap_pass)
                command.expect([cpe_prompt, enable_prompt])

                if cpe_prompt == command.last_match:
                    print(colored("###########Connection to Huawei Router was established.###########", "red"))
                    file1.write(ip + " Huawei" + " Telnet" + " successful access\n")  ####test if connection to router exactly##
                    time.sleep(0.5)

                elif enable_prompt == command.last_match:
                    print("###########Connection to Cisco Router was established.###########")
                    file1.write(ip + " Cisco" + " Telnet" + " successful access\n")  ####test if connection to router exactly##
                    time.sleep(0.5)

                else:
                    print("###########CPE is uncreachable.###########")  ###cannot access via telnet or ssh
                    file1.write(ip + " CPE is unreachable\n")

            else:
                print("###########CPE is unreachable at first.###########")
                file1.write(ip + " CPE is unreachable at first\n")

    except Exception as Error:
        print(Error)
    return 0


sys.exit()

##barka##
