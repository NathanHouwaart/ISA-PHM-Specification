"""Bundle validator inputs from their canonical locations in the specification."""

from pathlib import Path
from shutil import copy2

from setuptools import setup
from setuptools.command.build_py import build_py


class BuildWithAssets(build_py):
    def run(self):
        super().run()
        root = Path(__file__).resolve().parent
        paths = [root / name for name in (
            "specification/quantity-unit-warning-rules.json",
            "schemas/isa-tools-phm/study_config.json",
            "schemas/isa-tools-phm/acceleration-accelerometer.json",
            "schemas/isa-tools-phm/vibration-accelerometer.json",
        )]
        for source in paths:
            target = Path(self.build_lib) / "validator/_assets" / source.relative_to(root)
            target.parent.mkdir(parents=True, exist_ok=True)
            copy2(source, target)


setup(cmdclass={"build_py": BuildWithAssets})
