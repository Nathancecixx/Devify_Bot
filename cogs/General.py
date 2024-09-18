import discord
from discord.ext import commands
from discord import ApplicationContext
from config import DEV_GUILD_ID
from datetime import datetime


# List of role names we are allowing users to pick from
ROLE_NAMES = ["Developer", "Designer", "Tester"]

class RoleSelect(discord.ui.Select):
    def __init__(self):
        # Defining the options for the select menu using the role names
        options = [discord.SelectOption(label=role_name, description=f"Pick this if you are a {role_name.lower()}!") for role_name in ROLE_NAMES]
        
        # Initialize the select menu with the options
        super().__init__(placeholder="Choose a Role!", min_values=1, max_values=1, options=options)

    # Callback when the select menu is used
    async def callback(self, interaction: discord.Interaction):
        selected_role_name = self.values[0]  # The selected role name
        guild = interaction.guild
        
        # Search for the role in the guild by name
        role = discord.utils.get(guild.roles, name=selected_role_name)
        
        if role is None:
            await interaction.response.send_message("Role not found in this server.", ephemeral=True)
            return

        # Get the user (member) who interacted with the menu
        member = interaction.user

        # Assign the role to the member
        if role not in member.roles:
            await member.add_roles(role)
            await interaction.response.send_message(f"Awesome! You have been given the {role.name} role.", ephemeral=True)
        else:
            await interaction.response.send_message(f"You already have the {role.name} role.", ephemeral=True)


class MyView(discord.ui.View):
    def __init__(self):
        super().__init__()
        # Add the select menu to the view
        self.add_item(RoleSelect())


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot





    @commands.slash_command(
        name="hello",
        description="Sends a friendly greeting.",
        guild_ids=DEV_GUILD_ID,
    )
    async def hello(self, ctx: ApplicationContext):
        """
        A simple slash command that greets the user.
        """
        await ctx.respond(f"Hello, {ctx.author.mention}! 👋")




    @commands.slash_command(
            name='roles',
            description='Creates a selection embed for users to choose their roles.',
            guild_ids=DEV_GUILD_ID
    )
    async def roles(self, ctx: ApplicationContext):
        await ctx.respond("Choose a role!", view=MyView())
    



    @commands.slash_command(
        name='info', 
        description='Provides detailed information about the server.',
        guild_ids=DEV_GUILD_ID 
    )
    async def info(self, ctx: ApplicationContext):
        """
        A slash command that provides comprehensive information about the server.
        """
        guild = ctx.guild

        # Basic Information
        owner = str(guild.owner.name)
        guild_id = str(guild.id)
        member_count = guild.member_count
        desc = guild.description if guild.description else "No description set."

        # Advanced Information
        created_at_utc = guild.created_at.strftime("%B %d, %Y")
        verification_level = str(guild.verification_level).title()
        premium_tier = f"Tier {guild.premium_tier}" if guild.premium_tier > 0 else "None"
        premium_subscription_count = guild.premium_subscription_count

        # Role Information
        roles = [role for role in guild.roles if role != guild.default_role]
        # Sort roles by position (hierarchy)
        roles.sort(key=lambda r: r.position, reverse=True)

        # Check if roles exceed the embed field limit
        if len(roles) > 25:
            await ctx.respond("The server has more than 25 roles. Please refine the `/info` command to handle role pagination.")
            return

        # Embed Creation Date (current time)
        embed_creation = datetime.now()

        # Building the Embed
        embed = discord.Embed(
            title=f"📋 {guild.name} Server Information",
            description=desc,
            color=discord.Color.dark_blue(),
            timestamp=embed_creation
        )
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)

        # Adding Fields
        embed.add_field(name="🔑 Owner", value=owner, inline=True)
        embed.add_field(name="🆔 Server ID", value=guild_id, inline=True)
        embed.add_field(name="📅 Created On", value=created_at_utc, inline=True)
        embed.add_field(name="🔒 Verification Level", value=verification_level, inline=True)
        embed.add_field(name="🚀 Boost Tier", value=premium_tier, inline=True)
        embed.add_field(name="💎 Boosts", value=premium_subscription_count, inline=True)
        embed.add_field(name="📝 Active Template", value=f"Study_Server", inline=False)
        embed.add_field(name="👥 Members", value=f"{member_count}", inline=False)
        embed.add_field(name="🎭 Roles: ", value="", inline=False)

        for role in roles:
            member_count_role = len(role.members)
            embed.add_field(name=f"{role.name}", value=f"{member_count_role}", inline=True)

        await ctx.respond(embed=embed)





def setup(bot):
    """
    Synchronously add the General cog to the bot.
    """
    bot.add_cog(General(bot))
