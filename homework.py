from typing import Dict, Type
from dataclasses import dataclass

MINS_IN_HOUR = 60


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    TRAINING_INFO_MESSAGE = ('Тип тренировки: {0.training_type}; '
                             'Длительность: {0.duration:.3f} ч.; '
                             'Дистанция: {0.distance:.3f} км; '
                             'Ср. скорость: {0.speed:.3f} км/ч; '
                             'Потрачено ккал: {0.calories:.3f}.'
                             )

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self):
        """Method for creating human readable
        str for a specific workout."""
        return self.TRAINING_INFO_MESSAGE.format(self)


@dataclass
class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65  # meters in one step
    M_IN_KM = 1000  # meters in one kilometer

    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""

        return (self.action * self.LEN_STEP) / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        return self.get_distance() / self.duration

    def get_spent_calories(self):
        """Get calories spent during a workout.
        The method must be overridden in every child class."""

        raise NotImplementedError('get_spent_calories()'
                                  'must be defined in %s class'
                                  % type(self).__name__
                                  )

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


@dataclass
class Running(Training):
    """Тренировка: бег."""

    RUN_CAL_COEFF_1 = 18
    RUN_CAL_COEFF_2 = 20

    action: int
    duration: float
    weight: float

    def get_spent_calories(self) -> float:
        """Count calories burnt during the session."""

        return ((self.RUN_CAL_COEFF_1 * self.get_mean_speed()
                - self.RUN_CAL_COEFF_2)
                * self.weight
                / self.M_IN_KM
                * self.duration * MINS_IN_HOUR
                )


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    WALK_CAL_COEFF_1 = 0.035
    WALK_CAL_COEFF_2 = 2
    WALK_CAL_COEFF_3 = 0.029

    action: int
    duration: float
    weight: float
    height: int

    def get_spent_calories(self) -> float:
        """Count calories burnt during the session."""

        return ((self.WALK_CAL_COEFF_1 * self.weight
                + (self.get_mean_speed()**self.WALK_CAL_COEFF_2 // self.height)
                * self.WALK_CAL_COEFF_3 * self.weight)
                * self.duration * MINS_IN_HOUR
                )


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38  # meters in one stroke
    SWM_CAL_COEFF_1 = 1.1
    SWM_CAL_COEFF_2 = 2

    action: int
    duration: float
    weight: float
    length_pool: int
    count_pool: int

    def get_mean_speed(self) -> float:
        """Count average speed during the session."""

        return (((self.length_pool
                * self.count_pool)
                / self.M_IN_KM)
                / self.duration
                )

    def get_spent_calories(self) -> float:
        """Count calories burnt during the session."""

        return ((self.get_mean_speed()
                + self.SWM_CAL_COEFF_1)
                * self.SWM_CAL_COEFF_2
                * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные, полученные от датчиков
    и создать объект соответствующего класса."""

    # Dict to decipher a workout code from fitness-module
    workout_dict_type = Dict[str, Type[Training]]
    workout_dict: workout_dict_type = {'SWM': Swimming,
                                       'RUN': Running,
                                       'WLK': SportsWalking
                                       }

    # The creation of Training class instance
    workout_class = workout_dict.get(workout_type)
    if workout_class is None:
        raise KeyError(f'Sorry. <{workout_type}> is undefined workout type.')
    try:
        workout_session = workout_class(*data)
    except TypeError:
        print(f'Sorry, an error has occurred. Please check '
              f'that the correct number of data elements  '
              f'is passed to <{workout_dict.get(workout_type).__name__}> '
              f'class instance.')
    else:
        return workout_session


def main(training: Training) -> None:
    """Главная функция."""

    # The creation of MessageInfo class instance for a specific workout
    info = training.show_training_info()
    # Print str of human-readable data for a corresponding Training instance
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        # количество гребков, время в часах, вес пользователя,
        # длина бассейна, сколько раз пользователь переплыл бассейн
        ('SWM', [720, 1, 80, 25, 40]),
        # количество шагов, время тренировки в часах, вес пользователя.
        ('RUN', [15000, 1, 75]),
        # количество шагов, время тренировки в часах,
        # вес пользователя, рост пользователя.
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        # Passing of Training class instance to the main function
        main(training)
