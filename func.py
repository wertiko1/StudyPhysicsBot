from random import choice, randint


class GenTask:
    def __init__(self):
        self.dict_physics = {
            'Ускорение': 'boost.png',
            'Средняя скорость': 'medium_speed.png',
            'Перемещение\nБез конечной скорости': 'displacement_not_endspeed.png',
            'Перемещение\nБез времени': 'displacement_not_time.png',
            'Перемещение\nБез ускорения': 'displacement_not_boost.png',
            'Проекция скорости\nПри равноускореном прямолинейном движении': 'projection_speed.png',
            'Первый закон Ньютона': 'one_law_niuton.png',
            'Второй закон Ньютона': 'two_law_niuton.png',
            'Третий закон Ньютона': 'three_law_niuton.png',
            'Сила трения': 'friction_force.png',
            'Сила упругости': 'strength_of_elasticity.png',
            'Сила тяжести': 'gravity.png',
            'Сила нормального давления': 'pressure_force.png',
            'Механическая работа': 'mechanical_work.png',
            'Мощность': 'power.png',
            'Вес тела': 'body_weight.png',
            'Кинетическая энергия': 'kinetic_energy.png',
            'Потенциальная энергия': 'potential_energy.png',
            'Полная механическая энергия': 'total_mechanical_energy.png',
            'Коэффициент полезного действия\n(КПД)': 'kpd.png',
            'Давление твердого тела': 'solid_body_pressure.png',
            'Гидростатическое давление': 'hydrostatic_pressure.png',
            'Полное давление': 'full_dressing.png',
            'Закон Архимеда': 'law_archimedes.png',
            'Сила Архимеда': 'power_archimedes.png',
            'Условие плавания тел\nВсплывает': 'swimming_bodies_float_up.png',
            'Условие плавания тел\nПлавает в толще жидкости': 'body_thickening_fluid.png',
            'Условие плавания тел\nТонет': 'body_sinking.png',
            'Условие плавания\nПлавает на поверхности жидкости': 'body_on_surface.png',
            'Нагревание/охлаждение': 'heating_cooling.png',
            'Плавление/кристаллизация': 'melting_crystallization.png',
            'Парообразование/конденсация': 'vaporization_condensation.png',
            'Сгорание топлива': 'fuel_burnout.png',
            'Коэффициент полезного действия\n(КПД) теплового двигателя': 'kpd_dv.png',
        }
        self.dict_physics_elem = {
            'Ускорение': 'boost_elem.png',
            'Средняя скорость': 'medium_speed_elem.png',
            'Перемещение\nБез конечной скорости': 'displacement_elem.png',
            'Перемещение\nБез времени': 'displacement_elem.png',
            'Перемещение\nБез ускорения': 'displacement_elem.png',
            'Проекция скорости\nПри равноускореном прямолинейном движении': 'projection_speed_elem.png',
            'Первый закон Ньютона': 'one_law_niuton_elem.png',
            'Второй закон Ньютона': 'two_law_niuton_elem.png',
            'Третий закон Ньютона': 'three_law_niuton_elem.png',
            'Сила трения': 'friction_force_elem.png',
            'Сила упругости': 'strength_of_elasticity_elem.png',
            'Сила тяжести': 'gravity_elem.png',
            'Сила нормального давления': 'pressure_force_elem.png',
            'Механическая работа': 'mechanical_work_elem.png',
            'Мощность': 'power_elem.png',
            'Вес тела': 'body_weight_elem.png',
            'Кинетическая энергия': 'kinetic_energy_elem.png',
            'Потенциальная энергия': 'potential_energy_elem.png',
            'Полная механическая энергия': 'total_mechanical_energy_elem.png',
            'Коэффициент полезного действия\n(КПД)': 'kpd_elem.png',
            'Давление твердого тела': 'solid_body_pressure_elem.png',
            'Гидростатическое давление': 'hydrostatic_pressure_elem.png',
            'Полное давление': 'full_dressing_elem.png',
            'Закон Архимеда': 'law_archimedes_elem.png',
            'Сила Архимеда': 'power_archimedes_elem.png',
            # swimming_tel_elem
            'Условие плавания тел\nВсплывает': 'swimming_tel_elem.png',
            'Условие плавания тел\nПлавает в толще жидкости': 'swimming_tel_elem.png',
            'Условие плавания тел\nТонет': 'swimming_tel_elem.png',
            'Условие плавания\nПлавает на поверхности жидкости': 'swimming_tel_elem.png',
            'Нагревание/охлаждение': 'heating_cooling_elem.png',
            'Плавление/кристаллизация': 'melting_crystallization_elem.png',
            'Парообразование/конденсация': 'vaporization_condensation_elem.png',
            'Сгорание топлива': 'fuel_burnout_elem.png',
            'Коэффициент полезного действия\n(КПД) теплового двигателя': 'kpd_dv_elem.png'
        }
        self.instruments = {
            "Спидометр": "Скорость",
            "Динамометр": "Сила, момент силы",
            "Термометр": "Температура",
            "Манометр": "Давление газа или жидкости внутри сосуда",
            "Барометр": "Атмосферное давление",
            "Психрометр": "Относительная влажность воздуха",
            "Гигрометр": "Относительная влажность воздуха",
            "Ареометр": "Плотность веществ",
            "Мензурка": "Объем жидкостей",
            "Амперметр": "Сила тока",
            "Ваттметр": "Мощность тока",
            "Электрометр": "Электрический заряд",
            "Вольтметр": "Электрическое напряжение",
            "Омметр": "Электрическое сопротивление",
            "Счетчик Гейгера": "Ионизирующее излучение",
            "Акселерометр": "Проекцию кажущегося ускорения",
            "Секундомер": "Прибор для измерения интервалов времени",
            "Гальванометр": "Силы малых постоянных токов",
            "Электроскоп": "Наличие электрического заряда",
            "Весы": "Масса"
        }
        self.scientists_discoveries = {
            "Открытие закона о передаче давления жидкостями и газами, изменение атмосферного давления с высотой": "Б. Паскаль",
            "Закон всемирного тяготения, основные законы динамики, теория приливов и отливов, законы качаний маятника, объяснение радуги (открытие дисперсия сета), сложный состав белого света": "И. Ньютон",
            "Закон о выталкивающей силе, действующей на тело, погруженное в жидкость или газ, опыты по изучению плавания тел": "Архимед",
            "Представления о движении молекул, полярное сияние": "М.В. Ломоносов",
            "Открытие явления непрерывного беспорядочного движения частиц, взвешенных в жидкости или газе": "Р. Броун",
            "Открытие атмосферного давления, ртутный барометр": "Е. Торричелли",
            "Опыты по воздухоплаванию": "Монгольфье",
            "Электрическая природа молнии": "Б. Франклин",
            "Экспериментальное открытие магнитного взаимодействия двух проводников с током": "А.М. Ампер",
            "Законы преломления света": "В. Снеллиус",
            "Закон прямой пропорциональной зависимости между силой тока в проводнике и напряжением на концах проводника": "Г. Ом",
            "Закон движения идеальной жидкости": "И. Бернулли",
            "Паровая машина в России": "И.И. Ползунов",
            "Электрическая дуга": "В.В. Петров",
            "Закон сохранения энергии, тепловое действие тока, опыты по превращению механической энергии во внутреннюю": "Дж. Джоуль",
            "Экспериментальное открытие явления электромагнитной индукции": "М. Фарадей",
            "Гелиоцентрическая система": "Н. Коперник",
            "Опыты с магдебургскими полушариями": "О. фон Герике",
            "Ориентация магнитной стрелки вблизи проводника с током, экспериментальное открытие магнитного действия электрического тока": "Г.Х. Эрстед",
            "Открытие новых радиоактивных элементов": "М. Кюри",
            "Движение искусственных спутников Земли": "С.П. Королёв",
            "Скорость звука в воде": "Ж.-Д. Колладон",
            "Открытие атомного ядра, планетарная модель атома, открытие трех видов радиоактивного излучения": "Э. Резерфорд",
            "Маятниковые часы, период колебаний пружинного маятника": "Х. Гюйгенс",
            "Открытие радиоактивности, естественной радиоактивности урана": "А. Беккерель",
            "Инфракрасное излучение": "У. Гершель",
            "Усовершенствование паровой машины": "Дж. Уатт",
            "Свободное падение, явление инерции": "Г. Галилей",
            "Свойства постоянных магнитов": "В. Гильберт",
            "Взаимодействие покоящихся электрических зарядов, закон трения скольжения": "Ш.О. Кулон",
            "Теория межпланетных перелётов": "К.Э. Циолковский",
            "Первый гальванический элемент": "А. Вольта",
            "Температурная шкала": "А. Цельсий",
            "Закон упругой деформация": "Р. Гук",
            "Лампочка накаливания": "А.Н. Лодыгин",
            "Линии в спектре Солнца": "Й. Фраунгофер",
            "Экспериментальное открытие электромагнитных волн": "Г. Герц",
            "Открытие электрона, первая модель атома (\"булочка с изюмом\")": "Дж. Дж. Томсон",
            "Экспериментальное определение величины элементарного электрического заряда": "Р. Милликен",
            "Правило для определения направления индукционного тока в проводнике": "Э. Х. Ленц",
            "Волновая теория света": "Х. Гюйгенс"
        }

    def physic_form(self):
        random_key = choice(list(self.dict_physics.keys()))
        filename = self.dict_physics[random_key]
        return filename, random_key

    def search_form(self, name: str):
        filename = self.dict_physics[name]
        filename_elem = self.dict_physics_elem[name]
        return filename, name, filename_elem

    def physic_teor(self):
        random_key = choice(list(self.scientists_discoveries.keys()))
        author = self.scientists_discoveries[random_key]
        return random_key, author

    def physic_instr(self):
        random_key = choice(list(self.instruments.keys()))
        prim = self.instruments[random_key]
        return random_key, prim

    def math_task(self):
        math_signs = ['*', '**']
        sign = choice(math_signs)
        a = str(randint(11, 99))
        if sign == '**':
            b = 2
        else:
            b = str(randint(11, 99))
        equation = f'{a} {sign} {b}'
        answer = eval(equation)
        print([equation, answer])
        return [equation, answer]

    def gen_exem(self):
        lst = []
        lst_abc = ['A', 'B', 'C']
        lst_k = []
        for i in range(3):
            l = True
            while l:
                key = choice(list(self.dict_physics.keys()))
                filename = self.dict_physics[key]
                if key not in lst_k:
                    lst.append([key, filename, lst_abc[i]])
                    l = False
                lst_k.append(key)
        return lst

    def gen_teor(self):
        lst = []
        lst_k = []
        for i in range(3):
            l = True
            while l:
                key = choice(list(self.scientists_discoveries.keys()))
                answer = self.scientists_discoveries[key]
                if key not in lst_k:
                    lst.append([key, answer])
                    l = False
                lst_k.append(key)
        return lst

    def gen_device(self):
        lst = []
        lst_k = []
        for i in range(3):
            l = True
            while l:
                key = choice(list(self.instruments.keys()))
                answer = self.instruments[key]
                if answer not in lst_k:
                    lst.append([answer, key])
                    l = False
                lst_k.append(answer)
        return lst