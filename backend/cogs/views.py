from discord.ui import View, Button
from discord import Embed, Interaction
import discord
from utils.download import search_yotube, download_audio
from utils.playback import play_song
from utils.playing_list import Playlist

# ---------------- QueueView ----------------
class QueueView(View):
    def __init__(self, songs: list[dict], current_index: int):
        super().__init__(timeout=None)
        self.songs = songs
        self.page_size = 5
        self.current_index = current_index
        self.total_page = (len(self.songs) + self.page_size - 1) // self.page_size        
        
        self.current_page = self.current_index // self.page_size
        self.start_index = self.current_page * self.page_size
        self.page_songs = self.songs[self.start_index:self.start_index + self.page_size]

        # 初始化按鈕狀態
        self.previous_button.disabled = self.current_page == 0
        self.next_button.disabled = self.current_page == self.total_page - 1

    @discord.ui.button(label="", style=discord.ButtonStyle.secondary, emoji='◀️')
    async def previous_button(self, interaction: Interaction, button: Button):
        if self.current_page > 0:
            self.current_page -= 1
            await self.update_embed(interaction)

    @discord.ui.button(label="", style=discord.ButtonStyle.secondary, emoji='▶️')
    async def next_button(self, interaction: Interaction, button: Button):
        if self.current_page < self.total_page - 1:
            self.current_page += 1
            await self.update_embed(interaction)

    async def update_embed(self, interaction: Interaction) -> None:
        self.start_index = self.current_page * self.page_size
        self.page_songs = self.songs[self.start_index:self.start_index + self.page_size]
        self.previous_button.disabled = self.current_page == 0
        self.next_button.disabled = self.current_page == self.total_page - 1

        embed = self.create_embed()
        await interaction.response.edit_message(embed=embed, view=self)

    def create_embed(self) -> Embed:
        embed = Embed(title="待播清單：", color=discord.Color.blue())
        for i, song in enumerate(self.page_songs, start=self.start_index):
            display_title = f"**{song['title']}**" if i == self.current_index else song['title']
            embed.add_field(name=f"{i + 1}", value=display_title, inline=False)
        embed.set_footer(text=f"Page {self.current_page + 1} of {self.total_page}")
        return embed


# ---------------- SearchView ----------------
class SearchView(View):
    def __init__(self, keyword: str, playlist: Playlist, results: list[dict]):
        super().__init__(timeout=180)
        self.keyword = keyword
        self.playlist = playlist
        self.results = results
        self.message: discord.Message | None = None

        self.page_size = 5
        self.total_page = (len(self.results) + self.page_size - 1) // self.page_size
        self.current_page = 0
        self.page_results: list[dict] = []
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

    @classmethod
    async def create(cls, keyword: str, playlist: Playlist):
        results = await search_yotube(keyword)
        return cls(keyword, playlist, results)

    async def on_timeout(self):
        if self.message:
            try:
                await self.message.delete()
            except discord.NotFound:
                pass

    def update_page_results(self) -> None:
        start_index = self.current_page * self.page_size
        self.page_results = self.results[start_index:start_index + self.page_size]

    def update_navigation_buttons(self) -> None:
        self.previous_button.disabled = self.current_page == 0
        self.next_button.disabled = self.current_page == self.total_page - 1

    async def button_callback(self, interaction: Interaction):
        await interaction.response.defer()
        if self.message:
            await self.message.delete()

        index = int(interaction.data['custom_id']) - 1
        if index < 0 or index >= len(self.page_results):
            await interaction.followup.send("❌ 選擇無效", ephemeral=True)
            return

        item = self.page_results[index]
        song_url = f"https://www.youtube.com/watch?v={item['videoId']}"
        song_info = await download_audio(song_url)
        self.playlist.add_song(song_info)

        await interaction.followup.send(f'🎵 點播 {song_info["title"]}')

        voice_client = interaction.guild.voice_client
        if voice_client is None:
            if interaction.user.voice and interaction.user.voice.channel:
                voice_client = await interaction.user.voice.channel.connect(self_deaf=True)
            else:
                await interaction.followup.send("❌ 你不在語音頻道", ephemeral=True)
                return

        play_song(interaction.client, voice_client, self.playlist)

    async def previous_page(self, interaction: Interaction):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_page_results()
            self.update_navigation_buttons()
            await interaction.response.edit_message(embed=self.create_embed(), view=self)

    async def next_page(self, interaction: Interaction):
        if self.current_page < self.total_page - 1:
            self.current_page += 1
            self.update_page_results()
            self.update_navigation_buttons()
            await interaction.response.edit_message(embed=self.create_embed(), view=self)

    def create_embed(self) -> Embed:
        embed = Embed(title=f"\"{self.keyword}\" 搜尋結果：", color=discord.Color.green())
        for i, item in enumerate(self.page_results, start=1):
            embed.add_field(name=f"{i}", value=item['title'], inline=False)
        embed.set_footer(text=f"Page {self.current_page + 1} of {self.total_page}")
        return embed
