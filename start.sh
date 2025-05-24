#!/bin/bash
source venv/bin/activate 2>/dev/null || echo "No venv found, continuing without it..."
echo "Starting bot..."
python3 control_bot.py
