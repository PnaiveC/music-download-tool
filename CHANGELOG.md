# 修改日志 (Changelog)

所有值得注意的更改都将记录在此文件中。

## [未发布版本] - 2026-03-09

### 修复

- 修复了 `KeyError: 'target_dir'` 错误
  - 在 [config/settings.py](file:///Users/Prologue/develop/vs/music-download-tool/config/settings.py) 中添加了缺失的 `target_dir` 配置键
  - 确保配置文件中的 `target_dir` 与下载位置 (`download_location`) 保持同步
  - 添加了适当的加载和保存逻辑以维护配置一致性

- 修复了 `name 'os' is not defined` 错误
  - 在 [core/downloaders/downloader.py](file:///Users/Prologue/develop/vs\music-download-tool\core\downloaders\downloader.py) 中添加了缺失的 `import os` 语句
  - 在 [ui/widgets/threads.py](file:///Users/Prologue/develop/vs\music-download-tool\ui\widgets\threads.py) 中添加了缺失的 `import os` 语句，解决了 `os.path.join` 调用时的错误

- 修复了 cookie 文件处理问题
  - 改进了 cookie 文件路径处理，使用绝对路径替代相对路径
  - 添加了对 cookie 文件不存在的容错处理，使程序在缺少 cookie 时仍能运行
  - 优化了 cookie 文件格式，确保符合 Netscape HTTP Cookie 规范

### 功能增强

- 增强了 GUI 下载位置配置功能
  - 添加了 "下载位置" 菜单项，允许用户自定义下载目录
  - 实现了下载位置的持久化存储功能
  - 添加了下载前的位置有效性验证
  - 当下载位置无效时提供错误提示

- 改进了错误处理和用户体验
  - 在下载过程中提供了更清晰的错误提示
  - 优化了配置验证逻辑，确保所有必需配置项都存在
  - 添加了对各种错误情况的处理，提高程序稳定性

### 文档更新

- 更新了 [README.md](file:///Users/Prologue/develop/vs/music-download-tool/README.md) 以反映新功能
- 更新了 [TEST_REPORT.md](file:///Users/Prologue/develop/vs/music-download-tool/TEST_REPORT.md) 以包含新功能测试结果
- 更新了 [PARALLEL_OPTIMIZATION_REPORT.md](file:///Users/Prologue/develop/vs/music-download-tool/PARALLEL_OPTIMIZATION_REPORT.md) 以反映配置变更
- 更新了 [GUI_TEST_REPORT.md](file:///Users/Prologue/develop/vs/music-download-tool/GUI_TEST_REPORT.md) 以包含下载位置功能的实现验证

### 性能优化

- 优化了配置加载流程，减少不必要的文件 I/O 操作
- 改进了模块导入结构，减少启动时间
- 优化了错误处理路径，减少异常情况下的资源消耗