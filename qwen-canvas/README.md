# Qwen Canvas v0.1

Windows 本地无限画布 + Qwen-Image-2.1，目标硬件：RTX 4080 16GB。

## 安装
1. 安装 NVIDIA 驱动、Python 3.11 x64、Node.js 20+。
2. 双击 `install.bat`。
3. 双击 `start.bat`。
4. 浏览器打开 http://127.0.0.1:7860 。

首次生成会下载 Qwen/Qwen-Image-2.1 模型，耗时取决于网络和磁盘。

## v0.1
- 无限画布：拖动、滚轮缩放
- 本地图片导入
- Qwen-Image-2.1 文生图
- RTX 4080 16GB 默认 BF16 + model CPU offload
- 生成结果自动回填画布

## 下一阶段
单图编辑、多参考图选择、Mask 局部编辑、RGBA/抠图、拖拽扩图、工程保存、历史树和 Prompt Rewrite。
