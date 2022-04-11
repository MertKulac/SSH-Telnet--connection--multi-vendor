import sys
import time
import paramiko  ###SSH LIBRARY###
from paramiko_expect import \
    SSHClientInteraction  ###TAKES AN ACTION ACCORDING TO INPUT CODE AND PROVIDES STOP THE CODE (expect)###
import telnetlib
from queue import Queue
import threading
from termcolor import colored
