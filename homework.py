
MINS_IN_HOUR = 60  # minutes in one hour
# M_IN_KM = 1000  # meters in one kilometer


class InfoMessage:
    """Информационное сообщение о тренировке."""
    # workout_type_dict = {'Swimming': 'плавание',
    #                      'Running': 'бег',
    #                      'SportsWalking': 'спортивная ходьба'
    #
    #                      }

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        """Method for creating human readable
        str for a specific workout."""

        return (f'Тип тренировки: '
                # f'{self.workout_type_dict [self.training_type]}; '
                f'{self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.'
                )


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

        return (self.action * self.LEN_STEP) / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    def __init__(self, action: int,
                 duration: float,
                 weight: float) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Count calories burnt during the session."""

        run_cal_coeff_1 = 18
        run_cal_coeff_2 = 20
        return ((run_cal_coeff_1 * self.get_mean_speed()
                 - run_cal_coeff_2)
                * self.weight
                / self.M_IN_KM
                * self.duration * MINS_IN_HOUR
                )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 height: int,) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Count calories burnt during the session."""

        walk_cal_coeff_1 = 0.035
        walk_cal_coeff_2 = 2
        walk_cal_coeff_3 = 0.029
        return ((walk_cal_coeff_1 * self.weight
                + (self.get_mean_speed()**walk_cal_coeff_2 // self.height)
                * walk_cal_coeff_3 * self.weight)
                * self.duration * MINS_IN_HOUR
                )


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38  # meters in one stroke

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Count average speed during the session."""

        return (((self.length_pool
                * self.count_pool)
                / self.M_IN_KM)
                / self.duration
                )

    def get_spent_calories(self) -> float:
        """Count calories burnt during the session."""

        swm_cal_coeff_1 = 1.1
        swm_cal_coeff_2 = 2
        return ((self.get_mean_speed()
                + swm_cal_coeff_1)
                * swm_cal_coeff_2
                * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные, полученные от датчиков
    и создать объект соответствующего класса."""

    workout_dict = {'SWM': Swimming,  # Dict to decipher a workout code from fitness-module
                    'RUN': Running,
                    'WLK': SportsWalking
                    }

    workout_session = workout_dict[workout_type](*data)  # The creation of Training class instance
    return workout_session  # Return a workout instance


def main(training: Training) -> None:
    """Главная функция."""

    info = training.show_training_info()  # The creation of MessageInfo class instance for a specific workout
    print(info.get_message())  # Print str of human-readable data for a corresponding Training instance


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),  # количество гребков, время в часах, вес пользователя, длина бассейна, сколько раз пользователь переплыл бассейн.
        ('RUN', [15000, 1, 75]),  # количество шагов, время тренировки в часах, вес пользователя.
        ('WLK', [9000, 1, 75, 180]),  # количество шагов, время тренировки в часах, вес пользователя, рост пользователя.
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)  # Passing of Training class instance to the main function
