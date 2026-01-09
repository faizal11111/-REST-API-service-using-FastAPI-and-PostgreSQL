🎯 What This Project Does
This is a FastAPI + PostgreSQL service that saves posts from JSONPlaceholder to a local database.

Simple flow: Client gives me a post ID → I fetch it from external API → save to my PostgreSQL → provide CRUD operations.

Why JSONPlaceholder?
Free, no-auth, stable fake API. Perfect for demoing external API integration without keys/secrets.

📋 Quick Setup (2 minutes)
Clone & Virtual Env

bash
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
PostgreSQL (Docker or local)

bash
docker run --name showbay-db -e POSTGRES_PASSWORD=password -e POSTGRES_DB=showbay_db -p 5432:5432 -d postgres:16
Copy .env

text
DATABASE_URL=postgresql+psycopg2://postgres:password@localhost:5432/showbay_db
EXTERNAL_API_BASE_URL=https://jsonplaceholder.typicode.com
Run

bash
uvicorn app.main:app --reload
Docs: http://localhost:8000/docs

🔄 How Endpoints Work
text
POST /posts/          → Fetch from JSONPlaceholder → Save to DB → 201
GET  /posts/{id}      → Read from DB → 200 or 404
PUT  /posts/{id}      → Update DB (partial OK) → 200 or 404  
DELETE /posts/{id}    → Delete from DB → 200 or 404
Live example (POST returns real data):

json
{
  "id": 6,
  "external_id": 1,
  "title": "sunt aut facere...",
  "source": "jsonplaceholder",
  "created_at": "2026-01-09T20:04:04"
}
🗄️ Database Design
Single table: posts

text
id (PK)          → Local auto-increment ID
external_id (unique) → Original post ID from API
title            → Post title
body             → Post content  
source           → "jsonplaceholder"
created_at       → When saved
updated_at       → When modified
Why unique external_id? Prevents duplicate saves of same external post.

🧪 Tests
bash
pytest -v
What they test:

✅ POST fetches external API → saves to DB (201)

✅ External API 404 → returns 502

✅ GET reads from DB (200/404)

✅ PUT partial updates (200/404)

✅ DELETE works (200/404)

Uses SQLite for tests (isolated from prod PostgreSQL).

🚨 Error Handling
Scenario	Status Code	Response
External API down	502	{"detail": "External API error"}
Post not found	404	{"detail": "Post not found"}
Bad JSON	422	Pydantic validation errors
DB down	500	FastAPI default

🎉 Results
✅ 4 endpoints working
✅ PostgreSQL + external API bridge
✅ Pydantic validation
✅ 8/8 tests pass
✅ Auto Swagger/Redoc docs
✅ Production-ready structure