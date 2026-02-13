from flask import Flask, render_template, request, jsonify
import requests
from datetime import datetime, timedelta
import re
from collections import Counter
import os
from dotenv import load_dotenv  # Add this line

load_dotenv()  # Add this line

app = Flask(__name__)

# GitHub API base URL
GITHUB_API = "https://api.github.com"

class GitHubAnalyzer:
    def __init__(self, username, token=None):
        self.username = username
        self.headers = {'Authorization': f'token {token}'} if token else {}
        self.user_data = None
        self.repos = []
        self.score = 0
        self.recommendations = []
        
    def fetch_user_data(self):
        """Fetch user profile data"""
        try:
            response = requests.get(f"{GITHUB_API}/users/{self.username}", headers=self.headers)
            if response.status_code == 200:
                self.user_data = response.json()
                return True
            return False
        except Exception as e:
            print(f"Error fetching user data: {e}")
            return False
    
    def fetch_repositories(self):
        """Fetch all public repositories"""
        try:
            response = requests.get(
                f"{GITHUB_API}/users/{self.username}/repos",
                params={'per_page': 100, 'sort': 'updated'},
                headers=self.headers
            )
            if response.status_code == 200:
                self.repos = response.json()
                return True
            return False
        except Exception as e:
            print(f"Error fetching repositories: {e}")
            return False
    
    def analyze_readme_quality(self, repo):
        """Analyze README quality for a repository"""
        score = 0
        try:
            readme_response = requests.get(
                f"{GITHUB_API}/repos/{self.username}/{repo['name']}/readme",
                headers=self.headers
            )
            if readme_response.status_code == 200:
                readme_data = readme_response.json()
                # Check if README exists
                score += 20
                
                # Estimate content length (base64 encoded, so approximate)
                size = readme_data.get('size', 0)
                if size > 1000:
                    score += 20
                if size > 3000:
                    score += 10
                    
                return min(score, 50)
        except:
            pass
        return 0
    
    def analyze_commit_activity(self, repo):
        """Analyze commit frequency and consistency"""
        score = 0
        try:
            commits_response = requests.get(
                f"{GITHUB_API}/repos/{self.username}/{repo['name']}/commits",
                params={'per_page': 100},
                headers=self.headers
            )
            if commits_response.status_code == 200:
                commits = commits_response.json()
                commit_count = len(commits)
                
                # Score based on commit count
                if commit_count >= 50:
                    score += 30
                elif commit_count >= 20:
                    score += 20
                elif commit_count >= 5:
                    score += 10
                
                # Analyze commit dates for consistency
                if len(commits) > 1:
                    dates = []
                    for commit in commits[:20]:  # Check last 20 commits
                        try:
                            date_str = commit['commit']['author']['date']
                            dates.append(datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ'))
                        except:
                            pass
                    
                    if len(dates) > 1:
                        # Check if commits are spread over time
                        date_range = (max(dates) - min(dates)).days
                        if date_range > 30:
                            score += 10
                        if date_range > 90:
                            score += 10
                            
                return min(score, 50)
        except:
            pass
        return 0
    
    def analyze_code_structure(self, repo):
        """Analyze repository structure and organization"""
        score = 0
        
        # Check for important files
        important_files = ['.gitignore', 'LICENSE', 'CONTRIBUTING.md', 'requirements.txt', 
                          'package.json', 'Dockerfile', '.github/workflows']
        
        try:
            contents_response = requests.get(
                f"{GITHUB_API}/repos/{self.username}/{repo['name']}/contents",
                headers=self.headers
            )
            if contents_response.status_code == 200:
                contents = contents_response.json()
                file_names = [item['name'] for item in contents if isinstance(contents, list)]
                
                for important_file in important_files:
                    if important_file in file_names:
                        score += 5
                        
        except:
            pass
        
        # Check for topics/tags
        if repo.get('topics'):
            score += 10
            
        # Check for description
        if repo.get('description'):
            score += 10
            
        return min(score, 50)
    
    def calculate_portfolio_score(self):
        """Calculate overall GitHub portfolio score"""
        if not self.repos:
            return 0, {}
        
        metrics = {
            'documentation_quality': 0,
            'code_structure': 0,
            'activity_consistency': 0,
            'repository_organization': 0,
            'project_impact': 0,
            'technical_depth': 0
        }
        
        analyzed_repos = []
        total_stars = 0
        total_forks = 0
        languages = []
        
        # Analyze top repositories (pinned or most recent 10)
        repos_to_analyze = self.repos[:10]
        
        for repo in repos_to_analyze:
            if repo['fork']:
                continue
                
            repo_analysis = {
                'name': repo['name'],
                'description': repo.get('description', 'No description'),
                'stars': repo['stargazers_count'],
                'forks': repo['forks_count'],
                'language': repo.get('language', 'Unknown'),
                'updated_at': repo['updated_at'],
                'readme_score': 0,
                'commit_score': 0,
                'structure_score': 0
            }
            
            # Analyze README
            readme_score = self.analyze_readme_quality(repo)
            repo_analysis['readme_score'] = readme_score
            metrics['documentation_quality'] += readme_score
            
            # Analyze commits
            commit_score = self.analyze_commit_activity(repo)
            repo_analysis['commit_score'] = commit_score
            metrics['activity_consistency'] += commit_score
            
            # Analyze structure
            structure_score = self.analyze_code_structure(repo)
            repo_analysis['structure_score'] = structure_score
            metrics['code_structure'] += structure_score
            
            total_stars += repo['stargazers_count']
            total_forks += repo['forks_count']
            if repo.get('language'):
                languages.append(repo['language'])
            
            analyzed_repos.append(repo_analysis)
        
        # Calculate averages
        num_repos = max(len(analyzed_repos), 1)
        metrics['documentation_quality'] = min(metrics['documentation_quality'] / num_repos, 100)
        metrics['activity_consistency'] = min(metrics['activity_consistency'] / num_repos, 100)
        metrics['code_structure'] = min(metrics['code_structure'] / num_repos, 100)
        
        # Repository organization based on profile completeness
        org_score = 0
        if self.user_data.get('bio'):
            org_score += 20
        if self.user_data.get('blog'):
            org_score += 15
        if self.user_data.get('location'):
            org_score += 10
        if self.user_data.get('email'):
            org_score += 15
        if self.user_data.get('public_repos', 0) >= 5:
            org_score += 20
        if self.user_data.get('public_repos', 0) >= 10:
            org_score += 20
        metrics['repository_organization'] = min(org_score, 100)
        
        # Project impact based on stars and forks
        impact_score = 0
        if total_stars >= 50:
            impact_score = 100
        elif total_stars >= 20:
            impact_score = 80
        elif total_stars >= 10:
            impact_score = 60
        elif total_stars >= 5:
            impact_score = 40
        elif total_stars >= 1:
            impact_score = 20
        metrics['project_impact'] = impact_score
        
        # Technical depth based on language diversity
        unique_languages = len(set(languages))
        depth_score = min(unique_languages * 20, 100)
        metrics['technical_depth'] = depth_score
        
        # Calculate overall score (weighted average)
        weights = {
            'documentation_quality': 0.25,
            'code_structure': 0.20,
            'activity_consistency': 0.20,
            'repository_organization': 0.15,
            'project_impact': 0.10,
            'technical_depth': 0.10
        }
        
        overall_score = sum(metrics[key] * weights[key] for key in metrics)
        
        return overall_score, metrics, analyzed_repos, languages
    
    def generate_recommendations(self, metrics, analyzed_repos):
        """Generate actionable recommendations"""
        recommendations = []
        
        # Documentation recommendations
        if metrics['documentation_quality'] < 60:
            recommendations.append({
                'category': 'Documentation',
                'priority': 'High',
                'issue': 'README files are missing or incomplete',
                'action': 'Add comprehensive README files to your top projects. Include: project description, installation instructions, usage examples, screenshots/demos, and contribution guidelines.',
                'impact': '+15-20 points'
            })
        
        # Activity recommendations
        if metrics['activity_consistency'] < 50:
            recommendations.append({
                'category': 'Activity',
                'priority': 'High',
                'issue': 'Inconsistent commit history',
                'action': 'Maintain regular commit activity. Aim for at least 2-3 commits per week. Even small, meaningful updates show active development.',
                'impact': '+10-15 points'
            })
        
        # Structure recommendations
        if metrics['code_structure'] < 60:
            recommendations.append({
                'category': 'Structure',
                'priority': 'Medium',
                'issue': 'Missing important project files',
                'action': 'Add essential files: .gitignore, LICENSE, CONTRIBUTING.md, requirements.txt (or package.json). Add topics/tags to repositories for better discoverability.',
                'impact': '+8-12 points'
            })
        
        # Profile recommendations
        if metrics['repository_organization'] < 70:
            recommendations.append({
                'category': 'Profile',
                'priority': 'Medium',
                'issue': 'Incomplete profile information',
                'action': 'Complete your GitHub profile: add bio, location, website/blog, and email. Pin your best 4-6 repositories to showcase your skills.',
                'impact': '+10-15 points'
            })
        
        # Impact recommendations
        if metrics['project_impact'] < 40:
            recommendations.append({
                'category': 'Impact',
                'priority': 'Medium',
                'issue': 'Low project visibility and engagement',
                'action': 'Focus on quality over quantity. Build 2-3 substantial projects that solve real problems. Add detailed project descriptions, use cases, and live demos. Share your work on social media and developer communities.',
                'impact': '+15-20 points'
            })
        
        # Technical depth
        if metrics['technical_depth'] < 60:
            recommendations.append({
                'category': 'Technical Skills',
                'priority': 'Low',
                'issue': 'Limited technology diversity',
                'action': 'Expand your tech stack. Learn and showcase projects in complementary technologies. For example: if you know React, add Node.js backend projects; if you know Python, add data science or ML projects.',
                'impact': '+8-12 points'
            })
        
        # Repository-specific recommendations
        repos_without_readme = [r['name'] for r in analyzed_repos if r['readme_score'] < 20]
        if repos_without_readme:
            recommendations.append({
                'category': 'Quick Wins',
                'priority': 'High',
                'issue': f'Repositories without README: {", ".join(repos_without_readme[:3])}',
                'action': f'Add README files to these repositories immediately. This is the quickest way to improve your portfolio score.',
                'impact': '+20-30 points'
            })
        
        return recommendations[:6]  # Return top 6 recommendations
    
    def analyze(self):
        """Main analysis method"""
        if not self.fetch_user_data():
            return {'error': 'Failed to fetch user data. Please check the username.'}
        
        if not self.fetch_repositories():
            return {'error': 'Failed to fetch repositories.'}
        
        if not self.repos:
            return {'error': 'No public repositories found.'}
        
        score, metrics, analyzed_repos, languages = self.calculate_portfolio_score()
        recommendations = self.generate_recommendations(metrics, analyzed_repos)
        
        # Calculate grade
        if score >= 90:
            grade = 'A+'
            grade_desc = 'Outstanding'
        elif score >= 80:
            grade = 'A'
            grade_desc = 'Excellent'
        elif score >= 70:
            grade = 'B+'
            grade_desc = 'Very Good'
        elif score >= 60:
            grade = 'B'
            grade_desc = 'Good'
        elif score >= 50:
            grade = 'C+'
            grade_desc = 'Above Average'
        elif score >= 40:
            grade = 'C'
            grade_desc = 'Average'
        else:
            grade = 'D'
            grade_desc = 'Needs Improvement'
        
        return {
            'username': self.username,
            'profile': {
                'name': self.user_data.get('name', 'N/A'),
                'bio': self.user_data.get('bio', 'No bio'),
                'avatar_url': self.user_data.get('avatar_url'),
                'public_repos': self.user_data.get('public_repos', 0),
                'followers': self.user_data.get('followers', 0),
                'following': self.user_data.get('following', 0),
                'created_at': self.user_data.get('created_at', ''),
                'location': self.user_data.get('location', 'Not specified'),
                'blog': self.user_data.get('blog', ''),
            },
            'overall_score': round(score, 1),
            'grade': grade,
            'grade_description': grade_desc,
            'metrics': {k: round(v, 1) for k, v in metrics.items()},
            'analyzed_repositories': analyzed_repos[:5],  # Top 5 for display
            'languages': dict(Counter(languages).most_common(5)),
            'recommendations': recommendations,
            'strengths': self.identify_strengths(metrics),
            'red_flags': self.identify_red_flags(metrics, analyzed_repos)
        }
    
    def identify_strengths(self, metrics):
        """Identify portfolio strengths"""
        strengths = []
        if metrics['documentation_quality'] >= 70:
            strengths.append('Well-documented projects with clear READMEs')
        if metrics['activity_consistency'] >= 70:
            strengths.append('Consistent and regular commit activity')
        if metrics['code_structure'] >= 70:
            strengths.append('Professional repository structure and organization')
        if metrics['project_impact'] >= 60:
            strengths.append('Projects with community engagement (stars/forks)')
        if metrics['technical_depth'] >= 70:
            strengths.append('Diverse technology stack and skills')
        if metrics['repository_organization'] >= 70:
            strengths.append('Complete and professional profile setup')
        
        if not strengths:
            strengths.append('Opportunity for significant improvement across all areas')
        
        return strengths[:4]
    
    def identify_red_flags(self, metrics, analyzed_repos):
        """Identify red flags recruiters might notice"""
        red_flags = []
        
        if metrics['documentation_quality'] < 40:
            red_flags.append('⚠️ Most repositories lack proper documentation')
        if metrics['activity_consistency'] < 30:
            red_flags.append('⚠️ Very low commit activity - appears inactive')
        if metrics['code_structure'] < 40:
            red_flags.append('⚠️ Poor repository organization and missing essential files')
        if len(analyzed_repos) < 3:
            red_flags.append('⚠️ Very few non-forked repositories')
        if metrics['project_impact'] < 20:
            red_flags.append('⚠️ No community engagement or project visibility')
        
        return red_flags[:3]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    github_url = data.get('github_url', '')
    
    # Extract username from URL
    username = extract_username(github_url)
    if not username:
        return jsonify({'error': 'Invalid GitHub URL. Please provide a valid GitHub profile URL.'}), 400
    
    # Get token from environment variable (optional)
    token = os.environ.get('GITHUB_TOKEN')
    
    analyzer = GitHubAnalyzer(username, token)
    result = analyzer.analyze()
    
    if 'error' in result:
        return jsonify(result), 400
    
    return jsonify(result)

def extract_username(url):
    """Extract GitHub username from URL"""
    # Handle various GitHub URL formats
    patterns = [
        r'github\.com/([a-zA-Z0-9-]+)/?$',
        r'github\.com/([a-zA-Z0-9-]+)/.*',
        r'^([a-zA-Z0-9-]+)$'  # Just username
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return None

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
