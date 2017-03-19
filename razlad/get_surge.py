"""
Модуль формирования скачков
"""
import numpy as np

class FormSurge:
    """ Класс для формирования скачков """

    def __init__(self):
        """ Инициализация класса """
        self.cur_surge = 0
        self.num_surge = 3

    def get_surge(self):
        """Функция, возвращающая при каждом вызове очередной скачок"""
        if self.cur_surge == 0:
            """Первый скачок - скачок постоянной составляющей.
            Без входных аргументов. На выходе список на 1000 элементов."""
            surge = [0] * 500
            surge.extend([1]*500)
            self.cur_surge += 1
            return surge, 'Скачок постоянной составляющей'
        elif self.cur_surge == 1:
            len_surge = 100
            surge = [0] * ((1000 - len_surge)//2)
            surge.extend([1] * len_surge)
            surge.extend([0] * ((1000 - len_surge)//2))
            self.cur_surge += 1
            return surge, 'Кратковременный скачок постоянной составляющей'
        elif self.cur_surge == 2:
            len_surge = 100
            surge = [0] * ((1000 - len_surge) // 2)
            surge.extend([x/len_surge for x in range(len_surge)])
            surge.extend([1] * ((1000 - len_surge) // 2))
            self.cur_surge += 1
            return surge, 'Линейное изменение постоянной составляющей'
        else:
            return None, None

if __name__ == '__main__':
    """Функция служит для тестирования модуля"""
    cl = FormSurge()
    surge_ = cl.get_surge()
