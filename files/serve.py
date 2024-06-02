be.api.setvar("return", "1")
if vr("dev") not in be.devices:
    term.write("Camera not initialized.")
else:
    be.api.setvar("return", "0")
