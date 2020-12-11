# Allen Bruteforcer
#### A simple way to bruteforce a captcha system
![License](https://img.shields.io/github/license/lamergameryt/allen-bruteforce) ![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/lamergameryt/allen-bruteforce) ![GitHub followers](https://img.shields.io/github/followers/lamergameryt?style=social) [![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

This program lets you **bruteforce** your way through **Allen's GST Login System**.

## Download It
This program requires python to execute. To download python, you can visit https://python.org/downloads/ and install the latest version of python.

To download this program, click the `Code` button beside `Add File` and select `Download ZIP`.

After downloading the zip file, you can extract it to your preferred location.

## Requirements
The program requires some dependencies to work. The project requires the following external dependencies to work which are not in the `requirements.txt`:
* Tesseract (Recommended version is v5.0.0-alpha.20201127)
* ImageMagick (Recommended version is 7.0.10)
* Custom Tesseract traineddata (Included in the repository)

The recommnded version of Tesseract for Windows can be downloaded from [this link](https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v5.0.0-alpha.20201127.exe).
ImageMagick can be downloaded from https://imagemagick.org/script/download.php

The traineddata included in this repository was trained specifically for this type of captcha. This `.traineddata` file should be placed in the `tessdata` folder which is present in the directory you installed Tesseract.

## How to Use?
Once you've downloaded the program and all the external requirements, open a terminal in the folder you extracted this program and execute the following command:
`pip install -r requirements.txt`

Once this has been completed, you have the option to configure the program.
Open the file `run.py` in your favorite text editor and scroll to the `Configuration` section.

Below you can find what each variable corresponds to:
* `website_url`: The website which you want to bruteforce. (It only works for Allen's website)
* `autoinstall_driver`: Automatically install the Chrome Driver required for Selenium. **Do not modify** unless you know what you're doing.
* `magick_path`: The directory where you installed ImageMagick.
* `chrome_headless`: Open Google Chrome in GUI more or not. `True` means no GUI.
* `use_proxy`: If a proxy should be used to make the requests.
* `http_proxy`: Specify the proxy to use. Please make sure the proxy is a valid one before using else you'll get a bunch of error messages.
* `logs`: Choose to display logs to the terminal.

To execute the program, type `py run.py` or `python run.py` depending on your OS.
The program will bruteforce its way and display the date of birth of the student once it's done.

## Why did I release this?
This repository is just a way to help people building website scrappers to scrape websites which contain text based captchas.
In the future, Allen may change their authentication method. If that happens, this repository will be archived.

## Accuracy of captcha detection
This program can guess the captcha with an **accuracy of approximately 60%**. It takes around **2 tries** to guess one day.

Based on this calculation and time taken to load the website, on average it will take around 7 minutes to find the birthday of one student.

## License
This software is licensed under the GNU General Public License v3.0 License. See the LICENSE file in the top distribution directory for the full license text.

## Liked it?
Thank you for reading through this!

If you liked it, consider giving a star to this project and following me on GitHub as I have put my ❤ and a lot of effort in this.