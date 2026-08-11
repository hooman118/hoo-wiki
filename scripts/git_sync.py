#!/usr/bin/env python3
"""
Git 自动同步脚本：自动生成索引、提交代码并推送到 GitHub 远程仓库。
使用方式：
    python3 scripts/git_sync.py [可选: 提交信息]
"""

import sys
import subprocess
import os

# 确保输出实时刷到日志/终端中，避免缓冲延迟
sys.stdout.reconfigure(line_buffering=True)

def log(msg):
    print(msg, flush=True)

def run_cmd(cmd, timeout=None):
    log(f"➜ 执行: {cmd}")
    try:
        res = subprocess.run(cmd, shell=True, text=True, timeout=timeout)
        if res.returncode != 0:
            log(f"❌ 错误: 执行失败，退出码 {res.returncode}")
            return False
        return True
    except subprocess.TimeoutExpired:
        log(f"⏰ 错误: 执行超时（限时 {timeout} 秒），已自动取消操作。")
        return False

def check_github_connectivity():
    """预检 GitHub 远程仓库连通性（带 8 秒超时）"""
    log("🔍 正在测试 GitHub 远程网络连通性...")
    # 使用 git ls-remote 探测远程，限时 10 秒
    res = subprocess.run("git ls-remote --exit-code origin HEAD", shell=True, capture_output=True, text=True, timeout=10)
    if res.returncode == 0:
        log("✅ GitHub 网络连接正常！")
        return True
    else:
        log("❌ GitHub 网络连接失败或响应超时！")
        return False

def main():
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(repo_root)

    # 1. 如果存在 generate_index.py，先自动更新索引
    index_script = os.path.join(repo_root, "generate_index.py")
    if os.path.exists(index_script):
        log("📝 正在更新索引...")
        if not run_cmd("python3 generate_index.py --base_dir zh/pages/writing --index_file index.md"):
            sys.exit(1)

    # 2. git add
    log("📦 正在暂存文件...")
    if not run_cmd("git add ."):
        sys.exit(1)

    # 检查是否有改动需要 commit
    status_res = subprocess.run("git status --porcelain", shell=True, text=True, capture_output=True)
    has_changes = bool(status_res.stdout.strip())

    if has_changes:
        # 3. 构造提交信息
        if len(sys.argv) > 1:
            commit_msg = " ".join(sys.argv[1:])
        else:
            commit_msg = "docs: update articles, settings, and indexes"

        log(f"💬 提交 Commit: '{commit_msg}'")
        if not run_cmd(f'git commit -m "{commit_msg}"'):
            sys.exit(1)
    else:
        log("ℹ️ 没有新的文件改动需要提交，继续检查未推送的提交...")

    # 4. 优化 Git 传输参数与本地 Loose Objects 压缩 (瘦身)
    log("🧹 正在对本地 Git 仓库进行压缩瘦身 (git gc)...")
    run_cmd("git config http.postBuffer 524288000")
    run_cmd("git gc --auto")

    # 4. 检查网络并执行 git push
    try:
        if not check_github_connectivity():
            log("⚠️ 当前网络环境下无法连接 GitHub。")
            log("💡 本地改动已为您安全 Commit 提交！请检查网络代理/梯子后，重新运行此脚本或执行 `git push`。")
            sys.exit(1)
    except subprocess.TimeoutExpired:
        log("⏰ 测试网络连接超时（>10s），当前网络无法访问 GitHub。")
        log("💡 本地改动已为您安全 Commit 提交！请检查网络代理/梯子后重新重试。")
        sys.exit(1)

    # 获取当前分支名称
    branch_res = subprocess.run("git branch --show-current", shell=True, text=True, capture_output=True)
    branch = branch_res.stdout.strip() or "main"

    log("🚀 正在推送到 GitHub 远程仓库...")
    push_success = run_cmd(f"git push --progress origin {branch}", timeout=None)
    
    if not push_success:
        log("⚠️ 一次性完整推送失败（可能是提交包过大），正在启动智能分批推送 (Chunked Push) 策略...")
        # 获取未推送的 commit 列表 (由旧到新)
        commits_res = subprocess.run(f"git log origin/{branch}..{branch} --reverse --format='%H'", shell=True, text=True, capture_output=True)
        commits = [c.strip("' ").strip() for c in commits_res.stdout.strip().splitlines() if c.strip()]
        
        if not commits:
            log("❌ 未发现可推送的提交或无法获取提交列表。")
            sys.exit(1)

        batch_size = 5
        total_commits = len(commits)
        log(f"📦 共有 {total_commits} 个未推送提交，将按每 {batch_size} 个分批推送...")
        
        all_batches_successful = True
        for i in range(0, total_commits, batch_size):
            chunk = commits[i:i + batch_size]
            target_commit = chunk[-1]
            log(f"🚚 正在分批推送第 [{i + 1} ~ {min(i + batch_size, total_commits)} / {total_commits}] 个 Commit ({target_commit[:7]})...")
            if not run_cmd(f"git push --progress origin {target_commit}:refs/heads/{branch}", timeout=None):
                log(f"❌ 错误: 分批推送到 {target_commit[:7]} 失败！")
                all_batches_successful = False
                break
            else:
                log(f"✅ 第 [{i + 1} ~ {min(i + batch_size, total_commits)}] 批 Commit 推送成功！")

        if all_batches_successful:
            log("🎉 智能分批推送全部完成！Git 同步成功！")
        else:
            log("❌ 分批推送中断。本地改动已安全 Commit 提交，请检查网络后重试。")
            sys.exit(1)
    else:
        log("🎉 Git 同步成功！")

if __name__ == "__main__":
    main()

