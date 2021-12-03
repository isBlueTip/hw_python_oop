class InfoMessage:
    """Информационное сообщение о тренировке."""
    pass


class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65  # meters in one step
    M_IN_KM = 1000  # meters in one kilometer

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""

        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        pass


class Running(Training):
    """Тренировка: бег."""
    pass


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    pass


class Swimming(Training):
    """Тренировка: плавание."""

    def __init__(self, action: int, duration: float, weight: float, length_pool: int, count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    pass


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    workout_dict = {'SWM': Swimming,
                    'RUN': Running,
                    'WLK': SportsWalking}
    print(workout_dict ['SWM'])
    session_1 = (workout_dict[workout_type])(data)
    print(session_1)
    return session_1


def main(training: Training) -> None:
    """Главная функция."""
    pass


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),  # количество гребков, время в часах, вес пользователя, длина бассейна, сколько раз пользователь переплыл бассейн.
        ('RUN', [15000, 1, 75]),  # количество шагов, время тренировки в часах, вес пользователя.
        ('WLK', [9000, 1, 75, 180]),  # количество шагов, время тренировки в часах, вес пользователя, рост пользователя.
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        # main(training)

