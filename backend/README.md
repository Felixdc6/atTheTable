# At The Table - Backend

FastAPI backend for the bill splitting application with AI-powered receipt parsing.

## Features

- 🤖 **AI Bill Parsing**: Uses Gemini 2.5 Flash Lite to extract structured data from receipt images
- 🔗 **Public API**: Shareable links for participants to claim items
- 📊 **Real-time Updates**: Live updates for bill sharing and claiming
- 🔒 **Secure**: Token-based access for public participants

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `env/config.env` and add your API keys:

```env
GEMINI_API_KEY=your_gemini_api_key_here
SYSTEM_PROMPT=Your custom prompt for bill parsing...
```

### 3. Run the Server

```bash
python main.py
```

The API will be available at `http://localhost:8000`

## API Endpoints

### AI Parsing
- `POST /api/ai/parse-bill` - Parse receipt image with Gemini AI
- `GET /api/ai/health` - Check AI service status

### Public Routes (No Auth Required)
- `GET /api/public/{token}` - Get bill details by token
- `POST /api/public/{token}/claim-exclusive` - Claim exclusive items
- `POST /api/public/{token}/shared-init` - Initialize shared pool
- `POST /api/public/{token}/shared-join` - Join shared pool
- `POST /api/public/{token}/shared-leave` - Leave shared pool

## Project Structure

```
backend/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── env/
│   └── config.env         # Environment variables
└── app/
    ├── api/               # API route handlers
    │   ├── bill_parsing.py
    │   └── public_routes.py
    ├── services/          # Business logic services
    │   └── gemini_service.py
    ├── models/            # Data models
    └── core/              # Core utilities
```

## Development

### Running with Auto-reload

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Testing

```bash
pytest
```

## Environment Variables

- `GEMINI_API_KEY`: Google Gemini API key
- `SYSTEM_PROMPT`: Custom prompt for bill parsing (optional)
