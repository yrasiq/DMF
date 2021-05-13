# DMF
Бот для WoW classic warlock. Забытый город - восток.

Бот предназначен для личного использования и имеет настройки, специфичные для конкретного ПК, персонажа и интерфейса. В таком виде вы не сможете его использовать. Но можете просто ознакомится с проектом. Это законченная программа и ее дальнейшего изменения/улучшения не будет. Так же это мой первый проект на python и код во всех смыслах оставляет желать лучшего, но, тем не менее, все стабильно работает с середины 2020 г.

Бот выполняет довольно сложную работу прохождения подземелья, расчитанного на 5 человек максимального уровня в одиночку для добычи внутриигровых ресурсов. Для совершения подобных действий среднестатестическому игроку понадобится около недели подготовки. Он делает это без остановки по кругу до тех пор, пока не сломается вся экипировка.

### Общий принцип работы
Любой бот должен получать, обрабатывать информацию, и на ее основании производить какие-то действия.
##### Получение данных
Получать информацию из WoW можно разными способами:
- Чтение напрямую из памяти
- Из сетевого протокола между клиентом и сервером
- Из DirectX
- С экрана монитора (pixel hunting)
- Через WoWAPI с помощью аддона на LUA

В этом боте используется комбинация двух последних вариантов:
Часть данных получается через [аддон](DungeonCords/) написаный на языке LUA. Этот аддон работает с WoWAPI и добавляет в верхнем левом углу игры несколько разноцветных квадратов (далее это будет называтся симофором) где RGB цвета этих квадратов соответствуют данным. На пример R == 0 это ваше здоровье равно нолю, R == 125 - 50%, R == 255 - 100%, G == 0 это здоровье цели равно нолю и так далее. Вероятно, лучшим решением было бы передавать данные из аддона при помощи сокетов, но уже есть как есть :) Дополнительно этот аддон реализует в интерфейсе игры кнопку, по нажатии которой происходит распыление предметов "необычного" и "редкого" качества.

Многие важные данные получить таким способом нельзя, т.к. WoWAPI не дает к ним доступ. Эти данные получаются из скриншотов с экрана. Плюсы такого подхода в том, что получить бан крайне маловероятно и он относительно прост в реализации. Но есть довольно серьезные минусы:

Эти данные жестко связанны с настройками графики и разрешению экрана и будут актуальны для одних конкретных настроек, так же получение информации путем скриншотов занимает какое-то время (около 0.013с для отдельного пикселя, и около 0.1с для полного скриншота), в некоторых местах это может быть критично. Так же это приводит к накапливающейся погрешности, если бот жестко заскриптован (вероятно, из-за рассинхронизации с частотой кадров в игре). На одной операционной системе может быть запущен только один такой бот, программа игры обязательно должна быть открыта и во время его работы вы не можете пользоваться ПК.
##### Обработка данных
Обработка может производится как угодно. В этой программе это происходит с помощью python [здесь](DMF.py). Тут обрабатываются данные симофора и данные со скришнотов экрана при помощи python библиотек OpenCV и Pillow. Вообще, весь python код программы расположен в одном этом файле.
##### Действия
Наконец, после обработки данных совершаются итоговые действия, это может происходить так же по разному:
- Прямая работа с данными игры в памяти
- Подмена пакетов данных в сетевом протоколе
- Имитация нажатий клавишь в самой операционной системе
Здесь используется последний вариант с помощью WindowsAPI в [том же python файле](DMF.py). Он так же прост в реализации и безопасен, но так же имеет серьезные минусы: На одной операционной системе может быть запущен только один такой бот, программа игры обязательно должна быть открыта и во время его работы вы не можете пользоваться ПК.

### Некоторые особенности
Главная особенность в том, что внутри подземелья с помощью [способов получения данных этого бота](#получение-данных) именно внутри подземелья нельзя узнать координаты. Ни свои, ни мобов, ни какие. По этому основной маршрут персонажа жестко заскриптован, и перемещение по маршруту - это повторение заранее записанных человеком действий.

Все файлы вида inptN.txt в корне каталога представляют собой файлы маршрута, где:
- Каждая четвертая строка это отметка об относительном времени в секундах, когда изменилось положение курсора, состояние кнопок мыши или клавиатуры.
- Каждая четвертая +1 строка это координаты курсора на экране.
- Каждая четвертая +2 строка это состояние клавишь клавиатуры.
- Каждая четвертая +3 строка это состояние кнопок мыши.

Эти файлы записывались с помощью [кейлоггера](klgr.py), он так же присутствует в корне этого репозитория.

В [основном файле программы](DMF.py) запущен бесконечный цикл, который переберает по очереди эти файлы, все их строки с отметками времени и эмулирует нажатие необходимых клавишь согласно данным в них, когда время совпадает с отметкой в файле.
Между переключением файлов inptN.txt так же запускаются отдельные необходимые скрипты, на пример скрипт боя с боссом, или скрипт корректировки положения персонажа. т.к. при таком подходе в маршруте всегда присутствует некоторая погрешность.

Так же паралельно запущено два дополнительных потока с помощью threading библиотеки:

Один проверяет состояние смерти, такое иногда случается, т.к. подземелья имеют некоторое случайное расположение мобов и патрулей. В этом случае запускает маршрут для воскрешения и перезапускает, главный цикл.

Второй проверяет некоторые другие условия. На пример, если персонаж вступил в бой, то главный цикл "приостонавливается", запускается скрипт боя с мобом, после - скрипт восстановления ресурсов и скрипт сбора добычи. Далее маршрут продолжается.
