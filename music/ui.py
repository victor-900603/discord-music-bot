from discord.ui import View, Button
from discord import Embed
import discord
from music.utils.download import search_yotube, download_audio
import asyncio
from music.playlist import Playlist

class QueueView(View):
    def __init__(self, songs, current_index):
        super().__init__()
        self.songs = songs
        self.page_size = 5
        self.current_index = current_index
        self.total_page = (len(self.songs) + self.page_size - 1) // self.page_size

        
        self.current_page = self.current_index // self.page_size
        self.start_index = self.current_page * self.page_size
        self.page_songs = self.songs[self.start_index: self.start_index + self.page_size]
        
        self.previous_button.disabled = self.current_page == 0
        self.next_button.disabled = self.current_page == self.total_page - 1

    @discord.ui.button(label="", style=discord.ButtonStyle.secondary, emoji='◀️')
    async def previous_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page > 0:
            self.current_page -= 1
            await self.update_embed(interaction)

    @discord.ui.button(label="", style=discord.ButtonStyle.secondary, emoji='▶️')
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page < len(self.songs) - 1:
            self.current_page += 1
            await self.update_embed(interaction)

    async def update_embed(self, interaction: discord.Interaction):
        self.start_index = self.current_page * self.page_size
        self.page_songs = self.songs[self.start_index: self.start_index + self.page_size]
        
        self.children[0].disabled = self.current_page == 0
        self.children[1].disabled = self.current_page == self.total_page - 1

        embed = self.create_embed()
        await interaction.response.edit_message(embed=embed, view=self)
    
    def create_embed(self) -> Embed:
        embed = Embed(
            title="待播清單：",
            color=discord.Color.blue()
        )
        for i, song in enumerate(self.page_songs, start=0):
            index = self.current_page * self.page_size + i
            embed.add_field(name=f"{index + 1 }",
                            value=f"{song['title']}" if index != self.current_index else f"**{song['title']}**",
                            inline=False)
        embed.set_footer(text=f"Page {self.current_page + 1} of {self.total_page}")
        return embed
    
    
class SearchView(View):
    def __init__(self, keyword: str, playlist: Playlist, cog):
        super().__init__()
        self.keyword = keyword
        self.playlist = playlist
        self.cog = cog
        self.results = search_yotube(self.keyword)

        self.page_size = 5
        self.total_page = (len(self.results) + self.page_size - 1) // self.page_size

        self.current_page = 0
        self.start_index = self.current_page * self.page_size
        self.page_results = []
        self.update_page_results()

        for i in range(1, self.page_size + 1):
            button = Button(label=str(i), style=discord.ButtonStyle.primary, custom_id=str(i))
            button.callback = self.button_callback
            self.add_item(button)
            
        self.previous_button = Button(style=discord.ButtonStyle.secondary, emoji='◀️')
        self.previous_button.callback = self.previous_page
        self.add_item(self.previous_button)
        
        self.next_button = Button(style=discord.ButtonStyle.secondary, emoji='▶️')
        self.next_button.callback = self.next_page
        self.add_item(self.next_button)

        self.update_navigation_buttons()
        
    async def on_timeout(self):
        if self.message:
            try:
                await self.message.delete()
            except discord.NotFound:
                pass

    def update_page_results(self):
        self.start_index = self.current_page * self.page_size
        self.page_results = self.results[self.start_index:self.start_index + self.page_size]

    def update_navigation_buttons(self):
        self.previous_button.disabled = self.current_page == 0
        self.next_button.disabled = self.current_page == self.total_page - 1

    async def button_callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await self.message.delete()
        
        index = int(interaction.data['custom_id']) - 1
        item = self.page_results[index]
        song_url = "https://www.youtube.com/watch?v=" + item['videoId']
        song_info = download_audio(song_url)
        self.playlist.add_song(song_info)
        
        await interaction.followup.send(f'點播 {song_info["title"]}')
        
        if interaction.guild.voice_client is None:
            voice_channel = interaction.channel
            voice_client = await voice_channel.connect(self_deaf=True)
        else:
            voice_client = interaction.guild.voice_client
            
        if not voice_client.is_playing() and not voice_client.is_paused():
            self.cog.bot.loop.create_task(self.cog.play_next(voice_client, self.playlist))

    async def previous_page(self, interaction: discord.Interaction):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_page_results()
            self.update_navigation_buttons()
            await interaction.response.edit_message(embed=self.create_embed(), view=self)

    async def next_page(self, interaction: discord.Interaction):
        if self.current_page < self.total_page - 1:
            self.current_page += 1
            self.update_page_results()
            self.update_navigation_buttons()
            await interaction.response.edit_message(embed=self.create_embed(), view=self)

    def create_embed(self) -> Embed:
        embed = Embed(title=f"\"{self.keyword}\" 搜尋結果：")
        for i, item in enumerate(self.page_results, start=1):
            embed.add_field(name=f"{i}", value=item['title'], inline=False)
        embed.set_footer(text=f"Page {self.current_page + 1} of {self.total_page}")
        return embed
