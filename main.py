#!/usr/bin/env python 
# -*- coding: utf-8 -*-"
"""
IAzek - 2024 - por jero98772
IAzek - 2024 - by jero98772
"""
from core.main.bot_telegram import main as tl
from core.main.bot_whatsapp import main as ws
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
