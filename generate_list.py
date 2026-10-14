import os
import json
import re

# 🔥 配置：这里填你【本地图片的根目录】
# 比如你的本地路径是 D:\图片\me-de-tupian\images\chapters\个人烤肉
ROOT_FOLDER = r"D:\github project\me-de-tupian\images\chapters\个人烤肉"

# 支持的图片格式（可自行添加）
IMAGE_EXTS = (".png", ".jpg", ".jpeg", ".gif", ".webp")

def natural_parts(text):
    """把字符串切成 文本/数字 片段；数字转成 int，实现按数值大小比较"""
    parts = []
    for part in re.split(r"(\d+)", text):
        if part.isdigit():
            parts.append((1, int(part)))
        else:
            parts.append((0, part.lower()))
    return tuple(parts)

def natural_sort_key(name):
    """自然排序：主文件名按数字大小比较，避免 001.png 后面跟 0010.png"""
    stem, ext = os.path.splitext(name)
    return (natural_parts(stem), ext.lower())

def generate_list_json(folder_path):
    """遍历文件夹，生成list.json"""
    # 获取当前文件夹所有图片
    images = []
    for file in os.listdir(folder_path):
        # 过滤图片文件
        if file.lower().endswith(IMAGE_EXTS):
            images.append(file)

    # 按自然顺序排序（001.png < 002.png < ... < 009.png < 0010.png）
    images.sort(key=natural_sort_key)
    
    # 没有图片则跳过
    if not images:
        return
    
    # 生成list.json路径
    json_path = os.path.join(folder_path, "list.json")
    
    # 写入文件（格式化）
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(images, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 生成成功：{json_path}")

def scan_all_folders(root):
    """递归扫描所有子文件夹"""
    for dirpath, dirnames, filenames in os.walk(root):
        # 为每个文件夹生成list.json
        generate_list_json(dirpath)

if __name__ == "__main__":
    print("🚀 开始批量生成 list.json...")
    scan_all_folders(ROOT_FOLDER)
    print("\n🎉 所有章节 list.json 生成完成！")
    input("按回车键退出...")