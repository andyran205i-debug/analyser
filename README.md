# Football Live Game Prediction App

A web application that provides live football predictions for match outcomes, corners, cards, and goals.

## Features

- 🔴 **Live Match Tracking**: Real-time match data and statistics
- 🎯 **Match Outcome Predictions**: Predict win/draw/loss with confidence scores
- ⚽ **Goal Predictions**: Forecast potential goal scorers and goal trends
- 🟨 **Card Predictions**: Predict potential yellow/red cards
- 🔲 **Corner Predictions**: Forecast corner kicks and trends
- 📊 **Analytics Dashboard**: Interactive visualizations of predictions and match stats

## Tech Stack

- **Backend**: Python (Flask/FastAPI)
- **Frontend**: React (or Vue.js)
- **Database**: PostgreSQL
- **APIs**: API-FOOTBALL, football-data.org, BSD Football API
- **ML**: scikit-learn, XGBoost (for predictions)
- **Deployment**: Docker, AWS/Heroku

## Project Structure

```
football-prediction-app/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── models/
│   │   ├── routes/
│   │   ├── services/
│   │   └── utils/
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── public/
│   ├── src/
│   └── package.json
├── docker-compose.yml
└── README.md
```

## Getting Started

See individual README files in `backend/` and `frontend/` directories.

## API Keys Required

- API-FOOTBALL: https://www.api-football.com/
- football-data.org: https://www.football-data.org/
- BSD Football API (optional): https://sports.bzzoiro.com/
