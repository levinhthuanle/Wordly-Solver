# Docker Deploy Instructions

## Hướng dẫn Deploy với Docker

### Bước 1: Đảm bảo Docker Desktop đang chạy

1. Mở Docker Desktop
2. Đợi icon Docker trên taskbar ngừng xoay (thường 30-60 giây)
3. Kiểm tra:
```powershell
docker ps
```
Nếu thấy output (có thể rỗng) → OK!

---

### Bước 2: Build và Run

**Từ thư mục gốc project:**

```powershell
cd d:\study\term_7\AI\midterm_project\Wordly-Solver

# Build và start containers
docker-compose up --build
```

**Hoặc chạy ở background:**
```powershell
docker-compose up -d --build
```

---

### Bước 3: Truy cập

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

---

## Quản lý Containers

### Xem trạng thái
```powershell
docker-compose ps
```

### Xem logs
```powershell
# Tất cả services
docker-compose logs -f

# Chỉ backend
docker-compose logs -f backend

# Chỉ frontend
docker-compose logs -f frontend
```

### Dừng containers
```powershell
docker-compose down
```

### Restart containers
```powershell
docker-compose restart
```

### Rebuild và restart
```powershell
docker-compose down
docker-compose up --build
```

### Xóa tất cả (containers, networks, volumes)
```powershell
docker-compose down -v
docker system prune -a
```

---

## Troubleshooting

### Lỗi: "cannot find file dockerDesktopLinuxEngine"
**Nguyên nhân:** Docker Desktop chưa chạy

**Giải pháp:**
1. Mở Docker Desktop
2. Đợi khởi động hoàn tất (30-60s)
3. Chạy lại `docker-compose up --build`

---

### Lỗi: Port already in use
**Nguyên nhân:** Port 3000 hoặc 8000 đang được sử dụng

**Giải pháp:**
```powershell
# Tìm process đang dùng port 3000
netstat -ano | findstr :3000

# Tìm process đang dùng port 8000
netstat -ano | findstr :8000

# Kill process (thay <PID> bằng process ID)
taskkill /PID <PID> /F
```

**Hoặc đổi port trong docker-compose.yml:**
```yaml
services:
  frontend:
    ports:
      - "3001:3000"  # Host:Container
  backend:
    ports:
      - "8001:8000"  # Host:Container
```

---

### Lỗi: Build failed
**Giải pháp:**
```powershell
# Xóa cache và rebuild
docker-compose down -v
docker system prune -a
docker-compose build --no-cache
docker-compose up
```

---

### Container chạy nhưng không truy cập được
**Kiểm tra:**
```powershell
# Xem container có đang chạy không
docker-compose ps

# Xem logs để tìm lỗi
docker-compose logs backend
docker-compose logs frontend

# Test trực tiếp vào container
docker exec -it wordly-solver-backend-1 curl http://localhost:8000/health
```

---

### Frontend không kết nối được Backend
**Kiểm tra:**
1. Backend có chạy không: `curl http://localhost:8000/health`
2. Kiểm tra network: `docker network ls`
3. Kiểm tra env variable trong frontend container:
```powershell
docker exec -it wordly-solver-frontend-1 env | grep API_URL
```

---

## Development vs Production

### Development Mode (Khuyến nghị khi dev)
```powershell
# Terminal 1 - Backend
cd Backend
uvicorn main:app --reload --port 8000

# Terminal 2 - Frontend
cd FrontEnd
npm run dev
```

**Ưu điểm:**
- Hot reload
- Dễ debug
- Build nhanh hơn

### Production Mode (Docker)
```powershell
docker-compose up --build
```

**Ưu điểm:**
- Môi trường giống production
- Dễ deploy
- Isolated environment

---

## Kiểm tra sau khi Deploy

### 1. Backend Health Check
```powershell
curl http://localhost:8000/health
```
Kết quả mong đợi:
```json
{
  "status": "healthy",
  "words_count": 14855
}
```

### 2. Frontend Load
Mở browser: http://localhost:3000
- Trang game hiển thị đúng
- Có thể nhập từ
- Keyboard hoạt động

### 3. Agent Test
1. Click button "Agent"
2. Xem console log (F12)
3. Kiểm tra có message: "🚀 Using backend solver" hoặc "💻 Using client-side solver"

### 4. Backend Logs
```powershell
docker-compose logs backend | findstr "Loaded"
```
Phải thấy: "✅ Loaded 14855 words"

---

## Quick Commands

```powershell
# Start
docker-compose up -d

# Stop
docker-compose down

# Restart
docker-compose restart

# Logs
docker-compose logs -f

# Rebuild
docker-compose up --build

# Clean all
docker-compose down -v; docker system prune -a
```

---

## Notes

- Build lần đầu có thể mất 5-10 phút
- Frontend build chiếm nhiều memory (~2GB)
- Backend start nhanh (~10 giây)
- Nếu gặp lỗi, xem logs: `docker-compose logs`
