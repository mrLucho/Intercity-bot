from Intercity import Intercity
with Intercity()as bot:
    bot.wrapper_find_train()
    bot.wrapper_people_discount()
    bot.fill_name_of_traveller()
    _ = input('Did u click that button ? if so press ENTER:\n') # not sure if \n needed
    bot.click_buy_no_register()
    bot.wrapper_user_data()
    bot.click_regulations_accept()
    bot.submit_user_data()
    bot.click_zatwierdz_btn()
    _ = input('is everything ok?')
    bot.send_thanks()