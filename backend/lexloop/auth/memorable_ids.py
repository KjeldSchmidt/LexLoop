"""Memorable username/password generators with deliberately different shapes.

Usernames: PascalCase AdjectiveNoun, e.g. ``CoralLantern`` (optional ``42`` suffix).
Passwords: hyphen-joined passphrases from ``randompass`` (large wordlist).
"""

from __future__ import annotations

import secrets
from functools import lru_cache
from importlib.resources import files
from pathlib import Path

from randompass import Passphrase  # type: ignore[import-untyped]

_ADJECTIVES: tuple[str, ...] = (
    "amber",
    "ancient",
    "brave",
    "bright",
    "calm",
    "clever",
    "coral",
    "cozy",
    "crisp",
    "curious",
    "daring",
    "eager",
    "fancy",
    "gentle",
    "golden",
    "happy",
    "honest",
    "ivory",
    "jade",
    "jolly",
    "kind",
    "lively",
    "lucky",
    "merry",
    "noble",
    "peaceful",
    "proud",
    "quick",
    "quiet",
    "rapid",
    "rusty",
    "sable",
    "scarlet",
    "silent",
    "silver",
    "simple",
    "steady",
    "sunny",
    "swift",
    "tidy",
    "vivid",
    "warm",
    "wise",
)

_NOUNS: tuple[str, ...] = (
    "anchor",
    "apple",
    "arrow",
    "aspen",
    "aurora",
    "badge",
    "bamboo",
    "beacon",
    "berry",
    "blossom",
    "breeze",
    "brook",
    "canyon",
    "cedar",
    "cello",
    "cipher",
    "citrus",
    "cliff",
    "cloud",
    "cobalt",
    "comet",
    "cosmos",
    "cricket",
    "delta",
    "dove",
    "eagle",
    "echo",
    "ember",
    "falcon",
    "fern",
    "finch",
    "fjord",
    "flint",
    "flora",
    "flute",
    "forest",
    "frost",
    "galaxy",
    "garden",
    "glacier",
    "glen",
    "grove",
    "harbor",
    "hazel",
    "herald",
    "heron",
    "honey",
    "horizon",
    "iris",
    "island",
    "jasper",
    "jewel",
    "juniper",
    "kayak",
    "kettle",
    "kite",
    "lagoon",
    "lantern",
    "lark",
    "leaf",
    "lemon",
    "lilac",
    "lotus",
    "maple",
    "marble",
    "meadow",
    "melody",
    "meteor",
    "mint",
    "mirror",
    "moss",
    "nectar",
    "nest",
    "nova",
    "oak",
    "oasis",
    "ocean",
    "olive",
    "onyx",
    "opal",
    "orbit",
    "orchid",
    "otter",
    "owl",
    "palm",
    "panda",
    "pebble",
    "penguin",
    "petal",
    "phoenix",
    "pine",
    "plume",
    "pond",
    "prism",
    "quartz",
    "quill",
    "raven",
    "reef",
    "ridge",
    "river",
    "robin",
    "ruby",
    "saffron",
    "sage",
    "sapphire",
    "shadow",
    "shell",
    "sparrow",
    "sprite",
    "star",
    "stone",
    "storm",
    "stream",
    "summit",
    "swan",
    "tide",
    "tiger",
    "timber",
    "topaz",
    "trail",
    "tulip",
    "valley",
    "velvet",
    "violet",
    "vista",
    "wave",
    "willow",
    "wolf",
    "zephyr",
)

_PASSPHRASE_WORDS = 4


def _pick(words: tuple[str, ...]) -> str:
    return words[secrets.randbelow(len(words))]


@lru_cache(maxsize=1)
def _passphrase_generator() -> Passphrase:
    wordlist = Path(str(files("randompass").joinpath("assets/wordlist.txt")))
    return Passphrase(
        length=_PASSPHRASE_WORDS,
        separator="-",
        wordlist=wordlist,
    )


def generate_username(*, with_numeric_suffix: bool = False) -> str:
    """PascalCase AdjectiveNoun, e.g. ``CoralLantern`` or ``CoralLantern42``."""
    adjective = _pick(_ADJECTIVES).capitalize()
    noun = _pick(_NOUNS).capitalize()
    username = f"{adjective}{noun}"
    if with_numeric_suffix:
        username = f"{username}{secrets.randbelow(90) + 10}"
    return username


def generate_password() -> str:
    """Hyphen-joined passphrase from randompass (~7.7k-word list)."""
    return str(_passphrase_generator().generate_passphrase())
