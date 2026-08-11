#!/usr/bin/env python3
"""
一键工作流综合发布脚本：
做两件事：
1. 自动执行 Git 索引更新、Commit 与 Push 到 GitHub 远程仓库
2. (可选) 渲染排版并推送文章到微信公众号草稿箱

使用示例：
    # 仅同步 Git
    python3 scripts/publish.py --git

    # 同时同步 Git 并推送指定文章到微信草稿箱
    python3 scripts/publish.py "zh/pages/writing/20260726【生命⋅修行】时惑.md" --git --wechat
"""

import sys
import os
import argparse
import subprocess

def main():
    parser = argparse.ArgumentParser(description="hoo-wiki 文章发布与 Git/微信工作流工具")
    parser.add_argument("article", nargs="?", help="要发布的 Markdown 文章路径")
    parser.add_argument("--git", action="store_true", help="是否提交 Git 并推送到 GitHub")
    parser.add_argument("--wechat", action="store_true", help="是否推送到微信公众号草稿箱")
    parser.add_argument("--msg", default="", help="自定义 Git Commit 提交说明")
    args = parser.parse_args()

    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(repo_root)

    if not args.git and not args.wechat:
        # 默认同时执行两步（如果指定了文章）
        args.git = True
        if args.article:
            args.wechat = True

    # 1. 执行 Git 提交与 Push
    if args.git:
        print("\n================ Step 1: Git 同步 ================")
        git_script = os.path.join(repo_root, "scripts", "git_sync.py")
        cmd = [sys.executable, git_script]
        if args.msg:
            cmd.append(args.msg)
        elif args.article:
            article_name = os.path.basename(args.article)
            cmd.append(f"docs: publish {article_name}")
        subprocess.run(cmd, check=True)

    # 2. 推送微信草稿箱
    if args.wechat:
        print("\n================ Step 2: 微信草稿箱推送 ================")
        if not args.article:
            print("❌ 错误: 推送微信草稿箱需要指定 Markdown 文章路径！")
            print("示例: python3 scripts/publish.py \"zh/pages/writing/20260726【生命⋅修行】时惑.md\" --wechat")
            sys.exit(1)
        
        wechat_script = os.path.join(repo_root, "scripts", "publish_wechat.py")
        subprocess.run([sys.executable, wechat_script, args.article], check=True)

    print("\n✅ 所有发布任务执行完毕！")

if __name__ == "__main__":
    main()
