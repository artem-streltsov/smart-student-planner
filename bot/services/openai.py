import openai
import logging
from openai import AsyncOpenAI
from bot.config import config

client = AsyncOpenAI(api_key=config["openai"]["api_key"])

async def generate_study_plan(prompt: str) -> str:
    try:
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that creates structured study plans."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        logging.error(f"Error calling OpenAI API: {e}")
        return "Error generating study plan. Please try again later."