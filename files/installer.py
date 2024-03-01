for pv[get_pid()]["filee"] in ["camera.lja", "camera.py"]:
    be.based.run("cp " + vr("filee") + " /bin/" + vr("filee"))

be.based.run("cp camera.txt /usr/share/help/camera.txt")

be.api.setvar("return", "0")
