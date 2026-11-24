# GitHub同步

## 用户指定的仓库提交身份

```text
GitHub账号：troyeagle
Git提交姓名：troyeagle
提交邮箱：troyeagle@qq.com
```

以上为用户指定的仓库提交身份。邮箱是否已在 GitHub 验证，以用户账户设置为准；公开文档不记录账户设置页的个人资料。

仅在本仓库设置 `user.name=troyeagle` 与 `user.email=troyeagle@qq.com`；保留全局配置及其他工程的设置。

## 本地仓库

- 默认分支：`main`。
- 完成首次本地提交，包含实现、文字内容、工程文档及验证证据。
- 沿用已有GitHub工程的SSH连接方式。
- `origin` 的目标地址：`git@github.com:troyeagle/ai-video-reverse.git`。

具体提交哈希和工作树状态可以用以下命令查看：

```bash
git status --short
git log -1 --format=fuller
git remote -v
git var GIT_AUTHOR_IDENT
git var GIT_COMMITTER_IDENT
```

## 远端核验与同步

2026-11-24按用户给出的SSH地址执行 `git ls-remote`，命令成功返回且没有任何refs。核验时远端仓库已存在、可访问，并为空仓库，因此无需重新创建。

先前“GitHub仓库尚未创建”的表述没有经过远端核验，应区分“本次操作没有创建仓库”和“远端仓库不存在”。远端状态以实际命令结果为准。

从工程根目录同步主分支：

```bash
git push -u origin main
```

推送后核对远端 `refs/heads/main` 与本地 `HEAD` 是否相同：

```bash
git rev-parse HEAD
git ls-remote origin refs/heads/main
git status -sb
```

本地同步结果记录在 `.local/git-state.json`；该文件不进入Git。

## Git追踪范围

代码、文章、校订转写、页级讲稿、工程文档及验证图片进入Git。媒体、ZIP、模型与虚拟环境保留在案例目录并被忽略；GitHub克隆后可直接查看及重建网页内容，播放原声需要本地音频。

原始 `playurl.json`、`player.json`、浏览器标签标识及已确认不相关的字幕返回也仅作本地记录，不进入Git。

## HTML 产物自动发布

`main` 的源码发布工作流调用博客的固定版本共享构建器，验证并上传登记案例的 HTML 产物；博客收集后更新 `/ai-video-reverse/`，触发 Pages。即时通知和定时收集的区别、凭据权限、稳定 URL 与恢复步骤见 [HTML 自动发布规约](../.github/STATIC_PUBLISH.md)。
