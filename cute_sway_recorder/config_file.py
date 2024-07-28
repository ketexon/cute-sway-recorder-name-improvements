import configparser
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

DEFAULT_CONFIG_PATH = Path.home() / ".config" / "cute-sway-recorder" / "defaults.conf"

def validate_file_dest(file_dest: Path):
    """
    Tests if a file destination coming from the config file
    is a valid destination.
    Namely
     - It is not a directory
     - It's parent is an existing directory
    """
    if len(file_dest.name) == 0:
        raise ValueError(f"\"{file_dest}\" does not have a name.")

    if file_dest.is_dir():
        raise ValueError(f"\"{file_dest}\" is a directory.")

    if not file_dest.parents[0].expanduser().is_dir():
        raise ValueError(f"\"{file_dest}\"'s parent directory does not exist.")

@dataclass
class ConfigFile:
    """
    Contains data parsed from the config file 
    at `~/.config/cute-sway-recording/defaults.conf`
    Use :func:`ConfigFile.parse` to parse the ConfigFile.
    """

    file_dest: Optional[Path] = None
    include_audio: bool = False
    delay: int = 0
    flags: str = ""

    @staticmethod
    def parse(config_file_path: Path = DEFAULT_CONFIG_PATH) -> "ConfigFile":
        parser = configparser.ConfigParser()

        if config_file_path.exists(): 
            try:
                parser.read(config_file_path)
            except configparser.ParsingError as e:
                print(f"Error parsing config: {e}")

        config_file = ConfigFile(
            include_audio = parser.getboolean("DEFAULT", "include_audio", fallback=False),
            delay = parser.getint("DEFAULT", "delay", fallback=0),
            flags = parser.get("DEFAULT", "flags", fallback=""),
        )

        file_dest_str = parser.get("DEFAULT", "file_dest", fallback=None)
        if file_dest_str is not None:
            try:
                file_dest = Path(file_dest_str)
                validate_file_dest(file_dest)
                config_file.file_dest = file_dest.expanduser().resolve()
            except ValueError as e:
                print(f"Error parsing config: {e}")
                

        return config_file
