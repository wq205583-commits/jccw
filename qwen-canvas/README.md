# Qwen Canvas v0.3

本地优先的 Qwen-Image-2.1 无限画布。目标硬件：Windows + RTX 4080 16GB。

## 本地运行
1. 安装最新 NVIDIA 驱动、Python 3.11 x64、Node.js 20+、Git。
2. 下载/克隆本仓库，进入 `qwen-canvas`。
3. 双击 `install.bat`。它会创建虚拟环境并安装 Qwen/Diffusers、OpenAI、Gemini SDK 和前端依赖。
4. 双击 `start.bat`，浏览器打开 http://127.0.0.1:7860 。
5. 第一次本地生成会下载 `Qwen/Qwen-Image-2.1`，需要较大的磁盘空间和下载时间。

## GPT / Gemini（可选）
复制 `.env.example` 为 `.env`，只在你自己的电脑填写：

    OPENAI_API_KEY=你的key
    OPENAI_MODEL=gpt-5.6-luna
    GEMINI_API_KEY=你的key
    GEMINI_MODEL=gemini-3.8-flash

不要把真实 Key 提交到 GitHub。

当前 GPT/Gemini 用作 Prompt 导演：把简单中文要求优化成更明确的图片生成/编辑提示词；图片生成仍由本机 Qwen 完成，因此默认不会把画布图片上传到 OpenAI/Gemini。

## 已实现
- 无限画布、拖动、滚轮缩放
- 图片导入；Shift 点击多选
- Qwen 文生图、单图编辑、多参考图编辑（最多10张）
- 原生透明 RGBA Prompt 模式
- 比例、Steps、Seed
- GPT / Gemini Prompt 优化 Provider
- API Key 本机 .env 管理，.gitignore 防止误提交
- RTX 4080 16GB：BF16 + model CPU offload

## 下一阶段
Mask/圈选局部编辑、拖拽扩图、项目保存/恢复、历史分支、2K 高质量档位、错误诊断和安装自检。
