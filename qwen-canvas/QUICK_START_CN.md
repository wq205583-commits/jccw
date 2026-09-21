# Qwen Canvas Windows 首次运行

## 最短流程
1. 安装 Python 3.11 x64、Node.js 20+、Git、最新 NVIDIA 驱动。
2. 双击 check.bat；CUDA 应显示 True，并看到 NVIDIA GeForce RTX 4080。
3. 双击 install.bat，等待依赖安装完成。
4. 双击 start.bat，浏览器自动打开本地画布。
5. 输入提示词，先选择 1K，点击开始生成。首次生成会下载 Qwen-Image-2.1，时间取决于网络和磁盘。

## GPT / Gemini
它们不是启动 Qwen Canvas 的必要条件。需要时复制 .env.example 为 .env，再填写自己的 API Key。

## 第一次测试建议
先不要开 2K，不要加入多张参考图。确认 1K 文生图成功后，再测试单图编辑、多参考图和 2K。

## 出错
双击 run-doctor.bat，把完整窗口内容保留。常见问题优先检查 CUDA=False、Python 版本错误、磁盘不足、模型下载中断和端口 8000/7860 被占用。
