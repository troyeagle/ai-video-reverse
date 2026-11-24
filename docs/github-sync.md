# GitHub同步准备

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

## 后续同步

在GitHub创建名为 `ai-video-reverse` 的仓库时，保持为空仓库，不额外生成README或初始提交；远端仓库存在后，从工程根目录运行：

```bash
git push -u origin main
```

本轮完成本地仓库与同步目标配置。远端仓库创建和推送尚未执行。

## Git追踪范围

代码、文章、校订转写、页级讲稿、工程文档及验证图片进入Git。媒体、ZIP、模型与虚拟环境保留在案例目录并被忽略；GitHub克隆后可直接查看及重建网页内容，播放原声需要本地音频。

原始 `playurl.json`、`player.json`、浏览器标签标识及已确认不相关的字幕返回也仅作本地记录，不进入Git。
