from sqlalchemy import create_engine, text


engine = create_engine(url="mysql+pymysql://exsec_astra:OwsJ3f3C@exsec.beget.tech/exsec_astra", pool_timeout=20, pool_recycle=299)


#  Регистрация пользователя в базе данных
async def register(chat_id, username, name):
    engine.connect()
    data = False
    # Проверить наличие пользователя в базе
    result = engine.execute(text(f"SELECT * FROM `users` WHERE `users`.`chatid` = '{chat_id}'"))
    # Если не найден - зарегистрировать
    if result.fetchone() is None:
        data = True
        engine.execute(text(f"INSERT INTO `users` (`id`, `chatid`, `username`, `name`) VALUES (NULL, '{chat_id}', '{username}', '{name}');"))
    engine.dispose()
    return data


# Получить статус прогресса для модуля
async def get_status(chat_id, num):
    engine.connect()
    result = engine.execute(text(f"SELECT `users`.`Module {num}` FROM `users` WHERE `users`.`chatid` = '{chat_id}'"))
    data = ""
    for item in result.fetchone():
        data = str(item)
    engine.dispose()
    return data


# Установить статус прогресса для модуля
async def set_status(chat_id, num, test_num):
    engine.connect()
    previous = await get_status(chat_id, num)
    li = list(previous)
    li[int(test_num)-1] = '1'
    current = ''.join(li)
    engine.execute(text(f"UPDATE `users` SET `users`.`Module {num}` = '{current}' WHERE `users`.`chatid` = '{chat_id}'"))
    engine.dispose()


# Увеличить количество очков
async def set_score(chat_id, score):
    engine.connect()
    engine.execute(text(f"UPDATE `users` SET `users`.`score` = `users`.`score` + '{score}' WHERE `users`.`chatid` = '{chat_id}'"))
    engine.dispose()


# Получить количество очков
async def get_score(chat_id):
    engine.connect()
    result = engine.execute(text(f"SELECT `users`.`score` FROM `users` WHERE `users`.`chatid` = '{chat_id}'"))
    data = ""
    for item in result.fetchone():
        data = str(item)
    engine.dispose()
    return data


# Получить место в рейтинге
async def get_position(chat_id: str):
    engine.connect()
    result = engine.execute(text(f"SELECT `users`.`chatid` FROM `users` ORDER BY `users`.`score` DESC"))
    data = 0
    for item in result.fetchall():
        data += 1
        if str(item[0]) == chat_id:
            break
    engine.dispose()
    return str(data)


# Получить место в рейтинге
async def get_rating(chat_id: str):
    engine.connect()
    query = engine.execute(text(f"SELECT `users`.`name`, `users`.`score`, `users`.`chatid` FROM `users` ORDER BY `users`.`score` DESC"))
    result = query.fetchall()
    position = 0
    names = list()
    chat_ids = list()
    scores = list()
    positions = list()
    for item in result:
        position += 1
        chat_ids.append(str(item[2]))
        names.append(item[0])
        scores.append(item[1])
        positions.append(position)
        if position == 4:
            break
    position = 0
    if chat_id not in chat_ids:
        for item in result:
            position += 1
            if item[2] == chat_id:
                chat_ids.append(item[2])
                names.append(item[0])
                scores.append(item[1])
                positions.append(position)
                break
    data = "📊 *Таблица лидеров:*\n"
    for i in range(len(names)):
        if i == 0:
            names[i] = '🥇 ' + names[i]
        if i == 1:
            names[i] = '🥈 ' + names[i]
        if i == 2:
            names[i] = '🥉 ' + names[i]
        if i > 2 and chat_ids[i] == chat_id:
            data += "\n. . ."
        data += f"\n*{str(positions[i])}*. {names[i].replace(' None', '')} - {str(scores[i])} очков"
    engine.dispose()
    return data + "\n. . ."
