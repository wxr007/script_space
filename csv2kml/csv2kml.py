# 输入各种csv格式将其转换成kml格式
import ctypes  
import os
import sys
import utils
import convert_gici_truth
import convert_cpt7
import convert_ignav_rslt

# 输入文件的格式
File_Format = "ignav_rslt" # [cpt7 , gici_truth , ignav_rslt]
# 加载DLL文件  
csv2kmldll = ctypes.cdll.LoadLibrary(".\\csv2kmldll.dll")  

init=csv2kmldll.init #加载函数对象
init.argtypes = [ctypes.c_char_p, ctypes.c_int]  
finish=csv2kmldll.finish #加载函数对象

input_csv_line = csv2kmldll.input_csv_line #加载函数对象
input_csv_line.argtypes = [ctypes.c_char_p]  

# 获取输出路径的基本格式
def get_filename_without_extension(filepath):  
    return os.path.splitext(filepath)[0]  

# 根据输入格式把每行数据转换成默认格式
def Convert_to_defult_format(line):
    # Week,Sec,Lat,Lon,Height,VN,VE,VD,Roll,Pitch,Heading,Type
    if File_Format == 'cpt7':
        return convert_cpt7.convert_to_defult(line)
    elif File_Format == 'gici_truth':
        return convert_gici_truth.convert_to_defult(line)
    elif File_Format == 'ignav_rslt':
        return convert_ignav_rslt.convert_to_defult(line)

# 读取csv每一行然后转换
def read_csv(filename):
    basnamepath = get_filename_without_extension(filename)
    init(ctypes.c_char_p(basnamepath.encode('utf-8')), 1)
    with open(filename, 'r') as source_file:
        line_num = 0
        line_count = utils.get_file_total_lines(source_file)
        # 读取源文件的每一行 
        for line in source_file:  
            line_num += 1
            new_line = Convert_to_defult_format(line)
            if new_line is not None:
                input_csv_line(ctypes.c_char_p(new_line.encode('utf-8')))
            utils.do_process(line_num,line_count)
    print("\n")
    finish()

if __name__ == "__main__":  
    argv = sys.argv
    if len(argv) != 2:
        print("Usage: python csv2kml.py filename")
    else:
        filename = argv[1]
    read_csv(filename)