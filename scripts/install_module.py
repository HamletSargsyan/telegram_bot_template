import os
import shutil
import git


class ModuleInstaller:
    def __init__(self, module_dir: str, gh_username: str, repo_name: str):
        self.module_dir = module_dir
        self.repo_url = f"git@github.com:{gh_username}/{repo_name}"

    def install_module(self, module_name):
        module_path = os.path.join(self.module_dir, module_name)
        if os.path.exists(module_path):
            print(f"Module '{module_name}' is already installed.")
            return

        try:
            git.Repo.clone_from(self.repo_url, module_path)
            print(f"Module '{module_name}' installed successfully.")
        except git.GitCommandError as e:
            print(f"Failed to install module '{module_name}': {e}")

    def update_module(self, module_name):
        module_path = os.path.join(self.module_dir, module_name)
        if not os.path.exists(module_path):
            print(f"Module '{module_name}' is not installed.")
            return

        try:
            shutil.rmtree(module_path)
            git.Repo.clone_from(self.repo_url, module_path)
            print(f"Module '{module_name}' updated successfully.")
        except (git.GitCommandError, FileNotFoundError) as e:
            print(f"Failed to update module '{module_name}': {e}")

    def uninstall_module(self, module_name):
        module_path = os.path.join(self.module_dir, module_name)
        if not os.path.exists(module_path):
            print(f"Module '{module_name}' is not installed.")
            return

        try:
            shutil.rmtree(module_path)
            print(f"Module '{module_name}' uninstalled successfully.")
        except FileNotFoundError as e:
            print(f"Failed to uninstall module '{module_name}': {e}")


# Пример использования:
if __name__ == "__main__":
    installer = ModuleInstaller("./modules", "HamletSargsyan", "telegram_bot_modules")

    # Установка модуля
    installer.install_module("test")

    # Обновление модуля
    # installer.update_module("test")

    # # Удаление модуля
    # installer.uninstall_module("test")
