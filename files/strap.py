for i in ["camera.lja", "camera.py"]:
    shutil.copy(i, path.join(root, "bin", i))

shutil.copy("camera.txt", path.join(root, "usr/share/help", "camera.txt"))
