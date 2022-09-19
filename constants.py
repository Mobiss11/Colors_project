class SizesWindow:
    SIZE_MAIN_SCREEN = "zoomed"


class ButtonsWindow:
    BUTTON_SEND = "Отправить в таблицу"
    BUTTON_CLOSE = "Закрыть"
    BUTTON_RESET = "Cбросить Градиент"
    BUTTON_MISS = "Переключить"
    BUTTON_SORT = "Сортировать"
    CHANGE_BUTTON_COLOR_GRADIENT = 'Измените тон в окне градиента'
    CHANGE_BUTTON_FIRST_COLOR = 'Измените тон в первом маленьком окне'
    CHANGE_BUTTON_SECOND_COLOR = 'Измените тон во втором маленьком окне'
    CHANGE_BUTTON_THIRD_COLOR = 'Измените тон в третьем маленьком окне'
    SORTING_REGION = ['RU', 'EN', 'ES', 'UA']


class SettingsFontWindow:
    TITLE_FONT = 'Calibri 10'
    BUTTONS_FONT = 'Corbel 10'
    FIRST_FONT_COLOR = "black"
    SECOND_FONT_COLOR = "white"
    FONT_SELECT_BUTTON = ('Corbel', 9)


class ElementsColorWindow:
    BACKGROUND_COLOR_BUTTON = "#931e9f"
    BACKGROUND_COLOR_INNER_WINDOW = '#ffffff'
    HEX_ENCODING = "#%02x%02x%02x"


class TitlesWindow:
    TITLE_IMAGE = "Изображение:"
    TEXT_AFTER_SORTING = f"Сортировка закончена\nПерезагрузите программу"


class SettingsCanvas:
    CANVAS_CONSTANT = "#%4.4x%4.4x%4.4x"
    CONFIG = "<Configure>"
    ORIENT = "vertical"
    TAG_FRAME = "gradient"


class CommandsDb:
    COMMAND_INSERT_GRADIENT = "INSERT INTO gradient_colors VALUES (?)"
    COMMAND_INSERT_FIRST_COLOR = "INSERT INTO first_color VALUES (?)"
    COMMAND_INSERT_SECOND_COLOR = "INSERT INTO second_color VALUES (?)"
    COMMAND_INSERT_THIRD_COLOR = "INSERT INTO third_color VALUES (?)"
    COMMAND_INSERT_SORTING_IMAGE = "INSERT INTO sorting_images VALUES (?,?)"

    COMMAND_SELECT_GRADIENT = "SELECT color from gradient_colors"
    COMMAND_SELECT_FIRST_COLOR = "SELECT color from first_color"
    COMMAND_SELECT_SECOND_COLOR = "SELECT color from second_color"
    COMMAND_SELECT_THIRD_COLOR = "SELECT color from third_color"
    COMMAND_SELECT_SORTING_IMAGE = "SELECT * FROM sorting_images ORDER BY number_sort COLLATE NOCASE ASC"

    COMMAND_DELETED_GRADIENT_COLOR = "DELETE FROM gradient_colors;"
    COMMAND_DELETED_FIRST_COLOR = "DELETE FROM first_color;"
    COMMAND_DELETED_SECOND_COLOR = "DELETE FROM second_color;"
    COMMAND_DELETED_THIRD_COLOR = "DELETE FROM third_color;"
    COMMAND_DELETED_SORTING_IMAGE = "DELETE FROM sorting_images;"
    COMMAND_DELETED_IMAGE = "DELETE from sorting_images WHERE image=(?)"
