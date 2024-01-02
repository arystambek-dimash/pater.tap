from aiogram import Router
from ugc.management.commands.utils import import_routers

router = Router()

import_routers(__name__)
