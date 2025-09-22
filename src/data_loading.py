import os
import pandas as pd
from config.paths import ORIGN_FIELD_DATA_PATH

def load_datafiles(origin_field_data_path= ORIGN_FIELD_DATA_PATH):
    """
    从您创建的文件结构中加载数据
    """
    data_records = []

    # 遍历所有子目录
    for freq_dir in os.listdir(origin_field_data_path):
        freq_path = os.path.join(origin_field_data_path, freq_dir)
        if not os.path.isdir(freq_path):
            continue

        # 解析频率和轴承类型
        if "12kHz" in freq_dir:
            sampling_freq = 12000
        elif "48kHz" in freq_dir:
            sampling_freq = 48000
        else:
            sampling_freq = None

        if "DE" in freq_dir:
            bearing_type = "DE"
            bearing_model = "SKF6205"
        elif "FE" in freq_dir:
            bearing_type = "FE"
            bearing_model = "SKF6203"
        elif "Normal" in freq_dir:
            bearing_type = "Normal"
            bearing_model = None
        else:
            bearing_type = "Unknown"
            bearing_model = None

        # 遍历该目录下的所有.mat文件
        for file in os.listdir(freq_path):
            if file.endswith('.mat'):
                file_path = os.path.join(freq_path, file)

                # 从文件名解析故障信息
                if file.startswith('B'):
                    fault_type = '滚动体故障'
                    fault_size = file[1:4]  # 如 '007'
                elif file.startswith('IR'):
                    fault_type = '内圈故障'
                    fault_size = file[2:5]  # 如 '007'
                elif file.startswith('OR'):
                    fault_type = '外圈故障'
                    fault_size = file[2:5]  # 如 '007'
                elif file.startswith('N'):
                    fault_type = '正常'
                    fault_size = None
                else:
                    fault_type = '未知'
                    fault_size = None

                # 载荷信息
                load = file.split('_')[-1].replace('.mat', '')

                data_records.append({
                    'file_path': file_path,
                    'filename': file,
                    'sampling_freq': sampling_freq,
                    'bearing_type': bearing_type,
                    'bearing_model': bearing_model,
                    'fault_type': fault_type,
                    'fault_size': fault_size,
                    'load': load
                })

    return pd.DataFrame(data_records)


df = load_datafiles()
print(f"总共加载了 {len(df)} 个数据文件")
print(df.head())