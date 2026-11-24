# HTML 自动发布规约

## 发布位置与产物

- 博客接收仓库：[`troyeagle/troyeagle.github.io`](https://github.com/troyeagle/troyeagle.github.io)。
- 源码发布分支：`main`；线上入口：[视频演示目录](https://troyeagle.github.io/ai-video-reverse/)。
- 当前案例：[BV1MssN6ZE1v](https://troyeagle.github.io/ai-video-reverse/BV1MssN6ZE1v/)。案例 ID 是稳定的 URL，不随标题改变。
- `.github/static-pages.json` 明确列出可公开的案例。新增案例先按 `cases/<ID>/interactive-slides/` 维护源码和数据，再登记到该文件。
- `scripts/build_static_pages.py` 调用原有重建与校验脚本，导出 `dist/index.html` 和每个登记案例的 `<ID>/index.html`；页面内嵌文字、CSS、SVG、JavaScript 和讲稿数据。
- 媒体、模型、ASR 输出、文章原稿、模板、参考帧与验证截图不进入发布包。线上没有原声音频，按钮说明“原声仅本地提供”；自由翻页和自动演示可用，原视频链接可收听讲解。本地重建版本继续使用旁边的 `narration.m4a`。

## 本地检查

在工程根目录运行，Python 标准库即可：

```sh
python3 -m unittest discover -s tests -v
python3 scripts/build_static_pages.py
python3 -m http.server 8768 --directory dist
```

打开 <http://localhost:8768/>。页面和讲稿变更还须按 [AGENTS.md](../AGENTS.md) 做实际浏览器及图像检查；CI 会核对完整的 32 页、81 条讲稿和源文本一致性。

## 发布流程

1. 将源码、数据、案例登记和操作文档一同提交到 `main`。不要只提交 `dist/`，该目录由构建生成并被 Git 忽略。
2. [源码工作流](https://github.com/troyeagle/ai-video-reverse/actions/workflows/publish-static.yml) 在 push、PR 和手动运行时测试、重建；仅 `main` 的 push 或手动运行上传 `site-ai-video-reverse`。PR 不上传正式产物，也不通知博客。
3. 调用的共享工作流和 `publisher_ref` 均固定为博客同一份完整提交 SHA。升级公共发布器时一起改两处并通过测试；前四个已接入项目不必跟随升级。
4. 打包器生成 `_site-sync.json`，包括源码 SHA、运行身份和逐文件哈希；博客核验指定仓库、分支、工作流、成功构建、源历史、路径及所有 HTML 页面中的本地资源引用。
5. 博客收集后直接提交 `/ai-video-reverse/` 产物及发布状态，再触发 Pages 部署；正常产物更新不另建 PR。

## 配置入口

- [本仓库 Actions Secrets](https://github.com/troyeagle/ai-video-reverse/settings/secrets/actions)：可选保存 `BLOG_DISPATCH_TOKEN`，仅授权 **博客仓库 Actions: write**。成功构建会用它立即请求博客同步。可复用其他源码项目的同一个通知 PAT，但个人仓库 Secret 要分别保存。
- 没有通知 Secret 时，博客仍约每 30 分钟自动收集；定时任务可能延迟。要立即手动同步，打开 [博客同步工作流](https://github.com/troyeagle/troyeagle.github.io/actions/workflows/sync-apps.yml)，选择 `master`，取消 `dry_run`，保持 `include_disabled` 不勾选。
- [博客白名单](https://github.com/troyeagle/troyeagle.github.io/blob/master/.github/apps.json)：`ai-video-reverse.enabled` 控制单项目启停。
- [博客变量](https://github.com/troyeagle/troyeagle.github.io/settings/variables/actions)：`SITE_SYNC_ENABLED` 和 `SITE_SYNC_PUBLISH_ENABLED` 均为 `true` 才能正式同步。
- [博客 Secrets](https://github.com/troyeagle/troyeagle.github.io/settings/secrets/actions)：读取 PAT `SOURCE_ARTIFACTS_TOKEN` 对本仓库需 Contents: read、Actions: read；`BLOG_PUBLISH_TOKEN` 只保存在博客，不分发到源码项目。
- [已发布版本](https://github.com/troyeagle/troyeagle.github.io/blob/master/.github/apps-state.json)：核对本项目的 `sha`、`runId` 和 `runNumber`。

## 接入、暂停与恢复

新接入先保持白名单 `enabled: false`，源码构建成功后在博客勾选 `dry_run` 和 `include_disabled` 做预览；预览成功再启用并真实同步。日常发布无需重复此步骤。

回退前先暂停本项目同步，避免最新产物覆盖回退。优先在源码用新提交恢复内容，再重新构建；不要重写分支历史。产物保留 14 天，过期后可在源码 `main` 手动生成新构建。Token 过期应续期或覆盖对应 Secret，不将值写入代码、日志或文档。
