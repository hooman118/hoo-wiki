---
name: wechat-publish
description: 将指定的 Markdown 文章及文中内嵌的本地图片，自动转换为 Doocs 微信精美排版主题 HTML，并一键推送到微信公众号【草稿箱】。当用户需要发布文章至微信公众号草稿箱时触发使用。
---

# 微信公众号草稿箱一键发布 Skill (wechat-publish)

本 Skill 用于将 `hoo-wiki` 中的 Markdown 文章（含本地配图）自动上传至微信公众号素材库，并通过 Doocs 精美 Theme 排版后推送到微信公众号草稿箱。

---

## 依赖与环境准备

### 1. Python 依赖库
需安装 `requests` 和 `markdown` 模块：
```bash
pip3 install requests markdown
```

### 2. `.env` 凭证配置文件
在项目根目录下的 `.env` 文件（已被 `.gitignore` 保护）中配置微信 API 凭证：
```env
WECHAT_APP_ID=你的微信AppID
WECHAT_APP_SECRET=你的微信AppSecret
```

---

## 执行步骤与命令

### 1. 推送指定 Markdown 文章到草稿箱
```bash
python3 scripts/publish_wechat.py "zh/pages/writing/文章文件名.md"
```

### 2. 一键综合工作流（同时同步 GitHub + 推送微信草稿箱）
```bash
python3 scripts/publish.py "zh/pages/writing/文章文件名.md" --git --wechat
```

---

## 脚本核心逻辑说明

1. **凭证获取**：根据 `.env` 中的 `WECHAT_APP_ID` 和 `WECHAT_APP_SECRET` 自动向微信服务器请求最新的 `access_token`。
2. **图片解析与自动上传**：
   - 自动扫描 Markdown 文件中的图片语法 `![alt](image.jpg)`。
   - 将本地路径图片自动上传至微信公众号永久素材库 (`material/add_material`)。
   - 将转换后的微信图片 URL 替换回 HTML。
   - 自动将第一张配图设为草稿封面图（`thumb_media_id`）。
3. **Doocs 微信 Theme 主题渲染**：
   - 包含响应式字号、行距、标题下划线/边框、代码块及优雅引用框内联样式。
4. **推送到草稿箱**：
   - 自动调用 `cgi-bin/draft/add` 接口写入草稿箱。
   - 返回 `media_id` 并提示用户可在微信公众平台后台或「微信公众号助手」小程序查看 preview 并发表。
