import pyautogui as pg
# from time import sleep


def locate_mouse():
    try:
        while True:
            x, y = pg.position()
            positionStr = "X: " + str(x).rjust(4) + " Y: " + str(y).rjust(4)
            print(positionStr, end="")
            print("\b" * len(positionStr), end="", flush=True)
    except KeyboardInterrupt:
        print("\n")


def screenShot():
    pg.screenshot("pics/lm_take_sheeld_fs.png")


def locate_img():
    pg.sleep(3)
    try:
        coords_center = pg.locateCenterOnScreen(
            "icons/quests.png",
            grayscale=True,
            confidence=0.9,
            region=(815, 100, 1110, 160),
        )
        # pg.click(coords_center[0],coords_center[1])
        print(coords_center)
    except Exception as e:
        print(f"Image not found: {e}")


pg.sleep(3)
screenShot()
# locate_img()
# locate_mouse()

# --------------------------------------------------------------------------------
# Coordinates of icons
# --------------------------------------------------------------------------------
# hands - x: 1865 y: 868, region = (1800, 780, 1920, 890)
# sheeld - x: 1866, y: 381, region = (1800, 320, 1915, 430)
# main_page: x: 125, y: 985,  region = (40, 900, 1050, 220)
# quests: x: 963, y: 135, region=(815, 100, 1110, 160)
