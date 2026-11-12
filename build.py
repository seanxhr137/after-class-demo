from pathlib import Path
import shutil
r=Path(__file__).resolve().parent
for source,target in [("app.js","vn-app-v04.js"),("story.js","vn-story-v04.js"),("style.css","vn-style-v04.css")]:
    shutil.copy2(r/source,r/target)
print("已同步 v0.4 运行文件。新大版本请升级文件名和入口引用。")
