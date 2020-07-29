## 使用帮助

### 插件列表

- [管理(Admin)](#admin)
- [搜图(ImageSearch)](#image-search)
- [掷点(roll)](#roll)
- [点歌(song)](#song)
- [公主连结ReDive(Pcr)](#pcr)

### 命令列表

- [公告(notice)](#command-notice)
- [搜图(imagesearch)](#command-imagesearch)
- [掷点(roll)](#command-roll)
- [点歌(song)](#command-song)
- [档线(line)](#command-line)


### 帮助信息

---

#### <a name="admin">管理</a>:

提供机器人管理相关命令

##### <a name="command-notice">公告</a>

将下一条消息群发至所有所在群，输入单个`#`取消命令。

使用: `notice`

别名: `notice`, `群发`

权限: `机器人管理员`

---

#### <a name="image-search">搜图</a>:

提供搜图功能

##### <a name="command-imagesearch">搜图</a>

使用[saucenao](https://saucenao.com/), [ascii2d](https://ascii2d.net/)进行图片搜索，支持命令和图片分开发送。

使用: `搜图 图片`

别名: `imagesearch`, `搜图片`, `图片搜索`

权限: `任何人`

---

#### <a name="roll">掷点</a>:

提供掷点功能

##### <a name="command-roll">掷点</a>

coc跑团用掷点, d不区分大小写, 参数可缺省, 默认为1个100面。

使用: `roll 1d100`

别名: `roll`, `骰子`

权限: `任何人`

---

#### <a name="song">点歌</a>:

提供点歌功能

##### <a name="command-song">点歌</a>

网易云点歌, 参数为关键字, 关键字用空格隔开

使用: `song 关键字`

别名: `song`

权限: `任何人`

---

#### <a name="pcr">点歌</a>:

提供公主连结ReDive国服相关功能

##### <a name="command-line">档线</a>

获取当日早5点档线(5点前算前日), 支持参数分条发送
档线:3, 10, 20, 50, 200, 600, 1200, 2800, 5000, 10000, 15000, 25000, 40000, 60000

使用: `line 档线`

别名: `档线`

权限: `任何人`

---