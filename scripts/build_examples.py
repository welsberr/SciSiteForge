from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import build


def discover_example_configs(examples_dir: Path) -> list[Path]:
    return sorted(path for path in examples_dir.glob("*.site.json") if path.is_file())


def build_examples(examples_dir: Path, output_root: Path) -> list[dict[str, str]]:
    output_root.mkdir(parents=True, exist_ok=True)
    results: list[dict[str, str]] = []
    for config_path in discover_example_configs(examples_dir):
        bundle_name = config_path.name.removesuffix(".site.json")
        output_dir = output_root / bundle_name
        result = build.build_site(config_path, output_dir)
        results.append(
            {
                "config": str(config_path),
                "output_dir": result["output_dir"],
                "theme": result["theme"],
                "passed": str(result["regression_summary"]["passed"]),
                "failed": str(result["regression_summary"]["failed"]),
            }
        )
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="Build all shipped SciSiteForge example site configs.")
    parser.add_argument(
        "--examples-dir",
        default=str(ROOT / "examples"),
        help="Directory containing *.site.json example configs.",
    )
    parser.add_argument(
        "--output-root",
        default=str(ROOT / "examples" / "_build"),
        help="Directory where built example sites should be written.",
    )
    args = parser.parse_args()

    examples_dir = Path(args.examples_dir)
    output_root = Path(args.output_root)
    results = build_examples(examples_dir, output_root)

    if not results:
        print(f"No example configs found in {examples_dir}")
        return

    print(f"Built {len(results)} example site(s) into {output_root}")
    for item in results:
        print(
            f"- {Path(item['config']).name}: theme={item['theme']} passed={item['passed']} failed={item['failed']} -> {item['output_dir']}"
        )


if __name__ == "__main__":
    main()
