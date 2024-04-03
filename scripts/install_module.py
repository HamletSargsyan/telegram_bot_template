import os

import toml
from config import MODULES_SRC


class ModuleInstaller:
    def __init__(self, module_dir: str):
        self.module_dir = module_dir

        if not os.path.exists(self.module_dir):
            os.mkdir(self.module_dir)

    def install(self, name: str):
        cmd = f"cp -r {MODULES_SRC}/{name} {self.module_dir}/{name}"
        try:
            os.system(cmd)
        except Exception as e:
            return str(e)
        return f"Модуль {name} успешно установлен"

    def update(self, name: str):
        results = []
        try:
            results.append(self.remove(name))
            results.append(self.install(name))
        except Exception as e:
            return str(e)
        return "\n".join(results)

    def remove(self, name: str):
        cmd = f"rm -rf {self.module_dir}/{name}"
        try:
            os.system(cmd)
        except Exception as e:
            return str(e)
        return f"Модуль {name} успешно удален"
        
    def get(self, name: str):
        try:
            with open(f"{self.module_dir}/{name}/module.toml") as f:
                return toml.load(f)
        except Exception as e:
            return str(e)
        
    
    def list(self):
        result = []
        for mod in os.listdir(self.module_dir):
            info = self.get(mod)
            if isinstance(info, str):
                return info
            result.append(
                f"{mod} - {info['version']}"
            )
        return result


installer = ModuleInstaller("./modules",)
# Пример использования:
if __name__ == "__main__":

    # Установка модуля
    installer.install("test")

    # Обновление модуля
    # installer.update_module("test")

    # # Удаление модуля
    # installer.uninstall_module("test")
