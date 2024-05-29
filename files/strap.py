for i in ["camera.lja", "camera.py"]:
    shutil.copyfile(i, path.join(root, "bin", i))

shutil.copyfile("camera.txt", path.join(root, "usr/share/help", "camera.txt"))
