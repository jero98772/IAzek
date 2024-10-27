#!/usr/bin/env python 
# -*- coding: utf-8 -*-"
"""
IAzek - 2024 - por MLEAFIT
IAzek - 2024 - by MLEAFIT
"""
from core.bot_telegram.main import main as tl
from core.bot_whatsapp.main import main as ws
from multiprocessing import Process

def run_telegram_bot():
    tl()

def run_whatsapp_bot():
    ws()

if __name__ == '__main__':
    # Create process for each bot
    telegram_process = Process(target=run_telegram_bot)
    whatsapp_process = Process(target=run_whatsapp_bot)

    # Start the processes
    telegram_process.start()
    whatsapp_process.start()

    # Wait for both processes to finish
    telegram_process.join()
    whatsapp_process.join()
