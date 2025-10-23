# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

这是 ONLYOFFICE 构建工具仓库，用于自动获取和安装 ONLYOFFICE Document Server、Document Builder 和 Desktop Editors 编译所需的所有组件、依赖项和源代码。

## 核心架构

### 构建系统层次结构

1. **配置层 (configure.py)** - 解析命令行参数并生成配置文件
2. **构建编排层 (make.py)** - 主构建入口，协调所有构建步骤
3. **平台特定层 (tools/linux/automate.py)** - 平台特定的自动化脚本
4. **模块构建层 (scripts/)** - 各个模块的具体构建逻辑

### 主要模块

- **core**: 核心库和组件（文件格式转换、渲染等）
- **desktop**: 桌面编辑器应用
- **server**: 文档服务器组件
- **builder**: 文档构建器
- **mobile**: 移动端组件

### 构建流程

```
configure.py → make.py → [make_common.make() → build_sln.make() → build_js.make() → build_server.make() → deploy.make()]
```

## 常用命令

### 配置构建

```bash
# 基础配置（生成 config 文件）
./configure.py --module <模块名> --platform <平台> [其他选项]

# 示例：配置构建 Desktop 和 Server
./configure.py --module "desktop server" --platform linux_64
```

### 执行构建

```bash
# 完整构建流程
./make.py

# 仅构建特定模块（需要先配置）
./make.py

# 使用 automate.py（Linux 平台）
cd tools/linux
./automate.py [desktop|server|builder]
```

### 开发模式

```bash
# 启用开发模式构建（跳过某些打包步骤）
./configure.py --develop 1 --module server
./make.py
```

### Python 环境配置

```bash
# 解决 ICU 模块导入错误
export PYTHONPATH=$PYTHONPATH:$(pwd)/scripts/core_common/modules
```

### Git 代理配置（国内网络）

```bash
# 设置 GitHub 代理
git config --global url."https://gh-proxy.com/https://github.com/".insteadOf https://github.com/
```

## 重要配置选项

### configure.py 参数

- `--update`: 是否更新/克隆仓库（1=是，0=否）
- `--branch`: 指定分支/标签名称
- `--module`: 构建模块（desktop、server、builder、mobile 或组合）
- `--platform`: 目标平台（linux_64、win_64、mac_64 等）
- `--clean`: 是否清理重新构建
- `--develop`: 开发模式
- `--qt-dir`: Qt 目录路径
- `--branding`: 品牌定制路径

### 平台值

- `native`: 当前系统平台
- `linux_64`, `linux_32`: Linux 平台
- `win_64`, `win_32`: Windows 平台
- `mac_64`: macOS 平台
- `android_*`: Android 平台变体
- `ios`: iOS 平台

## 项目文件结构

- `scripts/`: Python 构建脚本
  - `base.py`: 基础工具函数（文件操作、命令执行等）
  - `config.py`: 配置解析和管理
  - `build_*.py`: 各模块构建脚本
  - `deploy_*.py`: 各模块部署脚本
  - `package_*.py`: 各模块打包脚本
  - `core_common/modules/`: 第三方依赖模块构建脚本
  - `develop/`: 开发模式相关脚本

- `tools/`: 平台特定工具
  - `linux/automate.py`: Linux 平台自动化构建入口
  - `common/`: 通用工具脚本

- `sln.json`: 项目解决方案配置（定义各模块的 .pro 文件依赖关系）
- `config`: 运行时配置文件（由 configure.py 生成）
- `defaults`: 默认配置值

## 依赖管理

### 第三方库

构建系统会自动下载和编译以下依赖：
- Qt 5.9.9
- ICU (国际化组件)
- V8 JavaScript 引擎
- OpenSSL
- Boost
- 各种格式处理库（见 scripts/core_common/modules/）

### 系统依赖

Linux 平台需要预先安装：
- Python 3
- Git
- 基础编译工具链（gcc/g++）
- PostgreSQL（Document Server）
- RabbitMQ（Document Server）
- NGINX（Document Server）

## 调试和故障排查

### 常见问题

1. **ICU 编译错误**: 设置 `PYTHONPATH` 环境变量指向 `scripts/core_common/modules`
2. **Qt 未找到**: 使用 `--qt-dir` 参数或让 automate.py 自动下载
3. **GitHub 访问慢**: 配置 git 代理（见上文）
4. **uintptr_t 未定义**: V8 编译问题，需要添加 `#include <cstdint>`

### 查看构建日志

构建过程会输出详细日志到终端。关键步骤包括：
- 仓库更新/克隆
- 第三方依赖编译
- 核心模块编译
- JavaScript 构建
- 部署和打包

## 输出目录

编译结果位于：
- `out/<平台>/onlyoffice/`: 主要输出目录
  - `documentserver/`: Document Server 文件
  - `desktopeditors/`: Desktop Editors 文件
  - `documentbuilder/`: Document Builder 文件

## 工作流程集成

仓库包含 GitHub Actions 工作流：
- `.github/workflows/build-server.yml`: 服务器构建流程
- `.github/workflows/check.yml`: 代码检查
- `.github/workflows/git-operations.yml`: Git 操作自动化
- `.github/workflows/update-version.yml`: 版本更新

## 注意事项

1. **仅 master 分支保证稳定**: 官方只保证从 master 分支构建的产品正常工作
2. **构建时间**: 完整构建可能需要数小时，取决于硬件配置
3. **磁盘空间**: 确保至少 50GB 可用空间
4. **内存要求**: 建议 16GB+ RAM 用于编译大型模块
5. **并行构建**: 默认使用多进程编译（通过 `--multiprocess` 控制）
