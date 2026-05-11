# API-FOOTBALL Setup Guide

## Overview
This application uses **API-FOOTBALL** as the primary data source for live football match predictions.

## Why API-FOOTBALL?
✅ **1,100+ leagues** covered globally  
✅ **Real-time live scores** with 30-second refresh  
✅ **Detailed match events**: goals, cards, corners, substitutions  
✅ **Pre-match predictions** built-in  
✅ **Team statistics** and historical data  
✅ **Head-to-head data** between teams  
✅ **100 free requests/day** sufficient for small-scale predictions  

---

## Getting Started

### Step 1: Get Your API Key

1. Go to **RapidAPI**: https://rapidapi.com/api-sports/api/api-football
2. Click **"Sign Up"** (free account)
3. Once logged in, click **"Subscribe to Test"** (free tier)
4. Copy your **API Key** from the dashboard
5. You get **100 free requests per day** on the free tier

### Step 2: Configure Environment

1. Navigate to the backend folder:
   ```bash
   cd backend
   ```

2. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

3. Edit `.env` and add your API key:
   ```env
   API_FOOTBALL_KEY=your_api_key_here_paste_here
   FLASK_ENV=development
   ```

### Step 3: Start the Application

**Option A: Using Docker (Recommended)**
```bash
cd ..  # Go back to repo root
docker-compose up --build
```

**Option B: Local Development**
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m app.main
```

### Step 4: Test the API

Once running, test with:

```bash
# Health check
curl http://localhost:5000/api/health/

# Get live matches
curl http://localhost:5000/api/matches/live

# Sync matches from API-FOOTBALL
curl -X POST http://localhost:5000/api/matches/sync
```

---

## API Endpoints Available

### Match Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/matches/live` | GET | Get all live matches |
| `/api/matches/sync` | POST | Manually sync live matches from API-FOOTBALL |
| `/api/matches/<id>` | GET | Get specific match details |

### Prediction Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/predictions/match/<id>` | GET | Get predictions for a match |
| `/api/predictions/generate/<id>` | POST | Generate new predictions for a match |

### Health Check

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health/` | GET | API health status |

---

## API-FOOTBALL Response Structure

### Live Matches Response
```json
{
  "get": "fixtures",
  "parameters": {"live": "all"},
  "errors": [],
  "results": 5,
  "paging": {"current": 1, "total": 1},
  "response": [
    {
      "fixture": {
        "id": 1234567,
        "referee": "John Doe",
        "timezone": "UTC",
        "date": "2026-05-11T15:00:00+00:00",
        "timestamp": 1715425200,
        "periods": {"first": 1700000000, "second": 1700001800},
        "venue": {"id": 123, "name": "Stadium Name", "city": "City"},
        "status": {"long": "Match Finished", "short": "FT", "elapsed": 90}
      },
      "league": {
        "id": 39,
        "name": "Premier League",
        "country": "England",
        "logo": "https://...",
        "flag": "https://...",
        "season": 2025,
        "round": "Regular Season - 10"
      },
      "teams": {
        "home": {"id": 33, "name": "Manchester United", "logo": "https://..."},
        "away": {"id": 42, "name": "Liverpool", "logo": "https://..."}
      },
      "goals": {"home": 2, "away": 1},
      "score": {
        "halftime": {"home": 1, "away": 0},
        "fulltime": {"home": 2, "away": 1},
        "extratime": null,
        "penalty": null
      },
      "events": [
        {
          "time": {"elapsed": 25},
          "type": "Goal",
          "detail": "Normal",
          "team": {"id": 33, "name": "Manchester United"},
          "player": {"id": 1001, "name": "Bruno Fernandes"},
          "assist": {"id": 1002, "name": "Marcus Rashford"}
        },
        {
          "time": {"elapsed": 45},
          "type": "Card",
          "detail": "Yellow Card",
          "team": {"id": 42, "name": "Liverpool"},
          "player": {"id": 2001, "name": "Mohamed Salah"}
        }
      ]
    }
  ]
}
```

---

## Available Data Points for Predictions

### From Match Events
- ⚽ **Goals** (team, player, minute, assist)
- 🟨 **Cards** (yellow/red, team, player, minute)
- 🚩 **Corners** (team, minute)
- 🔄 **Substitutions** (team, player in/out, minute)

### From Match Statistics
- 📊 **Possession** (%)
- 🎯 **Shots** (total, on target)
- 🛡️ **Tackles**
- 🚫 **Interceptions**
- 🤛 **Fouls**
- 📍 **Ball contacts**

### From Team Data
- 🏆 **League standings**
- 📈 **Form** (last 5 matches)
- 🎪 **Home/Away records**
- 📊 **Historical performance**

---

## Rate Limits & Quotas

**Free Tier**: 100 requests/day
- Perfect for dev/testing
- Good for single-league tracking
- ~3-5 requests per match event sync

**Usage Tips**:
1. Cache responses using Redis
2. Batch requests when possible
3. Use selective syncing (specific leagues)
4. Implement request queuing with Celery

---

## Prediction Features Enabled

With API-FOOTBALL data, our system predicts:

✅ **Match Outcome** (Home Win, Draw, Away Win)  
✅ **Total Goals** (Over/Under 2.5)  
✅ **Corners** (Over/Under 8.5)  
✅ **Cards** (Total yellow/red)  
✅ **Goal Scorers** (top scorers by team)  
✅ **Team Form** (recent performance trends)  

---

## Troubleshooting

### "401 Unauthorized" Error
- Check API key is correctly copied to `.env`
- Verify you have an active RapidAPI subscription
- Ensure headers include `x-rapidapi-key` and `x-rapidapi-host`

### "429 Too Many Requests"
- You've exceeded 100 free requests/day
- Upgrade to paid plan or wait for reset
- Implement caching to reduce API calls

### "Connection Timeout"
- API-FOOTBALL service may be down
- Check https://status.api-football.com/
- Verify your internet connection

### No Data Returned
- Ensure fixtures are actually happening (check schedule)
- Try with `GET /api/matches/live` first
- Check league/season parameters

---

## Next Steps

1. ✅ Add your API key
2. ✅ Start the application
3. ✅ Run `POST /api/matches/sync` to load data
4. ✅ Check `/api/matches/live` for results
5. ✅ Generate predictions with `POST /api/predictions/generate/<match_id>`

---

## Resources

- **API Documentation**: https://www.api-football.com/documentation-v3
- **Supported Leagues**: https://www.api-football.com/leagues
- **API Status**: https://status.api-football.com/
- **RapidAPI Dashboard**: https://rapidapi.com/dashboard
- **Football Data**: https://www.api-football.com/

---

Happy predicting! 🚀⚽
