import sys

last_persent = 0
all_persent = 100

# 计算文件大小
def get_file_total_lines(source_file):
    line_count = 0
    for _ in source_file: 
        line_count += 1; 
        pass  
    # 将文件指针移动到开始
    source_file.seek(0) 
    return line_count
    
def do_process(line_num,line_count):
    global last_persent, all_persent
    done = line_num / line_count * all_persent  # 计算完成百分比
    if int(done) != last_persent:
        sys.stdout.write('\r[{}{}] {:6.2f}%'.format('#'*int(done),' '*int((all_persent-int(done))), done))
        sys.stdout.flush()  # 刷新输出缓冲区
        last_persent = int(done)