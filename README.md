# Wordly-Solver

Game Wordle với AI Agent tích hợp 3 thuật toán: DFS, Hill Climbing, và Simulated Annealing.

## 🎯 Tính năng

- 🎮 Game Wordle với 14,855+ từ tiếng Anh
- 🤖 **AI Agent với 3 thuật toán** (DFS, Hill Climbing, Simulated Annealing)
- 📊 Theo dõi lịch sử và thống kê trò chơi
- ⌨️ Hỗ trợ bàn phím
- 🎨 Giao diện đẹp với animation
- 🐳 Docker deployment sẵn sàng

## 🏗️ Kiến trúc

```
Wordly-Solver/
├── Backend/                    # Python FastAPI server
│   ├── algorithms/            # ⭐ Thuật toán AI (Python)
│   │   ├── base_agent.py     # Abstract class cho tất cả thuật toán
│   │   ├── dfs_algorithm.py  # DFS algorithm
│   │   ├── hill_climbing_algorithm.py
│   │   └── simulated_annealing_algorithm.py
│   ├── history/              # Lưu trữ lịch sử game
│   │   └── game_history.py   # JSON storage cho game history
│   ├── main.py               # FastAPI endpoints
│   └── words.txt             # Danh sách 14,855 từ
│
└── FrontEnd/                  # Next.js UI
    └── src/
        ├── components/        # React components
        ├── hooks/            # Game logic hooks
        └── utils/            # Utilities & API client
```

### Phân chia trách nhiệm

**Backend (Python)**
- ✅ Tất cả logic thuật toán AI
- ✅ Lưu trữ và truy vấn lịch sử game
- ✅ Validation từ
- ✅ API endpoints

**Frontend (Next.js/TypeScript)**
- ✅ Giao diện người dùng
- ✅ Game state management (Zustand)
- ✅ API calls tới Backend
- ✅ Chỉ hiển thị, không có logic giải Wordle

## 🚀 Chạy dự án

### Yêu cầu
- Docker Desktop (khuyến nghị)
- Hoặc: Python 3.11+ và Node.js 18+

### Cách 1: Docker Compose (Khuyến nghị)

```bash
# Khởi động cả Frontend và Backend
docker-compose up --build
```

**Truy cập:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Cách 2: Development Mode

**Backend:**
```bash
cd Backend
pip install -r Requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend:**
```bash
cd FrontEnd
npm install
npm run dev
```

## 🤖 Hướng dẫn phát triển Thuật toán

### Kiến trúc thuật toán

Tất cả thuật toán đều nằm trong `Backend/algorithms/` và kế thừa từ `BaseAgent`:

```
algorithms/
├── __init__.py              # Factory pattern: create_agent()
├── base_agent.py            # Abstract base class với shared logic
├── dfs_algorithm.py         # DFS implementation
├── hill_climbing_algorithm.py
└── simulated_annealing_algorithm.py
```

### So sánh 3 thuật toán hiện tại

| Thuật toán | Chiến lược | Ưu điểm | Nhược điểm |
|-----------|-----------|---------|-----------|
| **DFS** | Frequency-based scoring | Ổn định, đáng tin cậy | Có thể chậm |
| **Hill Climbing** | Greedy local search | Nhanh | Dễ bị stuck ở local optima |
| **Simulated Annealing** | Probabilistic search | Thoát được local optima | Ít dự đoán được |

### BaseAgent - Shared Logic

File `base_agent.py` cung cấp các method dùng chung:

```python
from abc import ABC, abstractmethod

class BaseAgent(ABC):
    """Base class cho tất cả thuật toán"""
    
    def __init__(self, word_list: list[str]):
        self.word_list = [word.upper() for word in word_list]
        self.possible_words = self.word_list.copy()
    
    # Abstract method - phải implement trong subclass
    @abstractmethod
    def choose_best_guess(self, possible_words: list[str]) -> str:
        """Logic chọn từ tiếp theo - IMPLEMENT THUẬT TOÁN Ở ĐÂY"""
        pass
    
    # Shared methods - dùng được trong mọi thuật toán
    def filter_possible_words(self, guess: str, evaluation: list[str]) -> None:
        """Lọc danh sách từ dựa trên feedback"""
        pass
    
    def score_word_frequency(self, word: str, possible_words: list[str]) -> float:
        """Tính điểm dựa trên tần suất chữ cái"""
        pass
    
    def score_word_entropy(self, word: str, possible_words: list[str]) -> float:
        """Tính entropy (information gain) của từ"""
        pass
    
    def simulate_evaluation(self, guess: str, answer: str) -> list[str]:
        """Mô phỏng feedback nếu đoán từ này"""
        pass
    
    def get_optimal_starters(self) -> list[str]:
        """Trả về danh sách từ mở đầu tối ưu"""
        return ['AROSE', 'SLATE', 'CRATE', 'TRACE', 'STARE']
```

### Cách thêm thuật toán mới

#### Bước 1: Tạo file thuật toán mới

Tạo file `Backend/algorithms/my_algorithm.py`:

```python
from .base_agent import BaseAgent
import random

class MyAlgorithmAgent(BaseAgent):
    """Mô tả thuật toán của bạn"""
    
    def choose_best_guess(self, possible_words: list[str]) -> str:
        """
        Logic chọn từ tiếp theo.
        
        Args:
            possible_words: Danh sách từ còn khả năng đúng
            
        Returns:
            Từ được chọn để đoán
        """
        if not possible_words:
            return random.choice(self.word_list)
        
        # Nếu chỉ còn 1 từ, chọn luôn
        if len(possible_words) == 1:
            return possible_words[0]
        
        # === IMPLEMENT THUẬT TOÁN CỦA BẠN Ở ĐÂY ===
        
        # Ví dụ: Chọn từ có entropy cao nhất
        best_word = possible_words[0]
        best_score = -1
        
        # Sample 100 từ để tăng tốc độ
        sample_size = min(100, len(possible_words))
        candidates = random.sample(possible_words, sample_size)
        
        for word in candidates:
            # Dùng helper method từ BaseAgent
            score = self.score_word_entropy(word, possible_words)
            
            if score > best_score:
                best_score = score
                best_word = word
        
        return best_word
```

**Helper methods có sẵn từ BaseAgent:**

```python
# Tính điểm frequency (càng cao càng tốt)
score = self.score_word_frequency(word, possible_words)

# Tính entropy - information gain (càng cao càng tốt)
entropy = self.score_word_entropy(word, possible_words)

# Mô phỏng feedback
evaluation = self.simulate_evaluation(guess="AROSE", answer="SLATE")
# Returns: ["absent", "absent", "absent", "present", "correct"]

# Lấy từ mở đầu tối ưu
starters = self.get_optimal_starters()
# Returns: ['AROSE', 'SLATE', 'CRATE', 'TRACE', 'STARE']
```

#### Bước 2: Đăng ký vào Factory

Sửa file `Backend/algorithms/__init__.py`:

```python
from .base_agent import BaseAgent
from .dfs_algorithm import DFSAgent
from .hill_climbing_algorithm import HillClimbingAgent
from .simulated_annealing_algorithm import SimulatedAnnealingAgent
from .my_algorithm import MyAlgorithmAgent  # Import thuật toán mới

def create_agent(word_list: list[str], algorithm: str) -> BaseAgent:
    """Factory pattern để tạo agent"""
    algorithm = algorithm.lower()
    
    if algorithm == "dfs":
        return DFSAgent(word_list)
    elif algorithm == "hill_climbing":
        return HillClimbingAgent(word_list)
    elif algorithm == "simulated_annealing":
        return SimulatedAnnealingAgent(word_list)
    elif algorithm == "my_algorithm":  # Thêm case mới
        return MyAlgorithmAgent(word_list)
    else:
        return DFSAgent(word_list)  # Default

__all__ = [
    'BaseAgent',
    'DFSAgent', 
    'HillClimbingAgent',
    'SimulatedAnnealingAgent',
    'MyAlgorithmAgent',  # Export
    'create_agent'
]
```

#### Bước 3: Test thuật toán

```bash
cd Backend
python -c "
from algorithms import create_agent

# Load word list
with open('words.txt', 'r') as f:
    words = [line.strip() for line in f]

# Tạo agent với thuật toán mới
agent = create_agent(words, 'my_algorithm')

# Test
guess = agent.make_guess()
print(f'First guess: {guess}')

# Giả sử có feedback
agent.filter_possible_words('AROSE', ['absent', 'absent', 'absent', 'present', 'absent'])
guess2 = agent.make_guess()
print(f'Second guess: {guess2}')
"
```

#### Bước 4: Chạy qua API

Thuật toán tự động khả dụng qua API:

```bash
# Test qua endpoint /api/agent/run
curl -X POST http://localhost:8000/api/agent/run \
  -H "Content-Type: application/json" \
  -d '{
    "target_word": "SLATE",
    "algorithm": "my_algorithm",
    "max_attempts": 6
  }'
```

Frontend sẽ tự động hiển thị thuật toán mới trong dropdown nếu bạn thêm vào `GameControls.tsx`.

### Chi tiết 3 thuật toán hiện tại

#### 1. DFS Algorithm (`dfs_algorithm.py`)

**Chiến lược:** Frequency-based scoring với systematic exploration

```python
def choose_best_guess(self, possible_words: list[str]) -> str:
    # Nếu còn ít từ, chọn trực tiếp từ có frequency cao nhất
    if len(possible_words) <= 10:
        return max(possible_words, 
                   key=lambda w: self.score_word_frequency(w, possible_words))
    
    # Sample 50 từ và chọn từ tốt nhất
    candidates = random.sample(possible_words, min(50, len(possible_words)))
    return max(candidates,
               key=lambda w: self.score_word_frequency(w, possible_words))
```

**Khi nào dùng:** Khi cần kết quả ổn định và đáng tin cậy.

#### 2. Hill Climbing (`hill_climbing_algorithm.py`)

**Chiến lược:** Greedy local search - luôn chọn neighbor tốt hơn

```python
def choose_best_guess(self, possible_words: list[str]) -> str:
    # Bắt đầu từ từ ngẫu nhiên
    current = random.choice(possible_words[:50])
    current_score = self.score_word_entropy(current, possible_words)
    
    # Tối đa 20 iterations
    for _ in range(20):
        # Lấy 30 neighbors ngẫu nhiên
        neighbors = random.sample(possible_words, min(30, len(possible_words)))
        
        # Tìm neighbor tốt hơn
        improved = False
        for neighbor in neighbors:
            score = self.score_word_entropy(neighbor, possible_words)
            if score > current_score:
                current = neighbor
                current_score = score
                improved = True
                break
        
        # Nếu không tìm được neighbor tốt hơn, dừng
        if not improved:
            break
    
    return current
```

**Khi nào dùng:** Khi cần tốc độ nhanh, chấp nhận risk bị stuck.

#### 3. Simulated Annealing (`simulated_annealing_algorithm.py`)

**Chiến lược:** Probabilistic acceptance với temperature cooling

```python
def choose_best_guess(self, possible_words: list[str]) -> str:
    current = random.choice(possible_words[:50])
    current_score = self.score_word_entropy(current, possible_words)
    
    temperature = 100.0  # Nhiệt độ ban đầu
    cooling_rate = 0.85  # Tốc độ làm lạnh
    
    for _ in range(50):
        # Chọn neighbor ngẫu nhiên
        neighbor = random.choice(possible_words)
        neighbor_score = self.score_word_entropy(neighbor, possible_words)
        
        delta = neighbor_score - current_score
        
        # Chấp nhận nếu tốt hơn, hoặc theo xác suất
        if delta > 0 or random.random() < math.exp(delta / temperature):
            current = neighbor
            current_score = neighbor_score
        
        # Giảm nhiệt độ
        temperature *= cooling_rate
        
        if temperature < 1.0:
            break
    
    return current
```

**Khi nào dùng:** Khi cần explore solution space rộng hơn, tránh local optima.

### Ví dụ thuật toán nâng cao

#### Genetic Algorithm Example

```python
from .base_agent import BaseAgent
import random

class GeneticAlgorithmAgent(BaseAgent):
    """Genetic Algorithm cho Wordle"""
    
    def __init__(self, word_list: list[str], population_size=50, generations=20):
        super().__init__(word_list)
        self.population_size = population_size
        self.generations = generations
    
    def choose_best_guess(self, possible_words: list[str]) -> str:
        if len(possible_words) <= 2:
            return possible_words[0]
        
        # Tạo population ban đầu
        population = random.sample(
            possible_words, 
            min(self.population_size, len(possible_words))
        )
        
        for generation in range(self.generations):
            # Đánh giá fitness
            fitness_scores = [
                (word, self.score_word_entropy(word, possible_words))
                for word in population
            ]
            fitness_scores.sort(key=lambda x: x[1], reverse=True)
            
            # Selection: giữ top 50%
            survivors = [word for word, _ in fitness_scores[:len(population)//2]]
            
            # Crossover & Mutation: tạo thế hệ mới
            new_population = survivors.copy()
            while len(new_population) < self.population_size:
                # Random word từ possible_words
                new_word = random.choice(possible_words)
                new_population.append(new_word)
            
            population = new_population
        
        # Trả về best individual
        best_word = max(
            population,
            key=lambda w: self.score_word_entropy(w, possible_words)
        )
        return best_word
```

### Metrics để đánh giá thuật toán

Khi test thuật toán, track các metrics sau:

```python
# Trong Backend/test_algorithm.py
def benchmark_algorithm(algorithm_name: str, test_words: list[str]):
    results = {
        'total_games': len(test_words),
        'wins': 0,
        'losses': 0,
        'total_attempts': 0,
        'attempt_distribution': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0},
        'failed_words': []
    }
    
    for target_word in test_words:
        attempts = run_game(algorithm_name, target_word)
        
        if attempts <= 6:
            results['wins'] += 1
            results['attempt_distribution'][attempts] += 1
        else:
            results['losses'] += 1
            results['failed_words'].append(target_word)
        
        results['total_attempts'] += attempts
    
    # Tính metrics
    results['win_rate'] = results['wins'] / results['total_games'] * 100
    results['avg_attempts'] = results['total_attempts'] / results['total_games']
    
    return results
```

**Metrics quan trọng:**
- **Win Rate**: % game giải được trong 6 lượt
- **Average Attempts**: Số lượt trung bình để giải
- **Attempt Distribution**: Phân bố số lượt (1-6)
- **Failed Words**: Danh sách từ không giải được

## 📡 API Endpoints

### Agent API

```bash
# Chạy game tự động với agent
POST /api/agent/run
Body: {
  "target_word": "SLATE",      # Từ cần đoán (optional, random nếu không có)
  "algorithm": "dfs",          # dfs | hill_climbing | simulated_annealing
  "max_attempts": 6
}

Response: {
  "success": true,
  "word": "SLATE",
  "attempts": 4,
  "guesses": ["AROSE", "SLATE", ...],
  "evaluations": [[...], [...], ...]
}
```

### Word API

```bash
# Validate từ
POST /api/validate
Body: {"word": "hello"}

# Random word
GET /api/words/random

# Word stats
GET /api/words/stats
```

### History API

```bash
# Lưu game history
POST /api/history
Body: {
  "word": "SLATE",
  "won": true,
  "attempts": 4,
  "score": 600,
  "guesses": ["AROSE", "SLATE"],
  "evaluations": [[...], [...]]
}

# Lấy game history
GET /api/history?limit=100

# Lấy statistics
GET /api/history/stats

# Xóa history
DELETE /api/history
```

## 🐳 Docker Commands

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Backend logs only
docker-compose logs -f backend

# Stop services
docker-compose down

# Rebuild
docker-compose up --build

# Remove everything
docker-compose down -v
```

## 🧪 Testing

### Test thuật toán

```bash
cd Backend

# Test 1 thuật toán
python -c "
from algorithms import create_agent

with open('words.txt') as f:
    words = [line.strip() for line in f]

agent = create_agent(words, 'dfs')
guess = agent.make_guess()
print(f'Guess: {guess}')
"
```

### Test API

```bash
# Health check
curl http://localhost:8000/health

# Test agent
curl -X POST http://localhost:8000/api/agent/run \
  -H "Content-Type: application/json" \
  -d '{"algorithm": "hill_climbing", "max_attempts": 6}'
```

## 🔧 Troubleshooting

### Backend không chạy

```bash
# Check logs
docker-compose logs backend

# Hoặc chạy trực tiếp
cd Backend
uvicorn main:app --reload
```

### Frontend không connect Backend

1. Kiểm tra `FrontEnd/.env.local`:
   ```
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

2. Verify backend đang chạy:
   ```bash
   curl http://localhost:8000/health
   ```

### Port conflict

```powershell
# Kiểm tra port 8000
netstat -ano | findstr :8000

# Kiểm tra port 3000  
netstat -ano | findstr :3000

# Kill process
taskkill /PID <PID> /F
```

## 📚 Tech Stack

- **Backend**: Python 3.11, FastAPI, Uvicorn
- **Frontend**: Next.js 16, React 19, TypeScript, Zustand, Tailwind CSS
- **Deployment**: Docker, Docker Compose
- **Algorithms**: DFS, Hill Climbing, Simulated Annealing (extensible)

## 🎓 Dành cho Algorithm Developers

**Workflow phát triển thuật toán:**

1. **Research**: Nghiên cứu thuật toán (GA, A*, MCTS, etc.)
2. **Implement**: Tạo file mới trong `Backend/algorithms/`
3. **Extend BaseAgent**: Kế thừa và implement `choose_best_guess()`
4. **Register**: Thêm vào factory pattern trong `__init__.py`
5. **Test**: Chạy benchmark với test words
6. **Tune**: Điều chỉnh parameters để tối ưu performance
7. **Deploy**: Commit code, rebuild Docker

**Tài nguyên hữu ích:**
- BaseAgent source code: Xem `Backend/algorithms/base_agent.py`
- DFS example: Xem `Backend/algorithms/dfs_algorithm.py`
- Helper methods: Frequency scoring, Entropy calculation, Pattern matching
- Test framework: Tạo file `Backend/test_algorithm.py` để benchmark

**Tips:**
- Dùng `score_word_entropy()` cho information gain
- Dùng `score_word_frequency()` cho probability
- Sample words để tăng tốc độ (avoid brute force)
- Track metrics: win rate, average attempts, time
- Test với nhiều target words khác nhau

## 📝 License

MIT

---

**Contributor Guide**: Xem phần "🤖 Hướng dẫn phát triển Thuật toán" phía trên để bắt đầu implement thuật toán mới!

