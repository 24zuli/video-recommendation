# Video Recommendation Engine

A sophisticated recommendation system that suggests personalized video content based on user preferences and engagement patterns using deep neural networks. Ref: to see what kind of motivational content you have to recommend, take reference from our Empowerverse App [ANDROID](https://play.google.com/store/apps/details?id=com.empowerverse.app) || [iOS](https://apps.apple.com/us/app/empowerverse/id6449552284).


##  🎥 Project video

https://github.com/user-attachments/assets/744b94c2-ac4e-4db5-ae6f-ca1f3e3f4263


## 🚀 Postman collection

https://drive.google.com/file/d/1nOSpYOauYlNqFgmyJe_FYTRZz3ICHEKz/view?usp=sharing




## 🎯 Project Overview

This project implements a video recommendation algorithm that:

- Delivers personalized content recommendations
- Handles cold start problems using mood-based recommendations
- Utilizes deep neural networks for content analysis
- Integrates with external APIs for data collection
- Implements efficient data caching and pagination

## 🛠️ Technology Stack

- **Backend Framework**: FastAPI
- **Documentation**: Swagger/OpenAPI

## 📋 Prerequisites

- Virtual environment (recommended)

## 🚀 Getting Started

1. **Clone the Repository**

   ```bash
   git clone <repository-url>
   cd video-recommendation
   ```

2. **Set Up Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**
   Create a `.env` file in the root directory:

   ```env

   FLIC_TOKEN=your_flic_token
   API_BASE_URL=https://api.socialverseapp.com
   ```

5. **Run Database Migrations**

   ```bash
   alembic upgrade head
   ```

6. **Start the Server**

   ```bash
   uvicorn app.main:app --reload
   ```

## 📊 API Endpoints

### Main Recommendation Endpoints

1. **Get Personalized Feed**

   ```
   GET /feed?username={username}
   ```

   Returns personalized video recommendations for a specific user.

2. **Get Category-based Feed**

   ```
   GET /feed?username={username}&category_id={category_id}
   ```

   Returns category-specific video recommendations for a user.

### Data Collection Endpoints (Internal Use)

The system uses the following APIs for data collection:

### APIs

1. **Get All Viewed Posts** (METHOD: GET):

   ```
   https://api.socialverseapp.com/posts/view?page=1&page_size=1000&resonance_algorithm=resonance_algorithm_cjsvervb7dbhss8bdrj89s44jfjdbsjd0xnjkbvuire8zcjwerui3njfbvsujc5if
   ```

2. **Get All Liked Posts** (METHOD: GET):

   ```
   https://api.socialverseapp.com/posts/like?page=1&page_size=1000&resonance_algorithm=resonance_algorithm_cjsvervb7dbhss8bdrj89s44jfjdbsjd0xnjkbvuire8zcjwerui3njfbvsujc5if
   ```

3. **Get All Inspired posts** (METHOD: GET):

   ```
   https://api.socialverseapp.com/posts/inspire?page=1&page_size=1000&resonance_algorithm=resonance_algorithm_cjsvervb7dbhss8bdrj89s44jfjdbsjd0xnjkbvuire8zcjwerui3njfbvsujc5if
   ```

4. **Get All Rated posts** (METHOD: GET):

   ```
   https://api.socialverseapp.com/posts/rating?page=1&page_size=1000&resonance_algorithm=resonance_algorithm_cjsvervb7dbhss8bdrj89s44jfjdbsjd0xnjkbvuire8zcjwerui3njfbvsujc5if
   ```

5. **Get All Posts** (Header required\*) (METHOD: GET):

   ```
   https://api.socialverseapp.com/posts/summary/get?page=1&page_size=1000
   ```

6. **Get All Users** (Header required\*) (METHOD: GET):

   ```
   https://api.socialverseapp.com/users/get_all?page=1&page_size=1000
   ```

### Authorization

For autherization pass `Flic-Token` as header in the API request:

Header:

```json
"Flic-Token": "flic_11d3da28e403d182c36a3530453e290add87d0b4a40ee50f17611f180d47956f"
```

**Note**: All external API calls require the Flic-Token header:

## 🧮 Algorithm Implementation

The recommendation engine uses a Deep Neural Network (DNN) architecture with the following components:

1. **Data Preprocessing**

   - Feature engineering
   - Data normalization
   - Missing value handling
   - Categorical encoding

2. **Model Architecture**

   - Embedding layers for categorical features
   - Dense layers with ReLU activation
   - Dropout for regularization
   - Output layer with appropriate activation

3. **Cold Start Handling**

   - Mood-based initial recommendations
   - Content-based filtering fallback
   - Popularity-based recommendations

## 📝 Submission Requirements

1. **GitHub Repository**

   - Complete source code
   - This README.md file
   - Postman collection
   - Database migration scripts

2. **Video Submission**

   - Introduction Video (30-40 seconds)
     - Personal introduction
     - Project overview
   - Technical Demo
     - API demonstration using Postman
     - Database operations
     - Authentication flow

3. **Notification**

   - Join the Telegram group: [Video Recommendation](https://t.me/+VljbLT8o75QxN2I9)
   - Notify upon completion

## ✅ Evaluation Checklist

- [x] All APIs are functional
- [x] Database migrations work correctly
- [x] README is complete and clear
- [x] Postman collection is included
- [x] Videos are submitted
- [x] Code is well-documented
- [x] Implementation handles edge cases
- [x] Proper error handling is implemented

