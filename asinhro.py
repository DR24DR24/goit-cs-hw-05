import asyncio
import aiofiles
import shutil
import logging
import argparse
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def copy_file(file_path: Path, output_folder: Path):
    try:
        ext = file_path.suffix[1:] or "unknown"
        target_dir = output_folder / ext
        target_dir.mkdir(parents=True, exist_ok=True)
        
        target_file = target_dir / file_path.name
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, shutil.copy2, file_path, target_file)
        logging.info(f"Copied {file_path} -> {target_file}")
    except Exception as e:
        logging.error(f"Error copying {file_path}: {e}")

async def read_folder(source_folder: Path, output_folder: Path):
    tasks = []
    for file_path in source_folder.rglob("*"):
        if file_path.is_file():
            tasks.append(copy_file(file_path, output_folder))
    
    if tasks:
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sort files by extension asynchronously.")
    parser.add_argument("source", type=str, help="Path to the source folder.")
    parser.add_argument("destination", type=str, help="Path to the destination folder.")
    args = parser.parse_args()

    source_path = Path(args.source)
    output_path = Path(args.destination)

    if not source_path.exists() or not source_path.is_dir():
        logging.error("Invalid source directory.")
    else:
        asyncio.run(read_folder(source_path, output_path))
