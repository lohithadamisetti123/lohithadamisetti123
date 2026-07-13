from pathlib import Path
from textwrap import dedent
content=dedent(r'''
<h1 align="center">Hi 👋 I'm Lohitha Damisetti</h1>
<h3 align="center">Backend Engineer • AI Developer • Full Stack Developer</h3>

<p align="center">
Building scalable backend systems, AI-powered applications, and modern web experiences.
</p>

<p align="center">
<a href="https://github.com/lohithadamisetti123"><img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github"></a>
<a href="https://www.linkedin.com/in/lohitha-damisetti-2bb36829a/"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin"></a>
<a href="https://instagram.com/"><img src="https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram"></a>
<a href="https://your-portfolio.vercel.app"><img src="https://img.shields.io/badge/Portfolio-000000?style=for-the-badge&logo=vercel"></a>
<a href="mailto:damisettilohitha@gmail.com"><img src="https://img.shields.io/badge/Email-EA4335?style=for-the-badge&logo=gmail"></a>
</p>

<p align="center">
<img src="./Assets/output.gif" width="100%">
</p>

## 🚀 About Me

- 🎓 B.Tech Data Science, Aditya College of Engineering and Technology
- 💼 Full Stack Developer focused on Backend & AI
- 🏆 Top 100 – Myntra HackerRamp WeForShe
- 📹 Tech content creator sharing developer resources
- 🌱 Currently learning AWS, Kubernetes, System Design, AI Agents, Vector Databases

### 💬 Ask me about
`Python` `Django` `FastAPI` `React` `AWS` `Docker` `PostgreSQL` `MongoDB` `Redis` `LLMs` `Prompt Engineering` `System Design`

## 🛠 Tech Stack

### Backend
<p><img src="https://skillicons.dev/icons?i=python,django,fastapi,nodejs,express"/></p>

### Frontend
<p><img src="https://skillicons.dev/icons?i=react,js,html,css,tailwind"/></p>

### Cloud & DevOps
<p><img src="https://skillicons.dev/icons?i=aws,docker,linux,git,github"/></p>

### Databases
<p><img src="https://skillicons.dev/icons?i=postgres,mongodb,redis,mysql"/></p>

### AI / ML
<p><img src="https://skillicons.dev/icons?i=python"/></p>

OpenAI API • Gemini API • LangChain • LLMs • Prompt Engineering • Vector Databases • Ollama

### Tools
Postman • Swagger • VS Code • Figma • Vercel • Electron

## ⭐ Featured Projects

### 🔐 PolicyGuard AI
AI-powered Privacy Risk Analyzer using React, React Native, Electron, FastAPI, MongoDB and OpenAI APIs.

### 🏢 Multi-Tenant SaaS Platform
Secure multi-tenant application with RBAC, Docker and PostgreSQL.

### 💳 Payment Gateway
Hosted checkout with Spring Boot, React and PostgreSQL.

### 🌐 Tech360
Career portal with contest tracking and developer resources.

## 📊 GitHub Analytics

<p align="center">
<img width="49%" src="https://github-readme-stats.vercel.app/api?username=lohithadamisetti123&show_icons=true&theme=tokyonight"/>
<img width="49%" src="https://github-readme-stats.vercel.app/api/top-langs/?username=lohithadamisetti123&layout=compact&theme=tokyonight"/>
</p>

<p align="center">
<img width="70%" src="https://streak-stats.demolab.com?user=lohithadamisetti123&theme=tokyonight"/>
</p>

<p align="center">
<img src="https://github-profile-trophy.vercel.app/?username=lohithadamisetti123&theme=tokyonight&no-frame=true&row=1&column=6"/>
</p>

## 🐍 Contribution Snake

<p align="center">
<img src="https://raw.githubusercontent.com/lohithadamisetti123/lohithadamisetti123/output/github-contribution-grid-snake.svg">
</p>

## 🤝 Connect

- 📧 damisettilohitha@gmail.com
- 💼 LinkedIn: https://www.linkedin.com/in/lohitha-damisetti-2bb36829a/
- 💻 GitHub: https://github.com/lohithadamisetti123

---
<p align="center"><b>Thanks for visiting! ⭐ If you like my work, consider following my GitHub.</b></p>
''')
path=Path('/mnt/data/README.md')
path.write_text(content)
print(path)
