# Cloudflare Pages 自定义域名配置指南

## 问题
自定义域名 `https://bltestdata.aipush.fun` 无法访问，但 `https://ai-dashboard-6p0.pages.dev` 可以正常访问。

## 解决步骤

### 1. 访问 Cloudflare Dashboard
https://dash.cloudflare.com/

### 2. 选择你的域名（aipush.fun）
在左侧菜单找到 "Workers & Pages"

### 3. 进入 Pages 项目
- 点击 "Pages"
- 找到 "ai-dashboard" 项目
- 点击进入

### 4. 配置自定义域名
在项目设置中找到 "Custom domains"：
- 点击 "添加自定义域名"
- 输入：`bltestdata.aipush.fun`
- 系统会自动生成 DNS 记录

### 5. 配置 DNS 记录
有两种方式：

#### 方式A：使用 Cloudflare DNS（推荐）
如果 aipush.fun 已在 Cloudflare 托管：
- DNS 记录会自动创建
- 等待 DNS 传播（通常 1-2 分钟）

#### 方式B：使用其他 DNS 提供商
如果域名不在 Cloudflare 托管：
1. Cloudflare 会显示需要添加的 CNAME 记录
2. 登录你的 DNS 提供商（例如阿里云、腾讯云等）
3. 创建 CNAME 记录：
   - **记录类型**: CNAME
   - **记录名**: `bltestdata`
   - **记录值**: `ai-dashboard-6p0.pages.dev`
   - **TTL**: 3600 或自动

### 6. 验证配置
完成后，运行以下命令检查 DNS：
```bash
nslookup bltestdata.aipush.fun
# 或
dig bltestdata.aipush.fun
```

应该看到指向 Cloudflare Pages 的 DNS 记录。

### 7. 清除缓存
- 如果域名配置后仍然无法访问，可能是 DNS 缓存问题
- 在浏览器中按 `Ctrl+Shift+Delete` 清除缓存
- 或者在无痕模式下访问

## 常见问题

### DNS 传播延迟
DNS 记录可能需要 24 小时才能完全传播，但通常 5-10 分钟就有效。

### 仍然显示空白
1. 检查浏览器 F12 控制台，查看是否有加载错误
2. 确认 `data/latest.json` 文件是否存在于仓库
3. 检查网络请求，确保资源能正常加载

### HTTPS 证书错误
如果看到证书警告：
- 等待 SSL 证书生成（通常 5 分钟内）
- 尝试用 HTTP 访问（会自动重定向到 HTTPS）

## 技术细节

- **部署方式**: Cloudflare Pages（静态站点）
- **项目名称**: ai-dashboard
- **分支**: main
- **构建设置**: 无需构建（直接部署）

## 部署状态
可以在 Cloudflare Dashboard > Pages > ai-dashboard > Deployments 查看部署历史和状态。

---

**注**: 如果以上步骤无法解决问题，请检查：
1. GitHub 仓库是否为公开
2. Cloudflare 账户是否有效
3. GitHub Actions 的部署 workflow 是否成功
