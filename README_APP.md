# 💌 Judith Tribute App

A beautiful memorial Streamlit application celebrating the life of Judith through her letters and photographs.

## 🏗️ Project Structure

```
app/
├── main.py                    # Main application entry point
├── config.py                  # Configuration and CSS styling
├── utils.py                   # Utility functions
└── page_modules/              # Individual page modules
    ├── home.py               # Home page with hero image
    ├── gallery.py            # Letters gallery with pagination
    ├── rag_search.py         # AI-powered search functionality
    └── photo_gallery.py      # Photo gallery
```

## ✨ Features

### 🏠 Home Page
- Beautiful hero section with Judith's photo
- Overview of available features
- Elegant gradient design with custom fonts

### 📚 Letters Gallery
- Paginated view of all letters
- Beautiful card-based layout
- Image display for each letter
- Responsive design

### 🔍 Intelligent Search (RAG)
- AI-powered semantic search using OpenAI embeddings
- Natural language queries
- Relevance scoring and filtering
- Top results with similarity scores

### 📷 Photo Gallery
- Grid layout for photos
- Support for multiple image formats (JPG, PNG, HEIC)
- Responsive design with hover effects
- Error handling for corrupted images

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- OpenAI API key (for search functionality)

### Installation
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set environment variables:
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

3. Run the application:
   ```bash
   ./run_app.sh
   ```
   
   Or manually:
   ```bash
   cd app
   streamlit run main.py
   ```

## 📁 Data Structure

The app expects the following data structure:

```
data/
├── letters.json              # Letters metadata and content
├── letter_embeddings.json    # Precomputed embeddings
├── all_letters/              # Letter images
│   ├── CNH0001.jpg
│   ├── CNH0002.jpg
│   └── ...
└── photos/                   # Photo gallery images
    ├── IMG_7240.jpg         # Hero image
    ├── IMG_7241.jpg
    └── ...
```

## 🎨 Design Features

- **Modern UI**: Clean, elegant design with custom CSS
- **Responsive Layout**: Works on desktop and mobile devices
- **Custom Typography**: Montserrat font for better readability
- **Gradient Backgrounds**: Soft purple/pink gradients
- **Interactive Elements**: Hover effects and smooth transitions
- **Accessibility**: High contrast and clear navigation

## 🔧 Configuration

### Styling
All styling is centralized in `config.py`. You can customize:
- Color schemes
- Font families
- Card designs
- Spacing and layout

### Pagination
Letters per page can be adjusted in `pages/gallery.py`:
```python
LETTERS_PER_PAGE = 5  # Change this value
```

### Search Threshold
RAG search relevance threshold in `pages/rag_search.py`:
```python
threshold = 0.2  # Adjust for more/less strict matching
```

## 🚀 Deployment

### Streamlit Cloud
1. Push code to GitHub
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Set secrets for `OPENAI_API_KEY`
5. Deploy!

### Local Development
```bash
cd app
streamlit run main.py --server.port 8501
```

## 📋 Requirements

See `requirements.txt` for complete dependencies. Key packages:
- `streamlit>=1.28.0` - Web framework
- `openai>=1.0.0` - AI search functionality
- `pillow` - Image processing
- `numpy` - Numerical computations

## 🤝 Contributing

1. Ensure all new pages follow the structure in `page_modules/`
2. Use the styling functions from `config.py`
3. Add utility functions to `utils.py`
4. Update this README for new features

## 📝 License

This is a memorial application created with love and respect for Judith's memory.

---

*"As cartas são pontes entre corações, e as memórias são tesouros que o tempo não pode apagar."*
