# 🚀 GitHub Portfolio Analyzer & Enhancer

Turn your GitHub repositories into recruiter-ready proof. Get objective scores, actionable insights, and recommendations to improve your portfolio.

## 📹 Demo Video

[Screen Recording will be added here - showing full working functionality]

## ✨ Features

- **Instant Analysis**: Analyze any public GitHub profile in under 2 minutes
- **Portfolio Score**: Get an objective score (0-100) based on 6 key metrics
- **Recruiter Perspective**: Understand what recruiters notice first
- **Actionable Recommendations**: Get specific, prioritized improvement suggestions
- **Visual Dashboard**: Clean, intuitive interface with detailed metrics
- **Real-time Insights**: Analyze documentation quality, commit patterns, and project structure

## 🎯 Scoring Dimensions

The analyzer evaluates profiles across 6 key dimensions:

1. **Documentation Quality** (25%) - README files, comments, project descriptions
2. **Code Structure** (20%) - Organization, essential files, best practices
3. **Activity Consistency** (20%) - Commit frequency, development patterns
4. **Repository Organization** (15%) - Profile completeness, pinned repos
5. **Project Impact** (10%) - Stars, forks, community engagement
6. **Technical Depth** (10%) - Language diversity, technical breadth

## 🏗️ Tech Stack

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, JavaScript (Vanilla)
- **API**: GitHub REST API v3
- **Deployment Ready**: Configured for Render, Railway, Vercel, or Heroku

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- Git

### Local Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/github-portfolio-analyzer.git
cd github-portfolio-analyzer
```

2. **Create virtual environment (recommended)**
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Optional: Set GitHub Token** (for higher rate limits)
```bash
# Create a .env file
echo "GITHUB_TOKEN=your_github_token_here" > .env
```

To get a GitHub token:
- Go to GitHub Settings → Developer settings → Personal access tokens
- Generate a token with `public_repo` scope
- Copy and paste it in the .env file

5. **Run the application**
```bash
python app.py
```

6. **Open in browser**
```
http://localhost:5000
```

## 🌐 Deployment Options

### Option 1: Deploy to Render (Recommended - Free)

1. Create account at [render.com](https://render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: github-portfolio-analyzer
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Free
5. Add environment variable (optional):
   - Key: `GITHUB_TOKEN`
   - Value: Your GitHub token
6. Deploy!

### Option 2: Deploy to Railway

1. Create account at [railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Railway auto-detects Python
5. Add environment variable (optional): `GITHUB_TOKEN`
6. Deploy automatically!

### Option 3: Deploy to Vercel

1. Install Vercel CLI: `npm i -g vercel`
2. Create `vercel.json`:
```json
{
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}
```
3. Run: `vercel --prod`

### Option 4: Deploy to Heroku

1. Install Heroku CLI
2. Create `Procfile`:
```
web: gunicorn app:app
```
3. Deploy:
```bash
heroku create your-app-name
git push heroku main
```

## 🎮 Usage

1. **Enter GitHub URL**: Paste any GitHub profile URL (e.g., `https://github.com/torvalds`)
2. **Or enter username**: Just type the username (e.g., `torvalds`)
3. **Click Analyze**: Wait 10-30 seconds for comprehensive analysis
4. **Review Results**:
   - Overall portfolio score and grade
   - Detailed metrics breakdown
   - Your strengths
   - Red flags recruiters notice
   - Prioritized recommendations
   - Technology stack analysis
   - Top repositories review

## 📊 Understanding Your Score

| Score Range | Grade | Description |
|-------------|-------|-------------|
| 90-100 | A+ | Outstanding - Recruiter's dream portfolio |
| 80-89 | A | Excellent - Strong hiring signal |
| 70-79 | B+ | Very Good - Above average candidate |
| 60-69 | B | Good - Shows potential |
| 50-59 | C+ | Above Average - Needs polish |
| 40-49 | C | Average - Significant improvements needed |
| 0-39 | D | Needs Improvement - Major gaps |

## 🎯 Example Recommendations

The tool provides specific, actionable advice such as:

- **Documentation**: "Add comprehensive README files to your top projects. Include: project description, installation instructions, usage examples, screenshots/demos."
- **Activity**: "Maintain regular commit activity. Aim for at least 2-3 commits per week."
- **Structure**: "Add essential files: .gitignore, LICENSE, requirements.txt. Add topics/tags to repositories."
- **Profile**: "Complete your GitHub profile: add bio, location, website/blog, and email."
- **Impact**: "Focus on 2-3 substantial projects. Add detailed descriptions, use cases, and live demos."

## 🔧 Configuration

### GitHub API Rate Limits

Without authentication: 60 requests/hour
With token: 5,000 requests/hour

Set `GITHUB_TOKEN` environment variable to increase limits.

### Customizing Scoring Logic

Edit the scoring weights in `app.py`:

```python
weights = {
    'documentation_quality': 0.25,
    'code_structure': 0.20,
    'activity_consistency': 0.20,
    'repository_organization': 0.15,
    'project_impact': 0.10,
    'technical_depth': 0.10
}
```

## 🧪 Testing

Test with various GitHub profiles:

- Active developers: `torvalds`, `gaearon`, `tj`
- Your own profile
- Profiles with few/many repos
- Profiles with/without READMEs

## 📝 Project Structure

```
github-portfolio-analyzer/
├── app.py                 # Main Flask application
├── templates/
│   └── index.html        # Frontend interface
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── .gitignore           # Git ignore rules
└── Procfile             # For Heroku deployment (optional)
```

## 🤝 Contributing

Contributions are welcome! Ideas for improvements:

- [ ] Add caching to reduce API calls
- [ ] Compare with similar profiles
- [ ] Generate downloadable PDF reports
- [ ] Add more granular code quality checks
- [ ] Integration with LinkedIn
- [ ] Historical score tracking

## ⚠️ Limitations

- Only analyzes public repositories
- GitHub API rate limits apply
- Cannot access private repos or files
- Analysis time depends on number of repositories
- Code quality analysis is heuristic-based

## 🙏 Acknowledgments

Built for the UnsaidTalks Hackathon - helping students turn GitHub profiles into recruiter-ready proof.

## 📄 License

MIT License - feel free to use and modify for your needs.

## 📧 Contact

For questions or feedback:
- GitHub Issues: [Create an issue](https://github.com/yourusername/github-portfolio-analyzer/issues)
- Email: your.email@example.com

## 🎓 Made for Students

This tool is specifically designed to help students and early-career developers:
- Understand recruiter perspectives
- Identify portfolio gaps
- Get concrete improvement steps
- Build recruiter-ready profiles

---

**Note**: Replace demo video link, GitHub URL, and contact information before submission.

## 🚀 Quick Start Checklist

- [ ] Clone the repository
- [ ] Install dependencies
- [ ] Run locally and test
- [ ] (Optional) Add GitHub token for higher limits
- [ ] Deploy to hosting platform
- [ ] Record demo video
- [ ] Update README with deployment URL
- [ ] Test with multiple profiles
- [ ] Submit to hackathon portal

**Remember**: Your submission must include:
1. Public GitHub repository link
2. Working prototype (hosted or local demo video)
3. Screen recording in README
4. Complete documentation
