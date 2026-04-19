from flask import Flask, render_template_string, request
from datetime import datetime
import os

app = Flask(__name__)

# Храним данные в списке (для простоты)
plants = []

HTML = '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Садовод 🌱</title>
    <style>
        body {
            font-family: -apple-system, sans-serif;
            max-width: 90%;
            margin: 20px auto;
            padding: 10px;
            background: #f7f9f0;
        }
        input, button {
            padding: 14px;
            font-size: 16px;
            width: 100%;
            margin: 8px 0;
            border-radius: 8px;
            border: 1px solid #ddd;
        }
        button {
            background: #4caf50;
            color: white;
            border: none;
            cursor: pointer;
        }
        ul {
            list-style: none;
            padding: 0;
        }
        li {
            background: white;
            padding: 16px;
            margin: 10px 0;
            border-radius: 10px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        .alert {
            border-left: 5px solid #ff9800;
        }
        .actions {
            margin-top: 10px;
            display: flex;
            gap: 10px;
        }
        .actions button {
            flex: 1;
            padding: 10px;
            font-size: 14px;
        }
        .actions .water {
            background: #2196f3;
        }
        .actions .delete {
            background: #f44336;
        }
    </style>
</head>
<body>
    <h1>Садовод-помощник 🌱</h1>

    <form method="post">
        <input type="text" name="name" placeholder="Название растения" required>
        <input type="date" name="date" required>
        <input type="number" name="poliv" placeholder="Полив (дней)" min="1" required>
        <button type="submit">➕ Добавить</button>
    </form>

    <ul>
    {% for p in plants %}
      <li {% if p.needs_water %}class="alert"{% endif %}>
        <b>{{ p.name }}</b><br>
        Посадка: {{ p.date }} | Полив: {{ p.poliv }} дн.<br>
        Последний полив: {{ p.last_watered }} ({{ p.days_since }} дней назад)
        <div class="actions">
          <a href="/water/{{ loop.index0 }}"><button class="water">✅ Полил</button></a>
          <a href="/delete/{{ loop.index0 }}"><button class="delete">🗑️ Удалить</button></a>
        </div>
      </li>
    {% else %}
      <li>Пока нет растений. Добавьте первое!</li>
    {% endfor %}
    </ul>
</body>
</html>
'''

@app.route("/", methods=["GET", "POST"])
def index():
    global plants
    today = datetime.today()

    if request.method == "POST":
        plants.append({
            "name": request.form["name"].strip(),
            "date": request.form["date"],
            "poliv": int(request.form["poliv"]),
            "last_watered": request.form["date"]
        })

    # Подготовка данных
    plants_with_status = []
    for p in plants:
        try:
            last = datetime.strptime(p["last_watered"], "%Y-%m-%d")
            days_since = (today - last).days
            needs_water = days_since >= p["poliv"]
        except:
            days_since = 999
            needs_water = True

        plants_with_status.append({
            "name": p["name"],
            "date": p["date"],
            "poliv": p["poliv"],
            "last_watered": p["last_watered"],
            "days_since": days_since,
            "needs_water": needs_water
        })

    return render_template_string(HTML, plants=plants_with_status)

@app.route("/water/<int:i>")
def water(i):
    if 0 <= i < len(plants):
        plants[i]["last_watered"] = datetime.today().strftime("%Y-%m-%d")
    return "", 302, {'Location': '/'}

@app.route("/delete/<int:i>")
def delete(i):
    if 0 <= i < len(plants):
        del plants[i]
    return "", 302, {'Location': '/'}


port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)