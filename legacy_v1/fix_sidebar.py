"""
Quick fix for sidebar in all templates
"""

import os
import re

templates_dir = 'templates'

# Template files with sidebars
template_files = [
    'dashboard.html',
    'generate_campaign.html',
    'sales_update.html',
    'connect_accounts.html',
    'analytics_dashboard.html'
]

# Corrected sidebar HTML
corrected_sidebar = '''<aside class="sidebar">
    <div class="sidebar-header">
        <h2 class="sidebar-brand">🤖 Agentic AI</h2>
    </div>
    
    <nav class="sidebar-nav">
        <a href="{{ url_for('dashboard') }}" class="nav-item {% if request.endpoint == 'dashboard' %}active{% endif %}">
            <span class="nav-icon">📊</span>
            <span>Dashboard</span>
        </a>
        
        <a href="{{ url_for('generate_campaign_page') }}" class="nav-item {% if request.endpoint == 'generate_campaign_page' %}active{% endif %}">
            <span class="nav-icon">🎯</span>
            <span>Generate Campaign</span>
        </a>
        
        <a href="{{ url_for('sales.sales_update_page') }}" class="nav-item {% if 'sales' in request.endpoint %}active{% endif %}">
            <span class="nav-icon">💰</span>
            <span>Sales Update</span>
        </a>
        
        <a href="{{ url_for('analytics.analytics_page') }}" class="nav-item {% if 'analytics' in request.endpoint %}active{% endif %}">
            <span class="nav-icon">📈</span>
            <span>Analytics</span>
        </a>
        
        <a href="{{ url_for('social.connect_accounts_page') }}" class="nav-item {% if 'social' in request.endpoint or 'connect_accounts' in request.endpoint %}active{% endif %}">
            <span class="nav-icon">🔗</span>
            <span>Social Accounts</span>
        </a>
        
        <div class="sidebar-divider"></div>
        
        <a href="{{ url_for('demo_hub') }}" class="nav-item {% if 'demo' in request.endpoint %}active{% endif %}">
            <span class="nav-icon">🎬</span>
            <span>Live Demo</span>
        </a>
        
        <a href="{{ url_for('logout') }}" class="nav-item">
            <span class="nav-icon">🚪</span>
            <span>Logout</span>
        </a>
    </nav>
</aside>'''

for filename in template_files:
    filepath = os.path.join(templates_dir, filename)
    
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace sidebar content
        pattern = r'<aside class="sidebar">.*?</aside>'
        
        if re.search(pattern, content, re.DOTALL):
            new_content = re.sub(pattern, corrected_sidebar, content, flags=re.DOTALL)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f'✅ Fixed: {filename}')
        else:
            print(f'⚠️ No sidebar found in: {filename}')
    else:
        print(f'❌ Missing: {filename}')

print('\n✅ Sidebar fix complete!')
print('Restart Flask and refresh browser!')