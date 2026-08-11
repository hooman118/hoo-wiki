#!/usr/bin/env python3
"""
微信公众号草稿箱一键发布脚本 (Doocs 微信 Markdown 主题渲染)
使用方式：
    python3 scripts/publish_wechat.py <markdown文件路径>
配置说明：
    在根目录创建 .env 文件，写入：
    WECHAT_APP_ID=你的AppID
    WECHAT_APP_SECRET=你的AppSecret
"""

import os
import sys
import re
import json
import requests
import markdown

# 加载 .env 配置文件
def load_env(env_path):
    config = {}
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    config[k.strip()] = v.strip().strip('"').strip("'")
    return config

class WeChatPublisher:
    def __init__(self, app_id, app_secret):
        self.app_id = app_id
        self.app_secret = app_secret
        self.access_token = None

    def get_access_token(self):
        url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={self.app_id}&secret={self.app_secret}"
        res = requests.get(url).json()
        if "access_token" in res:
            self.access_token = res["access_token"]
            return self.access_token
        else:
            raise Exception(f"获取微信 AccessToken 失败: {res}")

    def upload_material_image(self, img_path):
        """上传图片至微信永久素材库获取 URL / media_id"""
        if not self.access_token:
            self.get_access_token()
        url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={self.access_token}&type=image"
        with open(img_path, "rb") as f:
            files = {"media": f}
            res = requests.post(url, files=files).json()
        if "url" in res:
            return res["url"], res.get("media_id")
        else:
            raise Exception(f"上传图片素材失败 {img_path}: {res}")

    def add_draft(self, title, content_html, thumb_media_id=None, digest=""):
        """向草稿箱添加文章"""
        if not self.access_token:
            self.get_access_token()
        url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={self.access_token}"

        article_data = {
            "title": title,
            "author": "发呆的浩然",
            "digest": digest[:120] if digest else "",
            "content": content_html,
            "content_source_url": "",
            "need_open_comment": 1,
            "only_fans_can_comment": 0,
            "is_original": 1
        }
        if thumb_media_id:
            article_data["thumb_media_id"] = thumb_media_id

        data = {"articles": [article_data]}
        res = requests.post(url, data=json.dumps(data, ensure_ascii=False).encode('utf-8')).json()
        if "media_id" in res:
            return res["media_id"]
        else:
            raise Exception(f"新增草稿箱文章失败: {res}")

def process_links_to_footnotes(md_text):
    """将外部链接转换为脚注（符合 Doocs / 微信外链处理规范）"""
    links = []

    def replacer(match):
        alt = match.group(1)
        url = match.group(2)
        if match.group(0).startswith("!"):
            return match.group(0)
        links.append((alt, url))
        idx = len(links)
        return f'{alt}<sup style="color: #059669; font-weight: bold;">[{idx}]</sup>'

    processed_text = re.sub(r'(?<!\!)\[(.*?)\]\((.*?)\)', replacer, md_text)

    footnote_html = ""
    if links:
        items = "".join([f'<li style="margin-bottom: 4px;">[{i+1}] {alt}: <span style="color: #059669; word-break: break-all;">{url}</span></li>' for i, (alt, url) in enumerate(links)])
        footnote_html = f'''
<hr style="border: none; border-top: 1px dashed #cbd5e1; margin: 30px 0 20px 0;" />
<section style="font-size: 13px; color: #64748b; line-height: 1.6; padding: 10px 0;">
  <p style="font-weight: bold; color: #334155; margin: 0 0 8px 0;">参考链接：</p>
  <ul style="padding-left: 20px; margin: 0; list-style-type: none;">
    {items}
  </ul>
</section>
'''
    return processed_text, footnote_html

def apply_doocs_inline_styles(html_body):
    """把 CSS 样式内联注入到每个 HTML 元素的 style 属性中 (Doocs 微信最大字号主题: 正文18px)"""
    html_body = re.sub(
        r'<blockquote>',
        '<blockquote style="margin: 18px 0; padding: 14px 18px; background-color: #f0fdf4; border-left: 4px solid #10b981; color: #166534; font-size: 17px; border-radius: 4px; line-height: 1.8;">',
        html_body
    )
    html_body = re.sub(
        r'<h2>',
        '<h2 style="font-size: 22px; font-weight: bold; color: #047857; margin: 28px 0 14px 0; padding-left: 10px; border-left: 4px solid #059669; line-height: 1.4;">',
        html_body
    )
    html_body = re.sub(
        r'<h3>',
        '<h3 style="font-size: 19px; font-weight: bold; color: #0f172a; margin: 22px 0 10px 0;">',
        html_body
    )
    html_body = re.sub(
        r'<p>',
        '<p style="font-family: -apple-system, BlinkMacSystemFont, \'Segoe UI\', Roboto, sans-serif; font-size: 18px; color: #2b2b2b; line-height: 1.85; letter-spacing: 0.05em; margin: 0 0 18px 0; text-align: justify;">',
        html_body
    )
    html_body = re.sub(
        r'<code>',
        '<code style="background-color: #f1f5f9; color: #0f766e; padding: 2px 6px; border-radius: 4px; font-family: monospace; font-size: 16px;">',
        html_body
    )
    html_body = re.sub(
        r'<pre>',
        '<pre style="background-color: #1e293b; color: #f8fafc; padding: 14px; border-radius: 8px; overflow-x: auto; margin: 18px 0; font-family: monospace; font-size: 16px; line-height: 1.6;">',
        html_body
    )
    html_body = re.sub(
        r'<img ',
        '<img style="max-width: 100%; height: auto; display: block; margin: 20px auto; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.08);" ',
        html_body
    )
    html_body = re.sub(
        r'<hr\s*/?>',
        '<hr style="border: none; border-top: 1px dashed #cbd5e1; margin: 24px 0;" />',
        html_body
    )
    html_body = re.sub(r'<ul>', '<ul style="padding-left: 20px; margin: 0 0 18px 0; color: #2b2b2b; font-size: 18px; line-height: 1.85;">', html_body)
    html_body = re.sub(r'<ol>', '<ol style="padding-left: 20px; margin: 0 0 18px 0; color: #2b2b2b; font-size: 18px; line-height: 1.85;">', html_body)
    html_body = re.sub(r'<li>', '<li style="margin-bottom: 6px;">', html_body)

    return f'<section style="font-family: -apple-system, BlinkMacSystemFont, \'Segoe UI\', Roboto, sans-serif; font-size: 18px; color: #2b2b2b; line-height: 1.85; padding: 10px;">\n{html_body}\n</section>'

def convert_md_to_wechat_html(md_file, publisher=None):
    base_dir = os.path.dirname(md_file)
    with open(md_file, "r", encoding="utf-8") as f:
        md_text = f.read()

    # 1. 提取标题 (第一个 # 标题) 并从正文剥离第一行标题（避免草稿箱正文中出现重复大标题）
    title_match = re.search(r'^#\s+(.+)$', md_text, re.MULTILINE)
    if title_match:
        title = title_match.group(1).strip()
        md_body_text = md_text[:title_match.start()] + md_text[title_match.end():]
    else:
        title = os.path.basename(md_file).replace('.md', '')
        md_body_text = md_text
    
    clean_title = re.sub(r'【.*?】', '', title).strip() or title

    # 2. 查找并替换本地图片链接，上传至微信
    thumb_media_id = None

    def replace_img(match):
        nonlocal thumb_media_id
        alt_text = match.group(1)
        img_rel_path = match.group(2)
        img_abs_path = os.path.normpath(os.path.join(base_dir, img_rel_path))

        if publisher and os.path.exists(img_abs_path):
            print(f"🖼️  正在上传图片至微信素材库: {img_abs_path}")
            wx_url, media_id = publisher.upload_material_image(img_abs_path)
            if not thumb_media_id and media_id:
                thumb_media_id = media_id
            return f'<img src="{wx_url}" alt="{alt_text}" />'
        return match.group(0)

    md_text_processed = re.sub(r'!\[(.*?)\]\((.*?)\)', replace_img, md_body_text)

    # 3. 转换外部链接为 Doocs 微信标准脚注
    md_text_processed, footnote_html = process_links_to_footnotes(md_text_processed)

    # 4. 使用 markdown 转换 HTML
    html_body = markdown.markdown(md_text_processed, extensions=['tables', 'fenced_code', 'nl2br'])
    
    # 5. 应用 Doocs 行内样式注入（直接挂载到每个 HTML 元素的 style 属性，微信不再被洗掉）
    full_html = apply_doocs_inline_styles(html_body) + footnote_html
    
    # 提炼摘要 (前100字纯文本)
    plain_text = re.sub(r'<[^>]+>', '', html_body).strip()
    digest = plain_text[:100].replace('\n', ' ')

    return clean_title, full_html, thumb_media_id, digest

def main():
    if len(sys.argv) < 2:
        print("用法: python3 scripts/publish_wechat.py <markdown文件路径>")
        sys.exit(1)

    md_file = os.path.abspath(sys.argv[1])
    if not os.path.exists(md_file):
        print(f"❌ 找不到 Markdown 文件: {md_file}")
        sys.exit(1)

    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    env_config = load_env(os.path.join(repo_root, ".env"))

    app_id = env_config.get("WECHAT_APP_ID") or os.environ.get("WECHAT_APP_ID")
    app_secret = env_config.get("WECHAT_APP_SECRET") or os.environ.get("WECHAT_APP_SECRET")

    if not app_id or not app_secret:
        print("⚠️ 提示: 未检测到 WECHAT_APP_ID 和 WECHAT_APP_SECRET。")
        print("请在项目根目录下创建 .env 文件并配置：")
        print("WECHAT_APP_ID=your_appid")
        print("WECHAT_APP_SECRET=your_appsecret")
        sys.exit(1)

    publisher = WeChatPublisher(app_id, app_secret)
    print("🔐 正在获取微信 AccessToken...")
    publisher.get_access_token()

    print(f"📄 正在解析 Markdown 文件: {md_file}")
    title, html_content, thumb_media_id, digest = convert_md_to_wechat_html(md_file, publisher)

    print(f"📤 正在把文章 《{title}》 推送到微信公众号【草稿箱】...")
    draft_id = publisher.add_draft(title, html_content, thumb_media_id, digest)

    print(f"🎉 推送成功！草稿 Media ID: {draft_id}")
    print("👉 请在微信公众平台后台或手机端「微信公众号助手」小程序查看草稿并预览发表。")

if __name__ == "__main__":
    main()
