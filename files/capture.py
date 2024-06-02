be.api.setvar("return", "1")
if vr("dev") not in be.devices:
    term.write("Camera not initialized.")
else:
    vr("photo_data", be.devices[vr("dev")][0].take(0.4))
    vr("ql", be.devices[vr("dev")][0].quality)
    while not isinstance(vr("photo_data"), memoryview):
        if be.devices[vr("dev")][0].quality < 20:
            be.devices[vr("dev")][0].quality += 1
        vr("photo_data", be.devices[vr("dev")][0].take(0.4))
    term.write(
        'Snapped! Quality={}\nSaving to "'.format(be.devices[vr("dev")][0].quality),
        end="",
    )
    be.devices[vr("dev")][0].quality = vr("ql")
    vr("tt", time.localtime())
    vr(
        "branding",
        cptoml.fetch(
            "branding",
            toml=be.api.fs.resolve("/etc/camera.d/config.toml"),
        ),
    )
    vr("pic_name", vr("branding") + "-")
    if vr("tt").tm_mday < 10:
        vrp("pic_name", "0")
    vrp("pic_name", str(vr("tt").tm_mday) + "-")
    if vr("tt").tm_mon < 10:
        vrp("pic_name", "0")
    vrp("pic_name", str(vr("tt").tm_mon) + "-" + str(vr("tt").tm_year) + "-")
    if vr("tt").tm_hour < 10:
        vrp("pic_name", "0")
    vrp("pic_name", str(vr("tt").tm_hour) + "-")
    if vr("tt").tm_min < 10:
        vrp("pic_name", "0")
    vrp("pic_name", str(vr("tt").tm_min) + "-")
    if vr("tt").tm_sec < 10:
        vrp("pic_name", "0")
    vrp("pic_name", str(vr("tt").tm_sec) + ".jpeg")
    term.write(vr("pic_name") + '"...')
    if "dry-run" not in vr("opts")["o"]:
        with be.api.fs.open(vr("pic_name"), "wb") as pv[get_pid()]["f"]:
            vr("f").write(vr("photo_data"))
    term.write("Saved!")
    be.api.setvar("return", "0")
