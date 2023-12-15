

def convert_to_defult(line):
    if line.startswith('Week') or line.startswith('week'):
        return None
     # 分割每一行
    data = line.split()  
    # 如果数据列数大于20
    if len(data) == 9:  
        # 拼装数据
        new_data = data[:2]
        # new_data.extend(data[3:6])
        new_data.append(data[4])
        new_data.append(data[3])
        new_data.append(data[5])
        new_data.extend(['0','0','0'])
        new_data.append(data[8])
        new_data.append(data[7])
        new_data.append(data[6])
        new_data.append('4')
        # 新的数据合并成一行
        new_line = ','.join(new_data) + '\n'
        return new_line
    return None