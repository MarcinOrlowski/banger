```ascii
▙▄▄                ▗▟█▙  ▟█▙    ▐▄▄              ▄▄▄▄▄▄▄▄▄█             ▗█    ▙▄▖
▜██████████▄▖        ▀    ▀ ▗█  ▝█████████▙▄ ▗▟██████████▀▚▖   ▗▄█████████▛   ▜█████████▙▄
█▙▄▀▀▀▀▀▀█████▖  ▗▄███████████  █▄▄▀▀▀▀▜█████ ████▀     ▗███▌ ▟██████▀▀▀▀▄▄█▌ █▙▄▛▀▀▀▀▜████▌
████      ▟███▌ ▟████▀   ▀▀▀▀▄▌ ████     ████ ████▖     ▐███▌ ████▀    ▄████▌ ████     ▐███▌
██████████████  ████      ▐███▌ ████     ████ ▝█████████████▌ ██████████████▌ ████▄▄▄▄▄▟███▌
████     ▝▜███▌ ████      ▐███▌ ████     ████    ▀▀▘    ▀███▌ ████▙▖     ▄▄▄  ████████████▀
████      ▟███▌ ████▖     ▟███▌ ████     ████  ▄▄        ███▘ ▝▜████████████  ████  ▝███▙
██████████████  ▝█████████████▌ ▄▄▄▄     ▄▄▄▄   ▜▄▄▄▟███████    ▝▀▀▀▀▀▀▀▀▀▀▘  ████    ▜███▖
▀▀▀▀▀▀▀▀▀▀▀▀▀     ▀▀▀▀▀▀▀▀▝▀▀▀▘ ▝▘▝▘     ▝▘▝▘  ▐█▀▀▀▀▀▀▀▀▀▀                   ▀▀▀▀     ▝▀▀▀▘
┅┅┅ Your banner deserves to be a bänger ┅┅┅┅┅┅ https://github.com/MarcinOrlowski/banger ┅┅┅
```

# Your `banner` deserves to be a `bänger`!

---

```ascii
█▀▄▀█           ▀  ▀
█ █ █ ▄▀▀▄ █▀▀▄ █  █
█   █ █▀▀  █  █ █  █
█   █ ▀▄▄▀ █  █ ▀▄▄▀
```

* Banger
  * [What it is?](#what-it-is)
  * [Key Features](#key-features)
* Usage and Features
  * [Quick Start](#quick-start)
  * [Special Text Patterns](#special-text-patterns)
* TTF/OTF Font Support
  * [Using TTF/OTF Fonts](#ttfotf-font-support)
  * [Font Size Guidelines](#font-size-guidelines)
  * [How TTF/OTF Conversion Works](#how-ttfotf-conversion-works)
* Configuration File
  * [Creating a Configuration File](#creating-a-configuration-file)
  * [Configuration Options](#configuration-options)
  * [How Configuration Works](#how-configuration-works)
* [What's New?](../CHANGES.md)
* [Developmer's corner](#development)
* [License](../README.md#license)

---

## What it is?

`Bänger` (pronounced just `banger`) is a modern tribute to the classic Unix `banner` command line
utility that produces text banners, with additional features added a top:  multiple built-in ASCII
character set and support for rendering any TTF/OTF font with Unicode!

## Key Features

* **Endless font options**: use any TTF/OTF font installed on your system,
* **Better typography**  with proportional spacing that saves significant screen space,
* **Compatible** with original Unix `banner` tool,
* and **moar**!

## Installation

This is regular Python package and is also hosted
on [PyPi](https://pypi.org/project/website-as-app/) so
you can install it as usual. But because this one is supposed to rather act as the application, I
strongly recommend to use [pipx](https://pipx.pypa.io/) to install this tool in isolated
environment be it on Linux, Windows or MacOS machines. Once you got `pipx` up
and running, install the package:

```bash
$ pipx install banger
```

Of course, you can also use plain `pip` to do that, but:

```bash
$ pip install banger
```

But that might be a problem as some distributions no longer allow system-wide installations,
therefore use of `pipx` is strongly recommended as the all-in-one solution.

Once installed you shold be able to run `banger` application in your terminal (session opened
prior installation might not see it unless restarted).
Please use `--demo` to see built-in fonts or type `--help` to see all available options.

### Requirements

* Python 3.8+
* Pillow (PIL fork) for TTF/OTF font rendering

---

>>>>>>> Stashed changes
# Quick Start

Create a banner with the default font:

```ascii
$ banger "Hello World"

█  █      ▀█  ▀█           █   █          ▀█     █
█▀▀█ ▄▀▀▄  █   █  ▄▀▀▄     █   █ ▄▀▀▄ █▄▀  █  ▄▀▀█
█  █ █▀▀   █   █  █  █     █ █ █ █  █ █    █  █  █
█  █ ▀▄▄▀ ▄█▄ ▄█▄ ▀▄▄▀     █▀ ▀█ ▀▄▄▀ █   ▄█▄ ▀▄▄▀
```

NOTE: to maintain behavior of the original `banner` command, you need to quote the text to keep it
as a single argument. Otherwise, the command will split the text into one word per line.

Try different fonts:

## Special Text Patterns

`Bänger` also supports special text patterns that expand to common character sets:

## Character Set Expansion

Use these special patterns (placeholders) in your text:

| Placeholder | Description                       |
|-------------|-----------------------------------|
| `:upper`    | Display all uppercase letters A-Z |
| `:lower`    | Display all lowercase letters a-z |
| `:digits`   | Display all digits 0-9            |

---

```ascii
▀▀█▀▀ ▀▀█▀▀ █▀▀▀   █ ▄▀▀▄ ▀▀█▀▀ █▀▀▀      ▄▀█            █
  █     █   █▀▀   ▄▀ █  █   █   █▀▀       █   ▄▀▀▄ █▀▀▄ ▀█▀  ▄▀▀▄
  █     █   █    ▄▀  █  █   █   █        ▀█▀  █  █ █  █  █    ▀▄
  █     █   █    █   ▀▄▄▀   █   █         █   ▀▄▄▀ █  █  ▀▄▀ ▀▄▄▀
```

## TTF/OTF Font Support

`Bänger` can also use **any** TTF/OTF font installed on your system and convert it to beautiful
ASCII art using Unicode quadrant blocks. Let's use TTF font of size 70pt and squeeze final banner
into 10 terminal lines:

```ascii
$ banger --ttf-font ~/.fonts/j/JetBrainsMonoNL_Regular.ttf --ttf-size 70 --ttf-lines 10 DäNgęR

██████████▙▄▄     ▐███▌  ▐███▌   ████▙       ███  ▗▄███████▄▐██▌  ▗▄▟███████▙▄▖  ███████████▙▄▄
███▌      ▀▜██▖                  ███▜█▙      ███ ▟██▛▘     ▝▜██▌ ▟██▛       ▜██▙ ███▌       ▀███▖
███▌       ▝███    ▄▄▄▄▄▄▄▄▄▄    ███ ▜██▖    ███ ███        ▐██▌ ███▄▄▄▄▄▄▄▄▄███ ███▌        ▐██▌
███▌        ███  ▟██▀▀▘  ▝▀▀██▙  ███  ▜██▖   ███ ███▖       ▐██▌ ███▀▀▀▀▀▀▀▀▀▀▀▀ ███▌      ▗▄██▛▘
███▌        ███     ▄▄▄▄▄▄▄▄███▌ ███   ▜██▖  ███ ▐██▙▖     ▄▟██▌ ▜██▖       ▗▄▄▄ ███████████▀▀▘
███▌        ███ ▗▟██▀▀▀▀▀▀▀▀███▌ ███    ▜██▖ ███  ▝▀▜█████▛▀▐██▌  ▀███▄▄▄▄▄▟██▀▘ ███▌    ▜██▙
███▌       ▐██▛ ███         ███▌ ███     ▀██▖███            ▐██▌     ▝▀▜██▛▀     ███▌     ▝███▖
███▙▄▄▄▄▄▄███▀  ▜██▙▄▄▄▄▄▄▄█▜██▌ ███      ▝█████   ▗▄▄▄▄▄▄▄▄███▘      ▐██▙       ███▌      ▝▜██▙
▀▀▀▀▀▀▀▀▀▀▘       ▝▀▀▀▀▀▀▀  ▝▀▀▘ ▀▀▀       ▝▀▀▀▀   ▝▀▀▀▀▀▀▀▀▀          ▝▀▀▀▀▀▘   ▀▀▀▘        ▀▀▀▘
```

Try a serif fonts for a different look!

Use `--ttl-list` option to list all available TTF/OTF fonts on your system:

```ascii
$ banger --ttf-list | tail -5
UbuntuMono[wght]               /usr/share/fonts/truetype/ubuntu/UbuntuMono[wght].ttf
UbuntuSans-Italic[wdth,wght]   /usr/share/fonts/truetype/ubuntu/UbuntuSans-Italic[wdth,wght].ttf
UbuntuSans[wdth,wght]          /usr/share/fonts/truetype/ubuntu/UbuntuSans[wdth,wght].ttf
UbuntuSansMono-Italic[wght]    /usr/share/fonts/truetype/ubuntu/UbuntuSansMono-Italic[wght].ttf
UbuntuSansMono[wght]           /usr/share/fonts/truetype/ubuntu/UbuntuSansMono[wght].ttf
```

### Font Size Guidelines

You can control the output adjusting font size as well as setting how many terminal lines you
want the banner to take using `--ttf-lines` (default is 7).

You can also control size of the rendered TTF font. When manually specifying `--ttf-size`, TTF/OTF
font sizes work differently than regular text. Use  these ranges for best results:

* **Low quality**: 24-40pt (faster rendering, acceptable quality)
* **Medium quality**: 40-80pt (good balance of speed and quality)
* **High quality**: 80-150pt+ (slower rendering, best quality)

Note: Since we convert to 1-bit quadrant blocks, very high font sizes don't provide significant
quality improvements. The auto-calculated size is usually optimal.

When not specified, `banger` automatically calculates the best font size based on expected output
height.

### How TTF/OTF Conversion Works

banger performs smart conversion of TTF/OTF fonts:

1. **Renders** the TTF/OTF font to a high-resolution bitmap using PIL/Pillow,
2. **Clips** the bitmap to remove unnecessary whitespace (making all fonts proportional),
3. **Samples** the bitmap into 2×2 pixel Unicode quadrants: `▘ ▝ ▀ ▖ ▌ ▞ ▛ ▗ ▚ ▐ ▜ ▄ ▙ ▟ █`
4. **Maps** each quadrant pattern to the appropriate Unicode block character.

This process works with **any TTF/OTF font** - serif, sans-serif, monospace, decorative, or even
emoji fonts!

---

```ascii
▄▀▀▄            ▄▀█  ▀            ▄▀█  ▀  ▀█
█    ▄▀▀▄ █▀▀▄  █   ▀█  ▄▀▀█      █   ▀█   █  ▄▀▀▄
█    █  █ █  █ ▀█▀   █  █  █     ▀█▀   █   █  █▀▀
▀▄▄▀ ▀▄▄▀ █  █  █   ▄█▄ ▀▄▄█      █   ▄█▄ ▄█▄ ▀▄▄▀
                         ▄▄▀
```
# Configuration File

`Bänger` supports YAML configuration files to set default options. This allows you to customize your
preferred settings without having to specify them on the command line every time.

The configuration file should be placed at `~/.config/banger/config.yml`

## Creating a Configuration File

Generate a template configuration file with all options commented out:

```ascii
banger --config-init
```

This creates a template file you can edit. If the file already exists, use `--force` to overwrite:

```ascii
banger --config-init --force
```

## Configuration Options

The configuration file supports these settings:

```yaml
# Configuration file for bagner
# Place this file at ~/.config/bagner/bagner.yml

# Default font to use
# Available fonts: default, matrix, banner, block, blur, compact, fire, quadrant, small
font: matrix

# Default banner width in characters (auto-detects terminal width if not specified)
banner_width: 80

# Default character width for proportional spacing
width: 10
```

## How Configuration Works

1. **Configuration file** provides the default values
2. **Command-line arguments** override configuration file settings
3. **Built-in defaults** are used if no configuration file exists

For example, if your config file sets `font: matrix`, running `banger "test"` will use the matrix
font, but `banger --font default "test"` will override the config and use the default font.

---

```ascii
█▀▀▄                ▀█                     ▄
█  █ ▄▀▀▄ █  █ ▄▀▀▄  █  ▄▀▀▄ █▀▀▄ ▄▀▀▄ █▄▀ ▛ ▄▀▀▄     ▄▀▀▄ ▄▀▀▄ █▄▀ █▀▀▄ ▄▀▀▄ █▄▀
█  █ █▀▀  █  █ █▀▀   █  █  █ █  █ █▀▀  █      ▀▄      █    █  █ █   █  █ █▀▀  █
█▄▄▀ ▀▄▄▀ ▀▄▀  ▀▄▄▀ ▄█▄ ▀▄▄▀ █▄▄▀ ▀▄▄▀ █     ▀▄▄▀     ▀▄▄▀ ▀▄▄▀ █   █  █ ▀▄▄▀ █
                             █
```

## Development

```ascii
$ git clone https://github.com/yourusername/banger
$ cd bannge

# Install dependencies incl. development tools.
# To update existing ones, use `upgrade` option
pip install -e ".[dev]"

# Run tests
pytest

# Check compatibility with original banner
banner "TEST" > original.txt
banger --font banner --width 7 "TEST" > new.txt
diff original.txt new.txt  # Should show minimal differences
```

To install dev version using `pipx` or `pip` for current sources, use (note we install no development dependencies):

```ascii
# as system wide app
$ pipx install -e .

# or as virtual environment app
$ pip install -e .
```
