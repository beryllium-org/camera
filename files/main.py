rename_process("camera")
import espcamera

vr("opts", be.api.xarg())

vr(
    "dev",
    cptoml.fetch("device", toml=be.api.fs.resolve("/etc/camera.d/config.toml")),
)

if "init" in vr("opts")["o"] or "i" in vr("opts")["o"]:
    be.api.subscript("/bin/camera/init.py")

if "capture" in vr("opts")["o"] or "c" in vr("opts")["o"]:
    be.api.subscript("/bin/camera/capture.py")

if "serve" in vr("opts")["o"] or "s" in vr("opts")["o"]:
    be.api.subscript("/bin/camera/serve.py")

if "deinit" in vr("opts")["o"] or "d" in vr("opts")["o"]:
    be.api.setvar("return", "1")
    if vr("dev") not in be.devices:
        term.write("Camera not initialized!")
    else:
        try:
            be.devices[vr("dev")][0].deinit()
        except:
            pass
        be.based.run(
            "rmnod " + vr("dev") + ("_" if vr("dev")[-1].isdigit() else "") + "0"
        )
        term.write("Camera deinitialized successfully.")
        be.api.setvar("return", "0")

if not len(vr("opts")["o"]) or "h" in vr("opts")["o"] or "help" in vr("opts")["o"]:
    be.based.run("cat /usr/share/help/camera.txt")
    be.api.setvar("return", "0")
