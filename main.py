import aiohttp
import asyncio
import sqlite3

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


def guest_clear():
    # Устанавливаем соединение с базой данных
    connection = sqlite3.connect('wedding_data.db')
    cursor = connection.cursor()

    # Добавляем нового пользователя
    cursor.execute('DELETE FROM guests')

    # Сохраняем изменения и закрываем соединение
    connection.commit()
    connection.close()


def guest_insert(guest_name):
    # Устанавливаем соединение с базой данных
    connection = sqlite3.connect('wedding_data.db')
    cursor = connection.cursor()

    # Добавляем нового пользователя
    cursor.execute('INSERT INTO guests (guest_name) VALUES (?)', (guest_name,))

    # Сохраняем изменения и закрываем соединение
    connection.commit()
    connection.close()


async def send_request(session, user_id, guest_id):
    url = 'https://weddingpost.ru/template/invent/userinvent.php'
    payload = {
        'Action': 'getInv',
        'user_id': user_id,
        'guest': guest_id,
        'type': 'electro',
        'mode': '0'
    }

    async with session.post(url, data=payload) as response:
        if response.status == 200:
            return await response.json()  # Возвращаем данные, если запрос успешен
        else:
            return f'Ошибка: {response.status}'


async def main():
    total_requests = 100
    batch_size = 10
    user_id = '749611'
    user_post = 1066200

    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(total_requests):
            guest_id = str(1066200 + i)  # Пример изменения guest_id
            tasks.append(send_request(session, user_id, guest_id))

            # Если достигли размера партии, ждем завершения задач
            if len(tasks) == batch_size:
                results = await asyncio.gather(*tasks)
                for result in results:

                    #print(result['guest_title'])  # Обработка результатов

                    if result['guest_title'] is None:
                        #print(result['guest_title'])
                        guest_name = 'Guest'
                    else:
                        guest_name = result['guest_title']
                        guest_name = guest_name.rsplit('<br> ', 2)[-1]
                        print(f'{user_post} имя гостя: {guest_name}')

                    guest_insert(guest_name)
                    user_post = user_post + 1
                tasks = []  # Сбрасываем задачи

        # Обработка оставшихся задач, если они есть
        if tasks:
            results = await asyncio.gather(*tasks)
            for result in results:
                print(result)


# Запуск главной асинхронной функции
guest_clear()
asyncio.run(main())
