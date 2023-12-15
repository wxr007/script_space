import os
import utils

def is_process_file(imu_file):
    with open(imu_file, 'r',encoding="utf-8-sig") as f_imu:
        line = f_imu.readline()
        if line.startswith('$IMUS'):
            return True
        else:
            return False
        
def convert_imu_process(imu_file):
    imu_process =  os.path.splitext(imu_file)[0] + '_process.txt'
    with open(imu_file, 'r',encoding="utf-8-sig") as f_imiu, open(imu_process, 'w',encoding="utf-8") as f_process:
        line_num = 0
        line_count = utils.get_file_total_lines(f_imiu)
        for line_imu in f_imiu.readlines():
            line_num += 1
            items = line_imu.strip().split(',')
            if len(items) > 2:
                imu_week = int(items[0])
                imu_second = float(items[1])
                new_line = "$IMUS,%4d,%11.4f,%14.10f,%14.10f,%14.10f,%14.10f,%14.10f,%14.10f\n"%(imu_week,imu_second,float(items[2]),float(items[3]),float(items[4]),float(items[5]),float(items[6]),float(items[7]))
                f_process.write(new_line)  
            utils.do_process(line_num,line_count)
        print(' imu has converted!')
    return imu_process
