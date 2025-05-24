# Arsenal-Tmux

> 🛠️ A `tmux`-integrated Clone of [arsenal-cli](https://github.com/Orange-Cyberdefense/arsenal)

This project is a customized clone of the original [arsenal](https://github.com/Orange-Cyberdefense/arsenal), developed by **Guillaume Muh** and **mayfly**. All credit for the core concept and functionality goes to them.

This clone enhances `arsenal` with seamless `tmux` integration, inspired by **Mojo8898**'s workflow ideas, allowing commands to be sent across tmux panes.

---

## ✨ Features in Arsenal-Tmux

- 💡 **Auto-execution mode** with `-e` flag
- 🧠 **Global variables** for dynamic argument replacement
- 🧾 Support for **Markdown** and **YAML** cheatsheets
- 🧩 Easily add your own cheatsheets
- 🎨 UI with color schemes and categories
- 🔐 Command prefixing (e.g. `proxychains`, `sudo`, etc.)
- 💬 Description and tagging support in cheatsheets

---

## 📦 Installation

### 🧪 Via `pipx` (Recommended)

```bash
pipx install "git+https://github.com/profzzor/arsenal-tmux.git"
```

### 🧱 Local Development Install

```bash
git clone --depth 1 https://github.com/profzzor/arsenal-tmux.git
cd arsenal-tmux
pip3 install . --break-system-packages
```

> 💡 You can also use a virtual environment.

---

## 🚀 Usage

Start Arsenal with:

```bash
arsenal-tmux
```

> We recommend adding an alias:
```bash
echo "alias at='arsenal-tmux'" >> ~/.bashrc
# or for Zsh
echo "alias at='arsenal-tmux'" >> ~/.zshrc
```

---

## 🔀 Tmux

Run inside a `tmux` session, Arsenal can send commands to another pane.

### Send to Current Pane if no other Pane Exists
```bash
arsenal-tmux
```
> ✅ Arsenal will auto-detect pane layout and decide whether to split or reuse an existing pane.

### Execute in the Pane 1 or Create a Pane (split vertical)
```bash
arsenal-tmux 1 -e
```

---

## 📂 Adding External Cheatsheets

You can store your own cheatsheets in:

- `~/.cheats`
- Or update paths in `arsenal_tmux/modules/config.py`:

```python
CHEATS_PATHS = [
    join(DATAPATH, "cheats"),  # DEFAULT
    # Additional paths below, add comma to line above
    join(BASEPATH, "my_cheats"),
    join(HOMEPATH, ".cheats"),
    # Add exegol folder
    "/opt/my-resources/my-cheats",
    "/opt/my-resources/setup/arsenal-cheats"
]
```

Accepted formats: `.md`, `.yaml`

---

## 🧪 Global Variables

Arsenal supports runtime variables for pre-filling commands:

```bash
> set ip=10.10.10.10
```

Then use `<ip>` inside your cheatsheets.

> The global variable file arsenal.json will be located in the directory where the tmux session was initiated.

---

## 🧰 Prefixing Commands

To prefix all commands (e.g., with `proxychains -q`):

```bash
> set arsenal_prefix_cmd=proxychains -q
arsenal -f
```

---

## 💡 Cheatsheet Format

You can add arguments with default values in your cheats like:

```bash
nmap -sC -sV <target|10.0.0.1>
```

This will show `10.0.0.1` as a default unless overridden.

---

## 🧯 Troubleshooting

### Color Errors in Terminal

```bash
export TERM='xterm-256color'
```

### PyYAML Import Error

```bash
pip install -U PyYAML
```

---

## 🙏 Credits

- **Original Project**: [Orange-Cyberdefense/arsenal](https://github.com/Orange-Cyberdefense/arsenal)
- **Original Authors**: Guillaume Muh, mayfly
- **Tmux Concept Inspired By**: [Mojo8898](https://github.com/Mojo8898)
- **Maintainer of Fork**: [profzzor](https://github.com/profzzor)

---

Built with ❤️ for pentesters who live in tmux.
