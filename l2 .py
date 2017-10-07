import subprocess
import shlex
import re

process_result = subprocess.check_output(['hdparm','-I','/dev/sda'])
model_number_re = re.compile('(?<=Model Number: {7}).*')
serial_number_re = re.compile('(?<=Serial Number: {6}).*')
firmware_revision_re = re.compile('(?<=Firmware Revision: {2}).*')
supported_re = re.compile('(?<=Supported: ).*')
used_re = re.compile('(?<=Used: ).*')
device_size_re = re.compile('(?<=device size with M = 1024\*1024: {6}).*(?= MBytes)')
DMA_re = re.compile('(?<=DMA: ).*')
PIO_re = re.compile('(?<=PIO: ).*')

print('Model: ' + model_number_re.findall(process_result.decode())[0] + '\n')
print('Serial Number: ' + serial_number_re.findall(process_result.decode())[0] + '\n')
print('Firmware Revision: ' + firmware_revision_re.findall(process_result.decode())[0] + '\n')
print('Supported ATA standarts: ' + supported_re.findall(process_result.decode())[0] + '\n')
print('Used: ' + used_re.findall(process_result.decode())[0] + '\n')
print('DMA: ' + DMA_re.findall(process_result.decode())[0] + '\n')
print('PIO: ' + PIO_re.findall(process_result.decode())[0] + '\n')
device_size_string = device_size_re.findall(process_result.decode())[0]
device_size_int = int(device_size_string)
print('Device Size: ' + device_size_string + ' MBytes')

unused_memory_re = subprocess.Popen(shlex.split('df -m'),stdout=subprocess.PIPE)
searched = subprocess.Popen(shlex.split('grep /dev/sda'),
                            stdin=unused_memory_re.stdout,stdout=subprocess.PIPE)
awked =subprocess.Popen(shlex.split('awk \'{print $4}\''),
                        stdin=searched.stdout, stdout=subprocess.PIPE)
out = awked.communicate()
total_unsed = 0
for unused in out[0].decode().split():
    total_unsed += int(unused)
print('Used and unavaliable to access: ' + str(device_size_int - total_unsed) + " MBytes")
print('Unused: ' + str(total_unsed) + " MBytes")