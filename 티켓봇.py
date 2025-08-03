import discord
from discord import app_commands
from discord.ext import commands

SERVER_ID = 1401496792541167686
STAFF_ROLE_ID = 1401497365742882927

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

class TicketButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    async def create_ticket(self, interaction: discord.Interaction, topic: str):
        guild = interaction.guild
        staff_role = guild.get_role(STAFF_ROLE_ID)
        channel_name = f"ticket-{topic.lower().replace(' ', '-')}-{interaction.user.name}".lower()

        existing = discord.utils.get(guild.text_channels, name=channel_name)
        if existing:
            await interaction.response.send_message(f"이미 '{channel_name}' 티켓 채널이 있어요!", ephemeral=True)
            return

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            staff_role: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True)
        }

        ticket_channel = await guild.create_text_channel(channel_name, overwrites=overwrites, topic=f"{topic} 문의 티켓 - {interaction.user}")

        await interaction.response.send_message(f"티켓이 생성되었어요: {ticket_channel.mention}", ephemeral=True)

    @discord.ui.button(label="구매문의", style=discord.ButtonStyle.primary, custom_id="ticket_buy")
    async def buy_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.create_ticket(interaction, "구매문의")

    @discord.ui.button(label="게임 문의", style=discord.ButtonStyle.primary, custom_id="ticket_game")
    async def game_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.create_ticket(interaction, "게임 문의")

    @discord.ui.button(label="서버문의", style=discord.ButtonStyle.primary, custom_id="ticket_server")
    async def server_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.create_ticket(interaction, "서버문의")

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)
        # self.tree는 이미 내장되어 있으니 따로 만들 필요 없음

    async def setup_hook(self):
        guild = discord.Object(id=SERVER_ID)
        self.tree.copy_global_to(guild=guild)
        await self.tree.sync(guild=guild)

bot = MyBot()

@bot.event
async def on_ready():
    print(f"{bot.user} 봇이 준비되었습니다!")

@bot.tree.command(name="티켓", description="티켓 버튼 메시지를 보냅니다.", guild=discord.Object(id=SERVER_ID))
async def ticket_command(interaction: discord.Interaction):
    view = TicketButtons()
    await interaction.response.send_message("문의할 버튼을 눌러 티켓을 생성하세요!", view=view, ephemeral=False)

bot.run("MTM3OTc2MDQ2NzgxOTQ5NTQ3NQ.GSFGA_.FdpOKLeqC76S2HlYPjIgBxL8jwoeUHViGRwiV4")
