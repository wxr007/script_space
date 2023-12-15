import numpy as np

def degree2rad(degree):
    return degree * np.pi / 180

def rad2degree(rad):
    return rad * 180 / np.pi

def BLH2xyz(L, B, H, rad=False):
    if not rad:
        L = degree2rad(L)
        B = degree2rad(B)
    a = 6378137.0000
    b = 6356752.3141
    e2 = 1 - (b / a)**2
    N = a/np.sqrt(1-e2*np.sin(B)**2)
    x = (N + H) * np.cos(B) * np.cos(L)
    y = (N + H) * np.cos(B) * np.sin(L)
    z = (N * (1 - e2) + H) * np.sin(B)
    return x, y, z


def xyz2BLH(x, y, z, rad=False):
    a = 6378137.0000
    b = 6356752.3141
    e2 = 1 - (b / a)**2
    p = np.sqrt(x**2+y**2)
    theta = np.arctan(z * a/(p * b))
    L = np.arctan2(y, x)
    B = np.arctan((z + e2/(1-e2)*b*np.sin(theta)**3) /
                  (p - e2*a*np.cos(theta)**3))
    N = a/np.sqrt(1-e2*np.sin(B)**2)
    H = p / np.cos(B) - N
    if rad:
        return L, B, H
    else:
        return rad2degree(L), rad2degree(B), H
    
def convert_sol_type(type):
    #Q=1:fix,2:float,3:sbas,4:dgps,5:single,6:ppp
    if type == 1:
        return 4
    elif type == 2:
        return 5
    elif type == 3:
        return 3
    elif type == 4:
        return 2
    elif type == 5:
        return 1
    elif type == 6:
        return 3

def convert_to_defult(line):
    if line.startswith('%'):
        return None
    # 分割每一行
    data = line.split()  
    if len(data) == 49:
        # 拼装数据
        new_data = data[:2]
        x = float(data[2])
        y = float(data[3])
        z = float(data[4])
        l, b, h = xyz2BLH(x, y, z)
        new_data.extend([str(b), str(l), str(h)])
        vx = data[16]
        vy = data[17]
        vz = data[18]
        new_data.extend([vx, vy, vz])
        new_data.append(data[25])
        new_data.append(data[26])
        new_data.append(data[27])
        sol_type = int(data[5])
        sol_type = convert_sol_type(sol_type)
        new_data.append(str(sol_type))
        new_line = ','.join(new_data) + '\n'
        return new_line
    return None