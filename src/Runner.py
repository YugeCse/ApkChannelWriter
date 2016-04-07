from src.ApkWriter import *


# 目标Apk文件
TARGET_APK = "../standard_apk/{filename}".format(filename="MeGuo_v3.0.2_10_standard__.apk")


# 输出APK的目录
OUTPUT_DIR = "../output_apk/"


# 渠道前缀名，完全名是,例如前缀是：baidu ,则为 baiduchannel@channelName
PREFIX_NAME = "meguo"


# 执行的主函数
if __name__ == "__main__":
    exec_write_channel(TARGET_APK, OUTPUT_DIR, PREFIX_NAME)
else:
    print("\t\tNone To Execute!")

