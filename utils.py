from reminders import reminder, cancelreminder
from guess import guess_command

def setup_bot(bot):
    # Commands setup
    @bot.command(name='reminder')
    async def reminder_command(ctx, time: str, *, reminder_text: str):
        await reminder(ctx, time, reminder_text=reminder_text)

    @bot.command(name='cancelreminder')
    async def cancelreminder_command(ctx, reminder_id: int):
        await cancelreminder(ctx, reminder_id)

    @bot.command(name='guess')
    async def guess(ctx, number: int):
        await guess_command(ctx, number)
