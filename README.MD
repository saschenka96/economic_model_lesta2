1. Данные аккаунтов: nickname, credits, items - хранятся в базе данных sqllite, структура описана в models.py
2. Для создания таблицы надо запустить db.py
3. В db.py описана работа с базой данных, изменение параметров аккаунтов пользователя при создании аккаунтов, покупки, продаже предметов
4. Возможные предметы и диапазон credits хранятся в constants.py
5. Для запуска работы приложения, после создания базы данных, запустить server.py и client.py
6. После запуска клиента надо ввести никнейм - любая возможная строка, ограничений на символы нету, нельзя вводить пустую строку и строку состоящую из одних пробелов
7. Если никнейма клиента нету в аккаунтах базы данных, создается новая запись с текущим никнеймом, определенным в диапазоне - credits и без какого-либо имущества, в соответствующее поле записывается пустая строка. На экран выводятся текущие данные аккаунта.
8. После логгинга состояние клиента менятся на State.GAME_SESSION и становятся доступны опции определенные в параметрах options в constants.py
9. Если пользователь ввел строку, которой нет в options, выводится сообщение об ошибке, регистр не важен. 
10. Можно посмотреть баланс на счету, можно посмотреть список своих предметов, можно купить новый, при покупке нового делается проверка на то, что такой предмет ёщё не куплен, такой предмет должен быть в списке доступных, что пользователю хватит денег. При продаже предмета проверяется то, что желаемый предмет уже есть у пользователя.  При успешной покупке продаже выводитя поздравительное сообщение и текущий баланс credits. Из покупки и продажи можно вернуться назад в главное меню с помощью "back". Также если пользователь пытается продать, а у него нет предметов, выводится предупреждение. Также можно выйти из аккаунта. При выходе из аккаунта состояние клиента изменится на State.Login
11. Закончить работу приложения можно непосредственным прерыванием самой программы, кнопочки exit нету

- Были использованы enum34==1.1.10 и peewee==3.17.1
- Версия пайтона : 2.7
- Протокол сетевого взаимодействия: сокеты