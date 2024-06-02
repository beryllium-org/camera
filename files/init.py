be.api.setvar("return", "1")
if vr("dev") not in be.devices:
    vr("conft", be.api.fs.resolve("/etc/camera.d/config.toml"))
    if "mode" in vr("opts")["o"] or "m" in vr("opts")["o"]:
        if "mode" in vr("opts")["o"]:
            vr("mode", vr("opts")["o"]["mode"])
        else:
            vr("mode", vr("opts")["o"]["m"])
    else:
        vr(
            "mode",
            cptoml.fetch(
                "default_preset",
                toml=vr("conft"),
            ),
        )
    vr("pr", be.api.fs.resolve("/etc/camera.d/presets/" + vr("mode") + ".toml"))
    exec(
        'vr("px", espcamera.PixelFormat.'
        + cptoml.fetch(
            "pixel_format",
            toml=be.api.fs.resolve(vr("pr")),
        )
        + ")"
    )
    exec(
        'vr("fr", espcamera.FrameSize.'
        + cptoml.fetch(
            "frame_size",
            toml=be.api.fs.resolve(vr("pr")),
        )
        + ")"
    )
    vr(
        "qual",
        cptoml.fetch(
            "jpeg_quality",
            toml=be.api.fs.resolve(vr("pr")),
        ),
    )
    vr(
        "data_pins",
        cptoml.fetch(
            "data_pins",
            toml=vr("conft"),
        ),
    )
    vr(
        "pixel_clock_pin",
        cptoml.fetch(
            "pixel_clock_pin",
            toml=vr("conft"),
        ),
    )
    vr(
        "vsync_pin",
        cptoml.fetch(
            "vsync_pin",
            toml=vr("conft"),
        ),
    )
    vr(
        "href_pin",
        cptoml.fetch(
            "href_pin",
            toml=vr("conft"),
        ),
    )
    vr(
        "node",
        cptoml.fetch(
            "i2c",
            toml=vr("conft"),
        ),
    )
    vr("i2c", None)
    vr("ok", False)
    be.api.subscript("/bin/stringproccessing/devid.py")
    if (
        vr("ok")
        and vr("dev_name") in be.devices.keys()
        and vr("dev_name") == "i2c"
        and vr("dev_id") in be.devices[vr("dev_name")].keys()
    ):
        if be.devices[vr("dev_name")][vr("dev_id")].try_lock():
            be.devices[vr("dev_name")][vr("dev_id")].unlock()
            vr("i2c", be.devices[vr("dev_name")][vr("dev_id")])
        else:
            term.write("I2C bus in use!")
    else:
        term.write("Could not find system I2C bus.")
    vr(
        "external_clock_pin",
        cptoml.fetch(
            "external_clock_pin",
            toml=vr("conft"),
        ),
    )
    vr(
        "external_clock_frequency",
        cptoml.fetch(
            "external_clock_frequency",
            toml=vr("conft"),
        ),
    )
    vr(
        "powerdown_pin",
        cptoml.fetch(
            "powerdown_pin",
            toml=vr("conft"),
        ),
    )
    vr(
        "reset_pin",
        cptoml.fetch(
            "reset_pin",
            toml=vr("conft"),
        ),
    )
    if vr("i2c") is not None:
        vrd("node")
        be.based.run("mknod " + vr("dev"))
        vr("node", be.api.getvar("return"))
        be.api.subscript("/bin/stringproccessing/devid.py")
        be.devices[vr("dev_name")][vr("dev_id")] = espcamera.Camera(
            data_pins=be.devices["gpiochip"][0].pin(vr("data_pins"), force=True),
            pixel_clock_pin=be.devices["gpiochip"][0].pin(
                vr("pixel_clock_pin"), force=True
            ),
            vsync_pin=be.devices["gpiochip"][0].pin(vr("vsync_pin"), force=True),
            href_pin=be.devices["gpiochip"][0].pin(vr("href_pin"), force=True),
            i2c=vr("i2c"),
            external_clock_pin=be.devices["gpiochip"][0].pin(
                vr("external_clock_pin"), force=True
            ),
            external_clock_frequency=vr("external_clock_frequency"),
            powerdown_pin=be.devices["gpiochip"][0].pin(
                vr("powerdown_pin"), force=True
            ),
            reset_pin=be.devices["gpiochip"][0].pin(vr("reset_pin"), force=True),
            pixel_format=vr("px"),
            frame_size=vr("fr"),
            jpeg_quality=vr("qual"),
            framebuffer_count=1,
            grab_mode=espcamera.GrabMode.LATEST,
        )
        term.write('Initializing camera on mode "' + vr("mode") + '"')
        be.devices[vr("dev")][0].vflip = cptoml.fetch(
            "flip",
            toml=be.api.fs.resolve(vr("pr")),
        )
        vr(
            "dn",
            cptoml.fetch(
                "denoise",
                toml=be.api.fs.resolve(vr("pr")),
            ),
        )
        if vr("dn"):
            be.devices[vr("dev")][0].denoise = vr("dn")
        be.devices[vr("dev")][0].awb_gain = cptoml.fetch(
            "awb_gain",
            toml=be.api.fs.resolve(vr("pr")),
        )
        sleep(0.5)
        be.devices[vr("dev")][0].take()
        term.write("Initialized!")
        be.api.setvar("return", "0")
else:
    term.write("Camera already initialized.")
