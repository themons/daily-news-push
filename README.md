# 📰 每日早报推送

通过 GitHub Actions 每天早上 8:00（北京时间）自动抓取新闻并推送到微信。

## 推送内容

- 🏛️ 国家大事 3-5条
- 📰 今日要闻 3-5条
- 😊 民生趣闻 3-5条
- 📜 古今今日 2-4条
- 🌅 今日人事 2-4条

## 部署步骤

### 1. 注册 PushPlus
1. 打开 https://pushplus.plus
2. 微信扫码登录
3. 复制你的 Token

### 2. Fork 本仓库

### 3. 添加 GitHub Secret
1. 进入仓库 Settings → Secrets and variables → Actions
2. 点击 `New repository secret`
3. Name: `PUSHPLUS_TOKEN`
4. Value: 粘贴你的 PushPlus Token
5. 保存

### 4. 测试
进入 Actions 页面 → 选择「每日早报推送」→ 点击 `Run workflow` 手动测试

## 注意
- GitHub Actions 的 cron 有几分钟延迟，属正常现象
- 免费额度足够日常使用
