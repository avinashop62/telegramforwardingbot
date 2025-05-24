#!/bin/bash
source venv/bin/activate 2>/dev/null || echo "No venv found, continuing without it..."
echo "Starting Control Bot..."
python3 control_bot.py &

echo "Starting UserBot Manager..."
python3 userbot_manager.py &
wait
