# 肉与便之恋

- [在线游玩](https://seanxhr137.github.io/after-class-demo/)
- [剧情编辑教程](docs/剧情编辑教程.md)
- [下载 PDF 教程](docs/剧情编辑教程.pdf)
- [直接编辑剧情](https://github.com/seanxhr137/after-class-demo/edit/main/story.json)

## 给剧情协作者

日常只需要修改 **story.json**。没有被所有者邀请的人不能直接改主分支；仓库公开不等于人人可写。
所有者稍后提供 GitHub 用户名并邀请，受邀者接受后可以在网页中直接编辑、提交到 main。
每次提交自动检查并构建。绿色成功后更新同一个网址；检查失败时线上保留上次成功版本。
人物图片和配音等素材由所有者后续提供，当前不要改 actors 里的 image: null。

## 给所有者

仓库 Settings > Collaborators > Add people，输入你允许的 GitHub 用户名，再发送邀请。
个人仓库协作者写入权限覆盖整个仓库，不会只限于 story.json；只邀请你信任的人，不授予管理员权限。
协作者名单尚未提供，目前仅 seanxhr137 有写权限。名单补充后可继续邀请。

## 文件说明

| 文件 | 用途 |
| --- | --- |
| story.json | 唯一剧情编辑源：角色、台词、场景和选项 |
| docs/剧情编辑教程.md 与 PDF | 面向协作者的中文步骤 |
| assets/ | 已有背景和后续正式素材 |
| app.js、style.css、index.html | 游戏运行与界面源，剧情协作者一般不改 |
| tools/check_story.py | 检查内容与素材引用 |
| build.py | 生成发布用文件，默认输出 .pages-dist |
| .github/workflows/publish.yml | 自动检查与 GitHub Pages 发布 |

本地开发：先 `python3 build.py`，再 `python3 -m http.server 8780 --directory .pages-dist --bind 127.0.0.1`。
检查：`python3 -m unittest discover -s tests -p 'test_*.py'`。
index.html 是带资源占位符的入口模板；请预览构建后的 .pages-dist，不直接双击源码入口。
运行文件由构建生成，协作者不需要维护重复的 story.js 或 vn-story 文件。
只发布到 GitHub Pages；旧 chatgpt.site 已停止公开访问，不再使用。

人物当前使用姓名占位牌，正式素材由用户提供。临时剧情和历史背景的来源见 ATTRIBUTION.md。
