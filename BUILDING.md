# 音乐下载器打包说明

## 打包前准备

1. 确保已安装PyInstaller：
   ```bash
   pip install pyinstaller
   ```

2. 安装项目依赖：
   ```bash
   pip install -r requirements.txt
   ```

## 打包步骤

### 方法一：使用自动化脚本（推荐）

运行自动化打包脚本：

```bash
python build.py
```

该脚本会自动执行以下操作：

1. 清理之前的打包产物（build/、dist/、*.spec）
2. 清理Python缓存文件（__pycache__、*.pyc）
3. 清除开发配置文件（如cookie文件等）
4. 执行PyInstaller打包命令
5. 显示打包结果和可执行文件位置

### 方法二：手动打包

直接运行PyInstaller命令：

```bash
pyinstaller music_downloader.spec
```

## 打包配置说明

- **模式**: 单文件模式（onefile）
- **控制台**: 隐藏控制台窗口（console=False）
- **图标**: 默认未设置，可在spec文件中添加图标配置
- **排除模块**: 排除了matplotlib、numpy等大型模块以减小体积
- **压缩**: 已禁用UPX压缩
- **输出文件**: `./dist/music-downloader.exe`

## 自定义图标

1. 准备 `.ico` 格式的图标文件
2. 打开 [music_downloader.spec](file:///c:/Users/Prologue/develop/vs/music-download-tool/music_downloader.spec) 文件
3. 找到 EXE 部分，取消注释并修改图标路径：
   ```python
   exe = EXE(
       # ... 其他配置 ...
       icon='app_icon.ico',  # 替换为实际图标文件路径
   )
   ```
4. 重新运行打包命令

## 优化建议

1. 如果生成的可执行文件过大，可以进一步在spec文件中排除不需要的模块
2. 检查是否有不必要的依赖被包含进来
3. 根据实际需要决定是否启用UPX压缩

## 注意事项

- 打包过程会在 `dist/` 目录下生成可执行文件
- 打包后的应用可以在没有安装Python的电脑上运行
- 打包过程会自动清理开发配置文件（如cookie文件）
- 如需保留某些配置文件，请在打包前备份
- 当前生成的可执行文件大小约为 44MB，可通过排除更多模块进一步减小