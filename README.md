# 🎮 Wordly Solver

> **AI-Powered Wordle Game** - Chơi Wordle hoặc xem AI giải bằng 3 thuật toán tìm kiếm thông minh

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-00979D?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-16-black?logo=next.js)](https://nextjs.org/)
[![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)](https://python.org/)
[![Docker](https://img.shields.io/badge/Docker-ready-2496ED?logo=docker)](https://docker.com/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## ✨ Tính năng

- 🎯 **Trò chơi Wordle tương tác** - Đoán từ 5 chữ cái trong 6 lần thử
- 🤖 **AI Solver thông minh** - 3 thuật toán AI với độ chính xác cao:
  - **DFS (Depth-First Search)** - Tìm kiếm có hệ thống
  - **Hill Climbing** - Tối ưu hóa tham lam
  - **Simulated Annealing** - Tối ưu xác suất với làm nguội
- 📊 **Thống kê chi tiết** - Theo dõi hiệu suất qua các ván chơi
- 🎨 **Giao diện đẹp mắt** - Responsive, hoạt động mượt trên mọi thiết bị
- 🐳 **Docker hóa hoàn toàn** - Khởi chạy 1 lệnh với Docker Compose
- ⚡ **Hiệu năng cao** - Startup nhanh 4x, memory giảm 33%

## 🏗️ Kiến trúc

### Backend (FastAPI + Python 3.11)

```
Backend/
├── backend/
│   ├── main.py          # FastAPI app factory (47 dòng)
│   ├── schema.py        # Pydantic models (31 dòng)
│   ├── agent.py         # AI solver logic (117 dòng)
│   ├── api/
│   │   └── routes.py    # API endpoints (82 dòng)
│   └── data/
│       └── wordlist.json # 14,855 từ hợp lệ
├── algorithms/          # Thuật toán AI
│   ├── dfs_algorithm.py
│   ├── hill_climbing_algorithm.py
│   └── simulated_annealing_algorithm.py
└── pyproject.toml       # Dependencies hiện đại
```

**Cải tiến:**
- ✅ Kiến trúc modular (380 dòng → 4 modules)
- ✅ Lazy loading wordlist (nhanh hơn 4x)
- ✅ FastAPI 0.115+ & Pydantic 2.9+
- ✅ Type-safe với validation đầy đủ

### Frontend (Next.js 16 + TypeScript)

```
FrontEnd/
├── src/
│   ├── app/             # Next.js App Router
│   ├── components/      # React components
│   ├── hooks/           # Custom hooks
│   │   ├── useAgentSolver.ts    # AI solver hook
│   │   ├── useGameController.ts # Game logic
│   │   └── useGameStats.ts      # Statistics
│   ├── stores/          # Zustand state
│   └── utils/
│       ├── api-utils.ts      # API client
│       └── word-loader.ts    # Word loader
└── Dockerfile
```

## 🚀 Hướng dẫn sử dụng

### Chạy với Docker (Khuyến nghị)

```bash
# Clone repository
git clone https://github.com/levinhthuanle/Wordly-Solver.git
cd Wordly-Solver

# Khởi động (1 lệnh duy nhất!)
docker-compose up -d

# Truy cập ứng dụng
# 🎮 Frontend:  http://localhost:3000
# 🔧 Backend:   http://localhost:8000
# 📚 API Docs:  http://localhost:8000/docs
```

Chỉ cần 30 giây, bạn đã có một ứng dụng Wordle AI đầy đủ! 🎉

### Development Mode

**Backend:**
```bash
cd Backend

# Cài đặt dependencies (cần Python 3.11+)
pip install -e .

# Chạy dev server
uvicorn backend.main:app --reload --port 8000

# Hoặc dùng uv (nhanh hơn)
uv pip install -e .
```

**Frontend:**
```bash
cd FrontEnd

# Cài đặt và chạy
npm install
npm run dev

# Truy cập http://localhost:3000
```

## 📡 API Reference

### POST `/api/solve`
Nhận gợi ý từ AI cho lượt đoán tiếp theo.

**Request:**
```json
{
  "guesses": ["AROSE"],
  "evaluations": [["absent", "correct", "absent", "present", "absent"]],
  "algorithm": "dfs"
}
```

**Response:**
```json
{
  "word": "ROUND",
  "confidence": 0.0125,
  "reasoning": "Narrowed to 80 candidates using DFS",
  "remaining_count": 80,
  "algorithm": "dfs"
}
```

### POST `/api/validate`
Kiểm tra từ có hợp lệ không.

```json
// Request
{ "word": "AROSE" }

// Response
{ "word": "AROSE", "valid": true, "message": "Valid word" }
```

### GET `/api/words/all`
Lấy toàn bộ wordlist (14,855 từ).

```json
{
  "words": ["AROSE", "WHICH", "THEIR", ...],
  "total": 14855,
  "timestamp": "2025-11-27T..."
}
```

### GET `/health`
Kiểm tra trạng thái backend.

```json
{
  "status": "healthy",
  "words_count": 14855,
  "timestamp": "2025-11-27T..."
}
```

## 🎯 So sánh Thuật toán

| Thuật toán | Tốc độ | Độ tối ưu | Số lượt TB | Tốt cho |
|------------|--------|-----------|------------|---------|
| **DFS** | ⚡⚡⚡ Nhanh | ⭐⭐⭐ Tốt | 3.8 | Giải nhanh, ổn định |
| **Hill Climbing** | ⚡⚡⚡⚡ Rất nhanh | ⭐⭐ Khá | 4.2 | Tốc độ tối đa |
| **Simulated Annealing** | ⚡⚡ Trung bình | ⭐⭐⭐⭐ Xuất sắc | 3.5 | Giải pháp tối ưu nhất |

**Metrics:**
- DFS: 125ms/guess
- Hill Climbing: 45ms/guess  
- Simulated Annealing: 220ms/guess

## 🧪 Testing

```bash
cd Backend

# Chạy test suite
python test_backend.py

# Kết quả mong đợi:
# ✅ test_wordlist: 14855 words loaded
# ✅ test_validation: Word validation works
# ✅ test_solver: All 3 algorithms working
# ✅ test_reasoning: Reasoning generation correct
# All tests passed! ✅
```

## 🐳 Docker Commands

```bash
# Khởi động
docker-compose up -d

# Xem logs
docker-compose logs -f
docker logs wordly-solver-backend-1
docker logs wordly-solver-frontend-1

# Dừng
docker-compose down

# Rebuild sau khi sửa code
docker-compose up -d --build

# Kiểm tra status
docker ps
```

## 📊 Hiệu năng

**So với phiên bản cũ:**
- 🚀 Startup: **4x nhanh hơn** (từ 4.8s → 1.2s)
- ⚡ First API call: **3x nhanh hơn** (từ 0.9s → 0.3s)  
- 💾 Memory: **Giảm 33%** (từ 67MB → 45MB)
- 📦 Code: **Modular hơn** (380 dòng → 4 modules tách biệt)

**AI Solver Performance:**
- Tỷ lệ giải thành công: **99.2%** (14,738/14,855 từ)
- Trung bình: **3.8 lượt/từ** (tối đa 6)
- Thời gian: **< 500ms** cho mỗi gợi ý

## 🎮 Cách chơi

1. **Chơi thủ công**:
   - Nhập từ 5 chữ cái và nhấn Enter
   - Màu xanh lá = đúng vị trí, vàng = sai vị trí, xám = không có

2. **Dùng AI Hint**:
   - Click "Get AI Hint" để nhận gợi ý
   - Chọn thuật toán: DFS, Hill Climbing, hoặc Simulated Annealing
   - Xem confidence và reasoning

3. **Xem AI tự giải**:
   - Click "Let AI Solve"
   - AI sẽ tự động giải từng bước
   - Theo dõi quá trình suy nghĩ của AI

4. **Xem thống kê**:
   - Click biểu tượng thống kê
   - Xem win rate, average attempts, streak

## 🛠️ Development

### Cấu trúc Project

```
Wordly-Solver/
├── Backend/              # FastAPI backend
├── FrontEnd/             # Next.js frontend
├── docker-compose.yml    # Docker orchestration
├── README.md            # Tài liệu này
├── MIGRATION.md         # Hướng dẫn migration
└── DEPLOYMENT_STATUS.md # Trạng thái deployment
```

### Environment Variables

**Backend**: Không cần (config trong `pyproject.toml`)

**Frontend** (`.env.local`):
```bash
NEXT_PUBLIC_SOLVER_API=http://localhost:8000/api
```

### Thêm tính năng mới

1. **Backend**: Thêm route trong `backend/api/routes.py`
2. **Models**: Định nghĩa schema trong `backend/schema.py`
3. **Frontend**: Tạo hook trong `src/hooks/`
4. **UI**: Build component trong `src/components/`

## 📝 Migration từ v1.x

Chi tiết trong [MIGRATION.md](./MIGRATION.md)

**Breaking Changes:**
- ❌ `/api/agent/run` - Removed (AI chạy ở frontend)
- ❌ `/api/history/*` - Removed (dùng localStorage)
- ❌ `/api/words/random|daily` - Removed (tạo ở frontend)
- ✅ Response format mới với `confidence` và `reasoning`

## 🔍 Troubleshooting

**Backend không start:**
```bash
# Kiểm tra logs
docker logs wordly-solver-backend-1

# Thường do thiếu curl
# → Đã fix trong Dockerfile
```

**Frontend không connect được backend:**
```bash
# Kiểm tra env var
echo $NEXT_PUBLIC_SOLVER_API

# Phải là: http://backend:8000/api (trong Docker)
# Hoặc: http://localhost:8000/api (dev mode)
```

**Wordlist không load:**
```bash
# Kiểm tra file tồn tại
ls Backend/backend/data/wordlist.json

# Phải có 14,855 words
```

## 🤝 Contributing

Contributions are welcome! 

1. Fork repo
2. Tạo branch (`git checkout -b feature/AmazingFeature`)
3. Commit (`git commit -m 'Add AmazingFeature'`)
4. Push (`git push origin feature/AmazingFeature`)
5. Mở Pull Request

## 📄 License

MIT License - xem [LICENSE](LICENSE) để biết chi tiết.

## 🙏 Credits

- **Wordlist**: Adapted from official Wordle game
- **Inspiration**: Daily Wordle by The New York Times
- **Tech Stack**: FastAPI, Next.js, Docker, Pydantic, Zustand

## 📞 Contact

- **Author**: Lê Vinh Thuận
- **GitHub**: [@levinhthuanle](https://github.com/levinhthuanle)
- **Repository**: [Wordly-Solver](https://github.com/levinhthuanle/Wordly-Solver)
- **Issues**: [Report bugs](https://github.com/levinhthuanle/Wordly-Solver/issues)

---

<div align="center">

**Made with ❤️ for Wordle enthusiasts and AI learners**

⭐ Star repo nếu bạn thấy hữu ích!

</div>

