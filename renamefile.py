import os
import shutil
from PIL import Image


def convert_image_and_rename_file(path):
    new_path = copy_path(path)
    convert_image_to_jpg(new_path)
    rename(new_path)
    return "成功"


def copy_path(path):
    # 获取当前文件夹的绝对路径和文件夹名称
    dir_path = os.path.abspath(path)
    dir_name = os.path.basename(dir_path)
    # 获取当前文件夹的上一级目录的绝对路径
    parent_path = os.path.dirname(dir_path)
    # 在上一级目录下创建同样的文件夹
    new_dir_path = os.path.join(parent_path, dir_name+'_copy')
    if os.path.exists(new_dir_path):
        shutil.rmtree(new_dir_path)
    os.mkdir(new_dir_path)
    # 遍历原始文件夹中的所有文件和文件夹，并将它们复制到副本文件夹中
    for item in os.listdir(path):
        source_item_path = os.path.join(path, item)
        destination_item_path = os.path.join(new_dir_path, item)
        if os.path.isfile(source_item_path):
            shutil.copy2(source_item_path, destination_item_path)
        else:
            shutil.copytree(source_item_path, destination_item_path)

    print(f"{new_dir_path} 文件夹已创建并复制完毕。")
    return new_dir_path


# 文件格式转换为jpg
def convert_image_to_jpg(path):
    # 遍历指定文件夹下的所有图片文件
    for root, dirs, files in os.walk(path):
        for name in files:
            # 获取图片文件的路径
            img_path = os.path.join(root, name)
            # 打开图片文件
            img = Image.open(img_path)
            # 如果当前图片格式不是jpg，则进行转换，否则跳过
            if img.format != 'JPEG':
                # 获取图片保存的路径
                path, ext = os.path.splitext(img_path)
                new_path = path + '.jpg'
                # 将图片保存为jpg格式
                img = img.convert('RGB')
                os.remove(img_path)
                img.save(new_path, format='JPEG')
                print('将%s转换为jpg格式并保存为%s' % (name, new_path))
            else:
                print('%s已经是jpg格式，不需要进行转换' % name)


# 重命名文件
def rename(path):
    # path = 'C:/Users/wangyu/Desktop/111'
    # 遍历指定文件夹下的所有图片文件
    for root, dirs, files in os.walk(path):
        i = 1
        files.sort()  # 按名称排序
        for file in files:
            # 获取文件后缀
            suffix = os.path.splitext(file)[1]
            # 构建新的文件名
            new_name = '{:03d}{}'.format(i, suffix)
            i += 1
            # 重命名文件
            os.rename(os.path.join(root, file), os.path.join(root, new_name))
