init python in const:
    PATH = r"^\s*(?!@)([^\[\n]+?)(?:\s*\[([^\]]+)\])?$"
    COMMENT = r"\s*(?<!<)#(?!>).*"

    FOLDER = ("FOLDER", r"^@folder:")
    RENPY = ("RENPY", r"^@renpy:")
    UNITY = ("UNITY", r"^@unity:")
    GODOT = ("GODOT", r"^@godot:")
    RPGM = ("RPGM", r"^@rpgm:")

    SYMBOLS = (FOLDER, RENPY, UNITY, GODOT, RPGM)

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
            self.projects_map = {"projects": [], "renpy": [], "unity": [], "godot": [], "rpgm": []}
            self.engines = {"renpy": True, "unity": False, "godot": False, "rpgm": False}
            self.query_input = ""
        
        @property
        def projects(self) -> list:
            all_projects = sum(self.projects_map.values(), start=[])
            projects = []

            for key in self.engines:
                if self.engines[key]: projects.extend(self.projects_map[key])

            projects = [p for p in projects if self.query_input in p.name]

            return projects

        def refresh(self):
            renpy.restart_interaction()

        def clear_projects_map(self):
            self.projects_map = {"projects": [], "renpy": [], "unity": [], "godot": [], "rpgm":  []}

        def find_projects(self):
            with open(os.path.join(config.basedir, "projects.txt"), "a+") as fl:
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
            self.executers = {}

            self._icon = None
            self._thumbnail = None

        def update(self, **kwargs):
            for (key, value) in kwargs.items():
                setattr(self, key, value)

        def __repr__(self):
            return self.name

        @property
        def execute(self):
            return self.executers.get(self.execute_mode, "")

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

            if os.path.exists(rm_folder_path):
                for file in os.listdir(rm_folder_path):
                    if file == "icon.png":
                        self._icon = os.path.join(rm_folder_path, file)
                        if os.name == "posix":
                            self._icon = SNARKY_PREFIX + self.icon

                    elif file == "rm_thumbnail.png":
                        self._thumbnail = os.path.join(rm_folder_path, file)

            if self._thumbnail is None:
                self._thumbnail = "gradient_1"

        @property
        def caller_exists(self) -> bool:
            return True
    
        @property
        def thumbnail(self) -> str:
            if os.name == "posix" and self._icon is not None:
                return self.snarky_pref(self._thumbnail)
            return self._thumbnail

        @property
        def icon(self) -> str:
            if os.name == "posix" and self._icon is not None:
                return self.snarky_pref(self._icon)
            return self._icon

        def snarky_pref(self, line: str):
            if persistent.rm_snark_hack:
                return SNARKY_PREFIX + line
            return line

    class LaunchAction(Action):
        def __init__(self, project: Project):
            self.project = project

        def __call__(self):
            try:
                cmd = [self.project.execute]

                process = subprocess.Popen(cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )

            except:
                renpy.notify("Could not launch project.")

            renpy.restart_interaction()

        def get_sensitive(self) -> bool:
            return self.project.caller_exists

        def get_selected(self) -> bool:
            return self.project.selected
    
    class RefreshManager(Action):
        def __call__(self):
            Manager.clear_projects_map()
            Manager.find_projects()
            renpy.restart_interaction()

    class CacheProjects(Action):
        def __call__(self):
            renpy.notify("Saving projects...")
            
    def filter_paths(lines: list[str]) -> list[str]:
        return [x.rstrip() for x in lines if (not match(r"\s+$", x) and not match(const.COMMENT, x))]
    
    def match2(pattern: str, line: str):
        return re.match(pattern, line)

    def match(pattern: str, line: str) -> bool:
        return re.match(pattern, line) is not None

    def matchs(patterns: tuple[str], line: str, old_symbol) -> str | None:
        for (key, pattern) in patterns:
            if match(pattern, line):
                return key

        return old_symbol

    Manager = ProjectManager()
    Manager.find_projects()