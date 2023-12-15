import os
import utils
import math

def is_process_file(gnss_file):
    with open(gnss_file, 'r',encoding="utf-8-sig") as f_gnss:
        line = f_gnss.readline()
        if line.startswith('$GPGNSS'):
            return True
        else:
            return False
        
def convert_gnss_process(gnss_file):
    gnss_process =  os.path.splitext(gnss_file)[0] + '_process.txt'
    with open(gnss_file, 'r',encoding="utf-8-sig") as f_gnss, open(gnss_process, 'w',encoding="utf-8") as f_process:
        line_num = 0
        line_count = utils.get_file_total_lines(f_gnss)
        for line_gnss in f_gnss:
            line_num += 1
            if line_gnss.startswith('GPS_Week'):
                continue
            items = line_gnss.strip().split(',')
            if len(items) == 19:
                gnss_week = int(items[0])
                gnss_second = float(items[1])
                pos_line = "$GPGNSS,%4d,%11.4f,%14.9f,%14.9f,%10.4f,%10.4f,%10.4f,%10.4f,%3d\n"%(gnss_week,gnss_second,float(items[3]),float(items[4]),float(items[5]),float(items[6]),float(items[7]),float(items[8]),int(items[2]))
                f_process.write(pos_line) 
                north_vel = float(items[13])
                east_vel =  float(items[14])
                trkgnd = math.degrees(math.atan2(east_vel,north_vel))
                horspd = math.sqrt(north_vel * north_vel + east_vel * east_vel)
                vertspd = float(items[15])
                vel_line = "$GPVELS,%4d,%11.4f,%14.9f,%14.9f,%14.9f\n"%(gnss_week,gnss_second,horspd,trkgnd,vertspd)
                f_process.write(vel_line)
            utils.do_process(line_num,line_count)
        print(' gnss has converted!')
    return gnss_process
