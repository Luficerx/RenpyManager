label rm_crop_thumbnail(message, project, thumbnail):
    call screen RMYesNo(message)

    if _return:
        call screen RMThumbnailCrop(thumbnail, project)
        $ _return.save_thumbnail()
        $ project._thumbnail = _return.thumb_path

    else:
        $ project._thumbnail = thumbnail

    $ renpy.restart_interaction()
    return

label rm_add_project:
    python:
        games_folder = config.gamedir

        if persistent.rm_default_games_folder is not None:
            games_folder = persistent.rm_default_games_folder

        folder_path = RenpyManager._renpytfd.selectFolderDialog("Select Default Game Folder", games_folder)
        if folder_path is not None:

            project = RenpyManager.Project()
            project.folder_path = folder_path
            project.update()

            project = renpy.call_screen("RMAddProject", project=project)

            if project is not None:
                RenpyManager.Manager.add_project(project)

                if persistent.rm_save_on_add:
                    renpy.run(RenpyManager.CacheProjects())

            renpy.restart_interaction()
    return