# 上传到 GitHub Pages（不用装 git，网页操作）

站点是纯静态文件，上传到 GitHub 仓库根目录、开启 Pages 就能访问。
本机没有安装 git，所以下面用 GitHub 网页上传，全程约 3 分钟。

> 本地先看效果：双击项目里的 `index.html`，或双击 `dist/index.html`，两者内容一致。

---

## 0. 先读：一个仓库 = 一个网站

这条规则能避免覆盖已有的个人主页：

- GitHub Pages 的网址是 `https://<用户名>.github.io/<仓库名>/`，
  **仓库名就是网址里的路径**。`Michelle-Cai` 这个仓库只对应
  `/Michelle-Cai/` 这个网址，别的仓库不会占用它，也不会影响它。
- **不要把这个站点上传到已有的个人主页仓库**（比如 `Michelle-Cai`）。
  两个网站都有 `index.html`，同名文件会被直接替换，个人主页就被覆盖了。
- **新建分支解决不了问题。** 同一个仓库的 Pages 只能发布一个分支 / 目录；
  切换分支只会把当前网站换掉，不会多出一个网址。
  要两个独立网站，就要两个独立仓库。

所以：个人主页留在 `Michelle-Cai`，李白杜甫放进新仓库 `li-du`，两者互不干扰。

---

## 1. 新建仓库

1. 打开 <https://github.com/new>
2. **Repository name** 填 `li-du`（小写字母、连字符；它会成为网址的一部分）
3. 选 **Public**
4. 下面的 README / .gitignore / license **都不要勾**
5. 点 **Create repository**

---

## 2. 上传站点文件（关键一步）

要上传的是 `dist` 文件夹**里面的内容**，不是 `dist` 文件夹本身。

1. 在访达里打开项目中的 **`dist`** 文件夹
2. 按 `⌘ A` 全选（应包含 `index.html`、`404.html`、`assets`、`robots.txt`、`sitemap.xml`、`manifest.json`、`_headers`）
3. 回到 GitHub 仓库页面 → **Add file** → **Upload files**
4. 把选中的文件拖进虚线框，等列表出现
5. 点 **Commit changes**

上传完成后，仓库根目录应当**直接**看到 `index.html` 和 `assets/`。
如果看到的是一个 `dist` 文件夹，说明拖错了层级，删掉重新按上面步骤上传。

---

## 3. 开启 Pages

1. 仓库 → **Settings** → 左侧 **Pages**
2. **Build and deployment** → Source 选 **Deploy from a branch**
3. Branch 选 **main**，目录选 **/ (root)**
4. 点 **Save**
5. 等 1–3 分钟

---

## 4. 访问

```
https://caimichelle214-lab.github.io/li-du/
```

第一次打开若 404，等两分钟再刷新。仍然 404 就检查第 2 步：
`index.html` 必须在仓库**根目录**，不能藏在子文件夹里。

---

## 5. 补上正式地址（本次已预先配好）

当前 `dist/` 已经按 `https://caimichelle214-lab.github.io/li-du` 写好了
canonical、分享卡片和 sitemap —— 只要仓库名用 **`li-du`**，这一步可以跳过。

如果你改用了别的仓库名（例如 `lidu`），在本机运行一次：

```bash
python3 tools/set_domain.py https://caimichelle214-lab.github.io/你的仓库名
```

重新构建后，把 **`dist/index.html`、`dist/robots.txt`、`dist/sitemap.xml`**
三个文件重新上传覆盖并提交即可。

分享卡片可用 <https://developers.facebook.com/tools/debug/> 输入网址检查。

---

## 6. 以后更新内容

改完本地文件后：

```bash
python3 build_data.py        # 若换了 CSV 才需要
python3 tools/build_dist.py  # 重新生成 dist/
```

然后在 GitHub 仓库里重新上传改动过的文件（或整个 `dist` 的内容）并提交。
Pages 一分钟内更新；浏览器用 `⌘ ⇧ R` 强制刷新。

---

## 7. 常见问题

**页面没有样式。**
`assets` 文件夹没有传上去，或层级不对。`assets` 必须和 `index.html` 同级。

**访问是 404。**
`index.html` 不在仓库根目录，或 Pages 还在首次构建中。

**改了文件但线上没变化。**
等 1–2 分钟；仍有旧内容就强制刷新（`⌘ ⇧ R`）。

**想连数据和源码一起放到 GitHub？**
可以把整个项目的内容（同样不要上传最外层文件夹）传上去，根目录的 `index.html`
也能直接作为 Pages 站点。但网页上传默认看不到 `.github`、`.nojekyll` 这类隐藏文件
（访达按 `⌘ ⇧ .` 可显示），自动部署工作流需要它们；不传也不影响网站访问。

**以后想用 git 管理。**
安装 Xcode 命令行工具或 GitHub Desktop 后，把本文件夹初始化为仓库，
`main` 分支推送即可；仓库里已带 `.github/workflows/deploy-pages.yml`，
可在 Pages 里把来源改为 **GitHub Actions** 实现自动构建发布。
