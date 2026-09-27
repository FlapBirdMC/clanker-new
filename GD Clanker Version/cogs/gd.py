import discord
from discord import app_commands
from discord.ext import commands
import aiohttp

class GeometryDash(commands.GroupCog, name="gd"):
    def __init__(self, bot):
        self.bot = bot
        self.headers = {"User-Agent": ""}
        self.secret = "Wmfd2893gb7"

    def _parse_gd_response(self, text: str) -> dict:
        """Parses RobTop's colon-delimited response string into a dictionary."""
        if not text or text == "-1":
            return {}
        
        item = text.split("|")[0]
        parts = item.split(":")
        
        data = {}
        for i in range(0, len(parts) - 1, 2):
            data[parts[i]] = parts[i+1]
        return data

    @app_commands.command(name="user", description="Lookup a Geometry Dash player profile")
    @app_commands.describe(username="The Geometry Dash username to search for")
    async def gd_user(self, interaction: discord.Interaction, username: str):
        await interaction.response.defer()
        
        url = "https://www.boomlings.com/database/getGJUsers20.php"
        payload = {
            "gameVersion": "22",
            "binaryVersion": "35",
            "str": username,
            "secret": self.secret
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=payload, headers=self.headers) as resp:
                data = self._parse_gd_response(await resp.text())

        if not data:
            await interaction.followup.send(f"❌ Player `{username}` not found on Geometry Dash.")
            return

        embed = discord.Embed(
            title=f"👤 Player Profile: {data.get('1', username)}",
            color=discord.Color.green()
        )
        embed.add_field(name="Account ID", value=data.get("16", "N/A"), inline=True)
        embed.add_field(name="Player ID", value=data.get("2", "N/A"), inline=True)
        embed.add_field(name="Stars ⭐", value=data.get("3", "0"), inline=True)
        embed.add_field(name="Demons 😈", value=data.get("4", "0"), inline=True)
        embed.add_field(name="Secret Coins 🪙", value=data.get("13", "0"), inline=True)
        embed.add_field(name="User Coins 🟡", value=data.get("17", "0"), inline=True)

        await interaction.followup.send(embed=embed)

    @app_commands.command(name="level", description="Lookup a Geometry Dash level by name or ID")
    @app_commands.describe(search="The level name or level ID to search for")
    async def gd_level(self, interaction: discord.Interaction, search: str):
        await interaction.response.defer()

        url = "https://www.boomlings.com/database/getGJLevels21.php"
        payload = {
            "gameVersion": "22",
            "binaryVersion": "35",
            "str": search,
            "type": "0",
            "secret": self.secret
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=payload, headers=self.headers) as resp:
                data = self._parse_gd_response(await resp.text())

        if not data:
            await interaction.followup.send(f"❌ Level `{search}` not found.")
            return

        embed = discord.Embed(
            title=f"🎮 Level: {data.get('2', 'Unknown')} (ID: {data.get('1', 'N/A')})",
            color=discord.Color.gold()
        )
        embed.add_field(name="Downloads 📥", value=data.get("10", "0"), inline=True)
        embed.add_field(name="Likes 👍", value=data.get("14", "0"), inline=True)
        embed.add_field(name="Version", value=data.get("5", "1"), inline=True)

        await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(GeometryDash(bot))