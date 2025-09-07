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

label rm_add_project():
    call screen RMAddProject()

    # $ renpy.restart_interaction()
    return