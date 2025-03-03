# 🚀 AttendEase

A simple and efficient employee attendance tracking system built using **Django, SQLite, and React**. Employees can check in, check out, and view their attendance records, while admins can manage and monitor attendance data seamlessly.

![Image](https://github.com/user-attachments/assets/b1f10146-f5ee-4833-9882-de23e621125a)

## 🌟 Features
- ✅ Employee check-in and check-out system
- 📊 Attendance record tracking
- 🛠️ Admin dashboard to view all employee records
- 🔐 Secure authentication system
- 🎨 User-friendly interface

## 🏗️ Tech Stack
- 💻 **Frontend:** React
- 🖥️ **Backend:** Django (Django REST Framework)
- 🗄️ **Database:** SQLite

## 🔗 API Endpoints
| ⚡ Method | 🔗 Endpoint | 📝 Description |
|--------|-------------|-------------|
| `POST` | `/api/auth/signup/` | 🆕 User registration |
| `POST` | `/api/auth/login/` | 🔑 User login |
| `POST` | `/api/auth/logout/` | 🚪 User logout |
| `POST` | `/api/attendance/check-in/<username>/` | ⏰ Employee check-in |
| `POST` | `/api/attendance/check-out/<username>/` | 🏁 Employee check-out |
| `GET` | `/api/attendance/<username>/` | 📅 Get employee attendance records |
| `GET` | `/api/attendance/all/` | 📂 Get all employees' attendance records |

## ☕ Buy Me a Coffee
[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-Support%20Me-orange?style=flat&logo=buy-me-a-coffee)](https://buymeacoffee.com/kan15hka)

My code runs on caffeine, and so do I. Help me fuel the next bug fix! Send caffeine my way like this. 🚀
