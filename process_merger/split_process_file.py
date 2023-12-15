import os
import utils

def split_process(process_name):
    ret_dict = {'gnss':None,'imu':None,'odo':None}
    imu_process =  os.path.splitext(process_name)[0] + '_imu_process.txt'
    odo_process =  os.path.splitext(process_name)[0] + '_odo_process.txt'
    gnss_process =  os.path.splitext(process_name)[0] + '_gnss_process.txt'
    f_imu = None
    f_odo = None
    f_gnss = None
    with open(process_name, 'r',encoding="utf-8") as f_process:
        line_num = 0
        line_count = utils.get_file_total_lines(f_process)
        for line in f_process:
            line_num += 1
            if line.startswith('$IMUS'):
                if f_imu is None:
                    f_imu = open(imu_process,'w',encoding="utf-8")
                f_imu.write(line)
            elif line.startswith('$ODOS'):
                if f_odo is None:
                    f_odo = open(odo_process,'w',encoding="utf-8")
                f_odo.write(line)
            elif line.startswith('$GPGNSS') or line.startswith('$GPVELS'):
                if f_gnss is None:
                    f_gnss = open(gnss_process,'w',encoding="utf-8")
                f_gnss.write(line)
            utils.do_process(line_num,line_count)
        print(' porcess has splited!')
        if f_imu is not None:
            f_imu.close()
        if f_odo is not None:
            f_odo.close()
        if f_gnss is not None:
            f_gnss.close()
    # 判断文件是否存在
    if os.path.exists(imu_process):
        ret_dict['imu'] = imu_process
    if os.path.exists(odo_process):
        ret_dict['odo'] = odo_process
    if os.path.exists(gnss_process):
        ret_dict['gnss'] = gnss_process
    return ret_dict