import os
from config import MODULES_SRC


class ModuleInstaller:
    def __init__(self, module_dir: str):
        self.module_dir = module_dir

    def install_module(self, name: str):
        cmd = f"cp -r {MODULES_SRC}/{name} {self.module_dir}/{name}"
        os.system(cmd)

    def update_module(self, name: str):
        self.uninstall_module(name)
        self.install_module(name)

    def uninstall_module(self, name: str):
        cmd = f"rm -rf {self.module_dir}/{name}"
        os.system(cmd)


# Пример использования:
if __name__ == "__main__":
    installer = ModuleInstaller("./modules",)

    # Установка модуля
    installer.install_module("test")

    # Обновление модуля
    # installer.update_module("test")

    # # Удаление модуля
    # installer.uninstall_module("test")
