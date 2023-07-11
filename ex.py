# import asyncio
# import math
#
# import aiogram.utils.markdown as md
# from aiogram import Bot, types
# from aiogram.dispatcher import Dispatcher
# from aiogram.types import Location, Message
# from typing import Dict
#
# # Replace YOUR_BOT_TOKEN with your actual bot token
# bot = Bot(token='5504892953:AAH-WUECmS8AUckggr1BhzKnTN5_FEgBoBQ')
# dp = Dispatcher(bot)
#
# # A dictionary to store each user's previous location
# prev_location: Dict[int, Location] = {}
#
#
# # A function to calculate the distance between two locations
# def distance(loc1: Location, loc2: Location) -> float:
#     lat1, lon1 = loc1.latitude, loc1.longitude
#     lat2, lon2 = loc2.latitude, loc2.longitude
#     radius = 6371  # km
#     dlat = (lat2 - lat1) * math.pi / 180
#     dlon = (lon2 - lon1) * math.pi / 180
#     a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
#          math.cos(lat1 * math.pi / 180) * math.cos(lat2 * math.pi / 180) *
#          math.sin(dlon / 2) * math.sin(dlon / 2))
#     c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
#     distance = radius * c
#     return distance
#
#
# # A function to track the user's movement every 5 seconds
# async def track_user_movement(user_id: int):
#     while True:
#         try:
#             # Get the user's current location
#             current_location = prev_location[user_id]
#
#             # Wait for 5 seconds
#             await asyncio.sleep(5)
#
#             # Get the user's updated location
#             updated_location = prev_location[user_id]
#
#             # Calculate the distance between the two locations
#             distance_walked = distance(current_location, updated_location)
#
#             # Send a message to the user with the distance they walked
#             await bot.send_message(user_id, md.text('You have walked {:.8f} km.'.format(distance_walked)))
#
#             # Update the user's previous location with the updated location
#             prev_location[user_id] = updated_location
#         except KeyError:
#             # If the user's location is not found in the dictionary, stop tracking them
#             break
#
#
# # Handler for live location updates
# @dp.message_handler(content_types=types.ContentType.LOCATION)
# async def handle_location_update(message: Message):
#     # Save the user's location in the dictionary
#     prev_location[message.from_user.id] = message.location
#
#     # Start tracking the user's movement
#     asyncio.create_task(track_user_movement(message.from_user.id))
#
#     # Send a message to the user to confirm their location was saved
#     await message.reply('Your location has been saved.')
#
#
# # Start the bot
# if __name__ == '__main__':
#     asyncio.run(dp.start_polling())
a = {'a':1}
a = str(a)[1:-1]
print(f'^{a}')