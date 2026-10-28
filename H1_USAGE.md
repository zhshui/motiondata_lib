# dance1_subject1 剪辑

已为 motiondata_lib 增加 SuperMimic NPZ 输入和 Unitree H1 MJCF 模型支持。

安装依赖 `uv sync` 后，在本仓库运行 `./open_h1_editor.sh /path/to/motion.npz`；也可以传入动作目录。无参数时打开当前目录。

原动作共 6571 帧，50 FPS，约 131.42 秒。界面帧号从 1 开始，剪辑包含起止两帧。拖动时间轴上的剪辑标记，点击 **Trim current**，选择一个新文件名保存。默认保存到原动作所在目录。

SuperMimic 剪辑保留原始字段、数组精度和元数据，同步截取关节姿态、速度及所有身体状态；不改变坐标系，不重新计算速度。任何已有文件都不能被剪辑导出覆盖，请使用新文件名。

**Export checked** 仍为上游的标准格式批量导出，请用 **Trim current** 保存训练格式片段。

本地将 PySide6 固定为 6.8 系列，以兼容 Ubuntu 20.04；Ubuntu 需安装 `libxcb-cursor0`；启动脚本也兼容在本地 `.runtime` 目录提取的库，该目录不会提交到 Git。

验证：首帧、末帧及中间采样帧的 H1 正向运动学与原始 body_pos_w 一致；单帧和多帧剪辑的所有字段与原始切片逐值一致。
