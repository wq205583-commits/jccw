# Qwen Canvas v0.2

Windows 本地无限画布 + Qwen-Image-2.1。目标硬件：RTX 4080 16GB。

## 安装
安装 NVIDIA 驱动、Python 3.11 x64、Node.js 20+，然后双击 `install.bat`，安装完成后双击 `start.bat`。首次生成会下载模型。

## 已实现
- 无限画布、拖动和滚轮缩放
- 本地图片导入和多选（Shift 点击）
- 文生图
- 单图/多参考图编辑，最多发送 10 张
- 原生透明 RGBA Prompt 模式
- 比例、Steps、Seed 控制
- AI 结果自动回填画布
- RTX 4080 16GB：BF16 + model CPU offload

## 操作
导入图片后，点击选择一张；按住 Shift 可追加选择。切换“图片编辑”，输入“删除人物，只保留背景”等指令后生成。多参考图可以选择人物、服装、背景等多张素材后一起编辑。

## 下一阶段
Mask/圈选局部编辑、真正的拖拽扩图、工程 JSON 保存/恢复、历史分支、2K 高质量档位、Prompt Rewrite。
