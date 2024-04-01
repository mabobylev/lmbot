import pyautogui as pg


class AutoClicker:
    ICON_PATHS = {
        "fury": "icons/fury.png",
        "attack": "icons/attack.png",
        "map": "icons/main_page.png",
        "castle": "icons/outside_page.png",
        "sheeld": "icons/sheeld.png",
        "quests": "icons/quests.png",
        "hands": "icons/hands.png",
        "chest": ["icons/chest.png", "icons/chest1.png"],
        "quest_g": ["icons/quest_g.png", "icons/questg_a.png"],
        "quest_d": ["icons/quest_d.png", "icons/questd_a.png"],
    }
    CLICK_COORDINATES = {
        "sheeld": (1480, 550, 2, 1.5),
        "hands": (665, 995, 1, 1),
        "chest": (960, 810, 1, 1),
        "quest_g": (1655, 430, 8, 1),
        "quest_d": (1655, 430, 9, 1),
    }
    REGIONS = {
        "quests": (815, 100, 1110, 160),
        "castle": (40, 900, 1050, 220),
        "map": (40, 900, 1050, 220),
        "attack": (1560, 100, 1695, 235),
        "shield": (1800, 320, 1915, 430),
        "fury": (1800, 320, 1915, 430),
    }

    SLEEP_INTERVAL = 1
    ACTIONS_DEFENCE = ["sheeld"]
    ACTIONS_DEFAULT = ["hands", "chest"]
    ACTIONS_QUESTS = ["quest_g", "quest_d"]
    SPECIAL_ACTIONS = ["hands", "quest_d"]

    def __init__(self):
        self.actions = self.ACTIONS_DEFAULT

    def click_on_icon(
        self,
        icon_paths,
        clicks=1,
        interval=0.5,
        button="left",
        x_offset=0,
        y_offset=0,
        grayscale=True,
        confidence=0.9,
    ):
        if not isinstance(icon_paths, list):
            icon_paths = [icon_paths]
        for icon_path in icon_paths:
            try:
                coords_center = pg.locateCenterOnScreen(
                    icon_path, grayscale=grayscale, confidence=confidence
                )
                if coords_center:
                    pg.click(
                        coords_center[0] + x_offset,
                        coords_center[1] + y_offset,
                        clicks=clicks,
                        interval=interval,
                        button=button,
                    )
                    return True
            except Exception:
                print("Нечего выполнять")
        return False

    def perform_action(self, action_name):
        if self.click_on_icon(self.ICON_PATHS[action_name], confidence=0.97):
            if action_name in self.CLICK_COORDINATES:
                x, y, clicks, interval = self.CLICK_COORDINATES[action_name]
                pg.click(x, y, clicks=clicks, interval=interval)
                pg.sleep(self.SLEEP_INTERVAL)
                if action_name in self.SPECIAL_ACTIONS:
                    pg.press("esc")
                if action_name in self.ACTIONS_DEFENCE:
                    pg.click(1110, 500)
            print(f'Выполняем: {action_name.replace("_", " ").capitalize()}')

    def check_events(self, icon, region) -> bool:
        try:
            pg.locateOnScreen(icon, region, grayscale=True, confidence=0.9)
            return True
        except Exception:
            return False

    def main_loop(self):
        while True:
            # Проверяем находимся ли мы на главной странице или на странице квестов
            if self.check_events(
                self.ICON_PATHS["map"], self.REGIONS["map"]
            ) or self.check_events(self.ICON_PATHS["castle"], self.REGIONS["castle"]):
                # Если да, то выполняем действия по умолчанию
                self.actions = self.ACTIONS_DEFAULT
                # Если нет запала:
                if not self.check_events(self.ICON_PATHS["fury"], self.REGIONS["fury"]):
                    # Проверяем, если идет атака и нет щита, то меняем действия на защиту
                    if self.check_events(
                        self.ICON_PATHS["attack"], self.REGIONS["attack"]
                    ) and not self.check_events(
                        self.ICON_PATHS["sheeld"], self.REGIONS["sheeld"]
                    ):
                        self.actions = self.ACTIONS_DEFENCE
            # Если на странице квестов, то выполняем действия по квестам
            elif self.check_events(self.ICON_PATHS["quests"], self.REGIONS["quests"]):
                self.actions = self.ACTIONS_QUESTS
            # Выполняем действия
            for action in self.actions:
                self.perform_action(action)

            pg.sleep(
                self.SLEEP_INTERVAL
            )  # Адаптивная задержка может быть добавлена здесь

            # Возможно, добавить условие для смены действий или проверки страницы квестов


if __name__ == "__main__":
    try:
        auto_clicker = AutoClicker()
        auto_clicker.main_loop()
    except KeyboardInterrupt:
        print("Работа прервана пользователем")
