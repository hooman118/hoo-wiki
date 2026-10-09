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
| **小黑猫风格** | 【生命·修行】 / 【随笔】 | 萌呆大眼白眶黑猫、纯黑色躯干与边缘毛刺划线、高饱和暖黄纯色背景、极简大留白 | **核心基准参考图**：<br>`.agents/skills/article-illustration/resources/black-cat-original-reference.png`<br>*(辅助历史参考：`zh/pages/writing/cat_typhoon_umbrella.jpg`)* |
| **【AI简史】题图动画风** | 【AI简史 / 小白话系列】（篇首题图 / 叙事封面） | 现代科普动画漫画插画、戏剧冲突角色群像、科技元素白板/看板、生动叙事隐喻、清亮数码柔和光影与轮廓线 | **历史基准图**：<br>`zh/pages/writing/Gemini_Generated_Image_202602130844.jpg`<br>`zh/pages/writing/Gemini_Generated_Image_3k3wl03k3wl03k3w.png`<br>`zh/pages/writing/Gemini_Generated_Image_4zaxs44zaxs44zax.png` |
| **【AI简史】黑板板书风** | 【AI简史 / 小白话系列】（文理/技术解析配图） | 深灰/黑青色真实黑板底色、彩色粉笔手绘框线与箭头、结构拓扑图解、参数标注与数学物理逻辑流程 | **历史基准图**：<br>`zh/pages/writing/Gemini_Generated_Image_lahx03lahx03lahx.png` |
| *(待扩充风格 D)* | 【科幻小说 / 方舟】 | *(后续根据需求新增)* | *(待定义)* |

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

## 3. 【AI简史 / 小白话系列】双轨视觉规范与指南

【AI简史 / 小白话系列】文章采用**双轨配图体系**，根据插画所承担的功能严格区分：

### 🎬 A 轨：题图 / 叙事封面（科普动画漫画风）
- **功能定位**：文章开篇题图或全篇叙事高潮，用于呈现技术路线冲突、历史人物交锋与时代风云。
- **视觉要素**：
  1. **现代 2.5D / 美式+日系融合的数码动画手绘风**：线条干净、色彩清丽柔和（科技蓝、暖橙、米白等搭配），带柔和立体光影，角色生动且具表现力。
  2. **戏剧冲突与叙事张力**：通过群像角色互动（如老派专家 vs 新生代极客、打瞌睡的 CPU vs 忙碌的 GPU 工厂、手忙脚乱的驱动团队等）幽默呈现核心技术矛盾。
  3. **科技道具与信息图表集成**：画面中自然融入白板、架构图、路标、公式、数据流管道、气泡对白或诙谐告示牌（例如 *“Every time I fire a linguist...”*、*“G80 Unified Architecture”*）。
  4. **画幅比例**：推荐横版宽幅（16:9 或 4:3），作为文章题图极具视觉抓地力。

### 📋 B 轨：原理 / 架构解析图（黑板板书风 Chalkboard Diagram）
- **功能定位**：插入在正文技术原理剖析段落，用于替代枯燥文字，直观呈现硬件架构、数学模型、状态转移或数据流水线。
- **视觉要素**：
  1. **真实黑板板书质感**：深灰/黑青色真实石板黑板纹理背景（Dark slate chalkboard texture）。
  2. **手绘粉笔质感线条与文字**：白色为主，配合浅黄、天蓝、浅绿粉笔笔触（Hand-drawn chalk lines and arrows），带自然的粉笔摩擦颗粒感与轻微擦拭痕迹。
  3. **架构拓扑与逻辑流程**：清晰的模块方框（如 TPC、SM、Crossbar Switch、HMM 状态节点）、流动箭头与英文/简中核心参数标注。

---

## 4. 跨系列风格绝对隔离原则（严禁串画）

为维护项目不同文章系列的专属审美与阅读心智，**严禁跨系列混用视觉风格**：

1. **【生命·修行 / 随笔】 ⇋ 严禁使用科技动画与黑板图**：
   - 只能使用「小黑猫风格」，以极简暖黄底色、大眼黑猫与大留白传递内省与生活质感。绝不可混入科技图表、冷色数码或复杂写实元素。
2. **【AI简史 / 小白话系列】 ⇋ 严禁使用小黑猫**：
   - 题图必须使用专属的「科普动画漫画风」，原理图必须使用「黑板板书风」。绝不可在 AI 简史中画小黑猫。
3. **【科幻小说 / 方舟】 ⇋ 严禁使用萌系动物与纯板书**：
   - 保持硬科幻废土与太空设定（待建立专属硬科幻写实/概念艺术风格）。

---

## 5. 配图处理与文章归档流程

生成配图后，自动执行以下后续步骤：

1. **文件规范重命名与移动**：
   将生成的临时图片复制并移动至 `zh/pages/writing/` 目录，命名格式为 `YYYYMMDD_<short_description>.jpg`。
2. **根据上下文灵活性嵌入 Markdown**：
   **严禁机械固定放在最顶部**。应根据配图意象所对应的文字节点与情感高潮决定嵌入位置：
   - **文章最顶部**：适合全篇总括意象、开篇即出现的核验场景。
   - **文章中段 / 文章末尾**：若配图承接文章后半段的叙事隐喻、思想升华或结尾余音（例如星空、流星雨、古老寓言等），**必须将配图置于对应的段落下方或文章最末尾**。
   ```markdown
   ![图片描述](YYYYMMDD_<short_description>.jpg)
   ```
