# 发布上线

站点是纯静态的（HTML + CSS + JS + 图片），没有后端、没有外部依赖，
把 `dist/` 目录原样放到任何静态托管上就能访问。

本文按「最快」到「最可控」排列，任选其一即可。

---

## 0. 先构建一次

```bash
python3 tools/build_dist.py
```

会生成：

- `dist/` —— 可直接上传的站点目录
- `release/lidu-site.zip` —— 同一个站点的压缩包，适合拖拽上传

> 修改了页面、样式或 CSV 数据后，重新运行一次即可。
> 若之后要绑定域名，见第 6 节。

---

## 1. Netlify Drop（最快，约 1 分钟，无需命令行）

1. 打开 <https://app.netlify.com/drop>
2. 把 **`dist` 文件夹**（或 `release/lidu-site.zip`）拖进页面
3. 几秒后得到一个 `https://xxxx-xxxx.netlify.app` 地址，可直接分享
4. 按页面提示登录并认领站点，即可长期保留；之后可以改站点名，例如 `li-du.netlify.app`
5. 以后更新：重新构建，再把 `dist` 拖一次（Deploys → Drag and drop）

netlify.toml、`_headers`、`404.html` 都已就位，拖上去即生效。

---

## 2. Vercel（命令行，适合经常更新）

```bash
npx vercel --prod
```

在**项目根目录**执行即可：`vercel.json` 已指定 `outputDirectory: dist` 与响应头。
按提示登录、确认，首次会问项目名，完成后得到 `https://<项目名>.vercel.app`。

- 也可以只发布构建产物：`cd dist && npx vercel --prod`。
- 更新：重新 `python3 tools/build_dist.py`，再执行一次上面的命令。
- 自定义域名：Vercel 项目 → Settings → Domains。

---

## 3. GitHub Pages

### 3A. 网页上传（无需 git，推荐新手）

完整步骤见 [GITHUB.md](GITHUB.md)：新建仓库 → 上传 `dist` 里的**内容** →
Settings → Pages → Deploy from a branch（main / root）。

### 3B. git + GitHub Actions（自动构建）

1. 在 GitHub 新建仓库，把本项目推上去（`main` 分支）
2. 仓库 → Settings → Pages → Source 选 **GitHub Actions**
3. 推送后 `.github/workflows/deploy-pages.yml` 会自动构建 `dist` 并发布
4. 地址为 `https://<用户名>.github.io/<仓库名>/`

页面内所有资源都是相对路径，放在子目录（`/仓库名/`）也能正常工作。
设置域名后提交 `site.config.json`，工作流会带上 canonical / 分享卡片重新构建。

---

## 4. Cloudflare Pages

**方式一（上传）：** Dashboard → Workers & Pages → Create → Pages →
Upload assets → 把 `dist` 拖进去。

**方式二（连 Git）：** 连接仓库后设置

- Build command：`python3 tools/build_dist.py`
- Build output directory：`dist`

Cloudflare 会自动读取 `dist/_headers`，缓存与安全响应头直接生效。
国内访问通常比 Netlify / Vercel 稳定一些。

---

## 5. 自有服务器 / 对象存储 / 国内云

把 `dist/` 内容上传即可，例如：

- **Nginx**：把 `dist/` 设为站点根目录；开启 `gzip on;` 与 `try_files $uri $uri/ =404;`，并把 `error_page 404 /404.html;` 指向 404 页。
- **阿里云 OSS / 腾讯云 COS**：开启「静态网站托管」，默认首页 `index.html`、默认 404 页 `404.html`；建议同时开启 CDN 与 gzip。
- 自定义域名在国内访问需要 **ICP 备案**；未备案可先用海外节点或 Cloudflare。

`_headers` 只对 Netlify / Cloudflare Pages 生效，其他环境请按文件在面板里配置缓存：

- `index.html`、`404.html`：`no-cache`
- `assets/data.js`、`app.js`、`styles.css`：`max-age=3600`
- 图片与图标：`max-age=31536000, immutable`

---

## 6. 设置站点地址（让分享卡片和搜索引擎正确）

canonical、`og:image` 与 `sitemap.xml` 需要绝对地址，所以默认不输出；
发布拿到正式域名后执行一次：

```bash
python3 tools/set_domain.py https://你的域名
```

脚本会把地址写入 `site.config.json`，重新生成 `dist/`，并自动生成
`sitemap.xml`、在 `robots.txt` 中写入 sitemap 地址。之后再上传一次 `dist` 即可。

- GitHub Pages 自定义域名可加 `--cname 你的域名`，会额外生成 `CNAME`。
- 校验分享卡片：<https://developers.facebook.com/tools/debug/>（填网址 → Scrape Again），
  或直接把链接发到微信/Telegram 看预览。

---

## 7. 上线检查清单

- [ ] 首屏两幅画像正常显示，标题与统计数字完整
- [ ] 「对照阅读」能搜索、能拖阈值、点卡片能并置原诗
- [ ] 「互文之网」悬停有提示、点击能进入原诗
- [ ] 「全唐诗诗库」切换李白/杜甫、搜索、加载更多正常
- [ ] 手机宽度（390px）下导航、卡片、模态正常
- [ ] 随意访问一个不存在的路径，出现 404 页面
- [ ] `https://你的域名/assets/og.jpg` 能打开（分享卡片配图）
- [ ] 首次加载后刷新，速度正常（数据约 1.4 MB，托管商会自动 gzip）

---

## 8. 更新数据或内容

```bash
# 1) 替换 李杜/ 下的 CSV 后，重建数据
python3 build_data.py

# 2) 重新打包站点
python3 tools/build_dist.py

# 3) 重新上传 dist / 推送仓库
```

---

## 本地预览（含局域网手机预览）

```bash
python3 -m http.server 8000
```

- 电脑：<http://127.0.0.1:8000/>
- 手机（同一 Wi-Fi）：`http://<电脑局域网 IP>:8000/`

手机端切到「共享 → 添加到主屏幕」后，会使用 `manifest.json` 与图标，像应用一样打开。
