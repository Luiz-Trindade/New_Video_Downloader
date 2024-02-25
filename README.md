<image src="https://www.gnu.org/graphics/gplv3-127x51.png">

# New Video Downloader

## Simple YouTube Video Downloader Written In Python!

This is a Python script for downloading YouTube videos. It provides a user-friendly interface built with CustomTkinter and utilizes the Pytube library for video downloading. The script is distributed under the GNU General Public License (GPL) version 3.

<image src="screenshots/screenshot1.png">

<image src="screenshots/screenshot2.png">


### Usage:

1. Run the script.
2. In the "Download" tab, enter the URL of the video you want to download.
3. Click the "Add" button to add the video to the download list.
4. Optionally, you can reset the list using the "Reset" button.
5. Choose the destination path by clicking the "Download" button.
6. The download process will be divided into four parts to enhance efficiency.

### Features:

- **Multi-Processing:** The script uses multiprocessing to download multiple videos simultaneously, improving download speed.

- **Notification:** Upon completion of the download, a notification sound is played, and a notification window appears.

- **Dark Mode:** The script supports dark mode for a more comfortable experience.

### Dependencies:

- CustomTkinter: A customized version of Tkinter for enhanced aesthetics.
  
- Pytube: A library for downloading YouTube videos.

- Pygame: Used for playing notification sounds.

### How to Run:

Make sure you have Python installed. Install the required libraries using:

```bash
pip install pytube customtkinter pygame
```

Run the script:

```bash
python new_video_downloader.py
```

### License:

This program is free software under the terms of the GNU General Public License as published by the Free Software Foundation. See the [GPL-3.0 License](https://www.gnu.org/licenses/) for more details.

### Author:

- Luiz Gabriel Magalhães Trindade

Feel free to contribute, report issues, or suggest improvements. Happy downloading! 🚀
