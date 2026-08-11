import os
import glob
import re
from collections import defaultdict
import argparse

# 解析命令行参数
parser = argparse.ArgumentParser(description='Generate an index of markdown files.')
parser.add_argument('--base_dir', required=True, help='The directory to scan for files.')
parser.add_argument('--index_file', required=True, help='The path to the index file to update.')
parser.add_argument('--file_template', default=r"(\d{4})(\d{2})(\d{2})(.*).md", 
                    help='The regex to match file names. Default is "(\d{4})(\d{2})(\d{2})(.*).md"')
parser.add_argument('--header', default='# 立身中正、舍己从人，养浩然之气！', 
                    help='The header to write at the top of the index file. Default is "# 立身中正、舍己从人，养浩然之气！"')
args = parser.parse_args()

# 指定基础目录、索引文件路径和文件模板
base_dir = args.base_dir
index_file_path = args.index_file
file_template = args.file_template
header = args.header

# 创建一个按年份和月份分类的文件字典
files_by_date = defaultdict(lambda: defaultdict(list))

# 遍历目录下的所有文件
for file_path in glob.glob(os.path.join(base_dir, "*.md")):
    # 提取文件名
    filename = os.path.basename(file_path)
    
    # 通过正则表达式匹配文件名
    match = re.match(file_template, filename)
    if match:
        # 如果文件名匹配，将其添加到对应的年份和月份列表中
        year, month, day, rest = match.groups()
        files_by_date[year][month].append((filename, filename))

# 创建一个字典来存储已经被索引的文件
indexed_files = {}

# 如果索引文件已经存在，读取它并添加已经被索引的文件到字典中
if os.path.exists(index_file_path):
    with open(index_file_path, "r") as index_file:
        for line in index_file:
            match = re.search(r'\((.*)\)', line)
            if match:
                indexed_files[match.group(1)] = True
            else:
                print(f"Warning: The line '{line.strip()}' in the index file does not match the expected format.")

# 创建索引文件的目录（如果它还不存在且不是当前目录）
dirname = os.path.dirname(index_file_path)
if dirname:
    os.makedirs(dirname, exist_ok=True)

# 打开或创建索引文件以写入
with open(index_file_path, "a") as index_file:
    # 写入文件头
    index_file.write(f"{header}\n")
    
    # 按年份和月份遍历文件
    for year in sorted(files_by_date.keys(), reverse=True):
        index_file.write(f"## {year}\n")
        
        for month in sorted(files_by_date[year].keys(), reverse=True):
            index_file.write(f"### {int(month)}月\n")
            
            # 按日期遍历该月份的文件
            for name, filename in sorted(files_by_date[year][month], reverse=True):
                # 计算文件的相对路径
                relative_path = os.path.join(os.path.relpath(base_dir, index_file_path), filename)
                
                # 如果文件已经被索引，跳过
                if relative_path in indexed_files:
                    continue
                
                # 如果文件不存在，打印警告信息
                if not os.path.exists(os.path.join(base_dir, filename)):
                    print(f"Warning: File {relative_path} does not exist.")
                
                # 写入文件名（或你可能想要写入的其他信息）
                index_file.write(f"- [{name}]({relative_path})\n")
            
            index_file.write("\n")

# --- 新增功能：自动同步更新各类目索引文件 (zh/pages/*.md) ---
pages_dir = os.path.dirname(os.path.abspath(base_dir))

category_files_map = {
    '生命⋅修行': '生命⋅修行.md',
    '生命·修行': '生命⋅修行.md',
    '生命•修行': '生命⋅修行.md',
    '随笔': '随笔.md',
    '创业': '创业.md',
    '区块链': '区块链.md',
    '生命•故事': '生命•故事.md',
    '生命⋅故事': '生命•故事.md',
    '生命·故事': '生命•故事.md',
    '教程': '教程.md'
}

cat_articles = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

for file_path in glob.glob(os.path.join(base_dir, "*.md")):
    filename = os.path.basename(file_path)
    match = re.match(r'(\d{4})(\d{2})\d{2}\s*【([^】]+)】(.*)\.md', filename)
    if match:
        year, month, tag, rest = match.groups()
        matched_cat_file = None
        for key, val in category_files_map.items():
            if key == tag or key.replace('⋅', '').replace('•', '').replace('·', '') == tag.replace('⋅', '').replace('•', '').replace('·', ''):
                matched_cat_file = val
                break
        if matched_cat_file:
            cat_articles[matched_cat_file][year][month].append(filename)

print("📝 正在自动更新各类目索引文件 (zh/pages/*.md)...")

for cat_file, years in cat_articles.items():
    cat_file_path = os.path.join(pages_dir, cat_file)
    
    # 默认 Header
    header_title = f"# {os.path.splitext(cat_file)[0]}"
    if os.path.exists(cat_file_path):
        with open(cat_file_path, 'r', encoding='utf-8', errors='ignore') as f:
            first_line = f.readline().strip()
            if first_line.startswith('#'):
                header_title = first_line

    lines = [header_title]
    for year in sorted(years.keys(), reverse=True):
        lines.append(f"## {year}")
        for month in sorted(years[year].keys(), reverse=True):
            lines.append(f"### {int(month)}月")
            for fname in sorted(years[year][month], reverse=True):
                lines.append(f"- [{fname}](writing/{fname})")
            lines.append("")
        lines.append("")

    with open(cat_file_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines).strip() + "\n")
    print(f"  ✅ 已成功更新类目索引: {cat_file}")

