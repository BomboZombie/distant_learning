# Cайт для дистанционного обучения

[Ссылка на сайт](https://distant-learning.herokuapp.com)

## Использование
В шапке сайта есть 3 вкладки (Решать, Мои Задания, Управлять Группами)

### Решать
Здесь отображаются все группы, в которых вы участвуете как ученик. Для каждого задания отображается статус (Не сдано, Сдано, или процент выполнения). Процент выполнния появляется после дедлайна. 

### Мои Задания
Здесь вы можете создать и редактировать задания. Задания - просто набор задач. Его можно назначать в разные группу на разные сроки.

### Управлять Группами
Здесь отображаются группы, в которых вы являетесь учителем. Можно создать новую группу или редактировать существующую.

---

## Идея
Сделать сайт, с помощью которого учителя смогут взаимодействовать с учениками.

## Реализация
Для создания сайта с базой данных были использованы следующие библиотеки
- Flask (в том числе и Flask-Login, Flask-WTF, WTForms)
- SQLAlchemy
- Datetime (установка сроков)

Для взаимодействия с БД создан отдельный модуль "manage_sql.py".

## Классы
- User
- Group
- Task
- Solution
- Problem
- Deadline

## Функционал
Каждый пользователь может создать группу и добавить в нее других пользователей. Это будет своего рода "класс". 

Создав группу вы становитесь для неё учителем. 

Права учителя: 
- назначать задания в этой группе
- приглашать других ползователей в качестве учеников/учителей
- просматривать результаты выполнения назначенных им заданий

Ученики - те пользователи, которым будут отображаться задания этой группы. Их задача - выполнять эти задания

## Уникальность
- Каждый пользователь может быть учителем/учеником
- Дедлайн и Задание не взаимосвязаны, поэтому не надо каждый раз пересоздавать то же самое
