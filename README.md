# 李杜 · 诗句互文

一个把李白、杜甫两家存诗与 23,448 组句级对照做成可视化浏览的静态网页。
纯前端、无外部依赖，可离线打开，也可直接发布到任意静态托管。

## 本地打开

- 直接双击 `index.html`（Chrome / Edge / Safari）。
- 或起一个本地服务器：`python3 -m http.server 8000`，访问 <http://127.0.0.1:8000/>。

## 在线发布（三步）

1. 构建（已预先构建好，改过内容才需要重跑）：

   ```bash
   python3 tools/build_dist.py
   ```

   得到 `dist/`（干净的站点目录）与 `release/lidu-site.zip`（压缩包）。

2. 上传：

   - **GitHub Pages（网页操作，不装 git）**：见 [GITHUB.md](GITHUB.md)。
     简要说：新建仓库 → 上传 `dist` 里的**内容** → Settings → Pages →
     Deploy from a branch（main / root）。
   - **Netlify**：打开 <https://app.netlify.com/drop>，拖入 `dist` 或压缩包。
   - **Vercel**：项目根目录 `npx vercel --prod`。
   - **Cloudflare Pages / 自有服务器**：上传 `dist/` 内容即可。

3. 拿到正式地址后，补齐 canonical、分享卡片与 sitemap：

   ```bash
   python3 tools/set_domain.py https://你的域名
   ```

   未设置时这些标签会自动省略，不会指向占位域名。

完整步骤、响应头、缓存与检查清单见 [DEPLOY.md](DEPLOY.md)。

## 页面结构

| 章节 | 内容 |
| --- | --- |
| 封面 | 两幅人物画像、关键数字与全文入口 |
| 一 · 两座高峰 | 李白、杜甫生平与存诗统计 |
| 二 · 相似度全景 | 23,448 组对照的相似度分布，可拖动阈值并联动筛选 |
| 三 · 对照阅读 | 按相似度 / 检索词筛选句对，点击并置两首原诗 |
| 四 · 互文之网 | 22 首代表作之间的对照网络，悬停高亮，点击读原诗 |
| 五 · 共用语汇 | 同组对照中共同出现的二字词，点击回到对照阅读 |
| 六 · 全唐诗诗库 | 按原书序号浏览两家的全部存诗 |
| 七 · 数据与方法 | 三份表格的字段说明与处理口径 |

## 数据

原始数据在 `李杜/` 目录：

- `李白.csv`：诗题、诗句、全唐诗序号、句序号
- `杜甫.csv`：同上
- `李白-杜甫.csv`：句级对照表，共 23,448 行

对照表各列（按用户说明）：

| 列 | 含义 |
| --- | --- |
| A–C | 李白：作者、诗题、诗句 |
| D–F | 杜甫：作者、诗题、诗句 |
| G | 相似度（原始整数 7000–10000，页面按 ÷10000 显示为 0.700–1.000） |
| H–I | 李白诗作在全唐诗中的序号 / 诗句在该诗中的位置（从 0 计） |
| J–K | 杜甫同上 |

页面使用的 `assets/data.js` 由 `build_data.py` 生成（Python 3，仅标准库）：

```bash
python3 build_data.py      # 校验序号并把 CSV 压成 data.js
python3 tools/build_dist.py
```

脚本会校验每一行对照的序号与诗句是否对得上，并统计相似度分布、每首诗参与对照的条数、
共现双字词与网络图所需的数据。更换 CSV 后重新运行即可。

## 目录

```
index.html            入口（含 SEO / Open Graph / manifest）
404.html              自定义 404
robots.txt            搜索协议（sitemap 地址在设置域名后自动写入）
manifest.json      应用清单（添加到主屏幕）
_headers              Netlify / Cloudflare Pages 的缓存与安全头
netlify.toml          Netlify 配置
vercel.json           Vercel 配置
.github/workflows/    GitHub Pages 自动部署
assets/               样式、脚本、数据、画像、分享图、图标
tools/build_dist.py   生成 dist/ 与 release/ 压缩包
tools/set_domain.py   写入正式域名并重建（生成 sitemap.xml）
GITHUB.md             上传到 GitHub Pages 的图文步骤
tools/og.html         1200×630 分享卡片源文件
李杜/                 原始 CSV
dist/                 可直接上传的站点（构建产物）
release/              可直接拖拽上传的 zip
screenshots/          页面预览图
```

## 说明

- 这份对照数据本身只保留相似度 ≥ 0.70 的句对，因此分布左端是截断的。
- 原始表格未注明相似度算法，页面只呈现数值关系，不作算法推断。
- 两幅画像用于版面陈设，不参与计算。
