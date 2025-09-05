init python in const:
    PATH = r"^\s*(?!@)([^\[\n]+?)(?:\s*\[([^\]]+)\])?$"
    COMMENT = r"\s*(?<!<)#(?!>).*"

    DIRECTIVES = ("projects", "renpy", "unity", "unreal", "godot", "rpgm")
    
    SYMBOLS = tuple([(x.upper(), fr"^@{x}:") for x in DIRECTIVES])

    IGNORE_NAME = ("notification_helper", "crashpad_handler", "UnityCrashHandler64", "UnityCrashHandler32")
    
    VALID_FMT = ("exe", "sh", "py")

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
    import os, re, subprocess, pathlib, shutil, json

    # HACK: This is the most satanic way of fixing a renpy system problem.
    SNARKY_PREFIX = "../" * len(list(filter(lambda x: x, config.gamedir.split("/"))))

    class ProjectManager():
        def __init__(self):
            self.project = None

            self.projects_map = {"projects": [], "renpy": [], "unity": [], "godot": [], "rpgm": [], "unreal": []}
            self.search = ""

            self.cache_projects = self.get_projects_from_cache()
            self.stars_query = 0.0
        
        @property
        def engines(self) -> dict[str, bool]:
            return persistent.rm_engines

        @engines.setter
        def engines(self, value: dict[str, bool]) -> dict[str, bool]:
            persistent.rm_engines = value

        @property
        def others(self):
            return persistent.rm_others

        @property
        def tags(self) -> dict[str, bool]:
            return persistent.rm_tags

        @property
        def tags_az(self) -> list[str]:
            a = list(persistent.rm_tags)
            a.sort()
            return a

        @tags.setter
        def tags(self, value: dict[str, bool]) -> dict[str, bool]:
            persistent.rm_tags = value
            
        @property
        def projects(self) -> list:
            projects = []
            projects_by_tag = []

            tags = [x for x in self.tags if self.tags[x]]

            for key in self.engines:
                if self.engines[key]: projects.extend(self.projects_map[key])

            projects = [p for p in projects if self.search in p.name]

            if self.others["pinned"]:
                projects = [p for p in projects if p.pinned]
                
            if self.others["stars_query"]:
                projects = [p for p in projects if p.stars == self.stars_query]

            if tags:
                for project in projects:
                    for tag in tags:
                        if project.tags.get(tag):
                            projects_by_tag.append(project)
                            break
                
            if projects_by_tag:
                return projects_by_tag

            return projects

        def toggle_all_tags(self):
            if False in self.tags.values():
                self.tags = {k: True for k in self.tags}
            else:
                self.tags = {k: False for k in self.tags}

        def toggle_all_engines(self):
            if False in self.engines.values():
                self.engines = {k: True for k in self.engines}
            else:
                self.engines = {k: False for k in self.engines}

        def refresh(self):
            renpy.restart_interaction()

        def get_all_projects(self) -> list[Project]:
            return sum(self.projects_map.values(), start=[])

        def clear_projects_map(self):
            self.projects_map = {key: [] for key in const.DIRECTIVES}

        def find_projects(self):
            with open(os.path.join(config.basedir, "projects.txt"), "a+") as fl:
                fl.seek(0)
                symbol = None

                for path in filter_paths(fl.readlines()):
                    is_dir = os.path.isdir(path)

                    if is_dir:
                        project = Project()
                        project.path = path
                        project.update()

                        if path in self.cache_projects: project.setattrs(**self.cache_projects[path])
                        key = "projects" if project.engine == "Unknown" else project.engine
                        self.projects_map[key].append(project)
                        continue

                    match symbol:
                        case "PROJECTS":
                            re_match = match2(const.PATH, path)
                            if re_match:
                                path = re_match.group(1)

                                if os.path.exists(path):
                                    files = os.listdir(path)

                                    for file in files:
                                        full_path = os.path.join(path, file)
                                        if not os.path.isdir(full_path): continue
                                        if full_path in self.get_all_projects(): continue
                                        
                                        project = Project()
                                        project.path = full_path
                                        project.update()

                                        if full_path in self.cache_projects: project.setattrs(**self.cache_projects[full_path])
                                        key = "projects" if project.engine == "Unknown" else project.engine
                                        self.projects_map[key].append(project)

                        case "RENPY" | "UNITY" | "GODOT" | "RPGM" | "UNREAL" as value:
                            project = Project()
                            self.add_project(project, value.lower(), match2(const.PATH, path))

                        case None:
                            pass

                    current_symbol = matchs(const.SYMBOLS, path, symbol)

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
                if path in self.cache_projects: project.setattrs(**self.cache_projects[path])
        
        def move_project(self, project: Project):
            for key in self.projects_map:
                if project in self.projects_map[key][:]:
                    self.projects_map[key].remove(project)
                    self.projects_map[project.engine].append(project)

        def get_projects_from_cache(self) -> dict:
            with open(os.path.join(config.basedir, "cache_projects.json"), "a+") as fl:
                fl.seek(0)
                try:
                    cache_projects = json.load(fl)
                
                except:
                    cache_projects = {}
            
            return cache_projects

        def load_projects_from_cache(self):
            for project in self.get_all_projects():
                if project.path in self.cache_projects:
                    project.setattrs(**self.cache_projects[project.path])
                    self.move_project(project)

        def save_projects_to_cache(self):
            for project in self.get_all_projects():
                self.cache_projects[project.path] = vars(project)

        def has_project(self, project) -> bool:
            return project in self.get_all_projects()

    class Project():
        def __init__(self):
            self.name = "Unknown"
            self.description = "No Description Given."

            self.version = "Unknown"
            self.path = None
            
            self.stars = 0.0
            self.pinned = False
            self.tags = {}

            self.executers = {"custom": ""}
            self.execute_mode = None
            self.engine = "Unknown"
            self.args = ""

            self._logo = "logo_placeholder"
            self._thumbnail = "thumbnail_placeholder"

        def setattrs(self, **kwargs):
            for (key, value) in kwargs.items():
                setattr(self, key, value)

        @property
        def name_s(self):
            if len(self.name) > 22:
                return self.name[:19] + "..."
            return self.name

        def __repr__(self):
            return self.name

        def __eq__(self, other):
            if type(other) is Project:
                return self.path == other.path

            if type(other) is str:
                return self.path == other

            return False

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
                name, *fmt = file.split(".")
                if name in const.IGNORE_NAME: continue

                if fmt:
                    value = fmt[-1]
                    match value:
                        case "exe":
                            self.executers["exe"] = os.path.join(self.path, file)

                        case "py":
                            self.executers["py"] = os.path.join(self.path, file)

                        case "sh":
                            self.executers["sh"] = os.path.join(self.path, file)

            if self.execute_mode in ("exe", "py", "sh"):
                if self.execute != "Not Set.":
                    self.name = pathlib.Path(self.execute).stem

            self.update_thumbnail()

        def update_thumbnail(self):
            match self.engine: 
                case "renpy" | "unity" | "godot" as value:
                    self._thumbnail = f"{value}_thumbnail_placeholder"
                case _:
                    self._thumbnail = f"thumbnail_placeholder"
            
            if self.engine == "renpy":
                rm_folder_path = os.path.join(self.path, "game")

            else:
                rm_folder_path = os.path.join(self.path, "rm_project")
    
            if os.path.exists(rm_folder_path):
                for file in os.listdir(rm_folder_path):
                    if file == "icon.png":
                        self._logo = os.path.join(rm_folder_path, file)

                    elif file == "rm_thumbnail.png":
                        self._thumbnail = os.path.join(rm_folder_path, file)

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

        @property
        def execute(self):
            if persistent.rm_execute_mode is not None:
                if (value := self.executers.get(persistent.rm_execute_mode, None)) is not None:
                    return value
            return self.executers.get(self.execute_mode, "Not Found.")

        @property
        def execute_s(self):
            return os.path.basename(self.execute)

        @property
        def caller_exists(self) -> bool:
            return True

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
                    self.project.pinned = not self.project.pinned

            renpy.restart_interaction()

        def get_sensitive(self) -> bool:
            return self.project.caller_exists
    
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
            Manager.save_projects_to_cache()
            with open(os.path.join(config.basedir, "cache_projects.json"), "w+") as fl:
                json.dump(Manager.cache_projects, fl, indent=4)

    class SetProjectExecutable(Action):
        def __init__(self, project: Project, name: str, executable_path: str):
            self.executable_path = executable_path
            self.project = project
            self.name = name

        def __call__(self):
            self.project.executers["custom"] = self.executable_path
            self.project.execute_mode = "custom"
            if self.project.name == "Unknown":
                self.project.name = pathlib.Path(self.name).stem
            Manager.cache_projects[self.project.path] = vars(self.project)
            renpy.restart_interaction()

    class SetProjectEngine(Action):
        def __init__(self, project: Project, engine: str):
            self.project = project
            self.engine = engine

        def __call__(self):
            self.project.engine = self.engine
            self.project.update_thumbnail()
            Manager.move_project(self.project)
            renpy.restart_interaction()

    def FetchExecutables(project: Project) -> list[tuple[str, str]]:
        items = []

        def skip_file(file):
            file_name, *fmt = file.split(".")
            if file_name in const.IGNORE_NAME:
                return True

            if fmt and fmt[-1] not in const.VALID_FMT:
                return True

            return False

        match os.name:
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