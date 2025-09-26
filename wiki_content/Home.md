# Github CVE Monitor 👀

> 基于 GitHub Actions 的自动 CVE 监控系统

## 项目简介

Github CVE Monitor 是一个自动化的安全情报收集工具，通过 GitHub Actions 定期扫描并监控最新的 CVE（常见漏洞和暴露）信息。系统每日自动更新，为安全研究人员和开发团队提供最新的漏洞情报。

## 主要功能

- 🔄 **自动化监控**: 使用 GitHub Actions 每日自动运行
- 📊 **数据分析**: 从 GitHub CVE 数据库收集和分析漏洞信息
- 📈 **趋势跟踪**: 按日期和类型跟踪漏洞趋势
- 🗂️ **分类整理**: 按 CVE 编号和日期进行系统化分类
- 📱 **易于访问**: 通过 GitHub Pages 提供 Web 界面

## 快速导航

- 📋 [每日报告](每日报告) - 查看最新的每日情报速递
- 📝 [更新日志](更新日志) - 项目变更记录
- 📊 [统计数据](统计数据) - CVE 统计信息和趋势分析
- ℹ️ [关于项目](关于项目) - 项目详细信息和作者介绍

## 数据来源

- **GitHub CVE 数据库**: 官方 CVE 记录
- **更新频率**: 每日凌晨 1:00 (UTC)
- **数据格式**: Markdown 报告和 JSON 数据

## 技术架构

- **运行环境**: GitHub Actions (Ubuntu Latest)
- **编程语言**: Python 3.x
- **数据存储**: GitHub 仓库
- **前端展示**: GitHub Pages + Docsify

## 版本信息

当前版本: **3.0**

![Version](https://img.shields.io/badge/version-3.0-blue.svg)

---

© 2025 [adminlove520](https://github.com/adminlove520) | 本项目基于开源协议发布