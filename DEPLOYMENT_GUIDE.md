# Cloudflare Pages 部署指南

## 问题说明
GitHub Actions的部署workflow失败，原因是缺少Cloudflare API Token配置。

## 解决方案（推荐）

### 方式：使用 Cloudflare Pages 的 GitHub 集成（自动部署）

这是最简单、最稳定的方式。无需配置任何token，代码推送后自动部署。

#### 步骤 1：访问 Cloudflare Dashboard

1. 登录 https://dash.cloudflare.com/
2. 左侧菜单选择 "Workers & Pages"
3. 点击 "Pages" 标签

#### 步骤 2：连接 GitHub 仓库

1. 点击 "创建应用" 按钮
2. 选择 "连接 Git" 标签
3. 点击 "GitHub" 按钮
4. 授权 Cloudflare 访问你的 GitHub 账户
5. 搜索 "ai-dashboard" 仓库
6. 点击 "连接"

#### 步骤 3：配置部署设置

配置项如下：

| 字段 | 值 |
|------|-----|
| **Production branch** | main |
| **Build command** | （留空 - 无需构建） |
| **Build output directory** | / |
| **Root directory** | / |

点击 "保存和部署"

#### 步骤 4：配置自定义域名

部署完成后，在项目设置中：

1. 左侧菜单选择 "Custom domains"
2. 点击 "添加自定义域名"
3. 输入：`bltestdata.aipush.fun`
4. 配置 DNS 记录（如需要）

#### 验证部署

部署完成后，可以访问：
- **默认域名**：https://ai-dashboard-6p0.pages.dev/
- **自定义域名**：https://bltestdata.aipush.fun/

## 手动部署（可选）

如果需要手动部署，可以在 Cloudflare Dashboard 中：

1. 进入项目 "ai-dashboard"
2. 点击 "Deployments" 标签
3. 找到最新的部署记录
4. 点击 "Revert" 或 "Retry" 按钮

## 常见问题

### 部署后网站仍显示旧内容

**原因**：浏览器缓存或CDN缓存

**解决**：
1. 按 `Ctrl+Shift+Delete` 清除浏览器缓存
2. 或在无痕模式下访问
3. 等待 CDN 缓存更新（通常 5-10 分钟）

### DNS 解析失败

**原因**：自定义域名的 DNS 记录配置不正确

**解决**：
1. 确认域名 `aipush.fun` 已在 Cloudflare 托管
2. 在 Cloudflare Dashboard 的 DNS 中检查 `bltestdata` 记录
3. 确保指向 Cloudflare Pages

### 页面加载为空白

**原因**：`data/latest.json` 文件缺失或网络请求失败

**解决**：
1. 检查 GitHub 仓库中是否存在 `data/latest.json`
2. 查看浏览器控制台是否有错误
3. 确认 GitHub Actions 数据更新任务是否成功运行

## 工作流程总结

```
代码推送到 GitHub main 分支
          ↓
Cloudflare Pages 自动检测变更
          ↓
部署到 Cloudflare CDN
          ↓
自动更新所有域名（ai-dashboard-6p0.pages.dev、bltestdata.aipush.fun）
          ↓
用户访问最新版本
```

## 参考链接

- [Cloudflare Pages 官方文档](https://developers.cloudflare.com/pages/)
- [Git 集成指南](https://developers.cloudflare.com/pages/get-started/git-integration/)
- [自定义域名配置](https://developers.cloudflare.com/pages/platform/custom-domains/)
