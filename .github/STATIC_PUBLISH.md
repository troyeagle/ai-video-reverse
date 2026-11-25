# 项目 Pages 与私有源码回退规约

## 默认发布

公开仓库 [`troyeagle/ai-video-reverse`](https://github.com/troyeagle/ai-video-reverse) 独立发布项目 Pages：[线上入口](https://troyeagle.github.io/ai-video-reverse/)。推送 `main` 或手动运行 [publish-static.yml](https://github.com/troyeagle/ai-video-reverse/actions/workflows/publish-static.yml)，即执行检查、构建和部署。PR 只检查和构建，不部署。

Pages 使用官方固定 SHA 的 configure-pages、upload-pages-artifact、deploy-pages，权限分为构建 Contents: read/Pages: read，部署 Pages: write/ID-token: write。默认模式不需要 PAT、博客通知或定时收集，使用 GitHub 自动提供的 GITHUB_TOKEN 和 OIDC。

[Pages 设置](https://github.com/troyeagle/ai-video-reverse/settings/pages) 的 Source 选择 GitHub Actions。构建输出为 `dist/`，不进入源码 Git；所有模式均关闭 source map。页面资产采用项目子路径 `/ai-video-reverse/` 或相对路径。查看本地实现与许可证要求以 README 为准。

## 两个互斥发布模式

[仓库 Variables](https://github.com/troyeagle/ai-video-reverse/settings/variables/actions) 中的 `SITE_PUBLISH_MODE`：

| 值 | 项目 Pages | 博客回退 |
| --- | --- | --- |
| 不设置或 `pages` | 仅公开仓库可构建、部署 | 跳过 |
| `blog` | 跳过 | 构建并上传 `site-ai-video-reverse` |

`.github/workflows/publish-to-blog.yml` 是保留的回退配置，默认 job 条件不成立，不能自动恢复博客发布。其共享工作流与 `publisher_ref` 必须固定到相同的完整 SHA。回退打包器生成 `_site-sync.json` 并验证 source map、路径和内容；元数据不进入网站。

## 未来转为私有仓库时的操作顺序

1. 审核允许公开的构建输出。源码仓库私有不等于网站私有；博客 Pages 仍公开，只发布已批准的静态输出，不能包含密钥、内部资料、原始媒体、模板或 source map。
2. 暂停本仓库独立部署：将 `SITE_PUBLISH_MODE` 设为 `blog`；在 [Pages 设置](https://github.com/troyeagle/ai-video-reverse/settings/pages) 下线项目站，必要时取消其自定义域名。不要让两个发布渠道同时承担相同入口。
3. 在博客保存的 `SOURCE_ARTIFACTS_TOKEN` 中给 `troyeagle/ai-video-reverse` 添加 Contents: read、Actions: read，并按要求把源码仓库改为私有。该读取 Token 只保存在博客。
4. 手动运行 [回退工作流](https://github.com/troyeagle/ai-video-reverse/actions/workflows/publish-to-blog.yml)，选择 `main`，等待构建成功。共享发布器自动使用博客旧路径 `/ai-video-reverse/`，而非默认项目路径。
5. 博客 `.github/apps.json` 中已保留 `ai-video-reverse` 槽位，默认 `enabled: false`。先在博客 [同步工作流](https://github.com/troyeagle/troyeagle.github.io/actions/workflows/sync-apps.yml) 勾选 `dry_run` 与 `include_disabled` 做预览；审核成功后将该槽位设为 `true`，再取消 `dry_run` 正式同步。`/ai-video-reverse/remark.md` 会由审核过的静态产物替换。
6. 验证博客地址 `https://troyeagle.github.io/ai-video-reverse/`、发布状态及正常 Pages 部署。没有通知 Token 时约每 30 分钟收集；若需立即通知，可在源码保存仅授权博客 Actions: write 的 `BLOG_DISPATCH_TOKEN`。不得把博客 Contents-write Token 分发到源码仓库。

项目路径与回退路径可能不同，调用者应按当时启用的发布模式更新入口链接。目录迁移说明位于博客 `ai-video-reverse/remark.md`。

## 返回公开项目站

先暂停博客槽位并验证其停止写入，再把源码改回公开、把模式设为 `pages` 或删除该变量、启用本仓库 Pages 的 GitHub Actions 来源，手动部署并检查项目路径。验证后恢复博客迁移说明。保留回退 workflow 和本规约，不清空历史配置。

## 本地检查与提交

```sh
python3 -m unittest discover -s tests -v
python3 scripts/build_static_pages.py
```

AI agent 的提交只使用 `Co-authored-by: Bot <bot@anonymous.com>` 一条匿名尾注，推送前读取实际提交信息核对；主作者仍使用用户指定的仓库身份。发布身份、构建记录与回退说明随代码提交，不写入任何 Token 值。

## 已授权原声

2026-11-25用户确认获授权并要求以M4A发布。`.github/static-pages.json`的`audio`字段只登记当前三个案例，包含精确的`public-audio/<ID>.m4a`路径、字节数、SHA-256和用户授权确认记录。构建校验案例登记、授权状态、普通文件路径、容器标识、大小与哈希，任何缺失或不匹配都会失败，不静默发布其他媒体。

公开页面使用同目录的`narration-<SHA前12位>.m4a`，新文件名避免更新后引用旧缓存；`preload="metadata"`且没有自动播放，访问者点击后收听。M4A支持按时间定位，保留原声跟随和讲稿高亮。音频不内嵌Base64。前两例64kbps单声道，求是案例不二次有损转码；总量18,954,648字节，约18.95MB。完整来源和确认说明见`public-audio/README.md`。

本地案例HTML仍引用旁边的原始`narration.m4a`。没有`audio`登记的案例按无音频模式导出；也可明确运行：

```sh
python3 scripts/build_static_pages.py --without-audio --output .local/silent-site
```

此回退只导出登记的HTML，不包含任何音频。未来使用博客回退时，应先核验共享发布器是否允许登记的M4A；若仍采用HTML-only审核，使用无音频产物。当前独立项目Pages不新增Token、后台服务或对象存储账户。


## 新增审计案例

- [LFCRI分省解读](https://troyeagle.github.io/ai-video-reverse/BV11ts56mEVt/)：59个画面阶段，原讲稿、审计、来源及条件性校核。非公开底稿未提供，不能认证原始指数；非公开参考截图不进Git或发布包。
- [求是三文解读](https://troyeagle.github.io/ai-video-reverse/BV1JXxB6rErv/)：30个画面阶段，三篇官方原文的转述与作者演绎分列。

原32页/81条讲稿案例继续保持兼容。新案例源码位于`scripts/audit-deck/`与各案例`interactive-slides/source/`，注册后只导出HTML。完整Markdown审计报告与验证记录留在案例目录，公开网页内可查看全片审计，不导出原文快照、媒体或参考帧。

## Git 提交身份

人类作者和提交者统一为 `troyeagle <troyeagle@qq.com>`，AI 协作者为 `Bot <bot@anonymous.com>`；按根目录 `AGENTS.md` 配置本仓库本地身份。历史改写后，共享 workflow 与 publisher_ref 必须使用博客新历史中的同一固定 SHA，并重新构建验证。
