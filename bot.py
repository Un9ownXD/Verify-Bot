import discord
from discord import app_commands
from discord.ui import Modal, InputText, View, Button
from database import setup_db, save_entries

TOKEN = ""

class FirstModal(Modal, title="First Dialog"):
    field1 = InputText(label="First Entry")
    field2 = InputText(label="Second Entry")

    async def on_submit(self, interaction: discord.Interaction):
        interaction.client.temp_data[interaction.user.id] = {
            "first": self.field1.value,
            "second": self.field2.value
        }

        
        await interaction.response.send_modal(SecondModal())


class SecondModal(Modal, title="Second Dialog"):
    field3 = InputText(label="Final Entry")

    async def on_submit(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        data = interaction.client.temp_data.get(user_id, {})

        data["third"] = self.field3.value

    
        await save_entries(
            user_id,
            data["first"],
            data["second"],
            data["third"]
        )

        await interaction.response.send_message(
            "Your data has been saved successfully!",
            ephemeral=True
        )



class MainButton(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Open Dialog", style=discord.ButtonStyle.primary)
    async def open_dialog(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_modal(FirstModal())



class MyBot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)
        self.temp_data = {}  

    async def on_ready(self):
        await setup_db()      
        await self.tree.sync()
        print(f"Logged in as {self.user}")


bot = MyBot()



@bot.tree.command(name="openembed", description="Shows embed with button")
async def openembed(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Main Feature",
        description="Click the button below to open the dialog.",
        color=discord.Color.blurple()
    )

    await interaction.response.send_message(
        embed=embed,
        view=MainButton()
    )



bot.run(TOKEN)

# Contact "un9own" on discord for more such projects
