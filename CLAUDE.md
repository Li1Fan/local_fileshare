# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目简介

`local_fileshare` 是一个局域网文件共享工具，基于 Flask 实现，允许同一局域网内的多台设备互传文件。

## 运行方式

```bash
pip install flask
python run.py
```

默认监听 `0.0.0.0:9999`，可在 `run.py` 末尾修改端口号。

## 架构说明

项目极为精简，核心只有两个文件：

- **`run.py`**：Flask 应用入口，包含全部路由逻辑：
  - `GET /` — 列出 `uploads/` 目录下的文件，按 mtime 降序排列，渲染首页
  - `POST /upload` — 接收多文件上传，保存至 `uploads/`
  - `GET /download/<filename>` — 以附件形式下载文件
  - `GET /delete/<filename>` — 删除单个文件
  - `GET /delete_all` — 删除全部文件
  - `file_icon` Jinja2 模板过滤器 — 根据扩展名返回对应 emoji 图标
- **`templates/index.html`**：唯一的 Jinja2 模板，包含内联 CSS 与 JS，实现拖拽上传、按日期分组展示、文件图标、删除确认等交互。
- **`uploads/`**：文件存储目录，启动时自动创建（若不存在）。

## 配置项

均在 `run.py` 的 `app.config` 中设置：

| 配置键 | 来源 | 说明 |
|---|---|---|
| `UPLOAD_FOLDER` | 硬编码 `./uploads/` | 文件存储路径 |
| `CLIPBOARD_URL` | 环境变量 `CLIPBOARD_URL`，默认空字符串 | 导航栏剪贴板跳转地址，为空时自动隐藏入口 |

## 注意事项

- 以 `debug=True` 模式运行，仅适用于局域网内部，不可暴露至公网。
- 无身份验证、无文件类型校验、无上传大小限制。
- 开发环境使用 Python 3.8。