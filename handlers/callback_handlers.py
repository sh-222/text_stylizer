from aiogram import Router, F
from aiogram.types import CallbackQuery, BufferedInputFile
from aiogram.fsm.context import FSMContext
from utils.states import TextStates
from utils.zalgofy import zalgofy
from utils.fancy_font import generate_fancy_text
from PIL import Image, ImageDraw, ImageFont
import io
import os

callback_router = Router()

# Константы для генерации изображений
DEFAULT_FONT_SIZE = 32
MIN_IMAGE_WIDTH = 400
MIN_IMAGE_HEIGHT = 150
PADDING = 40

@callback_router.callback_query(F.data.in_(["zalgo", "fancy", "spaced", "uppercase", "text_to_image"]))
async def handle_callback(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    text = data.get('text', '')
    operation = callback.data
    
    try:
        if operation == "zalgo":
            modified = zalgofy(text)
        elif operation == "spaced":
            modified = ".".join(text)
        elif operation == "uppercase":
            modified =  " ".join(text.upper())
        elif operation == "fancy":
            modified = generate_fancy_text(text.upper())
        elif operation == "text_to_image":
            # Генерируем изображение с текстом
            try:
                # Используем читаемый шрифт из файла
                font_path = os.path.join(os.path.dirname(__file__), '../fonts/DejaVuSans.ttf')
                font = ImageFont.truetype(font_path, size=DEFAULT_FONT_SIZE)
                
                # Создаем временное изображение для расчета размеров текста
                with Image.new('RGB', (1, 1)) as temp_image:
                    temp_draw = ImageDraw.Draw(temp_image)
                    text_bbox = temp_draw.textbbox((0, 0), text, font=font)
                    text_width = text_bbox[2] - text_bbox[0]
                    text_height = text_bbox[3] - text_bbox[1]
                
                # Определяем размеры изображения
                img_width = max(text_width + PADDING*2, MIN_IMAGE_WIDTH)
                img_height = max(text_height + PADDING*2, MIN_IMAGE_HEIGHT)
                
                # Создаем основное изображение
                image = Image.new('RGB', (img_width, img_height), color=(255, 255, 255))
                draw = ImageDraw.Draw(image)
                
                # Рассчитываем позицию для центрированного текста
                x = (img_width - text_width) // 2
                y = (img_height - text_height) // 2
                
                # Рисуем текст по центру
                draw.text((x, y), text, fill=(0, 0, 0), font=font)
                
                # Сохраняем изображение в байт-поток
                img_byte_arr = io.BytesIO()
                image.save(img_byte_arr, format='PNG')
                img_byte_arr.seek(0)
                
                # Отправляем изображение как файл
                photo = BufferedInputFile(img_byte_arr.getvalue(), filename="text_image.png")
                await callback.message.answer_photo(photo=photo)
                await callback.message.delete()
                await state.clear()
                return
            except Exception as e:
                await callback.message.answer("Ошибка при генерации изображения: " + str(e))
                return
            
        await callback.message.answer(f"{modified}")
        await callback.message.delete()
        await state.clear()
    except Exception as e:
        await callback.message.answer(f"Ошибка: {str(e)}")

@callback_router.callback_query(F.data == "clear")
async def clear(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.clear()
