import os
import argparse
import convert_imu_process
import convert_gnss_process
import convert_odo_process
import split_process_file
import utils

gnss_week = 0
gnss_second = 0
gnss_line = None

odo_week = 0
odo_second = 0
odo_line = None

def insert_odo(f_odo,f_new,week,second):
    global odo_week,odo_second,odo_line
    if odo_line is not None:
        if odo_week == week and odo_second < second:
            f_new.write(odo_line)
            odo_line = None
        else:
            return
    for line_odo in f_odo:
        odo_line = line_odo
        items_odo = line_odo.split(',')
        if len(items_odo) > 3:
            odo_week = int(items_odo[1])
            odo_second = float(items_odo[2])
            if odo_week == week and odo_second < second:
                f_new.write(odo_line)
            else:
                break

def insert_gnss(f_gnss,f_new,week,second):
    global gnss_week,gnss_second,gnss_line
    if gnss_line is not None:
        if gnss_week == week and gnss_second < second:
            f_new.write(gnss_line)
            gnss_line = None
        else:
            return
    for line_gnss in f_gnss:
        gnss_line = line_gnss
        items_gnss = line_gnss.strip().split(',')
        if len(items_gnss) > 3:
            gnss_week = int(items_gnss[1])
            gnss_second = float(items_gnss[2])
            if gnss_week == week and gnss_second < second:
                f_new.write(gnss_line)
            else:
                break

def merge_process(gnss_process,imu_process,odo_process,Output_name):
    if Output_name is None:
        return
    if imu_process is None:
        return    
    f_odo = None
    if odo_process is not None:
        f_odo = open(odo_process,'r',encoding="utf-8")
    with open(imu_process, 'r',encoding="utf-8") as f_imiu, open(gnss_process,'r',encoding="utf-8") as f_gnss, open(Output_name,'w',encoding="utf-8") as f_new:
        line_num = 0
        line_count = utils.get_file_total_lines(f_imiu)
        for line_imu in f_imiu:
            line_num += 1
            items_imu = line_imu.strip().split(',')
            if len(items_imu) > 3:
                imu_week = int(items_imu[1])
                imu_second = float(items_imu[2])                
                if f_odo is not None:
                    insert_odo(f_odo,f_new,imu_week,imu_second)
                insert_gnss(f_gnss,f_new,imu_week,imu_second)
                f_new.write(line_imu)
            utils.do_process(line_num,line_count)
        print(' process has merged!')
    if f_odo is not None:
        f_odo.close()

def main(process_name,imu_name,gnss_name,odo_name,Output_name):
    files = {'gnss':None,'imu':None,'odo':None}
    if process_name is not None:
        Output_name =  os.path.splitext(process_name)[0] + '_merged.txt'
        files = split_process_file.split_process(process_name)
        # print(files)
    imu_process = None
    if imu_name is not None:
        if convert_imu_process.is_process_file(imu_name) == False:
            imu_process =convert_imu_process.convert_imu_process(imu_name)
        else:
            imu_process = imu_name
    gnss_process = None
    if gnss_name is not None:
        if convert_gnss_process.is_process_file(gnss_name) == False:
            gnss_process = convert_gnss_process.convert_gnss_process(gnss_name)
        else:
            gnss_process = gnss_name
    odo_process = None
    if odo_name is not None:
        if convert_odo_process.is_process_file(odo_name) == False:
            odo_process = convert_odo_process.convert_odo_process(odo_name)
        else:
            odo_process = odo_name
    if imu_process is not None:
        files['imu'] = imu_process
    if gnss_process is not None:
        files['gnss'] = gnss_process
    if odo_process is not None:
        files['odo'] = odo_process
    merge_process(files['gnss'],files['imu'],files['odo'],Output_name)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p","--process", help="process file name")
    parser.add_argument("-i","--imu", help="imu file name")
    parser.add_argument("-g","--gnss", help="gnss file name")
    parser.add_argument("-o","--odo", help="odo file name")
    parser.add_argument("-O","--Output", help="Output file name")
    args = parser.parse_args()
    process_name = args.process
    imu_name = args.imu
    gnss_name = args.gnss
    odo_name = args.odo
    Output_name = args.Output
    main(process_name,imu_name,gnss_name,odo_name,Output_name)

