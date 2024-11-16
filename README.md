# wgm_wallpapers

Automatically update wallpapers daily from [https://willguimont.github.io/](https://willguimont.github.io/).

## Installation

```bash
make install

# add the following line to your crontab (crontab -e) to run each hour on the hour
0 * * * * cd /opt/wgm_wallpapers && make run
```
