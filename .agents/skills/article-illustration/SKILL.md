---
name: article-illustration
description: 文章自动配图生成与视觉风格管理规范。当用户要求生成文章配图、提及特定视觉风格（如“小黑猫风格”），或需要为不同分类文章匹配图片时触发使用。
---

# 文章配图生成与视觉风格规范 (article-illustration)

本 Skill 用于管理 `hoo-wiki` 项目中文章配图的风格一致性、生成 Prompt 规范及流程自动化。

---

## 1. 风格库管理架构 (可扩展)

不同分类与主题的文章对应特定的视觉插画风格。当前已确立核心风格，并预留后续新增分类风格的扩展空间：

| 风格名称 | 适用文章类型 | 核心视觉元素 | 基准参考图路径 |
| :--- | :--- | :--- | :--- |
| **小黑猫风格** | 【生命·修行】 / 【随笔】 | 萌呆大眼白眶黑猫、纯黑色躯干与边缘毛刺划线、高饱和暖黄纯色背景 | **核心基准参考图**：<br>`.agents/skills/article-illustration/resources/black-cat-original-reference.png`<br>*(辅助历史参考：`zh/pages/writing/cat_typhoon_umbrella.jpg`)* |
| *(待扩充风格 B)* | 【科幻小说 / 方舟】 | *(后续根据需求新增)* | *(待定义)* |
| *(待扩充风格 C)* | 【AI简史 / 科普】 | *(后续根据需求新增)* | *(待定义)* |

---

## 2. 【小黑猫风格】核心规范与一致性指南

当用户提及“**小黑猫风格**”或为【生命·修行】/【随笔】生成配图时，必须严格遵守以下原则：

### 🎨 视觉要素
1. **黑猫角色形象（以 `resources/black-cat-original-reference.png` 为风格基准）**：
   - **大圆白眼与小黑瞳孔**：极其标志性的硕大、呆萌圆形白眼（Huge cartoonish round white circle eyes with small black pupils looking straight, up, or toward objects），神态逗趣、呆滞而富有灵性。
   - **纯黑身躯与毛发小划线**：猫咪身体主体为高对比纯黑色（Solid jet-black body silhouette），边缘与侧背带有手绘细腻小短划线毛刺纹理（Sketchy fine hair stroke outlines along edges）。绝非普通虎斑纹理，亦非生硬几何块。
2. **动作与场景高度匹配（Dynamic Pose Adaptability）**：
   - **严禁固定半身或机械重复单一站姿**！猫咪的姿态必须根据具体的文章隐喻和场景情节进行**动态变化**（例如：在井边踮脚伸爪试探、雨中抓着伞飘浮、蜷缩成一圈、蹲伏在桌角、探头远眺等）。
3. **色彩搭配与构图**：
   - 高对比度纯色温暖金黄底色（Solid Vibrant Warm Yellow Background），背景平整干净，大面积留白（负空间占比 65%~75%），主体处于中央附近，呼吸感充裕。

### 🖼️ 图生图（Image-to-Image）生成规范
为确保角色风格绝对一致，每次使用 `generate_image` 工具生成“小黑猫风格”配图时，**必须**在 `ImagePaths` 参数中将资源目录下的基准图传入：

```json
"ImagePaths": [
  "/Users/hooman/Work/Writing/hoo-wiki/.agents/skills/article-illustration/resources/black-cat-original-reference.png"
]
```

#### 标准 Prompt 模板：
```text
Maintain the EXACT SAME black cat character design, goofy cartoonish wide round white eyes with tiny black pupils, solid pitch-black body with sketchy edge hair strokes, and solid warm yellow background color from black-cat-original-reference.png.

Dynamic Pose & Scene Integration:
- The black cat's FULL BODY pose MUST interact dynamically with the scene (e.g., reaching paw towards the hanging water bucket, crouching at the well edge, floating with an umbrella, etc.). Do not use a static half-body crop unless requested.
- Expression: Comical, curious, wide-eyed, bewildered.

Composition & Background:
- Flat, solid vibrant warm yellow background, minimalist hand-drawn line art style.
- Centered subject (~30% canvas size) with large breathable yellow negative space.
```

---

## 3. 配图处理与文章归档流程

生成配图后，自动执行以下后续步骤：

1. **文件规范重命名与移动**：
   将生成的临时图片复制并移动至 `zh/pages/writing/` 目录，命名格式为 `YYYYMMDD_<short_description>.jpg`。
2. **自动嵌入 Markdown**：
   在对应的 Markdown 文章顶部（或标题 `# Title` 正下方）插入标准 Markdown 引用：
   ```markdown
   ![图片描述](YYYYMMDD_<short_description>.jpg)
   ```
