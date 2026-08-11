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
| **小黑猫风格** | 【生命·修行】 / 【随笔】 | 木刻版画线条、暖色大留白背景、灵性小黑猫 | `zh/pages/writing/20260731_sleeping_cat.jpg`<br>`zh/pages/writing/cat_typhoon_umbrella.jpg` |
| *(待扩充风格 B)* | 【科幻小说 / 方舟】 | *(后续根据需求新增)* | *(待定义)* |
| *(待扩充风格 C)* | 【AI简史 / 科普】 | *(后续根据需求新增)* | *(待定义)* |

---

## 2. 【小黑猫风格】核心规范与一致性指南

当用户提及“**小黑猫风格**”或为【生命·修行】/【随笔】生成配图时，必须严格遵守以下原则：

### 🎨 视觉要素
1. **艺术画风**：木刻版画 / 细腻黑线手绘风格（Linocut / Woodcut / Fine Line Art），保留质感黑线纹理。
2. **色彩搭配**：高对比度纯色温暖底色（以暖黄色 `#E5AC24` / 鹅黄 / 静谧暗金为主），背景干净统一。
3. **构图与留白**：
   - **大面积留白**：主体猫咪在画面中的占比控制在 **25% ~ 35%** 左右，居于中央。
   - **四周呼吸感**：四周保留极充裕、平整的大面积空白（Negative Space），衬托空灵、对峙与内省的叙事张力。
4. **猫咪神态与动向**：
   - 角色为纯黑亮泽小猫，根据文章情绪微调表情（如：蜷缩警惕、睁眼惶恐、沉思远眺、雨中打伞等）。

### 🖼️ 图生图（Image-to-Image）生成规范
为确保风格绝对一致，每次使用 `generate_image` 工具生成“小黑猫风格”配图时，**必须**在 `ImagePaths` 参数中传入至少 1~2 张基准参考图：

```json
"ImagePaths": [
  "/Users/hooman/Work/Writing/hoo-wiki/zh/pages/writing/20260731_sleeping_cat.jpg",
  "/Users/hooman/Work/Writing/hoo-wiki/zh/pages/writing/cat_typhoon_umbrella.jpg"
]
```

#### 标准 Prompt 模板：
```text
Maintain the exact same linocut/woodcut black cat illustration style, fine line art texture, and solid warm yellow background color from the reference image. 

Composition & Scaling:
- Subject: A cute, sleek black cat positioned right in the dead center of the frame.
- Scale & Margin: The cat is small in scale (occupying only ~30% of the canvas), surrounded by a vast amount of empty solid warm background with generous negative space and wide breathable margins.

Expression & Emotion:
- [在此描述具体的姿态与神态，例如：curled up tight with wide open expressive timid eyes, looking startled into the vast empty space.]
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
