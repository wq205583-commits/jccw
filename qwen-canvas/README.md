# Qwen Canvas v0.4

Windows + RTX 4080 16GB 的本地优先 Qwen-Image-2.1 无限画布。

## 第一次运行
1. 安装 NVIDIA 驱动、Python 3.11 x64、Node.js 20+、Git。
2. 进入 qwen-canvas，先双击 `check.bat` 检查环境。
3. 双击 `install.bat` 安装全部依赖。
4. 双击 `start.bat`，自动打开 http://127.0.0.1:7860 。
5. 首次生成会下载 Qwen/Qwen-Image-2.1。

## GPT / Gemini（可选）
复制 `.env.example` 为 `.env`，在自己电脑填写 API Key。真实 Key 不要提交 GitHub。GPT/Gemini 当前作为 Prompt 导演，默认不上传画布图片。

## 已实现
- 无限画布、图片导入、多选参考图
- Qwen 文生图 / 单图编辑 / 最多10图参考编辑
- 透明 RGBA 模式
- GPT / Gemini Prompt 导演
- 1K 预览 / 2K 高质量档位、比例、Steps、Seed
- 工程 JSON 保存后端与画布参数保存
- 环境自检 check.bat
- RTX 4080 16GB BF16 + model CPU offload

## 开发中
Mask/圈选局部编辑、扩图、完整工程图片恢复、历史分支、安装/启动错误自动诊断。
