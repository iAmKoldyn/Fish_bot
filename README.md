**Установка виртуального окружения и зависимостей**:
Выполнить в терминале в главном каталоге проекта (или в терминаме PyCharm):
- Добавить виртуальное окружение: **python -m venv venv**
- Активировать окружение: **venv\Scripts\activate.bat**
- Установить все зависимости: **pip install -r requirements.txt**


**Запуск**
- В `main.py` указываем `win_name="Название отслеживаемого окна"`
- `hsv_filter=None` для активации трекбара HCV
- Комментируем строки 26-28 чтобы не было сучайного срабатывания мыши
- Через main.py запускаем бота
- По окну `Processed` настраиваем изображение так, чтобы оно выделяло необходимую облать как можно точнее
- По завершению настроек в `main.py` заполняем `hsv_filter=HsvFilterDTO` значениями, которые плучились в трекбаре HCV
- Останавливаем бота
- Раскомментируем строки 26-28
- В `fish_main.py` `self.control.press_key("4")` указываем клавишу заброса поплавка
- Запускаем бота
- Кликаем по окну игры, забрасываем поплавок
- Бот должен определять поплавок корректно выделяя область. Когда поплавок клюет, наводить мышь и кликать ПКМ

- Чтобы не отображались окна трекбара. Коммент на строку `self._trackbar = self._f_main.vision.init_trackbar_gui()` в `fish_single.py`. Снять коммент со строки `self._trackbar = True`
- Чтобы не отображались окна настройки. Коммент строк `self.vision.show_debug_window` в `fish_main.py`