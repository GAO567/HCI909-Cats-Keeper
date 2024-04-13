# Cats Keeper

We worked on a CatsKeeper project that can be considered as part of a smart home. However our implementation works as a helper for human - cats interaction, allowing a remote communication of cats with humans and vice versa.

We have implemented several types of cats - computer interactions: audio recognition, video recognition, and a push button. And a human-computer interaction by a telegram bot.


## How to use ?
Here are three main files:

- arduino_wifi_button.ino - an arduino sketch uploaded to the arduino board with wifi. Requires WiFi.h, UniversalTelegramBot.h, and ArduinoJson.h libraries

- audioTracker.py - can run separately, listens to the micro for some time, sends a message once heard a cat

- videoTracker.py - can run separately, once running, “/whereareyou” command is activated. After receiving the command in a chat with bot, starts looking for cats using camera for several seconds, answers with results
