init python in const:
    PATH = r"^\s*(?!@)([^\[\n]+?)(?:\s*\[([^\]]+)\])?$"
    COMMENT = r"\s*(?<!<)#(?!>).*"

    FOLDER = ("FOLDER", r"^@folder:")
    RENPY = ("RENPY", r"^@renpy:")
    UNITY = ("UNITY", r"^@unity:")
    GODOT = ("GODOT", r"^@godot:")
    RPGM = ("RPGM", r"^@rpgm:")

    SYMBOLS = (FOLDER, RENPY, UNITY, GODOT, RPGM)
    IGNORE_FMT = (".txt",)

    THUMBNAIL_PLACEHOLDERS = (
        "thumbnail_placeholder",
        "renpy_thumbnail_placeholder",
        "unity_thumbnail_placeholder",
        "godot_thumbnail_placeholder"
    )

    LOGOS_PLACEHOLDERS = (
        "logo_placeholder",
        "renpy_logo_placeholder",
        "unity_logo_placeholder",
        "godot_logo_placeholder"
    )

init python in RenpyManager:
    from __future__ import annotations
    from renpy.store import Action, persistent, const
    from renpy import config
    import os, re, subprocess, pathlib, shutil

    # HACK: This is the most satanic way of fixing a renpy system problem.
    SNARKY_PREFIX = "../" * len(list(filter(lambda x: x, config.gamedir.split("/"))))

    if persistent.cached_projects is None:
        persistent.cached_projects = { }

    class ProjectManager():
        def __init__(self):
            self.project = None

            self.projects_map = {"projects": [], "renpy": [], "unity": [], "godot": [], "rpgm": []}
            self.engines = {"renpy": True, "unity": True, "godot": False, "rpgm": False}
            self.query = ""
        
        @property
        def projects(self) -> list:
            all_projects = sum(self.projects_map.values(), start=[])
            projects = []

            for key in self.engines:
                if self.engines[key]: projects.extend(self.projects_map[key])

            projects = [p for p in projects if self.query in p.name]

            return projects

        def refresh(self):
            renpy.restart_interaction()

        def clear_projects_map(self):
            self.projects_map = {"projects": [], "renpy": [], "unity": [], "godot": [], "rpgm":  []}

        def find_projects(self):
            with open(os.path.join(config.basedir, "projects.txt"), "a+") as fl:
                fl.seek(0)
                symbol = None

                for line in filter_paths(fl.readlines()):
                    value = os.path.isdir(line)
                    if value:
                        project = Project()
                        project.path = line
                        project.update()
                        self.projects_map["projects"].append(project)
                        continue

                    match symbol:
                        case "FOLDER":
                            re_match = match2(const.PATH, line)
                            if re_match:
                                path = re_match.group(1)

                                if os.path.exists(path):
                                    files = os.listdir(path)

                                    for file in files:
                                        full_path = os.path.join(path, file)
                                        project = Project()
                                        project.path = full_path
                                        project.update()
                                        self.projects_map["projects"].append(project)

                        case "RENPY":
                            project = Project()
                            self.add_project(project, "renpy", match2(const.PATH, line),)

                        case "UNITY" | "GODOT" | "RPGM" as value:
                            project = Project()
                            self.add_project(project, value.lower(), match2(const.PATH, line))

                        case None:
                            pass

                    current_symbol = matchs(const.SYMBOLS, line, symbol)

                    if current_symbol != symbol:
                        symbol = current_symbol
                        continue
    
        def add_project(self, project: Project, key: str, re_match):
            if re_match:
                path = re_match.group(1)
                args = re_match.group(2) or ""
                
                project.path = path
                project.args = args
                project.engine = key

                project.update()
                self.projects_map[key].append(project)
        
        def has_project(self, project):
            return (project in sum(self.projects_map.values(), start=[]))

    class Project():
        def __init__(self):
            self.name = "Unknown"
            self.path = None
            self.description = "No Description Given."
            self.stars = 0.0
            self.version = "Unknown"
            self.args = ""
            self.engine = None
            self.selected = False
            self.execute_mode = None
            self.executers = {"custom": ""}
            self.pin = False

            self._logo = "logo_placeholder"
            self._thumbnail = "thumbnail_placeholder"

        def update(self, **kwargs):
            for (key, value) in kwargs.items():
                setattr(self, key, value)

        def __repr__(self):
            return self.name

        def __eq__(self, other):
            if type(other) is Project:
                return self.path == other.path
            return False

        @property
        def execute(self):
            return self.executers.get(self.execute_mode, "Not Found.")

        @property
        def execute_s(self):
            return os.path.basename(self.execute)

        def update(self):
            match os.name:
                case "nt":
                    self.execute_mode = "exe"

                case "posix":
                    self.execute_mode = persistent.rm_execute_mode
                
                case _ as error:
                    raise Exception(f"This system is not supported or is unknown. {_}")
            
            base_folder = os.listdir(self.path)

            for file in base_folder:
                if file.endswith(".exe"):
                    self.executers["exe"] = os.path.join(self.path, file)

                elif file.endswith(".py"):
                    self.executers["py"] = os.path.join(self.path, file)

                elif file.endswith(".sh"):
                    self.executers["sh"] = os.path.join(self.path, file)
            
            match self.execute_mode:
                case "exe" | "py" | "sh" as key:
                    self.name = pathlib.Path(self.execute).stem

            if self.engine == "renpy":
                rm_folder_path = os.path.join(self.path, "game")

            else:
                rm_folder_path = os.path.join(self.path, "rm_project")

            self.thumbnail_by_engine()

            if os.path.exists(rm_folder_path):
                for file in os.listdir(rm_folder_path):
                    if file == "icon.png":
                        self._logo = os.path.join(rm_folder_path, file)

                    elif file == "rm_thumbnail.png":
                        self._thumbnail = os.path.join(rm_folder_path, file)

        @property
        def caller_exists(self) -> bool:
            return True
    
        @property
        def thumbnail(self) -> str:
            if persistent.rm_snark_hack and os.name == "posix" and self._thumbnail not in const.THUMBNAIL_PLACEHOLDERS:
                return (SNARKY_PREFIX + self._thumbnail)
            return self._thumbnail

        @property
        def logo(self) -> str:
            if persistent.rm_snark_hack and os.name == "posix" and self._logo not in const.LOGOS_PLACEHOLDERS:
                return (SNARKY_PREFIX + self._logo)
            return self._logo

        def thumbnail_by_engine(self):
            match self.engine:
                case "renpy": self._thumbnail = "renpy_thumbnail_placeholder"
                case "unity": self._thumbnail = "unity_thumbnail_placeholder"
                case "godot": self._thumbnail = "godot_thumbnail_placeholder"

    class Execute(Action):
        def __init__(self, project: Project, mode: str = "launch"):
            self.project = project
            self.mode = mode

        def __call__(self):
            match self.mode:
                case "launch":
                    try:
                        cmd = [self.project.execute]

                        process = subprocess.Popen(cmd,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            text=True,
                        )

                    except:
                        renpy.notify("Could not launch project.")

                case "pin":
                    self.project.pin = not self.project.pin

            renpy.restart_interaction()

        def get_sensitive(self) -> bool:
            return self.project.caller_exists

        def get_selected(self) -> bool:
            return self.project.selected
    
    class RefreshManager(Action):
        def __call__(self):
            Manager.clear_projects_map()
            Manager.find_projects()
            if Manager.project is not None and not Manager.has_project(Manager.project):
                Manager.project = None
            renpy.restart_interaction()

    class CacheProjects(Action):
        def __call__(self):
            renpy.notify("Saving projects...")

    class SetProjectExecutable(Action):
        def __init__(self, project: Project, name: str, executable_path: str):
            self.executable_path = executable_path
            self.project = project
            self.name = name
        
        def __call__(self):
            self.project.executers["custom"] = self.executable_path
            self.project.execute_mode = "custom"
            self.project.name = pathlib.Path(self.name).stem
            renpy.restart_interaction()

    def FetchExecutables(project: Project) -> list[tuple[str, str]]:
        items = []

        def skip_file(file):
            for fmt in const.IGNORE_FMT:
                if file.endswith(fmt):
                    return True

        match os.name:
            case "nt":
                pass

            case "posix":
                files = os.listdir(project.path)
                for file in files:
                    if skip_file(file): continue
                    
                    file_path = os.path.join(project.path, file)
                    if os.path.isfile(file_path) and os.access(file_path, os.X_OK):
                        items.append((file, file_path))

        return items

    def filter_paths(lines: list[str]) -> list[str]:
        return [x.rstrip() for x in lines if (not match(r"\s+$", x) and not match(const.COMMENT, x))]
    
    def matchs(patterns: tuple[str], line: str, old_symbol) -> str | None:
        for (key, pattern) in patterns:
            if match(pattern, line):
                return key

        return old_symbol

    def match(pattern: str, line: str) -> bool:
        return re.match(pattern, line) is not None

    def match2(pattern: str, line: str):
        return re.match(pattern, line)

    Manager = ProjectManager()
    Manager.find_projects()