import re


class YoutubeDownloder:
    def __init__(self, save_folder: str, file_type=Literal["video", "audio"]) -> None:
        self.save_folder = save_folder
        self.file_type = file_type

        if self.file_type == "video":
            self.download_format = "mp4"
        else:
            self.download_format = "mp3"

    def sanitize_title(self, title: str) -> str:
        """Sanitize the title to be used as a filename."""
        sanitized_title = re.sub(r"[^a-z0-9 ]", "", title.lower())
        return "_".join(sanitized_title.split(" "))

    def __download_youtube_video(self, url):
        yt = YouTube(url)

        file_name = self.sanitize_title(title=str(yt.title))

        self.save_pth = Path(self.save_folder).joinpath(file_name)
        # self.save_pth.mkdir(parents=True, exist_ok=True)

        save_video_dir = self.save_pth.joinpath(f"{file_name}.{self.download_format}")
        print(f"Passed save path {save_video_dir}")

        if os.path.exists(str(save_video_dir)):
            console.print("Video already downloaded.", style="bold green")
            return str(self.save_pth), str(save_video_dir)

        else:
            command = f"yt-dlp -o '{str(save_video_dir)}' -f 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]' '{url}'"
            os.system(command)
            return str(self.save_pth), str(save_video_dir)

    def __download_youtube_audio(self, url):
        yt = YouTube(url)

        file_name = self.sanitize_title(title=str(yt.title))

        self.save_pth = Path(self.save_folder).joinpath(file_name)
        # self.save_pth.mkdir(parents=True, exist_ok=True)

        save_video_audio = self.save_pth.joinpath(f"{file_name}.{self.download_format}")

        if os.path.exists(save_video_audio):
            console.print("Audio already downloaded.", style="bold green")

            return str(self.save_pth), str(save_video_audio)
        else:
            command = f"yt-dlp '{url}' -o '{str(save_video_audio)}' --extract-audio --audio-format mp3 --audio-quality 0"
            os.system(command)
            return str(self.save_pth), str(save_video_audio)

    def download_youtube(self, url):
        """_summary_

        Args:
            url (_type_): _description_

        Returns:
            _type_: _description_
        """
        if self.file_type == "video":
            return self.__download_youtube_video(url)

        elif self.file_type == "audio":
            return self.__download_youtube_audio(url)


yt = YoutubeDownloder()

yt.download_youtube()
