# Cambridge History Examiner Bot

A sophisticated AI-powered chatbot designed to simulate a Cambridge O-Level History examiner. This application helps students prepare for their History exams by providing examiner-style responses according to the Cambridge marking scheme.

## Features

- **Examiner Simulation Engine**: Follows a strict 10-step protocol to simulate Cambridge History examiner behavior
- **Mark Allocation**: Supports 4, 7, and 14 mark questions with appropriate response structures
- **RAG System**: Retrieves context from `history_data.json` containing textbook content and past papers
- **PEEL Structure**: Enforces Point-Evidence-Explanation-Link paragraph formatting
- **Examiner Audit**: Provides detailed feedback on predicted marks and reasoning
- **Premium Dark UI**: Modern, responsive interface with glassmorphism effects

## Tech Stack

### Backend
- **FastAPI** - High-performance API framework
- **Groq API** - Primary LLM engine (llama-3.3-70b-versatile)
- **Hugging Face** - Fallback LLM engine
- **Python 3.12+**

### Frontend
- **React 18** - UI framework
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **Framer Motion** - Animations
- **TypeScript** - Type safety

## Project Structure

```
History/
├── backend/
│   ├── main.py           # FastAPI application
│   ├── requirements.txt  # Python dependencies
│   └── .env             # API keys (not committed)
├── frontend/
│   ├── src/
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   ├── index.css
│   │   └── components/
│   │       └── HistoryExaminer.tsx
│   ├── package.json
│   ├── vite.config.ts
│   └── tailwind.config.js
└── data/
    └── history_data.json  # Knowledge base
```

## Setup Instructions

### Prerequisites
- **Node.js** v22+ and npm
- **Python** 3.12+
- **Groq API Key** (primary) - Get from [console.groq.com](https://console.groq.com)
- **Hugging Face API Key** (optional fallback) - Get from [huggingface.co](https://huggingface.co)

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the `backend/` directory:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   HF_API_KEY=your_hf_api_key_here
   MONGO_URI=mongodb://127.0.0.1:27017
   SECRET_KEY=your_secret_key_here
   ```

4. Start the backend server:
   ```bash
   python main.py
   ```
   The API will be available at `http://127.0.0.1:8000`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```
   The app will be available at `http://localhost:5173`

## Usage

1. **Select Marks**: Choose the question mark allocation (4, 7, or 14 marks)
2. **Ask Questions**: Type your history question in the input field
3. **Review Answer**: The bot provides a structured, examiner-style response
4. **Check Audit**: Review the examiner audit footer for predicted marks and feedback

### Example Questions

- "Explain the main causes of the Mughal decline." (4 marks)
- "Why was the Simon Commission rejected?" (7 marks)
- "Was the Khilafat Movement successful?" (14 marks)
- "Evaluate the role of Sir Syed Ahmad Khan." (14 marks)

## Cambridge Marking Scheme

- **4 Marks**: 2 PEEL paragraphs (110-150 words)
- **7 Marks**: 3 analytical PEEL paragraphs (220-260 words)
- **14 Marks**: Full evaluation essay with Introduction, Agree, Disagree, and Final Judgement (450-550 words)

## API Endpoints

### `POST /ask-ai`
Submit a history query and receive an examiner-style response.

**Parameters:**
- `query` (string): The history question
- `marks` (int): Mark allocation (4, 7, or 14)

**Response:**
```json
{
  "answer": "Examiner-style response...",
  "marks": 4
}
```

## Contributing

Contributions are welcome! Please ensure:
- Code follows existing style conventions
- All tests pass
- New features include documentation

## License

This project is for educational purposes. Please ensure compliance with API provider terms of service.

## Acknowledgments

- Cambridge International O-Level History (2059/01) syllabus
- Nigel Kelly textbook references
- Past paper marking schemes

---

**Note**: This is an educational tool. Always verify responses with official Cambridge materials and your teacher.
