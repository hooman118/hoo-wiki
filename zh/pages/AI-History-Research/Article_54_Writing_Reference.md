# 第 54 篇【双雄对决与改名求生 (1995–2005)】写作参考手册与深度资料库

> **文档定位**：本文档为《小白话系列——人工智能简史》第 54 篇的专属写作参考与学术底稿。系统梳理了三大学派（符号、统计、连接）演进脉络、统计学派的盛世帝国与特征工程天花板、贝尔实验室世纪决斗、学界改名自保的政治痕迹、欧陆孤狼与北境联盟的学术恩怨、心智哲学中“符号”的本质，以及前沿 AGI（o1/DeepSeek R1）对历史的终极呼应。

---

## 一、 篇章定位与三大学派 70 年演进全景

在整部《人工智能简史》中，第 54 篇处于**“承接显卡算力、回溯算法流亡、缝合十年断层”的枢纽地位**。

### 1. 三大学派演进脉络图（1956 – 2026+）

```text
 1956 达特茅斯古典起步           1980s–1990s 范式大分化                   2012–2026+ 现代与终局
┌──────────────────────┐        ┌────────────────────────────────┐        ┌──────────────────────────────┐
│ 1. 符号学派          │ ─────► │ 逻辑与显式规则体系 (GOFAI)      │ ─────► │ 1997 深蓝绝唱 / 规则专家系统崩溃
│ (Symbolism / 逻辑推理)│        │ (布尔逻辑 / Prolog / 专家系统)   │        │ 2024+ o1/R1 形式化逻辑验证复活 │
└──────────────────────┘        └────────────────────────────────┘        └──────────────────────────────┘
                                    ▲
                                    │ (90年代引入概率统计与凸优化)
                                    ├────────────────────────────────────► ┌──────────────────────────────┐
                                    │ 2. 统计学习学派 (Statistical ML)   │ │ 1995–2012 盛世霸权：         │
                                    │ (夺舍“机器学习”名号，凸几何划分)    │ │ SVM/SIFT/HOG/PageRank/SMT   │
                                    │                                    │ 撞上“人类特征工程天花板”     │
                                    ▼                                    └──────────────────────────────┘
┌──────────────────────┐        ┌────────────────────────────────┐        ┌──────────────────────────────┐
│ 2. 连接学派          │ ─────► │ 神经网络与分布式表征           │ ─────► │ 2006 DBN 破冰 / 2012 AlexNet │
│ (Connectionism/仿生) │        │ (1986 BP / 1997 LSTM / LeNet)  │        │ 2017 Transformer 统一多模态  │
└──────────────────────┘        └────────────────────────────────┘        └──────────────────────────────┘
```

### 2. 缝合主线的关键时间断层
* **接驳显卡支线**：在 [第 53 篇](file:///Users/hooman/Work/Writing/hoo-wiki/zh/pages/writing/20260226%E3%80%90AI%E3%80%91%E5%B0%8F%E7%99%BD%E8%AF%9D%E7%B3%BB%E5%88%97%E2%80%94%E2%80%94%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD%E7%AE%80%E5%8F%B2%EF%BC%88%E4%BA%8C%E5%8D%81%E4%B8%89%EF%BC%89.md) 中，G80 显卡与 CUDA（2006）问世，宣布“算力已经准备就绪”；
* **填补算法空白**：在 [第 22 篇](file:///Users/hooman/Work/Writing/hoo-wiki/zh/pages/writing/20250903%E3%80%90AI%E3%80%91%E5%B0%8F%E7%99%BD%E8%AF%9D%E7%B3%BB%E5%88%97%E2%80%94%E2%80%94%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD%E7%AE%80%E5%8F%B2%EF%BC%88%E4%BA%8C%E5%8D%81%E4%BA%8C%EF%BC%89.md)（LeNet-5）到 [第 23 篇](file:///Users/hooman/Work/Writing/hoo-wiki/zh/pages/writing/20250904%E3%80%90AI%E3%80%91%E5%B0%8F%E7%99%BD%E8%AF%9D%E7%B3%BB%E5%88%97%E2%80%94%E2%80%94%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD%E7%AE%80%E5%8F%B2%EF%BC%88%E4%BA%8C%E5%8D%81%E4%B8%89%EF%BC%89.md)（AlexNet）之间，跳过了整整 14 年。
* **点题 [第 16 篇（深蓝）](file:///Users/hooman/Work/Writing/hoo-wiki/zh/pages/writing/20250802%E3%80%90AI%E3%80%91%E5%B0%8F%E7%99%BD%E8%AF%9D%E7%B3%BB%E5%88%97%E2%80%94%E2%80%94%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD%E7%AE%80%E5%8F%B2%EF%BC%88%E4%BA%8C%E5%8D%81%E4%B8%89%EF%BC%89.md)**：点破 1997 年战胜人类的深蓝其实是**符号派最后的工业烟花**（8000 条手工规则 + VLSI 专用硬件暴力树搜索，完全不具备自学习能力）。

---

## 二、 统计学派的盛世帝国与特征工程天花板（1995–2012）

必须破除一个误区：统计学派绝不是过渡期的陪衬，**从 1995 到 2012 年，统计学派建立了无可撼动的帝国，塑造了整个 Web 2.0 的繁荣底座。**

### 1. 传统计算机视觉（CV）的四大丰碑
1. **1999 年 SIFT 特征（David Lowe）**：尺度不变特征变换。将像素旋转、缩放、光照变化归一化，奠定了全景拼接、3D 视觉重建与早期机器人建图的基石。
2. **2001 年 Viola-Jones 人脸检测（CVPR 2001）**：
   * **核心发明**：Haar-like 矩形特征 + **积分图（Integral Image，任意面积求和只需 3 次加减法，常数级 $O(1)$ 复杂度）** + AdaBoost 级联分类器（漏斗过滤 99% 的背景）。
   * **工业痕迹**：在奔腾 III 时代跑出 15 帧/秒。直接集成入 Intel OpenCV，成为**索尼（Cyber-shot 笑脸快门）、佳能、尼康数码相机取景器里那个黄色/绿色人脸对焦框的绝对技术源头**。
3. **2005 年 HOG + SVM（Dalal & Triggs）**：方向梯度直方图 + 支持向量机，把人体轮廓解构为梯度边缘，是安防监控“行人检测”的行业标准。
4. **2008 年 DPM（Deformable Part Models，Felzenszwalb）**：传统 CV 特征工程的最高峰（人体弹簧组件模型），在 PASCAL VOC 竞赛统治数年，直到被 AlexNet 击碎。

### 2. 统治工业界 Web 2.0 的隐形巨浪
* **搜索引擎与排序**：Google PageRank（高维马尔可夫链稳态分布求解，纯概率矩阵代数）。
* **广告点击率预估（CTR）**：Google、百度支撑每年数百亿美元收入的竞价广告核心，常年是**逻辑回归（Logistic Regression）+ 几亿维人工交叉特征工程**。
* **自然语言与翻译**：IBM Models 1-5 统计机器翻译（SMT），Fred Jelinek 名言：“*每当我开除一个语言学家，语音识别系统的表现就会上升一点。*”
* **推荐系统**：2006–2009 年 Netflix 百万美金推荐大赛，冠军团队 BellKor 靠的是 **SVD 矩阵分解与集成模型**。
* **反垃圾邮件**：Paul Graham 2002 年普及的**朴素贝叶斯过滤器**。

### 3. 统计学派为什么在 2012 年撞墙？（特征工程天花板）
* **哲学生产方式缺陷**：统计派把任务分为两段——**人类专家手工设计数学特征提取公式（SIFT/HOG），算法只负责最后一道凸优化分类（SVM）**。
* **撞墙时刻**：面对 ImageNet 上千类现实复杂图片，人类专家的数学想象力被榨干了。调参几年只能提升 0.1%，错误率死死卡在 26% 无法前进。

### 4. 工业分水岭：Viola-Jones 刷脸框 vs 中国“AI 四小龙”（2014–2018）
* **本质概念厘清**：
  * **人脸检测（Detection，Viola-Jones 搞定的）**：判断“图里有没有人脸，脸在哪个框里”，但**完全不知是谁**；
  * **人脸识别（Recognition，AI 四小龙搞定的）**：千万级数据库里秒级比对“这人是张三还是李四”（1:N），或判定“持证人是否为本人”（1:1）。
* **技术归属**：**中国 AI 四小龙（商汤、旷视、依图、云从）是 100% 的深度学习产物！**
  * 2012 年前，传统统计派（PCA 特征脸、LBP 纹理、SVM）识别人脸在真实环境准确率仅 70%~80%，遇到光照、侧脸就瘫痪，无法商用。
  * **历史转折点（2014）**：香港中文大学汤晓鸥实验室发布 **DeepID**（深度卷积神经网络），在 LFW 数据库上刷出 **99.15%** 准确率，**人类历史上首次在视觉识别上超越人眼肉眼精度（97.53%）**，这才直接催生了商汤科技的创立。
  * 随后孙剑、何恺明（ResNet 残差网络发明人）加入旷视，中国安防、刷脸支付与智慧城市全面由深度学习接管。

---

## 三、 贝尔实验室决战与“机器学习”夺舍求生记

### 1. 贝尔实验室的双雄决战：Vladimir Vapnik vs Yann LeCun (1995)
* **物理舞台**：新泽西州 Holmdel 贝尔实验室自适应系统研究部（主管 Larry Jackel）。
* **人物反差**：
  * **Vladimir Vapnik**：苏联流亡数学宗师，统计学习理论奠基人。带着苏联学派极端的纯粹数学理性与傲慢，坚信“没有严谨数学证明的算法全是杂耍”。
  * **Yann LeCun**：法国青年工程师，Hinton 门生。信奉仿生学直觉与端到端反向传播，坚信“物理现实有用优先于严密证明”。
* **历史名场面**：
  * **1995 红酒赌局**：Vapnik 扬言打赌：“*到 2000 年，没有任何人会再用你们这种多层神经网络！*”赌注是丰盛大餐与昂贵红酒。
  * **杀人诛心的踢馆**：1995 年 Vapnik 与 Corinna Cortes 正式发表 SVM 软间隔算法。为了证明神经网络的冗余，Vapnik 直接用 SVM 去跑 LeCun 引以为傲的 **MNIST 手写支票数据集**。
  * **降维打击**：没有卷积层、没有深度特征提取，仅靠高斯核（RBF Kernel）加两页凸二次规划求解，SVM 错误率打到 **1.1%**，打平甚至超越了 LeNet-5！
  * **学界的审判**：学界全面倒戈。SVM 拥有唯一的全局最优解（凸优化保证），不存在局部极小，数学优美；神经网络动辄梯度消失、局部最优，被嘲讽为“没有理论支撑的中世纪炼金黑盒”。

### 2. “改名求生”记：统计学家如何“夺舍”机器学习？
* **AI 沦为诈骗犯代名词**：80 年代末 90 年代初，专家系统崩塌、日本五代机失败，DARPA 与 NSF 怒撤资金。“Artificial Intelligence”与“Neural Network”成了学术界的脏词（Dirty Words），标书写上这几个字直接被枪毙。
* **借尸还魂与自立门户**：
  * “Machine Learning”（机器学习）一词本是 Arthur Samuel 1959 年下跳棋时提出的冷门小词。
  * 90 年代初，统计学家们（Vapnik、Michael I. Jordan 等）急于与过去吹牛的符号派 AI 彻底切割，从废墟中捡起这个词并**反向夺舍**：“*我们不是搞不切实际‘智能’的 AI，我们搞的是严谨的‘统计学习与机器学习’！*”
* **连接派的流亡潜伏**：
  * 2001 年 AT&T 拆分衰落，贝尔实验室研究组解散，LeCun 流亡到纽约大学（NYU），长达数年申请不到硬件经费，论文被 CVPR 屡屡冷嘲热讽；
  * 搞神经网络的学者为了活命养活学生，不得不全面抹掉“神经网络”字样，把论文包装成“非线性流形学习”、“统计模式识别”、“贝叶斯图模型”去投稿骗经费。

---

## 四、 欧陆孤狼与北境联盟：暗夜里的学术恩怨与失落先驱

### 1. 共同的噩梦：梯度消失（Vanishing Gradient Problem）
* 1991 年，Jürgen Schmidhuber 的硕士生 **Sepp Hochreiter** 论文从数学上严格论证：反向传播跨越层数/时间步连乘权重矩阵，梯度呈指数级衰减为零，导致深度模型根本训不动。
* 1994 年，Bengio 也发表独立论文证实循环网络的梯度消失难题。

### 2. 1997 LSTM：征服时间的神经网络神作
* **发明者**：Sepp Hochreiter & Jürgen Schmidhuber（德国慕尼黑工大）。
* **技术创新**：
  * 放弃连乘，修建一条**线性加法的“记忆传送带”（Cell State，加法导数为 1，梯度永不衰减）**；
  * 设计**三大智能门控阀门**（遗忘门、输入门、输出门），用 Sigmoid 动态控制信息的擦除、写入与调取。
* **历史功勋**：统治时序与文本 20 年，成为 2014–2016 年 Siri、各大输入法、Google 翻译（GNMT，8 层 LSTM 堆叠）的底层引擎。

### 3. 2004 加拿大 CIFAR 联盟 vs 欧陆孤狼的世纪公案
* **北境守夜人联盟**：
  * 2004 年，加拿大高等研究院（CIFAR）总裁 **Chaviva Hošek** 顶住主流压力设立 **NCAP 计划**，给流亡的 Hinton、LeCun、Bengio 每年提供稳定的自由研讨资助。
  * 三人带着学生（Alex Krizhevsky、Salakhutdinov 等）在温哥华、多伦多或滑雪胜地秘密集会，研究受限玻尔兹曼机（RBM）与深度信念网络（DBN）。
  * 2006 年 Hinton 在《Science》发表封面论文，正式为这项技术定名为**“深度学习（Deep Learning）”**，摆脱旧污名。
* **欧陆孤狼 Schmidhuber 的愤怒与 2018 图灵奖公案**：
  * 身处瑞士卢加诺（IDSIA）的 Schmidhuber 完全被排挤在 CIFAR 圈子之外。
  * 2018 年图灵奖颁给 Hinton、LeCun、Bengio 三人时，Schmidhuber 怒发长文抗议，怒斥“加拿大黑手党”掠夺欧洲学术遗产：指出全球大厂翻译用的 **LSTM（1997）** 和早于 AlexNet 一年用 GPU 夺冠的 **DanNet（2011）** 全出自他的实验室。
* **贯通两界的摆渡人：Alex Graves**
  * 他是 Schmidhuber 的爱徒（将 LSTM 与 CTC 结合做语音），博士毕业后去多伦多大学做 **Hinton 的博士后**；
  * 后来 Graves 加入 DeepMind，成为亲手将 LSTM 带入 Google 核心业务的传奇摆渡人。

### 4. DanNet 悲歌：为什么更早拿第一的 GPU-CNN 没能引爆时代？
Dan Cireșan 和 Schmidhuber 在 2011 年就用 CUDA 跑通了 CNN，在德国交通标志识别（IJCNN 2011）上刷出 99.46% 甚至超越人类肉眼。**为什么历史记住了 2012 年的 AlexNet，却遗忘了 2011 年的 DanNet？**（卡洛测试深度剖析）：
1. **战场格局差异（地方擂台 vs 罗马斗兽场）**：
   * DanNet 打的是 MNIST、交通路标等“干净玩具数据集”，传统 CV 主流视其为小打小闹；
   * AlexNet 直捣 **ImageNet（ILSVRC 2012）**——涵盖 120 万张高难度真实图片的大杂烩中央战场，把传统统计特征大师们打得落花流水（甩开第二名 10.8 个百分点），主流学界无法再装聋作哑。
2. **技术范式代差（技巧堆叠 vs 现代深度学习三大基石）**：
   * DanNet 靠老激活函数和 7~10 个网络强行取平均（Multi-Column Bagging），算力浪费且缺乏新理论；
   * AlexNet 确立了**现代积木标准**：**ReLU** 根治梯度消失，**Dropout** 解决过拟合，模型简洁优雅。
3. **极客开源精神（军火扩散）**：
   * Alex Krizhevsky 手写汇编级优化的 **`cuda-convnet` 代码完全开源**，全世界研究生用 500 美元的游戏卡（GTX 580）即可在宿舍复现并改写，掀起全球革命。
4. **资本与话语权中心（硅谷超级扩音器）**：
   * Schmidhuber 偏居瑞士小城，孤僻傲慢；
   * Hinton 团队处于北美学术政治中枢，夺冠后成立 3 人公司引发 **Google、微软、百度 4400 万美元秘密竞拍**，被 Google 收入囊中，获得了科技巨头最顶级的全球公关与工程机器加持。

---

## 五、 哲学深水区：符号的本质、Transformer 的抛弃与脑科学终局

### 1. 符号派的“符号” vs LSTM/深度学习的“符号”
* **符号派的符号（思维的积木）**：离散、原子、显式。机器靠布尔逻辑和 IF-THEN 规则拼装，脆弱无感知地基；
* **LSTM / 深度学习的符号（外在的皮囊）**：在进门时就被 **Embedding（词嵌入）彻底粉碎成了连续的浮点数向量**（512 维几何坐标）。
  * 深度学习内部运算只有**线性代数、微积分与概率激活**；
  * “语义”变成了高维流形里的几何空间距离；直到最后一刻通过 Softmax 才重新把向量“凝固重构”为人类看得懂的汉字或英文单词。

### 2. Transformer 到底扔掉了什么？
* **它没有扔掉符号**：输入输出依然是 Token 符号，内部依然是连续高维向量；
* **它扔掉的是时间的锁链（Recurrence）**：
  * LSTM 强求按时序单线程逐字排队推进，锁死了硬件并行；
  * Transformer 依靠**自注意力机制（Self-Attention）**，把一千个词同时拍在桌面上，让全词全向同时关注，一举释放了数万个 GPU 流处理器并发的吞吐暴力。

### 3. 脑科学视角：人类真正的“符号能力”更接近谁？
**人类大脑是神奇的“双层嵌套结构”：**
1. **底层物理硬件（100% 连接派/LSTM）**：
   * 大脑神经元之间传递的是毫伏级动作电位、离子浓度与神经递质，记忆是全皮层分布式表征（Distributed Representation），纯粹是连续混沌的流体；
2. **顶层认知功能（涌现出了古典符号派的虚拟机）**：
   * 人类前额叶皮层（PFC）演化出了**“离散组合性”与“变量绑定”**能力；
   * 人类能把大自然连续的彩虹切分成“七色”，能发明代数 $E=mc^2$，能做非黑即白的因果推演与反事实假想。
   * **卡尼曼双系统映射**：
     * **System 1（快思考 / 连续直觉 / 感知匹配）** $\approx$ **连接派（LSTM / Transformer 连续流）**；
     * **System 2（慢思考 / 离散逻辑 / 严格推演）** $\approx$ **古典符号学派（离散符号虚拟机）**。

### 4. 终局预测（2025–2026+ 推理模型大爆发）
* 为什么纯大模型（GPT-4、Claude）会幻觉撞墙？因为它只有连续直觉（System 1），缺乏严格形式化检验的符号虚拟机；
* **OpenAI o1 / o3 与 DeepSeek R1 的本质**：人类工程师正**在连续的 Transformer 底座上，重新构建离散符号推理与搜索的 System 2 虚拟机**（思维链 MCTS 搜索、编译器验证、符号求解器对齐）。
* **终极历史回响**：
  > **符号派错在试图在流沙上徒手搭积木；连接派错在以为光靠烂泥就能长成参天大厦。真正的 AGI，必然是以连续神经为肥沃土壤，最终在顶层开出严谨确定性的离散符号之花。**

---

## 六、 核心一手论文、专著与官方史料链接库

### 1. 奠基与对决经典学术论文（Primary Literature）

| 论文名称 | 作者与年份 | 核心意义与历史地位 | 权威可访问链接 |
| :--- | :--- | :--- | :--- |
| **《Support-Vector Networks》** | Corinna Cortes, Vladimir Vapnik (1995) | **SVM 封神之作**。软间隔与高斯核，建立凸优化在 ML 界 15 年霸权。 | [Springer 官方全文](https://link.springer.com/article/10.1007/BF00994018) / [PDF 下载](https://link.springer.com/content/pdf/10.1007/BF00994018.pdf) |
| **《Gradient-Based Learning Applied to Document Recognition》** | Yann LeCun 等 (1998) | **LeNet-5 集大成作**。46 页长文，奠定现代 CNN 卷积池化范式与 MNIST 基准。 | [IEEE Xplore](https://ieeexplore.ieee.org/document/726791) / [LeCun 官网 PDF](http://yann.lecun.com/exdb/publis/pdf/lecun-01a.pdf) |
| **《Long Short-Term Memory》** | Sepp Hochreiter, Jürgen Schmidhuber (1997) | **LSTM 诞生之作**。发明常数误差轮与门控阀门，根治 RNN 梯度消失。 | [Neural Computation 官方](https://direct.mit.edu/neco/article/9/8/1735/6109/Long-Short-Term-Memory) / [TU Munich PDF](https://www.bioinf.jku.at/publications/photocopies/neco_97.pdf) |
| **《Rapid Object Detection using a Boosted Cascade of Simple Features》** | Paul Viola, Michael Jones (2001) | **实时人脸检测里程碑**。Haar 特征 + 积分图 $O(1)$ + AdaBoost，数码相机人脸框源头。 | [IEEE 官方链接](https://ieeexplore.ieee.org/document/990517) / [MIT 原版 PDF](https://www.cs.cmu.edu/~efros/courses/LBMV07/Papers/viola-cvpr-01.pdf) |
| **《Reducing the Dimensionality of Data with Neural Networks》** | G. E. Hinton, R. R. Salakhutdinov (2006) | **深度学习破冰之作**。《Science》封面文章，提出 DBN 与无监督逐层预训练，命名“深度学习”。 | [Science 官方页面](https://www.science.org/doi/10.1126/science.1127647) / [多伦多大学 PDF](https://www.cs.toronto.edu/~hinton/science.pdf) |
| **《Deep Neural Networks Segment Neuronal Membranes in Electron Microscopy Images》** | Dan Cireșan, Jürgen Schmidhuber 等 (2012) | **DanNet 代表作**。早于 AlexNet 用纯 GPU-CNN 拿下生物医学与路标竞赛全球第一。 | [NeurIPS 官方页面](https://proceedings.neurips.cc/paper/2012/hash/459a4ddcb586f24e419b1a04b0937ba8-Abstract.html) / [PDF 下载](https://proceedings.neurips.cc/paper/2012/file/459a4ddcb586f24e419b1a04b0937ba8-Paper.pdf) |
| **《Deep Learning Face Representation from Predicting 10,000 Classes》** | 汤晓鸥、王晓刚团队 (DeepID, 2014) | **中国 AI 爆发点**。LFW 刷出 99.15% 历史上首次超越人眼，催生商汤科技与人脸商业化。 | [CVPR 2014 页面](https://openaccess.thecvf.com/content_cvpr_2014/html/Sun_Deep_Learning_Face_2014_CVPR_paper.html) / [PDF 下载](https://openaccess.thecvf.com/content_cvpr_2014/papers/Sun_Deep_Learning_Face_2014_CVPR_paper.pdf) |

---

### 2. 纪实原著与自传文献（Biographies & Books）

| 书籍名称 | 作者 | 推荐查阅章节与细节 | 权威访问链接 |
| :--- | :--- | :--- | :--- |
| **《深度学习革命》（*Genius Makers*）** | Cade Metz（纽约时报记者） | **第 1–3 章**：全景还原 Hinton 避难多伦多、贝尔实验室傲慢、CIFAR 设立秘密会议细节。 | [Penguin 出版社](https://www.penguinrandomhouse.com/books/609033/genius-makers-by-cade-metz/) / [豆瓣读书](https://book.douban.com/subject/35882650/) |
| **《科学之路：人、机器与未来》** | Yann LeCun（图灵奖得主自传） | **第 3–4 章**：亲笔自述与 Vapnik 赌局、AT&T 崩盘、转投 NYU 招不到学生的辛酸。 | [Odile Jacob 原版](https://www.odilejacob.fr/catalogue/sciences/informatique/quand-la-machine-apprend_9782738149312.php) / [豆瓣读书](https://book.douban.com/subject/35458022/) |
| **《统计学习理论的本质》** | Vladimir Vapnik (1995) | 统计学习圣经。系统阐述对经验主义黑盒（神经网络）的哲学宣判。 | [Springer 链接](https://link.springer.com/book/10.1007/978-1-4757-3264-1) |

---

### 3. 一手官方历史与口述史档案（Archives）

* **CIFAR 官方深度回顾**：[《How a Canadian Foundation Seeded the Deep Learning Revolution》](https://cifar.ca/cifarnews/2017/10/24/how-a-canadian-foundation-seeded-the-deep-learning-revolution/)（2004 NCAP 启动口述史）。
* **CIFAR LMB 研究项目主页**：[CIFAR Learning in Machines & Brains Program](https://cifar.ca/research-programs/learning-in-machines-brains/)。
* **Yann LeCun 贝尔实验室时代归档**：[The Bell Labs Machine Learning Era (1988–2002)](http://yann.lecun.com/exdb/bell-labs/)（实录老照片与 LeNet 系统视频）。
* **Schmidhuber 个人学术抗辩长文**：[《Critique of 2018 Turing Award for Deep Learning》](https://people.idsia.ch/~juergen/deep-learning-miracle-turing-award.html)（还原 LSTM 与 DanNet 优先权的历史檄文）。
