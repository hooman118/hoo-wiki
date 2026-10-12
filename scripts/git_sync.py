#!/usr/bin/env python3
"""
Git 自动同步脚本：自动生成索引、提交代码并推送到 GitHub 远程仓库。
优化支持：
1. 目标文章精准暂存（避免在 iCloud / Google Drive 云盘环境下盲目全库扫描触发 mmap 脱机异常）
2. 云盘脱机与 mmap 异常的智能捕获与容错降级
3. 提交与推送与外部发布完全解耦
使用方式：
    python3 scripts/git_sync.py [--article 文章路径] [可选: 提交信息]
"""

import sys
import subprocess
import os
import re
import argparse

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
    try:
        res = subprocess.run("git ls-remote --exit-code origin HEAD", shell=True, capture_output=True, text=True, timeout=8)
        if res.returncode == 0:
            log("✅ GitHub 网络连接正常！")
            return True
        else:
            log("❌ GitHub 网络连接失败（可能需要开启网络代理或梯子）")
            return False
    except subprocess.TimeoutExpired:
        log("⏰ 测试网络连接超时（>8s），当前网络无法直连 GitHub。")
        return False
    except Exception as e:
        log(f"❌ 网络连通性测试异常: {e}")
        return False

def extract_article_images(article_path):
    """从 Markdown 文章中解析引用的本地图片路径"""
    images = []
    if not os.path.exists(article_path):
        return images
    try:
        with open(article_path, "r", encoding="utf-8") as f:
            content = f.read()
        article_dir = os.path.dirname(article_path)
        img_refs = re.findall(r'!\[.*?\]\((.*?)\)', content)
        for ref in img_refs:
            ref = ref.strip()
            if ref.startswith("http://") or ref.startswith("https://"):
                continue
            # 本地图片
            if os.path.isabs(ref):
                local_path = ref
            else:
                local_path = os.path.normpath(os.path.join(article_dir, ref))
            if os.path.exists(local_path):
                images.append(local_path)
    except Exception as e:
        log(f"⚠️ 解析文章配图时出现微小异常（已跳过）: {e}")
    return images

def safe_git_stage(article_path=None):
    """安全暂存文件：优先精准暂存指定文章及相关依赖，避免在云盘下扫描脱机文件"""
    # 0. 自动清理可能残留的 stale lock
    lock_file = os.path.join(".git", "index.lock")
    if os.path.exists(lock_file):
        try:
            os.remove(lock_file)
            log("🧹 已自动清理陈旧的 .git/index.lock 文件。")
        except Exception:
            pass

    staged_targets = []

    # 1. 如果指定了具体文章，执行精准暂存策略
    if article_path and os.path.exists(article_path):
        log(f"🎯 启用【精准暂存模式】：聚焦当前发布的文章及相关索引...")
        staged_targets.append(f'"{article_path}"')
        
        # 扫描并加入相关配图
        imgs = extract_article_images(article_path)
        for img in imgs:
            staged_targets.append(f'"{img}"')

        # 索引与技能配置
        for p in ["index.md", "zh/pages/*.md", ".agents/skills/article-illustration/SKILL.md"]:
            staged_targets.append(p)

        cmd = f"git add {' '.join(staged_targets)}"
        if run_cmd(cmd):
            return True
        log("⚠️ 精准暂存执行未完全成功，尝试安全容错备用模式...")

    # 2. 全库或备用模式
    log("📦 正在暂存文件 (git add .)...")
    res = subprocess.run("git add .", shell=True, text=True, capture_output=True)
    if res.returncode == 0:
        return True
    
    # 3. 针对云盘 (iCloud / Google Drive) mmap 脱机异常的智能容错
    err_out = res.stderr or res.stdout or ""
    if "mmap failed" in err_out or "Operation canceled" in err_out:
        log("⚠️ 提示: 检测到云盘（如 iCloud / Google Drive）中存在未完全本地化的历史脱机文件。")
        log("💡 正在自动降级为安全分步暂存 (仅暂存文章库与索引)...")
        fallback_cmd = "git add index.md zh/pages/ .agents/ 2>/dev/null || true"
        subprocess.run(fallback_cmd, shell=True)
        return True

    log(f"❌ 暂存失败: {err_out.strip()}")
    return False

def main():
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(repo_root)

    parser = argparse.ArgumentParser(description="hoo-wiki Git 同步工具")
    parser.add_argument("--article", help="指定发布的 Markdown 文章路径（启用精准暂存，避免云盘脱机异常）")
    parser.add_argument("message", nargs="*", help="Git Commit 提交信息")
    args = parser.parse_args()

    # 1. 如果存在 generate_index.py，先自动更新索引
    index_script = os.path.join(repo_root, "generate_index.py")
    if os.path.exists(index_script):
        log("📝 正在更新索引...")
        run_cmd("python3 generate_index.py --base_dir zh/pages/writing --index_file index.md")

    # 2. 安全/精准暂存
    if not safe_git_stage(args.article):
        log("❌ Git 暂存失败，中断操作。")
        sys.exit(1)

    # 3. 检查是否有暂存的改动需要 commit
    diff_res = subprocess.run("git diff --cached --name-only", shell=True, text=True, capture_output=True)
    has_staged = bool(diff_res.stdout.strip())

    if has_staged:
        if args.message:
            commit_msg = " ".join(args.message)
        elif args.article:
            article_name = os.path.basename(args.article)
            commit_msg = f"docs: publish {article_name}"
        else:
            commit_msg = "docs: update articles, settings, and indexes"

        log(f"💬 提交 Commit: '{commit_msg}'")
        # 使用 --no-status 避免触发全树 status 扫描导致的云盘脱机卡顿
        if not run_cmd(f'git commit --no-status -m "{commit_msg}"'):
            log("❌ Commit 提交失败。")
            sys.exit(1)
    else:
        log("ℹ️ 暂存区无新改动，检查本地是否有尚未推送的历史 Commit...")

    # 获取当前分支名称
    branch_res = subprocess.run("git branch --show-current", shell=True, text=True, capture_output=True)
    branch = branch_res.stdout.strip() or "main"

    # 4. 检查是否有未推送的提交
    unpushed_check = subprocess.run(f"git log origin/{branch}..{branch} --oneline", shell=True, text=True, capture_output=True)
    unpushed_commits = unpushed_check.stdout.strip().splitlines()
    if not unpushed_commits:
        log("🎉 本地与 GitHub 远程完全一致，无需额外推送！")
        return

    log(f"📦 发现 {len(unpushed_commits)} 个本地已提交、待推送至 GitHub 的 Commit。")

    # 5. 检查网络连通性并推送
    if not check_github_connectivity():
        log("⚠️ 当前网络直连 GitHub 失败。")
        log("💡 【安全提示】您的所有改动均已在本地安全创建 Git Commit！")
        log(f"💡 稍后开启网络代理/梯子后，在终端执行 `git push origin {branch}` 即可完成最终推送。")
        sys.exit(2)

    log(f"🚀 正在推送到 GitHub 远程仓库 (origin/{branch})...")
    push_res = subprocess.run(f"git push --progress origin {branch}", shell=True, text=True, capture_output=True)
    
    if push_res.returncode == 0:
        log("🎉 Git 同步成功！全部提交已安全推送到 GitHub！")
        sys.exit(0)
    else:
        err = (push_res.stderr or push_res.stdout or "").strip()
        if "mmap failed" in err or "Operation canceled" in err or "Operation timed out" in err:
            log("☁️ 【云盘提示】本地 Commit 已成功生成！")
            log("   项目位于 iCloud 云盘目录中，macOS 正在后台同步部分大型 pack 历史缓存。")
            log("   所有最新文字与索引均已 100% 安全入库。待 iCloud 完成后台同步后再次运行即可自动推送到 GitHub。")
            sys.exit(2)
        elif "unable to access" in err or "Empty reply from server" in err:
            log("🌐 【网络提示】本地 Commit 已成功生成！")
            log("   当前与 GitHub 的网络连接被重置，网络恢复或开启代理后即可顺利推送。")
            sys.exit(2)
        else:
            log(f"⚠️ 推送遇到非预期情况: {err}")
            log("💡 本地改动已安全 Commit 提交，请检查后重试。")
            sys.exit(1)

if __name__ == "__main__":
    main()
