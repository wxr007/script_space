import os
import utils

def is_process_file(odo_file):
    with open(odo_file, 'r',encoding="utf-8-sig") as f_odo:
        line = f_odo.readline()
        if line.startswith('$ODOS'):
            return True
        else:
            return False

def convert_odo_process(odo_file):
    odo_process =  os.path.splitext(odo_file)[0] + '_process.txt'
    with open(odo_file, 'r',encoding="utf-8-sig") as f_odo, open(odo_process, 'w',encoding="utf-8") as f_process:
        line_num = 0
        line_count = utils.get_file_total_lines(f_odo)
        for line_odo in f_odo:
            line_num += 1
            if line_odo.startswith('GPS_Week'):
                continue
            items = line_odo.strip().split(',')
            if len(items) > 2:
                odo_week = int(items[0])
                odo_second = float(items[1])
                new_line = "$ODOS,%4d,%11.4f,%14.10f,%2d\n"%(odo_week,odo_second,float(items[3]),int(items[4]))
                f_process.write(new_line)
            utils.do_process(line_num,line_count)
        print(' odo has converted!')
    return odo_process
