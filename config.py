language = 'ru'

sticker_id = {
    'hello': 'CAACAgIAAxkBAAEFE91irjUKGAbLaaTbvkM6_cPw39A1bwACbgADwDZPE22H7UqzeJmXJAQ',
    'error': 'CAACAgIAAxkBAAEFE9NirjNASnFs6L5DyvxRN9579rp80QACdgADwDZPE3QapjQbGEnJJAQ',
    'victory': 'CAACAgIAAxkBAAEFE8BiriqdBsWK8csW3exdwmW5VO8HZwACbQADwDZPE7mMKCVnSEkbJAQ'
}

answer_variants = {
    'ru':
        {
            'hello_message':
                'Привет! Я помогу тебе с любым сложным выбором!\n\n'
                'Просто отправь мне список в формате\n'
                '*Зеленая миля, Побег из Шоушенка, Форрест Гамп и т.д*',
            'type_to_choose':
                'Введите, что хотите выбрать в формате\n'
                '*Зеленая миля, Побег из Шоушенка, Форрест Гамп и т.д*',
            'more_than_two_values':
                'Введите больше *двух* значений\n'
                '*P.S. – в качестве разделителя используйте запятую с пробелом*',
            'do_not_understand': 'Ничего не понимаю!',
            'something_went_wrong': 'Что-то пошло не так, мой создатель *обязательно* это исправит!\n'
                                    'Попробуйте ещё раз...\nТекст ошибки:',
            'final_choice': 'Финальный выбор!\n',
            'winner_is': 'Победитель'
        },
    'en':
        {
            'hello_message': 'Hi! I can help you to solve a hard choice!\n\n'
                             'Just send me a list like\n'
                             '*The Green Mile, Shawshank Redemption, Forrest Gump, etc.*',
            'type_to_choose': 'Send me what to choose like\n'
                              '*The Green Mile, Shawshank Redemption, Forrest Gump, etc.*',
            'more_than_two_values': 'Type more than *two* values\n'
                                    '*P.S. – use a coma with space as a separator*',
            'do_not_understand': 'I don\'t understand you!',
            'something_went_wrong': 'Something went wrong, my creator will *necessarily* fix that!\n'
                                    'Try again...\nError text:',
            'final_choice': 'Final choice!\n',
            'winner_is': 'The winner is'
        }
}

reply_variants = answer_variants[language]
