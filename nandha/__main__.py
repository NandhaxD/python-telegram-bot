

import os
import importlib
import pkgutil
import asyncio
import logging
import pyrogram 

from nandha import app, pgram
from nandha import plugins  

# Initialize logging
logging.basicConfig(level=logging.DEBUG)

def import_plugins(package):
    package_name = package.__name__
    package_file = package.__file__

    logging.debug(f"Importing plugins from package: {package_name}")
    logging.debug(f"Package file attribute: {package_file}")

    if package_file is None:
        raise ValueError(f"Package {package_name} does not have a __file__ attribute. It might be a namespace package.")

    package_dir = os.path.dirname(package_file)
    logging.debug(f"Package directory: {package_dir}")

    for _, name, is_pkg in pkgutil.iter_modules([package_dir]):
        full_name = f"{package_name}.{name}"
        logging.debug(f"Importing module: {full_name}")
        importlib.import_module(full_name)



import_plugins(plugins)


async def main():
    loop = asyncio.get_event_loop()
    task1 = loop.create_task(app.run_polling())
    task2 = loop.create_task(pgram.run())
    await asyncio.gather(task1, task2)

if __name__ == '__main__':
    asyncio.run(main())
  
