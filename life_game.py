from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import random

app = FastAPI()

# Создание поля и случайное размещение "живых" клеток
field_width = 50
field_height = 50
field = [[random.choice([0, 1]) for _ in range(field_width)] for _ in range(field_height)]


@app.get("/game_of_life")
async def get_game_of_life():
    # Обработка текущего изменения состояния поля
    new_field = [[0] * field_width for _ in range(field_height)]
    while field != new_field:
        for i in range(field_height):
            for j in range(field_width):
                live_neighbors = 0
                # Подсчет количества живых соседей
                for x in range(-1, 2):
                    for y in range(-1, 2):
                        if x == 0 and y == 0:
                            continue
                        if field[(i + x) % field_height][(j + y) % field_width] == 1:
                            live_neighbors += 1
                # Применение правил игры
                if field[i][j] == 1 and live_neighbors in [2, 3]:
                    new_field[i][j] = 1
                elif field[i][j] == 0 and live_neighbors == 3:
                    new_field[i][j] = 1

        # Проверка условий окончания игры
        if field == new_field:
            return {"message": "Игра завершена"}

        live_count = 0

        for i in new_field:
            for item in i:
                if item == 1:
                    live_count += 1

        if live_count == 0:
            return {"message": "Игра завершена"}

        # Обновление поля
        field[:] = new_field

        print("\n".join(map(str, field)))
        print("________________________")
        print("\n".join(map(str, new_field)))

    return "\n".join(map(str, new_field))
