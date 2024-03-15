nohup python3 main.py & > /dev/null
echo $! > .pid

echo Бот включен
echo Версия python: $(python3 -V)  