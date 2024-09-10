import aiohttp
import asyncio

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


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

    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(total_requests):
            guest_id = str(1066200 + i)  # Пример изменения guest_id
            tasks.append(send_request(session, user_id, guest_id))

            # Если достигли размера партии, ждем завершения задач
            if len(tasks) == batch_size:
                results = await asyncio.gather(*tasks)
                for result in results:
                    print(result['guest_title'])  # Обработка результатов
                tasks = []  # Сбрасываем задачи

        # Обработка оставшихся задач, если они есть
        if tasks:
            results = await asyncio.gather(*tasks)
            for result in results:
                print(result)


# Запуск главной асинхронной функции
asyncio.run(main())
