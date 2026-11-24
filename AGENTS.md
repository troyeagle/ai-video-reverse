# 工程约定

## 用户要求

- 新工作开始前先读 `README.md`、`docs/user-instructions.md` 和对应案例记录。
- 视频转文章时保留原作者观点和引用口径；转写与事实核查须分别标明。
- 复原Slides必须重建文字、图形和交互元素。视频截图仅作为参考或验证证据，不作为演示页面背景替代元素。
- 原视频口播文字放在对应的讲稿表中。每页应有来源时间范围，支持自由选页。
- 图形优先CSS/SVG绘制；如使用公共素材，记录具体来源和许可。
- 用户要求“移动”时完整迁移原工作目录，不自行删除模型、缓存或实验记录。

## Git身份

本项目的提交身份为：

```text
troyeagle <troyeagle@qq.com>
```

账号为 `troyeagle`；提交邮箱按用户指定使用 `troyeagle@qq.com`。所有本项目提交须使用仓库本地身份；邮箱验证状态以用户账户设置为准，不改动全局配置。

提交前核对 `git var GIT_AUTHOR_IDENT` 与 `git var GIT_COMMITTER_IDENT`。模型、虚拟环境、媒体文件、临时签名下载地址和浏览器会话标识由 `.gitignore` 排除。

## 实现和验证

- 案例目录位于 `cases/<视频ID>/`。保留原始识别输出和校订结果，错误字幕单独隔离。
- 网页交付应支持直接以 `file://` 打开；用于渲染的CSS、SVG、JavaScript和讲稿数据内嵌在HTML中。
- `interactive-slides/slides-data.json` 是已交付页面与讲稿的数据源。编辑后使用该目录的 `source/rebuild.py` 重建。
- 脚本用相对路径定位案例，不把开发者本机绝对路径写入发布入口。
- 页面变更后运行 `python3 scripts/validate_case.py`，再按变更范围做浏览器验证。
- HTML 发布按 `.github/STATIC_PUBLISH.md`：仅导出 `.github/static-pages.json` 登记的案例，运行 `python3 -m unittest discover -s tests -v` 和 `python3 scripts/build_static_pages.py`。不发布媒体、参考帧、校订资料或可编辑模板；本地原声与线上无音频模式都要保留。
- 排版检查必须包括实际图像；元素没越界不能证明它们没有互相遮挡。
- Chrome是共享浏览器。按browser-use技能的要求串行使用默认连接，在后台测试；临时开启焦点模拟必须在 `finally` 中关闭。
- 不因截图显示透明、原声尚未加载，就直接判断页面代码失效；先核对标签可见性及动画完成状态。
