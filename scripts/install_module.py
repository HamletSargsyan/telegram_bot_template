import git
import os
import shutil
from git import GitCommandError, NoSuchPathError

# Путь, куда вы хотите склонировать папку
LOCAL_FOLDER_PATH = "./modules/"

USERNAME = "HamletSargsyan"
REPO = "telegram_bot_modules"
REPO_URL = f"git@github.com:{USERNAME}/{REPO}.git"


class ModuleInstaller:
    def __init__(self) -> None:
        pass

    def install(self, name: str):
        """
        Устанавливает модуль из репозитория.

        Args:
            name (str): Имя папки, в которую будет установлен модуль.

        Returns:
            str: Сообщение об успешной установке.
        """
        try:
            git.Repo.clone_from(
                REPO_URL,
                os.path.join(LOCAL_FOLDER_PATH, name),
                branch="main",
                depth=1,
                single_branch=True,
            )
            return f"{name} успешно установлен"
        except GitCommandError as e:
            return f"Ошибка при клонировании репозитория: {str(e)}"
        except Exception as e:
            return f"Ошибка при установке модуля: {str(e)}"

    def update(self):
        """
        Обновляет все модули.

        Returns:
            str: Сообщение об успешном обновлении.
        """
        try:
            for module_folder in os.listdir(LOCAL_FOLDER_PATH):
                module_path = os.path.join(LOCAL_FOLDER_PATH, module_folder)
                if os.path.isdir(module_path):
                    repo = git.Repo(module_path)
                    origin = repo.remote(name="origin")
                    origin.pull()
            return "Модули успешно обновлены"
        except NoSuchPathError as e:
            return f"Ошибка: {str(e)}"
        except GitCommandError as e:
            return f"Ошибка при обновлении репозитория: {str(e)}"
        except Exception as e:
            return f"Ошибка при обновлении модулей: {str(e)}"

    def remove(self, name: str):
        """
        Удаляет модуль.

        Args:
            name (str): Имя папки модуля для удаления.

        Returns:
            str: Сообщение об успешном удалении.
        """
        try:
            module_path = os.path.join(LOCAL_FOLDER_PATH, name)
            if os.path.exists(module_path):
                shutil.rmtree(module_path)
                return f"Модуль {name} успешно удален"
            else:
                return f"Модуль {name} не найден"
        except Exception as e:
            return f"Ошибка при удалении модуля: {str(e)}"


# Пример использования:
if __name__ == "__main__":
    installer = ModuleInstaller()
    module_name = "example_module"
    print(installer.install(module_name))
    print(installer.update())
    print(installer.remove(module_name))
