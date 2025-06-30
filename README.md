# Cognitaria Bot

**注意事项：在观看这玩意的代码的时候提前备好高血压药，我的代码全是用Gemini 2.5pro和DeepSeek R1 0528，纯Prompt，无技术🤣。就连README.md也是LLM写的，本人是神秘初中生，没那么多时间写代码，索性直接Vibe Coding了**

总之，这是一个给我呆的小团体Cognitaria写的机器入，目前功能只有改名字颜色一个。
或许小团体大了我会尝试去做一些其他功能以便管理。


## 功能列表 (Features)

*   动态颜色身份组管理

## 安装与设置 (Setup)

1.  在项目根目录下创建一个名为 `.env` 的文件，并填入你的 Discord Bot Token。这是一个模板：
    ```
    DISCORD_TOKEN=YOUR_DISCORD_BOT_TOKEN_HERE
    ```

2.  使用 `pip` 安装所有依赖：
    ```bash
    pip install -r requirements.txt
    ```

## 如何运行 (Usage)

1.  启动机器人：
    ```bash
    python bot.py
    ```

2.  主要斜杠命令：
    *   `/color_panel`: 显示颜色选择面板，让用户选择或自定义他们的身份组颜色。
    *   `/reload`: 重新加载指定的 cog，用于在不重启机器人的情况下更新功能。
    *   `/sync`: 将斜杠命令同步到 Discord 服务器。

## 项目结构 (Project Structure)

*   **`cogs/`**: 存放机器人的功能模块 (Cogs)。每个子目录代表一个独立的功能，例如 `color_cog` 负责颜色身份组相关的所有命令和逻辑。
*   **`core/`**: 包含机器人核心逻辑。例如 `config.py` 用于加载配置，`role_manager.py` 负责身份组的创建、删除和分配。
*   **`data/`**: 存储持久化数据，例如 `role_config.json` 用来保存颜色身份组的配置信息。
