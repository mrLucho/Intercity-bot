from Intercity import Intercity
with Intercity()as bot:
    bot.land_first_page()
    bot.fill_start_city()
    bot.fill_end_city()
    bot.fill_date()
    bot.fill_time()
    bot.seek()
    try:
        bot.fill_normal_people()
        bot.fill_students()
        bot.fill_discount_type()
        bot.click_dalej_button()
    except:
        print('no train available')
        exit(-1)
    bot.fill_name_of_traveller()