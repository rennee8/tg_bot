def convert_schedule(schedule_dict: dict) -> dict:
    format_schedule_dict = {}
    for key, value in schedule_dict.items():
        text_list = value.split('\n')
        day = text_list[0]

        # Словарь для хранения группировок по времени
        schedule = {}

        # Проходим по оставшимся строкам и группируем по времени
        for line in text_list[2:]:  # Пропускаем первые две строки
            time = line.split(' ')[0]  # Получаем время (первая часть строки)
            if time not in schedule:
                schedule[time] = []
            schedule[time].append(line)

        # Формируем итоговую строку
        output = [day, '—' * 21]

        for time, entries in schedule.items():
            for entry in entries:
                if 'нечетная' in entry.lower():  # Проверка на "нечетная"
                    output.append(f'_{entry}_')  # Жирный текст
                else:
                    output.append(f'`{entry}`')  # Моноширинный текст
            output.append('—' * 21)  # Добавляем разделитель

        # Присоединяем все части и выводим результат
        final_text = '\n'.join(output)
        format_schedule_dict[key] = final_text

    return format_schedule_dict