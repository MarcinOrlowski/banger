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

---

# What it is?

`Bänger` (pronounced just `banger`) is a modern tribute to the classic Unix `banner` command line
utility that produces text banners, with additional features added a top:  multiple built-in ASCII
character set and support for rendering any TTF/OTF font with Unicode!

## Key Features

- **Endless font options**: use any TTF/OTF font installed on your system,
- **Better typography**  with proportional spacing that saves significant screen space,
- **Compatible** with original Unix `banner` tool,
- and **moar**!

---

## Quick start

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

## Using TTF/OTF fonts

`Bänger` can also use **any** TTF/OTF font installed on your system and convert it to beautiful
ASCII art using Unicode quadrant blocks. Let's use TTF font of size 70pt and squeeze final banner
into 10 terminal lines:

```ascii
$ banger --ttf-font ~/.fonts/j/JetBrainsMonoNL_Regular.ttf --ttf-size 70 --ttf-lines 10 DäNgęR

█████████▙▄▄     ▐███   ▐██▌   ████▙       ███  ▗▄██████▄▐██▌  ▗▄▟██████▙▄▖  ██████████▙▄▄
██▌      ▀▜██▖                 ███▜█▙      ███ ▟██▛▘    ▝▜██▌ ▟██▛      ▜██▙ ███▌      ▀███▖
██▌       ▝███    ▄▄▄▄▄▄▄▄▄    ███ ▜██▖    ███ ███       ▐██▌ ███▄▄▄▄▄▄▄▄███ ███▌       ▐██▌
██▌        ███  ▟██▀▀▘ ▝▀▀██▙  ███  ▜██▖   ███ ███▖      ▐██▌ ███▀▀▀▀▀▀▀▀▀▀▀ ███▌     ▗▄██▛▘
██▌        ███     ▄▄▄▄▄▄▄███▌ ███   ▜██▖  ███ ▐██▙▖    ▄▟██▌ ▜██▖      ▗▄▄▄ ██████████▀▀▘
██▌        ███ ▗▟██▀▀▀▀▀▀▀███▌ ███    ▜██▖ ███  ▝▀▜████▛▀▐██▌  ▀███▄▄▄▄▟██▀▘ ███▌   ▜██▙
██▌       ▐██▛ ███        ███▌ ███     ▀██▖███           ▐██▌     ▝▀▜█▛▀     ███▌    ▝███▖
██▙▄▄▄▄▄▄███▀  ▜██▙▄▄▄▄▄▄█▜██▌ ███      ▝█████   ▗▄▄▄▄▄▄▄███▘      ▐█▙       ███▌     ▝▜██▙
▀▀▀▀▀▀▀▀▀▘       ▝▀▀▀▀▀▀  ▝▀▀▘ ▀▀▀       ▝▀▀▀▀   ▝▀▀▀▀▀▀▀▀          ▝▀▀▀▀▘   ▀▀▀▘       ▀▀▀▘
```

---

## Further reading

- [Installation guide](docs/README.md#installation)
- [Project documentation](docs/README.md)
- [Usage examples](docs/README.md#usage)
- [What's new?](CHANGES.md)

---

## License

- Written and copyrighted &copy;2025 by Marcin Orlowski <https://marcinOrlowski.com>
- Bänger is the open-sourced software licensed under
  the [MIT license](http://opensource.org/licenses/MIT)
