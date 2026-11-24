# ai-video-reverse

把讲解视频还原为可阅读文章和可交互的网页演示。这个工程保存本次B站视频逆向工作的完整案例、实现源码、验证记录和方法总结。

## 当前案例

**严查税、补社保只是序章：土地财政退潮后，钱从哪里来？**  
作者：Alpha茶水间  
来源：https://www.bilibili.com/video/BV1MssN6ZE1v

- 原视频：约10分25秒，下载版本为480p，H.264/AAC。
- 完整文章：约3800字，基于音频识别并结合画面校订。
- 交互演示：19个主要标题拆成32页，右侧对应81条讲稿记录。
- 图形实现：HTML文字、CSS布局及SVG图标、柱状图、资金流向；演示页面的元素可独立编辑。
- 交互：自由选页、目录搜索、键盘翻页、逐步展开、动画重播、自动演示、原声跟随及讲稿复制。

**[打开交互Slides](cases/BV1MssN6ZE1v/interactive-slides/index.html)**  
**[阅读完整文章](cases/BV1MssN6ZE1v/严查税、补社保只是序章：土地财政退潮后，钱从哪里来？.md)**  
**[逐页讲稿对照](cases/BV1MssN6ZE1v/interactive-slides/页面与讲稿对照.md)**

在本地直接用浏览器打开HTML即可使用。原声文件与网页放在同一目录。Git只追踪代码、文字内容、文档和验证图像；视频、音频、ZIP、模型及运行缓存保留在本地案例目录。

[线上演示目录](https://troyeagle.github.io/ai-video-reverse/)通过博客的静态产物流程发布；[当前案例](https://troyeagle.github.io/ai-video-reverse/BV1MssN6ZE1v/)保留完整演示及讲稿，原声仅在本地提供。重建、案例登记和通知配置见 [HTML 自动发布规约](.github/STATIC_PUBLISH.md)。

## 工程结构

```text
ai-video-reverse/
├── README.md
├── AGENTS.md
├── .gitignore
├── requirements-asr.txt
├── scripts/
│   ├── build_slides.py           # 从已打包源码重建案例网页
│   └── validate_case.py          # 核验页数、讲稿分配及HTML数据一致性
├── docs/
│   ├── user-instructions.md     # 用户原始指示与执行范围
│   ├── workflow.md              # 实际工作流程与复现步骤
│   ├── lessons-learned.md       # 本次错误、修正与经验
│   ├── validation.md            # 已完成的验证与证据位置
│   ├── github-sync.md           # GitHub身份及同步准备
│   └── migration.md             # 原目录迁移记录
└── cases/BV1MssN6ZE1v/
    ├── interactive-slides/      # 网页、数据、讲稿和可编辑源文件
    ├── slides-work/             # 页面构建脚本、逐字对齐和浏览器验证
    ├── 核对画面/                 # 从原视频提取的参考帧
    ├── 重点校订画面/              # 专有名词和数字的校订参考帧
    ├── 校订转写.json
    ├── 校订字幕.srt
    ├── 语音识别.json             # 未清洗的原始识别输出
    ├── transcribe.py
    ├── ocr_frames.swift
    ├── 原视频.mp4                # 本地保留，Git忽略
    └── .model-cache/等           # 本地保留，Git忽略
```

## 重建与验证

只重建网页时无需安装第三方Python库：

```bash
python3 scripts/build_slides.py
python3 scripts/validate_case.py
```

重新识别音频需要macOS Apple Silicon、可用的Metal GPU、Python 3.12和FFmpeg；依赖见 `requirements-asr.txt`，具体步骤见[工作流程](docs/workflow.md)。迁移后的旧虚拟环境包含原路径入口，重新运行ASR前应重新创建环境。

## 工作记录

- [用户原始指示](docs/user-instructions.md)
- [实际工作流程及复现](docs/workflow.md)
- [经验教训](docs/lessons-learned.md)
- [验证记录](docs/validation.md)
- [GitHub同步准备](docs/github-sync.md)
- [迁移记录](docs/migration.md)

内容沿用原视频的观点、数字及预测口径。本次工作完成了转写、画面校订和演示复原；数据的外部事实核查不属于本次任务。
