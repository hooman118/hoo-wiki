#!/usr/bin/env python3
"""
一键综合发布工作流脚本 (hoo-wiki)
核心升级：
1. 【解耦运行】：微信草稿箱推送与 Git 提交同步完全独立，互不阻塞、互不影响
2. 【异常隔离】：任一步骤出现网络波动、IP 白名单或 iCloud 云盘未就绪时，均有针对性提示，并在结束时汇总汇报
3. 【精准暂存】：自动将待发布文章传递给 git_sync.py，启用精准暂存，免疫云盘脱机全库扫描异常

使用方式：
    # 综合发布（默认同时执行微信草稿箱与 Git 提交，解耦且容错）：
    python3 scripts/publish.py "zh/pages/writing/文章文件名.md"

    # 仅发布微信公众号草稿箱：
    python3 scripts/publish.py "zh/pages/writing/文章文件名.md" --wechat

    # 仅同步 Git 与 GitHub：
    python3 scripts/publish.py "zh/pages/writing/文章文件名.md" --git
    python3 scripts/publish.py --git
"""

import sys
import os
import argparse
import subprocess

# 确保输出实时刷到日志/终端中
sys.stdout.reconfigure(line_buffering=True)

def log(msg=""):
    print(msg, flush=True)

def run_wechat_step(repo_root, article_path):
    """子步骤 1: 微信公众号草稿箱发布"""
    log("================ 🟢 Step A: 微信草稿箱推送 ================")
    if not article_path:
        log("⚠️ 未指定 Markdown 文章路径，跳过微信草稿箱推送。")
        return {"status": "skipped", "msg": "未指定文章"}

    wechat_script = os.path.join(repo_root, "scripts", "publish_wechat.py")
    if not os.path.exists(wechat_script):
        log(f"❌ 未找到微信发布脚本: {wechat_script}")
        return {"status": "failed", "msg": "发布脚本缺失"}

    cmd = [sys.executable, wechat_script, article_path]
    log(f"➜ 执行微信推送: {' '.join(cmd)}")
    res = subprocess.run(cmd, text=True, capture_output=True)
    
    # 实时输出子进程的标准输出与标准错误
    if res.stdout:
        print(res.stdout.strip())
    if res.stderr:
        print(res.stderr.strip())

    if res.returncode == 0:
        # 尝试提取 Media ID
        media_id = "已入草稿箱"
        for line in res.stdout.splitlines():
            if "Media ID:" in line:
                media_id = line.split("Media ID:")[-1].strip()
                break
        return {"status": "success", "msg": f"发布成功 (Media ID: {media_id})"}
    else:
        err_msg = res.stderr.strip() or res.stdout.strip()
        # 提取关键错误（如 40164 IP 白名单）
        if "40164" in err_msg:
            return {"status": "failed", "msg": "微信 API 报错: 出口 IP 未在白名单中"}
        return {"status": "failed", "msg": f"推送失败 (退出码 {res.returncode})"}

def run_git_step(repo_root, article_path=None, custom_msg=""):
    """子步骤 2: Git 索引更新、Commit 与推送"""
    log("\n================ 🔵 Step B: Git 索引与推送 ================")
    git_script = os.path.join(repo_root, "scripts", "git_sync.py")
    if not os.path.exists(git_script):
        log(f"❌ 未找到 Git 同步脚本: {git_script}")
        return {"status": "failed", "msg": "同步脚本缺失"}

    cmd = [sys.executable, git_script]
    if article_path:
        cmd.extend(["--article", article_path])
    if custom_msg:
        cmd.append(custom_msg)

    log(f"➜ 执行 Git 同步: {' '.join(cmd)}")
    res = subprocess.run(cmd, text=True)

    if res.returncode == 0:
        return {"status": "success", "msg": "已成功提交并推送到 GitHub"}
    elif res.returncode == 2:
        return {"status": "warning", "msg": "本地已安全 Commit 入库，推送待网络/云盘后台就绪"}
    else:
        return {"status": "failed", "msg": f"Git 处理异常 (退出码 {res.returncode})"}

def main():
    parser = argparse.ArgumentParser(description="hoo-wiki 一键发布与同步解耦工具")
    parser.add_argument("article", nargs="?", help="要发布的 Markdown 文章路径")
    parser.add_argument("--git", action="store_true", help="仅执行 Git 提交与推送")
    parser.add_argument("--wechat", action="store_true", help="仅推送到微信公众号草稿箱")
    parser.add_argument("--msg", default="", help="自定义 Git Commit 提交说明")
    args = parser.parse_args()

    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(repo_root)

    do_git = args.git
    do_wechat = args.wechat

    # 如果既未指定 --git 也未指定 --wechat，默认根据是否传入文章智能决策：
    if not do_git and not do_wechat:
        do_git = True
        if args.article:
            do_wechat = True

    results = {}

    # 1. 优先执行微信草稿箱推送（耗时短、用户首要关注）
    if do_wechat:
        results["wechat"] = run_wechat_step(repo_root, args.article)

    # 2. 执行 Git 本地提交与远程同步（精准暂存，容错隔离）
    if do_git:
        results["git"] = run_git_step(repo_root, args.article, args.msg)

    # 3. 打印清晰美观的综合报告
    log("\n================ 📋 一键发布结果汇总 ================")
    if "wechat" in results:
        w = results["wechat"]
        icon = "✅" if w["status"] == "success" else ("⚠️" if w["status"] == "skipped" else "❌")
        log(f"[{icon} 微信公众号草稿箱] : {w['msg']}")
    if "git" in results:
        g = results["git"]
        icon = "✅" if g["status"] == "success" else ("☁️" if g["status"] == "warning" else "❌")
        log(f"[{icon} GitHub 代码仓库]  : {g['msg']}")
    log("====================================================")

if __name__ == "__main__":
    main()
