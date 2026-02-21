"""
Quick fix for all template files - adds DOCTYPE
"""

import os

templates_dir = 'templates'

# Files to fix
template_files = [
    'generate_campaign.html',
    'sales_update.html',
    'connect_accounts.html',
    'analytics_dashboard.html',
    'demo_hub.html',
    'live_dashboard.html',
    'architecture.html'
]

for filename in template_files:
    filepath = os.path.join(templates_dir, filename)
    
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if DOCTYPE is missing
        if not content.strip().startswith('<!DOCTYPE'):
            # Add DOCTYPE before {% extends
            if content.strip().startswith('{% extends'):
                new_content = '<!DOCTYPE html>\n' + content
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                print(f'✅ Fixed: {filename}')
            else:
                print(f'⚠️ Skipped: {filename} (unusual structure)')
        else:
            print(f'✅ OK: {filename}')
    else:
        print(f'❌ Missing: {filename}')

print('\n✅ Template fix complete!')
print('Restart Flask and refresh browser!')