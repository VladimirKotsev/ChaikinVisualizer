# Chaikin Visualizer

**Chaikin Visualizer** е инструмент за интерактивна визуализация на алгоритъма за изглаждане на криви на Chaikin. Позволява добавяне на точки, прилагане на итерации за изглаждане и регулиране на параметрите на алгоритъма.

## 🔧 Инсталация

За да използвате този инструмент, трябва да имате **Python 3** и следните библиотеки:

```sh
pip install numpy matplotlib
```

## 🚀 Стартиране на приложението

За да стартирате визуализатора, изпълнете следната команда:

```sh
python chaikin_visualizer.py
```

## 🎨 Основни функционалности

- **Добавяне на точки** – Кликнете върху графиката, за да добавите върхове към полилинията.
- **Изглаждане на кривата** – Натиснете бутона `Iterate`, за да приложите една итерация на алгоритъма на Chaikin.
- **Промяна на параметрите** – Регулирайте `u` и `v` чрез плъзгачите или текстовите полета.
- **Изчистване на чертежа** – Натиснете `Clear`, за да премахнете всички точки.
- **Нулиране на итерациите** – Натиснете `Reset`, за да започнете отначало.
- **Затворена/отворена крива** – Натиснете `Toggle Open/Closed`, за да превключите между затворена и отворена форма.

## 📊 Контроли

| Контрол | Описание |
|---------|---------|
| `Iterate` | Изпълнява една итерация на алгоритъма за изглаждане. |
| `Clear` | Изчиства всички въведени точки. |
| `Reset` | Връща инструмента в начално състояние. |
| `Toggle Open/Closed` | Превключва между отворена и затворена крива. |
| `u` и `v` плъзгачи | Регулират параметрите на алгоритъма (ограничаващи стойности 0 ≤ u + v ≤ 1). |

## 📸 Преглед

![Примерен изглед](https://github.com/VladimirKotsev/ChaikinVisualizer/blob/main/Chaikin%20visualization.png)

## 📝 Забележки

- Алгоритъмът изисква **поне 2 точки**, за да бъде приложен.
- Ако `u + v > 1`, стойностите автоматично ще се коригират.
*Този проект е създаден с образователна цел и е с отворен код.*
