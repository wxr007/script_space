

def convert_to_defult(line):
    # 分割每一行
    data = line.split()  
    # 如果数据列数大于20
    if len(data) > 20:  
        # 只取前11列
        new_data = data[:11]  
        # 加上第20列
        new_data.append(data[20])
        # 新的数据合并成一行
        new_line = ','.join(new_data) + '\n'
        return new_line
    return None