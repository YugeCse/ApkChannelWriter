import os
import re
import zipfile
import fileinput


# 文件拷贝函数
# srcfile 源文件
# targetfile 目标文件
def copy_apkfile(srcfile, targetfile):
    """ copy apk to other dicrectory\n
        :param srcfile resource apk-file\n
        :param targetfile target apk-file\n
    """
    # print("文件目录：%s" % folder)
    if os.path.exists(targetfile):  # 如果目标文件存在，则删除目标文件
        os.remove(targetfile)
    open(targetfile, "wb").write(open(srcfile, "rb").read())


# 读取渠道配置文件
# config_file 配置文件名
def read_channelconfig(config_file):
    channels = dict()
    fileinput.hook_encoded("utf-8")
    file = open(config_file, mode='r', encoding='utf-8')
    while True:
        line = file.readline().lstrip().rstrip('\n')
        if line is None or line == '':
            break
        if not line.startswith("#"):
            regex = re.compile('\[([^\]]*)\]\s*([A-Za-z0-9_]+)')
            match = regex.match(line)
            if match:
                channelname = match.group(1)
                channelvalue = match.group(2)
                channel_key = channelname if not (channelname == '' or channelname is None) else channelvalue
                channels["{channelName}".format(channelName=channel_key)] = channelvalue
            del match
            del regex
    return channels


# 写入渠道数据
# standard_apkfile 标准APK文件
# channel_name 渠道名称
# prefix_name 文件前缀名
def write_channelconfig(standard_apkfile, channel_name, prefix_name):
    zf = zipfile.ZipFile(standard_apkfile, 'a', zipfile.ZIP_DEFLATED)
    empty_file = 'META-INF/{prefix_name}channel_{channel}'.format(prefix_name=prefix_name, channel=channel_name)
    zf.write('../config/empty_channel.chl', empty_file)
    zf.close()  # 关闭Apk-Zip文件


# 递归清空目录
# folder_name 目录
def clear_folder(folder_name):
    folder = os.path.dirname(folder_name)
    if not os.path.exists(folder):  # 如果文件夹不存在，则创建文件夹
        os.makedirs(folder)
    for file in os.listdir(folder_name):
        filename = "%s%s" % (folder_name, file)
        if os.path.isfile(filename):
            if file == 'ReadMe.txt':  # 不删除说明文件
                continue
            # print("\t\t正在删除APK缓存文件 ------> %s\n" % filename)
            os.remove(filename)  # 删除缓存文件
        elif os.path.isdir(filename):
            clear_folder(filename)
            # os.removedirs(filename)
        else:
            print("\t\tunknown file!")


# 主程序函数执行代码
# (1).应该写入多个原生态Apk，数量由渠道数量确定
# (2).读取渠道名称，并写入渠道空文件
# (3).根据渠道名称重命名文件，并附上文件名称
# standard_apkfile 标准文件名
# outfolder 输出文件目录
# channel_prefix 渠道前缀名
# is_clear_outputdir 是否清空输出文件夹，默认为True
def exec_write_channel(standard_apkfile, outfolder, channel_prefix, is_clear_outputdir=True):
    if not os.path.exists(standard_apkfile):  # 检测文件是否找到
        print("\t\t错误，文件： %s  未找到" % standard_apkfile)
        exit(-1)
    config_channels = read_channelconfig("../config/channel.config")
    if is_clear_outputdir:  # 如果需要清空输出目录，则清理输出目录
        clear_folder(outfolder)
    print()  # 换行而已
    if config_channels is not None:  # 判断渠道数据是否存在
        print("\t\t【进行中】美团团队分渠道打包流程进行中：")
        for channel_key in config_channels:
            channel = config_channels[channel_key]  # 获取当前的渠道值
            print()
            print("\t\t【{channel_key}】-【{channel}】".format(channel_key=channel_key, channel=channel))
            print("--------------------------------------------------------")
            print("\t\t正在获取渠道名称，准备复制Apk文件 >>>> {channel}".format(channel=channel_key))  # 输出Apk渠道打包信息
            targetfilename = "{out_folder}/【{channel_name}】{standard_apkfile}"\
                .format(out_folder=outfolder,
                        channel_name=channel_key,
                        standard_apkfile=standard_apkfile.split("/")[-1])  # 目标文件名
            copy_apkfile(standard_apkfile, targetfilename)  # 复制APK文件
            print("\t\tApk文件已复制，正在处理渠道打包 >>> {channel_key}".format(channel_key=channel_key))
            write_channelconfig(targetfilename, channel, channel_prefix)  # 写入渠道空文件
            print("\t\t渠道打包已完成 >>> {channel_key}".format(channel_key=channel_key))
        print("\n\t\t【结果】：渠道打包都已完成")
    else:
        print("\t\t【结果】：未配置渠道数据，程序已结束")
    del config_channels  # 释放对象
    exit(0)
