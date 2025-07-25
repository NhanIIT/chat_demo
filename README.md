# Chatbot nội bộ LLM + SQL (Qwen + LangChain + Flask)

## 1. Chuẩn bị
- Tải model Qwen1.5-1.8B-Chat từ HuggingFace về thư mục `models/`
- Cài Docker, Docker Compose

## 2. Khởi tạo database và sinh dữ liệu mẫu
```bash
docker run --rm -v ${PWD}:/app -w /app python:3.10 python db.py
docker run --rm -v ${PWD}:/app -w /app python:3.10 python mock_data.py
```

## 3. Chạy hệ thống
```bash
docker-compose up --build
```

## 4. Gửi câu hỏi tới chatbot
```bash
curl -X POST http://localhost:5000/chat -H "Content-Type: application/json" -d '{"query": "Liệt kê danh sách nhân sự phòng Kỹ thuật"}'
```

## 5. Tuỳ chỉnh
- Sửa schema, prompt, hoặc mở rộng API theo nhu cầu.

---