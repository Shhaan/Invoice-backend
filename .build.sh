
set -e
 
pip install -r requirements.txt

echo "Running migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Creating superuser..."
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    User.objects.create_superuser(email='sss@gmail.com', password='sss#admin')
EOF

echo "Superuser created (if it didn't exist), migrations run, and static files collected."
