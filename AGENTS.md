# 游戏项目工作规则

本目录是《肉と便の恋》的唯一开发源码。

每次完成用户要求的本地修改后：
1. 获取 origin/main，保留未完成改动，整合远端更新。
2. 运行 `python3 -m unittest discover -s tests -p 'test_*.py'` 和 `python3 build.py`。
3. 检查清单，仅提交本次已完成且适合公开的文件，推送 main。
4. 确认本次 GitHub Actions 发布成功并验证公开网址；失败时修复或明确报告阻碍。

仓库：https://github.com/seanxhr137/after-class-demo
游戏：https://seanxhr137.github.io/after-class-demo/
剧情唯一来源为 story.json，人物素材由用户后续提供。
清理时保留当前源码、素材、教程和原稿；对独有内容先核对用途。
