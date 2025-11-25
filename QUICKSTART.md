# Quick Start Guide - Wordly Solver

## 🚀 Chạy Project (Full Stack)

### Option 1: Docker Compose (Khuyến nghị)

```bash
# Đảm bảo Docker Desktop đang chạy
docker-compose up --build
```

**Truy cập:**
- Game: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

---

### Option 2: Development Mode (Riêng biệt)

#### 1. Backend (Terminal 1)
```bash
cd Backend
pip install -r Requirements.txt
uvicorn main:app --reload --port 8000
```

✅ Backend chạy tại: http://localhost:8000

#### 2. Frontend (Terminal 2)
```bash
cd FrontEnd
npm install
npm run dev
```

✅ Frontend chạy tại: http://localhost:3000

---

## 📝 Test Backend API

### Health Check
```bash
curl http://localhost:8000/health
```

### Validate Word
```bash
curl -X POST http://localhost:8000/api/validate \
  -H "Content-Type: application/json" \
  -d "{\"word\": \"hello\"}"
```

### Agent Solver
```bash
curl -X POST http://localhost:8000/api/solve \
  -H "Content-Type: application/json" \
  -d "{\"guesses\": [\"AROSE\"], \"evaluations\": [[\"absent\",\"absent\",\"absent\",\"present\",\"absent\"]]}"
```

### Word Statistics
```bash
curl http://localhost:8000/api/words/stats
```

---

## 🎮 Cách Chơi

1. Mở http://localhost:3000
2. Nhập từ 5 chữ cái
3. Nhấn Enter để submit
4. Xem feedback:
   - 🟩 Xanh = Đúng vị trí
   - 🟨 Vàng = Sai vị trí
   - ⬛ Xám = Không có trong từ
5. Đoán đúng trong 6 lượt!

### 🤖 Sử dụng Agent
- Nhấn button **"Agent"** để AI tự động giải
- Agent sẽ sử dụng Backend API (nếu có)
- Tự động fallback về client-side nếu backend down

---

## 🛠️ Docker Commands

```bash
# Khởi động
docker-compose up -d

# Xem logs
docker-compose logs -f

# Xem logs backend
docker-compose logs -f backend

# Dừng
docker-compose down

# Rebuild
docker-compose up --build

# Xóa hết
docker-compose down -v
```

---

## 🐛 Troubleshooting

### Backend không kết nối
```bash
# Kiểm tra backend có chạy không
curl http://localhost:8000/health

# Xem logs
docker-compose logs backend
```

### Port bị chiếm
```bash
# Windows - Kiểm tra port 8000
netstat -ano | findstr :8000

# Kill process
taskkill /PID <PID> /F
```

### CORS Error
- Kiểm tra `NEXT_PUBLIC_API_URL` trong `.env.local`
- Xem CORS settings trong `Backend/main.py`

---

## 📚 API Documentation

Sau khi chạy backend, truy cập:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## ✅ Checklist Deploy

- [ ] Docker Desktop đang chạy
- [ ] Port 3000 và 8000 không bị chiếm
- [ ] File `words.txt` có trong cả `Backend/` và `FrontEnd/public/`
- [ ] `.env.local` đã được tạo trong `FrontEnd/`
- [ ] Dependencies đã install (nếu dev mode)

---

## 🎯 Features

- ✅ 14,855+ từ vựng
- ✅ Daily & Random mode
- ✅ AI Agent với DFS algorithm
- ✅ Backend API (FastAPI)
- ✅ Real-time validation
- ✅ Statistics tracking
- ✅ Beautiful UI với animations
- ✅ Keyboard support
- ✅ Auto-fallback (Backend → Client)

---

## 📞 Hỗ trợ

Nếu gặp vấn đề:
1. Check logs: `docker-compose logs`
2. Verify health: `curl http://localhost:8000/health`
3. Restart: `docker-compose restart`
