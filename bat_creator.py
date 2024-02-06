class BatCreator:

    @staticmethod
    def create_bat_script(main_folder_path: str,
                          tags_folder_path: str = None,
                          tmp_folder_path: str = None,
                          tag_number: int = None) -> None:
        script = BatCreator.construct_bat_script(main_folder_path,
                                                 tags_folder_path,
                                                 tmp_folder_path,
                                                 tag_number)
        with open("tagger.bat", 'w') as file:
            file.write(script)

    @staticmethod
    def create_bat_script_folder(main_folder_path: str,
                          tags_folder_path: str = None,
                          tag_number: int = None) -> None:

        script = BatCreator.construct_bat_script_folder(main_folder_path,
                                                        tags_folder_path,
                                                        tag_number)
        with open("tagger_folder.bat", 'w') as file:
            file.write(script)

    @staticmethod
    def construct_bat_script(main_folder_path: str,
                             tags_folder_path: str = None,
                             tmp_folder_path: str = None,
                             tag_number: int = None) -> str:
        if main_folder_path is None:
            raise ValueError("Main folder path is required.")
        tags_folder_path = tags_folder_path if tags_folder_path else main_folder_path
        tmp_folder_path = tmp_folder_path if tmp_folder_path else main_folder_path
        tag_number = tag_number if tag_number else 5

        script = ("@echo off\n"
                  f"python {main_folder_path}\\main.py tag "
                  "-f \"%~1\" "
                  f"-t {tags_folder_path}\\tags.md "
                  f"-tn {tag_number} > "
                  f"{tmp_folder_path}\\output.txt\n"
                  f"type {tmp_folder_path}\\output.txt\n"
                  "pause\n"
                  f"del {tmp_folder_path}\\output.txt\n")
        return script

    @staticmethod
    def construct_bat_script_folder(main_folder_path: str,
                                    tags_folder_path: str = None,
                                    tag_number: int = None) -> str:

        if main_folder_path is None:
            raise ValueError("Main folder path is required.")
        tags_folder_path = tags_folder_path if tags_folder_path else main_folder_path
        tag_number = tag_number if tag_number else 4

        script = ("@echo off\n"
                  "setlocal enabledelayedexpansion\n"
                  "set \"exclude=\"\n"
                  "\n"
                  ":loop\n"
                  "if \"%~1\"==\"\" goto :continue\n"
                  "if \"%~1\"==\"--exclude\" set \"exclude=%~2\"\n"
                  "if \"%~1\"==\"-e\" set \"exclude=%~2\"\n"
                  "shift\n"
                  "goto :loop\n"
                  "\n"
                  ":continue\n"
                  "set \"count=0\"\n"
                  "set \"total=0\"\n"
                  "\n"
                  "for %%i in (*.md) do (\n    "
                  "set /a \"total+=1\"\n    "
                  "if /I not \"%%~nxi\"==\"%exclude%\" (\n        "
                  f"python {main_folder_path}\\main.py tag "
                  f"-f \"%%i\" "
                  f"-t {tags_folder_path}\\tags.md "
                  f"-tn {tag_number} > nul\n        "
                  f"set /a \"count+=1\"\n    "
                  f")\n    "
                  f"echo Processed !count! out of !total! files.\n"
                  f")\n"
                  f"\n"
                  f"endlocal")
        return script
