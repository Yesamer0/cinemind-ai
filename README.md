# CineMind AI

AI-Powered Personalized Movie Recommendation System

## About

This project aims to develop an AI-powered personalized movie recommendation platform.

## Technologies

- Python
- FastAPI
- React
- PostgreSQL
- Scikit-Learn


Sprint 3: Built the first working movie recommendation engine using the MovieLens dataset. Users can select a movie genre through the console and receive the highest-rated movies in that category.



# Sprint 5 - Keyword-Based AI Recommendation

## Features

- Content-Based Movie Recommendation
- TF-IDF Vectorization
- Cosine Similarity
- Text Cleaning
- Interactive Keyword Search
- Command Line Interface (CLI)

## Example

Enter a keyword:

```
space
```

Output:

```
1. Interstellar
2. Gravity
3. The Martian
4. Moon
...
```

## Technologies

- Python
- Pandas
- NumPy
- Scikit-learn
- TF-IDF
- Cosine Similarity

## Sprint 6 - Semantic Search with AI

### Completed Features

- Added semantic movie search using Sentence Transformers.
- Loaded and processed TMDB movie overviews.
- Generated AI embeddings for all movies.
- Saved embeddings using pickle for faster loading.
- Implemented cosine similarity for semantic recommendations.
- Added interactive user input for movie search.
- Displayed similarity scores for recommended movies.
- Organized the application using a main() function.

### Technologies

- Sentence Transformers
- scikit-learn
- Cosine Similarity
- Pickle
- Pandas


## Sprint 7 - FastAPI Integration

### Completed
- Installed FastAPI and Uvicorn
- Created the first REST API
- Added Swagger documentation
- Connected Semantic Search with FastAPI
- Returned movie recommendations as JSON
- Tested API endpoints successfully

### Technologies
- FastAPI
- Uvicorn
- Sentence Transformers
- Cosine Similarity

## Sprint 8 - Advanced REST API Features

### Completed Features

- Movie Detail Endpoint
- Movie List Endpoint
- Pagination
- Sorting
- Input Validation
- Search Limit
- Semantic Search Improvements
- Better JSON Responses

### API Endpoints

GET /

GET /search

GET /movie/{movie_id}

GET /movies

# 🎬 CineMind AI

An AI-powered movie recommendation system that combines semantic search with a modern React frontend.

## Features

- 🤖 AI Semantic Movie Search
- 🎯 Sentence Transformers
- 🔍 Semantic Search
- ⚡ FastAPI REST API
- 🌐 React Frontend
- 🔗 React + FastAPI Integration
- 📦 Axios API Requests
- ⏳ Loading State
- ❌ Error Handling
- 📄 Swagger API Documentation
- 🎬 Movie Search
- 📚 Movie Details
- 📑 Pagination
- 🔎 Sorting

## Tech Stack

### Backend
- Python
- FastAPI
- Uvicorn
- Sentence Transformers
- Scikit-Learn
- Pandas

### Frontend
- React
- Vite
- Axios

### AI
- all-MiniLM-L6-v2
- Semantic Search
- Cosine Similarity

### Dataset
- MovieLens
- TMDB Metadata

## Tech Stack

### Backend
- Python
- FastAPI
- Uvicorn
- Sentence Transformers
- Scikit-Learn
- Pandas

### Frontend
- React
- Vite
- Axios

### AI
- all-MiniLM-L6-v2
- Semantic Search
- Cosine Similarity

### Dataset
- MovieLens
- TMDB Metadata


## ✅ Sprint 9 – React Router & Movie Detail

### Completed Features

- React Router integration
- Dynamic routes (/movie/:id)
- Movie Detail page
- Axios API integration
- FastAPI movie endpoint
- Movie information display
- Genre display
- Rating display
- Release date display
- Improved navigation between pages

### Technologies Used

- React Router DOM
- Axios
- FastAPI
- React Hooks (useState, useEffect, useParams)