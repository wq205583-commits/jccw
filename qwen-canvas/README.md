# Qwen Canvas v0.5

Windows + RTX 4080 16GB 的本地优先 Qwen-Image-2.1 无限画布。

## 第一次运行
安装 NVIDIA 驱动、Python 3.11 x64、Node.js 20+、Git。进入 qwen-canvas 后依次双击 `check.bat`、`install.bat`、`start.bat`。浏览器自动打开 http://127.0.0.1:7860 。首次生成会下载模型。

## GPT / Gemini（可选）
复制 `.env.example` 为 `.env`，只在自己的电脑填写 API Key。当前 GPT/Gemini 是 Prompt 导演，默认不上传画布图片。

## 已实现
- 无限画布、图片导入、Shift 多选
- Qwen 文生图 / 单图 / 最多10图参考编辑
- 框选局部编辑工具：在画布拖出区域，再输入删除人物、换衣服、改背景等指令
- 扩图模式：将“保持原图、自然延展边界”约束交给 Qwen 编辑
- 透明 RGBA
- GPT / Gemini Prompt 导演
- 1K / 2K、比例、Steps、Seed
- 工程 JSON 保存
- Windows 环境自检
- RTX 4080 16GB BF16 + model CPU offload

## 注意
当前框选是“区域引导编辑”：Qwen-Image-2.1 官方支持圈选、涂画或独立 mask 的局部编辑，但 v0.5 先使用区域坐标+编辑指令。下一版会加入真正的 Mask 图层导出和工程图片恢复。
