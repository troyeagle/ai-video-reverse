# 工作记录迁移

用户要求将本轮工作记录移动到 `projects/ai-video-reverse`。

```text
原案例目录：/Users/{youraccountname}/Downloads/BV1MssN6ZE1v
工程目录：/Users/{youraccountname}/projects/ai-video-reverse
新案例目录：/Users/{youraccountname}/projects/ai-video-reverse/cases/BV1MssN6ZE1v
```

整个案例目录通过同一文件系统内的目录重命名迁移，包含原视频、音频流、文章、原始识别、校订转写、参考画面、交互网页、构建和验证文件、离线包、模型及缓存。

迁移脚本核对案例目录inode，以及视频、文章、HTML、校订转写和ZIP的SHA-256。详细机器记录写入工程本地的 `.local/migration.json`；本轮设置脚本和浏览器标签标识移入 `.local/setup/`。

旧Downloads案例目录不保留副本。网页使用相对音频路径，重建脚本根据自身所在案例目录定位文件；迁移后运行工程级构建与语料验证。浏览器中本任务保留的演示页更新为新目录地址。

迁移保留了原虚拟环境目录，但其中某些入口仍指向旧绝对路径，重新运行ASR前应重新创建环境。模型、环境和媒体的完整本地保留不等于Git追踪；具体忽略规则见 `.gitignore`。
