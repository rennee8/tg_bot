def convert_schedule(schedule_dict: dict) -> dict:
    format_schedule_dict = {}
    for key, value in schedule_dict.items():
        text_list = value.split('\n')
        day = text_list[0]

        schedule = {}

        for line in text_list[2:]:
            time = line.split(' ')[0]
            if time not in schedule:
                schedule[time] = []
            schedule[time].append(line)

        output = [day, '—' * 21]

        for time, entries in schedule.items():
            for entry in entries:
                if 'нечетная' in entry.lower():
                    output.append(f'_{entry}_')
                else:
                    output.append(f'`{entry}`')
            output.append('—' * 21)

        final_text = '\n'.join(output)
        format_schedule_dict[key] = final_text

    return format_schedule_dict
