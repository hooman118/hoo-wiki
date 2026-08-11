#!/usr/bin/env python3
"""
分批大文件提交脚本 (修复中文文件名与quotePath)：
解决 GitHub HTTPS 传输 2GB 大 Payload 时的 408 HTTP Timeout 超时问题。
机制：将未推送的数据按每 100MB 拆分为独立的小 Commit 并立即 Push。
"""

import os
import sys
import subprocess

def run(cmd):
    print(f"➜ {cmd}", flush=True)
    res = subprocess.run(cmd, shell=True, text=True)
    return res.returncode == 0

def main():
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(repo_root)

    run("git config core.quotePath false")
    
    print("🔍 正在拉取最新的分支点信息...", flush=True)
    run("git reset --mixed origin/gh-pages")

    # 使用 git status -z 以 NULL 分隔符读取原生 UTF-8 路径，完美支持空格与中文字符
    raw_status = subprocess.check_output(["git", "status", "-z"]).decode("utf-8", errors="replace")
    entries = raw_status.split('\0')

    files_to_commit = []
    for entry in entries:
        if not entry:
            continue
        # status code is first 2 chars, followed by space or filename
        status = entry[:2]
        filepath = entry[3:] if len(entry) > 3 else ""
        if filepath and os.path.exists(os.path.join(repo_root, filepath)):
            files_to_commit.append(filepath)

    if not files_to_commit:
        print("✅ 没有未提交的修改！", flush=True)
        return

    print(f"📦 发现 {len(files_to_commit)} 个变更文件，准备按 100MB 分批打包推送...", flush=True)

    current_batch = []
    current_size = 0
    MAX_BATCH_SIZE = 100 * 1024 * 1024 # 100 MB
    batch_idx = 1

    for filepath in files_to_commit:
        abs_path = os.path.join(repo_root, filepath)
        file_size = 0
        if os.path.isfile(abs_path):
            file_size = os.path.getsize(abs_path)

        current_batch.append(filepath)
        current_size += file_size

        if current_size >= MAX_BATCH_SIZE:
            print(f"\n🚚 正在处理第 {batch_idx} 批提交 (包大小: {current_size / 1024 / 1024:.2f} MB, 文件数: {len(current_batch)})...", flush=True)
            
            # 使用列表传参调用 git add，避免 shell 转义字符异常
            subprocess.run(["git", "add"] + current_batch, check=True)
            
            commit_msg = f"docs: sync batch #{batch_idx} ({current_size / 1024 / 1024:.1f}MB)"
            if run(f'git commit -m "{commit_msg}"'):
                if not run("git push --progress origin gh-pages"):
                    print(f"❌ 第 {batch_idx} 批推送失败，脚本中断！", flush=True)
                    sys.exit(1)
                print(f"✅ 第 {batch_idx} 批推送成功！", flush=True)
            
            current_batch = []
            current_size = 0
            batch_idx += 1

    # 处理最后一批
    if current_batch:
        print(f"\n🚚 正在处理最后一批提交 (包大小: {current_size / 1024 / 1024:.2f} MB, 文件数: {len(current_batch)})...", flush=True)
        subprocess.run(["git", "add"] + current_batch, check=True)
        
        commit_msg = f"docs: sync final batch ({current_size / 1024 / 1024:.1f}MB)"
        if run(f'git commit -m "{commit_msg}"'):
            if not run("git push --progress origin gh-pages"):
                print("❌ 最后一批推送失败！", flush=True)
                sys.exit(1)
            print("✅ 最后一批推送成功！", flush=True)

    print("\n🎉 所有批次分拆推送完毕！GitHub 已完全同步！", flush=True)

if __name__ == "__main__":
    main()
