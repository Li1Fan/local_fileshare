# local_fileshare
局域网的文件共享站



## 介绍
- 本项目是一个局域网内文件共享的工具，可以在局域网内的多台电脑之间互传文件。

  

## 使用

**安装依赖：**
```bash
pip install flask
```

**启动服务：**
```bash
python run.py
```

可在 `run.py` 末尾修改端口号，默认为 `9999`。

**浏览器访问：**`http://<本机IP>:9999`

选择文件（支持多选或拖拽），点击上传，局域网内其他设备访问同一地址即可查看并下载。

**可选：配置在线剪贴板入口**

若需在导航栏显示跳转至[共享剪贴板](https://github.com/Li1Fan/local_clipboard)的链接，通过环境变量设置地址：

```bash
# Linux / macOS
CLIPBOARD_URL=http://192.168.x.x:8888 python run.py

# Windows
set CLIPBOARD_URL=http://192.168.x.x:8888
python run.py
```

不设置该变量时，导航栏中的剪贴板入口会自动隐藏。

## 命令行上传（API）

服务端提供 `POST /api/upload` 接口，返回 JSON，可在 Linux / macOS 上通过 `curl` 直接推送文件：

```bash
# 上传单个文件
curl -F "file=@/path/to/file.txt" http://<本机IP>:9999/api/upload

# 同时上传多个文件
curl -F "file=@a.txt" -F "file=@b.zip" http://<本机IP>:9999/api/upload
```

成功响应：
```json
{"ok": true, "saved": ["file.txt"]}
```

**封装为 shell 函数（加入 `~/.bashrc` 或 `~/.zshrc`）：**

```bash
push() {
    curl -sS $(printf ' -F "file=@%s"' "$@") http://<本机IP>:9999/api/upload
    echo
}
```

之后即可直接使用：
```bash
push report.pdf data.csv
```



界面如下：

![page](page.png)