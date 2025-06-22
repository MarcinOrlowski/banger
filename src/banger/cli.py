"""
##################################################################################
#
# Bänger by Marcin Orlowski
# Because your `banner` deserves to be a `bänger`!
#
# @author    Marcin Orlowski <mail@marcinOrlowski.com>
# Copyright  ©2025 Marcin Orlowski <MarcinOrlowski.com>
# @link      https://github.com/MarcinOrlowski/banger
#
##################################################################################

Command-line interface for banger.
"""

import argparse
import string
import sys

from .config import get_config, create_config_template
from .constants import Consts
from .core import BannerGenerator
from .fonts import get_available_fonts
from .terminal import get_terminal_width


def expand_special_text(text: str) -> str:
    """Expand special text patterns like :upper, :lower, :digits.

    Args:
        text: Input text that may contain special patterns

    Returns:
        Expanded text with special patterns replaced
    """
    # Define replacements
    replacements = {
        ":upper": string.ascii_uppercase,
        ":lower": string.ascii_lowercase,
        ":digits": string.digits,
    }

    # Apply replacements
    expanded_text = text
    for pattern, replacement in replacements.items():
        expanded_text = expanded_text.replace(pattern, replacement)

    return expanded_text


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser."""

    epilog = "\n".join(
        [
            "Examples:",
            "  banger 'Hello World'                    # Basic usage",
            "  banger --font fire 'TEXT'               # Use fire font",
            "  banger --width 8 'ABC'                  # Set minimum character width (monospace)",
            "  banger --banner-width 40 'Long Text'    # Limit total banner width",
            "  banger --font-list                      # List available TTF/OTF fonts",
            "  banger --ttf-font /path/to/font.ttf 'Hi' # Use system font to render text",
            "",
            f"This is {Consts.APP_NAME} {Consts.APP_VERSION}",
            f"{Consts.APP_URL}",
        ]
    )

    parser = argparse.ArgumentParser(
        prog="banger",
        description="Prints text in large letters",
        epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # Load configuration defaults
    config = get_config()
    default_font = config.get_font() or "quadrant"

    available_fonts = get_available_fonts()
    parser.add_argument(
        "--font",
        default=default_font,
        choices=available_fonts,
        help="Built-in font to use for rendering (default: %(default)s).",
    )

    parser.add_argument(
        "--banner-width",
        type=int,
        metavar="CHARS",
        help="Maximum total banner width in characters (default: auto-detect terminal width)",
    )

    def positive_int(value):
        ivalue = int(value)
        if ivalue <= 0:
            raise argparse.ArgumentTypeError(
                f"--width must be a positive integer, got {value}"
            )
        return ivalue

    parser.add_argument(
        "--width",
        type=positive_int,
        metavar="CHARS",
        help="Minimum recommended width for each character (default: use characters' real width)",
    )

    parser.add_argument(
        "--demo",
        action="store_true",
        help="Display sample text in all available built-in fonts",
    )

    parser.add_argument(
        "--demo-md",
        action="store_true",
        help="Display all available fonts in Markdown format for documentation",
    )

    parser.add_argument(
        "--config-init",
        action="store_true",
        help="Create a template configuration file at ~/.config/banger/banger.yml",
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help="Force overwrite existing configuration file (use with --config-init)",
    )

    parser.add_argument(
        "--ttf-font",
        metavar="PATH",
        help="Use a system TTF or OTF font file instead of built-in fonts",
    )

    parser.add_argument(
        "--ttf-size",
        type=positive_int,
        metavar="SIZE",
        help="TTF font size in points (default: auto-calculated based on --ttf-lines)",
    )

    parser.add_argument(
        "--ttf-lines",
        type=positive_int,
        default=7,
        metavar="LINES",
        help="Output height in terminal lines (default: %(default)s)",
    )

    parser.add_argument(
        "--ttf-list",
        action="store_true",
        help="List available system TTF and OTF fonts",
    )

    parser.add_argument(
        "--ttf-list-sort",
        choices=["name", "path"],
        default="path",
        metavar="SORT",
        help="Sort TTF/OTF font list by name or path (default: %(default)s)",
    )

    parser.add_argument(
        "--font-list",
        action="store_true",
        help="List all built-in font names in alphabetical order",
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"{Consts.APP_NAME} {Consts.APP_VERSION} - {Consts.APP_URL}",
    )

    parser.add_argument(
        "text",
        nargs="*",
        help="Text to convert to banner. Multiple arguments create separate banners. "
        "Special patterns: :upper (A-Z), :lower (a-z), :digits (0-9)",
    )

    return parser


def display_all_fonts() -> None:
    """Display all available fonts with samples."""
    from .fonts import _font_supports_lowercase, _font_supports_uppercase

    available_fonts = get_available_fonts()

    for font_name in available_fonts:
        # Print font name in normal text
        print(
            f"---[ {font_name} ]---------------------------------------------------------\n"
        )

        # Determine what examples to show based on font capabilities
        examples = []

        # Add font name in different cases if supported
        font_name_str = ""
        if _font_supports_uppercase(font_name):
            font_name_str = font_name.upper()
        if _font_supports_lowercase(font_name):
            if font_name_str:
                font_name_str += " "
            font_name_str += font_name.lower()

        # Add digits and punctuation
        if font_name_str:
            font_name_str += " "
        font_name_str += "123.!?"

        examples.append(font_name_str)

        # Generate and print each example
        for example_text in examples:
            generator = BannerGenerator(font=font_name)
            generator.add_text(example_text)
            print(generator.render(), end="")


def display_all_fonts_markdown() -> None:
    """Display all available fonts in Markdown format for documentation."""
    from .fonts import _font_supports_lowercase, _font_supports_uppercase

    available_fonts = get_available_fonts()

    for font_name in available_fonts:
        # Print font name as markdown header
        print(f"### {font_name}")

        # Determine what examples to show based on font capabilities
        examples = []

        # Add font name in different cases if supported
        if _font_supports_uppercase(font_name):
            examples.append(font_name.upper())
        if _font_supports_lowercase(font_name):
            examples.append(font_name.lower())

        # If font doesn't support both cases, just use the font name as-is
        if not examples:
            examples.append(font_name)

        # Add digits and punctuation
        examples.append("123")
        examples.append(".!?")

        # Create single line with all examples
        font_examples = []
        if _font_supports_uppercase(font_name):
            font_examples.append(font_name.upper())
        if _font_supports_lowercase(font_name):
            font_examples.append(font_name.lower())
        if not font_examples:
            font_examples.append(font_name)

        # Combine font names and add digits/punctuation
        combined_text = " ".join(font_examples) + " 123.!?"

        # Print usage example in bash code block
        print()
        print(f'```ascii\nbanger --font {font_name} "{combined_text}"\n```')
        print()

        # Add separator text
        print("That would output the following:")
        print()

        # Generate and print single merged line
        print("```ascii")
        generator = BannerGenerator(font=font_name)
        generator.add_text(combined_text)
        output = generator.render()
        print(output.rstrip())
        print("```")
        print()


def main() -> int:
    """Main entry point for banger CLI."""
    parser = create_parser()

    # Handle special case for -- separator (original banner compatibility)
    argv = sys.argv[1:]
    if argv and argv[0] == "--":
        # Remove the -- and treat everything after as text (bypass argparse for these)
        text_args = argv[1:]
        if not text_args:
            parser.error("argument text: expected at least one argument after --")

        # Create a minimal args object with config defaults
        config = get_config()

        class Args:
            def __init__(self):
                self.font = config.get_font() or "default"
                self.banner_width = config.get_banner_width()
                self.width = config.get_width()
                self.demo = False
                self.demo_md = False
                self.config_init = False
                self.force = False
                self.ttf_font = None
                self.ttf_size = None  # Will be auto-calculated
                self.ttf_lines = 7
                self.ttf_list = False
                self.ttf_list_sort = "path"
                self.font_list = False
                self.text = text_args

        args = Args()
    else:
        try:
            args = parser.parse_args(argv)
        except SystemExit as e:
            return e.code if e.code is not None else 1

    # Handle --demo option
    if getattr(args, "demo", False):
        display_all_fonts()
        return 0

    # Handle --demo-md option
    if getattr(args, "demo_md", False):
        display_all_fonts_markdown()
        return 0

    # Handle --config-init option
    if getattr(args, "config_init", False):
        force_overwrite = getattr(args, "force", False)
        create_config_template(force=force_overwrite)
        return 0

    # Handle --ttf-list option
    if getattr(args, "ttf_list", False):
        from .fonts.ttf import list_system_ttf_fonts

        sort_by = getattr(args, "ttf_list_sort", "path")
        system_fonts = list_system_ttf_fonts(sort_by=sort_by)
        if system_fonts:
            try:
                print(f"Available system TTF/OTF fonts (sorted by {sort_by}):")
                for font_name, font_path in system_fonts:
                    print(f"  {font_name:<30} {font_path}")
            except BrokenPipeError:
                # Handle broken pipe gracefully when output is piped to head, less, etc.
                pass
        else:
            print("No system TTF/OTF fonts found.")
        return 0

    # Handle --font-list option
    if getattr(args, "font_list", False):
        available_fonts = get_available_fonts()
        available_fonts.sort()  # Sort alphabetically
        print("Available built-in fonts:")
        for font_name in available_fonts:
            print(f"  {font_name}")
        return 0

    # Handle TTF font usage
    font_name = args.font
    if getattr(args, "ttf_font", None):
        try:
            from .fonts.ttf import TtfFont

            # Auto-calculate font size based on desired output lines if not provided
            ttf_size = args.ttf_size
            if ttf_size is None:
                # Calculate font size to get reasonable bitmap coverage for desired lines
                # Rough estimate: each terminal line needs about 8-10 points
                ttf_size = max(24, args.ttf_lines * 8)

            # Create TTF font instance
            ttf_font = TtfFont(args.ttf_font, ttf_size, args.ttf_lines)
            # Use the TTF font directly
            font_name = ttf_font
        except Exception as e:
            print(f"Error loading TTF font '{args.ttf_font}': {e}", file=sys.stderr)
            return 1

    # Validate that text is provided when not using special options
    if not args.text:
        parser.error("argument text: expected at least one argument")

    # Use specified banner width or auto-detect terminal width
    banner_width = (
        args.banner_width if args.banner_width is not None else get_terminal_width()
    )

    # Process each text argument as a separate banner
    for word in args.text:
        generator = BannerGenerator(
            max_width=banner_width, font=font_name, character_width=args.width
        )

        # Expand special text patterns first
        expanded_word = expand_special_text(word)

        # Convert all whitespace to spaces (original behavior)
        processed_word = expanded_word
        for whitespace_char in "\t\n\r\v\f":
            processed_word = processed_word.replace(whitespace_char, " ")

        generator.add_text(processed_word)
        print(generator.render(), end="")

    return 0


if __name__ == "__main__":
    sys.exit(main())
