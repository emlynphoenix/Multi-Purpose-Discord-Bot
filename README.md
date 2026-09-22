<a id="readme-top"></a>

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![project_license][license-shield]][license-url]

<br />
<div align="center">

<h3 align="center">Sparkles Discord Bot</h3>

  <p align="center">
    A multi-purpose Discord bot with moderation, utility, and fun commands.
    <br />
    <a href="https://github.com/emlynphoenix/Sparkles-Discord-Bot"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/emlynphoenix/Sparkles-Discord-Bot/issues/new?labels=bug">Report Bug</a>
    &middot;
    <a href="https://github.com/emlynphoenix/Sparkles-Discord-Bot/issues/new?labels=enhancement">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

<!-- TODO: add a screenshot of the bot in action to images/screenshot.png -->
<!-- ![Sparkles Bot Screenshot](images/screenshot.png) -->

Sparkles is a Discord bot built to bring moderation, utility, and fun commands to a Discord server in one place.

<!-- TODO: replace this with 2-3 real sentences on why you built it / what problem it solves -->

**Key features:**
<!-- TODO: keep the ones that are true, delete the rest, add anything missing -->
- 🛡️ Moderation commands (kick, ban, mute, warn)
- 🎟️ Ticket system for support requests
- 🎉 Fun / utility commands
- ⚙️ Configurable per-server settings

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

<!-- TODO: swap these badges for your actual stack. Common Discord bot ones below — delete what doesn't apply -->
* [![Python][Python.badge]][Python-url]
* [![Pycord][Pycord.badge]][Pycord-url]
* [![SQLite][SQLite.badge]][SQLite-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running, follow these steps.

### Prerequisites

* Python 3.10+
* A Discord bot token — create one via the [Discord Developer Portal](https://discord.com/developers/applications)

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/emlynphoenix/Sparkles-Discord-Bot.git
   cd Sparkles-Discord-Bot
   ```
2. Install dependencies
   ```sh
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the project root and add your bot token
   ```
   DISCORD_TOKEN=your_token_here
   ```
4. Run the bot
   ```sh
   python main.py
   ```

<!-- TODO: correct the exact install/run commands to match your actual file structure -->

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

<!-- TODO: replace with your real prefix/commands -->
```
$help          Show all available commands
$kick @user    Kick a user from the server
$ban @user     Ban a user from the server
$delete        Delete a support ticket
$close         Close a support ticket
$access        Access a support ticket
$add           Add a user to a support ticket
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ROADMAP -->
## Roadmap

<!-- TODO: real planned features, or delete this section if not needed -->
- [ ] Slash command support
- [ ] Web dashboard
- [ ] Multi-language support

See the [open issues](https://github.com/emlynphoenix/Sparkles-Discord-Bot/issues) for a full list of proposed features.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
## License

<!-- TODO: pick a license (MIT is the common default) and add a LICENSE.txt file to the repo -->
Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

Emlyn - emlynphoenix1@gmail.com<!-- TODO: add your email / Discord / contact method or delete this line -->

Project Link: [https://github.com/emlynphoenix/Sparkles-Discord-Bot](https://github.com/emlynphoenix/Sparkles-Discord-Bot)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
[contributors-shield]: https://img.shields.io/github/contributors/emlynphoenix/Sparkles-Discord-Bot.svg?style=for-the-badge
[contributors-url]: https://github.com/emlynphoenix/Sparkles-Discord-Bot/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/emlynphoenix/Sparkles-Discord-Bot.svg?style=for-the-badge
[forks-url]: https://github.com/emlynphoenix/Sparkles-Discord-Bot/network/members
[stars-shield]: https://img.shields.io/github/stars/emlynphoenix/Sparkles-Discord-Bot.svg?style=for-the-badge
[stars-url]: https://github.com/emlynphoenix/Sparkles-Discord-Bot/stargazers
[issues-shield]: https://img.shields.io/github/issues/emlynphoenix/Sparkles-Discord-Bot.svg?style=for-the-badge
[issues-url]: https://github.com/emlynphoenix/Sparkles-Discord-Bot/issues
[license-shield]: https://img.shields.io/github/license/emlynphoenix/Sparkles-Discord-Bot.svg?style=for-the-badge
[license-url]: https://github.com/emlynphoenix/Sparkles-Discord-Bot/blob/main/LICENSE.txt

[Python.badge]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://www.python.org/
[Pycord.badge]: https://img.shields.io/badge/Pycord-5865F2?style=for-the-badge&logo=discord&logoColor=white
[Pycord-url]: https://docs.pycord.dev/
[SQLite.badge]: https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white
[SQLite-url]: https://www.sqlite.org/
