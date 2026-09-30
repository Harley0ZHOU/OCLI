# OCLI

OCLI 是一个基于 DeepSeek API 的交互式命令行助手原型。它提供终端内的多轮对话，并可通过函数调用获取日期、查询模拟天气，以及在当前工作目录内创建或修改文本文件。
（中秋没事干写着完的，帮助自己回忆一下python）

> 当前版本：`v0.1.0 beta`

## 功能

- 使用 DeepSeek `deepseek-flash` 模型进行多轮对话
- 首次启动时校验并将 API Key 保存到系统钥匙串（keyring）
- 自动将对话上下文保存到 `chat.json`，下次启动时继续使用
- 内置工具调用：
  - `get_date`：返回当前日期
  - `get_weather`：返回天气信息（目前为模拟结果）
  - `write_file`：仅在启动时的当前工作目录及其子目录中写入文本文件
- 基于 `curses` 的启动选项界面

## 环境要求

- Python 3.12 或更高版本
- DeepSeek API Key
- 支持 `curses` 的终端环境（macOS、Linux 通常已具备）

项目使用 [uv](https://docs.astral.sh/uv/) 管理依赖；也可使用常规 Python 虚拟环境安装。

## 安装

克隆或进入项目目录后，使用 uv 安装依赖：

```bash
uv sync
```

如果尚未安装 uv，请先按其官方文档完成安装；或使用 pip：

```bash
python -m pip install openai keyring
```

## 启动

在项目根目录执行：

```bash
uv run main.py
```

首次运行时：

1. 在启动界面中选择 **Provide your own API key**。
2. 输入 DeepSeek API Key，程序会向 API 发起一次简短请求验证密钥。
3. 验证通过后，密钥会以服务名 `OCLI`、账户名 `api_key` 保存至系统钥匙串。
4. 进入聊天界面后，直接在 `>` 提示符后输入问题即可。

若钥匙串中已经存在密钥，程序会直接进入聊天界面。

## 聊天命令

| 命令 | 作用 |
| --- | --- |
| `-help` | 显示可用命令提示 |
| `-key` | 删除已保存的 API Key，之后可重新设置 |
| `-exit` | 确认后退出程序 |

除上述命令外，输入的内容都会作为对话消息发送给模型。

## 配置与数据文件

| 文件 | 作用 |
| --- | --- |
| `config.json` | 显示的模型名称和客户端版本信息 |
| `chat.json` | 自动保存的聊天上下文；删除此文件可开始新对话 |
| `tools_definitions.py` | 提供给模型的工具定义 |
| `tools.py` | 文件写入与配置读取等本地工具实现 |

API Key 不写入项目文件，而是由操作系统的 keyring 服务保存。

## 注意事项

- `get_weather` 目前固定返回 `Cloudy 7~13°C`，并不查询真实天气服务。
- 模型可调用 `write_file` 创建、覆盖或追加文本文件。该工具会拒绝访问当前工作目录之外的路径，但使用前仍应检查模型的请求和生成结果。
- 对话内容会保存到 `chat.json`。若内容包含敏感信息，请在结束后删除该文件或将其加入 `.gitignore`。
- 程序目前固定使用 `https://api.deepseek.com` 和 `deepseek-flash`；修改模型或版本展示信息可编辑 `config.json`，但实际调用模型在 `ds.py` 中配置。

## 项目结构

```text
.
├── main.py              # 启动界面、API Key 校验与程序入口
├── ds.py                # 对话循环与模型工具调用
├── tools.py             # 本地文件和配置工具
├── tools_definitions.py # 工具调用声明
├── chatsave.py          # 聊天记录持久化
├── secrets.py           # 系统钥匙串中的 API Key 管理
├── config.json          # 客户端配置
└── pyproject.toml       # Python 依赖与项目元数据
```
