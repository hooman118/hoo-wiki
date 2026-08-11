---
name: git-sync
description: 自动更新 hoo-wiki 全站文章索引 index.md，并将本地提交与更改自动同步推送至 GitHub 远程仓库。当用户需要同步/提交文章到 GitHub 时触发使用。
---

# Git 自动索引与推送 Skill (git-sync)

本 Skill 用于自动更新 `hoo-wiki` 项目的全站文章索引，并完成 Git 暂存、Commit 及推送到 GitHub 远程仓库（`gh-pages` 分支）。

---

## 依赖与环境准备
- **操作系统需求**：macOS / Linux
- **Python 环境**：Python 3.x
- ** Git 凭证**：确认已在 macOS Keychain 或系统中配置好 Git 凭证。

---

## 执行步骤与命令

### 1. 单独运行 Git 自动同步脚本
在项目根目录下，直接运行：
```bash
python3 scripts/git_sync.py "自定义提交说明（可选）"
```
*如果不传提交说明参数，默认 Commit 消息为 `"docs: update articles, settings, and indexes"`。*

### 2. 脚本底层执行流程
该脚本会自动完成以下操作：
1. **更新索引**：自动调用 `generate_index.py --base_dir zh/pages/writing --index_file index.md` 扫描所有日常随笔与文章，生成结构化 Markdown 目录。
2. **暂存文件**：执行 `git add .`。
3. **提交 Commit**：如果存在未提交改动，自动创建 git commit。
4. **推送到 GitHub**：获取当前分支（如 `gh-pages` 或 `main`），推送到远程仓库 `origin`。

---

## 常用衍生组合命令
如果需要同时发布文章到微信草稿箱并同步 GitHub，请配合使用 `publish.py`：
```bash
python3 scripts/publish.py "zh/pages/writing/文章文件名.md" --git
```
