TEST MARKS MANAGER — DJANGO ONLINE VERSION

इस ZIP में Django आधारित ऑनलाइन सिस्टम है:
- Admin username + password/PIN login
- Classes, subjects, students, tests
- Bulk student entry
- Marks entry और AB (Absent)
- Result table, percentage और rank
- Django Advanced Admin में पूरा edit/delete नियंत्रण
- PostgreSQL cloud database के लिए Render configuration

LOCAL COMPUTER पर चलाने के लिए:
1. Python 3.11+ install करें.
2. ZIP extract करें और इस folder में terminal खोलें.
3. python -m venv venv
4. Windows: venv\Scripts\activate
   Mac/Linux: source venv/bin/activate
5. pip install -r requirements.txt
6. python manage.py migrate
7. python manage.py createsuperuser
   Username और password set करें. यही password login PIN की तरह इस्तेमाल होगा.
8. python manage.py runserver
9. Browser में http://127.0.0.1:8000 खोलें.

ADMIN:
- सामान्य admin dashboard: /
- Advanced Admin: /django-admin/
- Admin user बनाने के बाद Advanced Admin में सभी records create/edit/delete कर सकते हैं.

ONLINE DEPLOY:
- GitHub पर पूरा project upload करें.
- Render पर New Blueprint चुनकर repository connect करें.
- render.yaml web service और PostgreSQL database बनाएगा (plan availability/provider pricing बदल सकती है).
- Deploy के बाद Render Shell में `python manage.py createsuperuser` चलाकर login user बनाएं.
- फिर apne onrender.com URL से kahin se bhi login karein.

IMPORTANT:
- यह starter project है. Production use से पहले PIN/password मजबूत रखें, HTTPS चालू रखें,
  backups लें और test करें. Public shared computer पर logout करें.
- PIN को कम अंकों का सरल numeric PIN न रखें; कम से कम 8 characters का मजबूत password रखें.
- Cloud provider की free-tier और database persistence की शर्तें बदल सकती हैं.
