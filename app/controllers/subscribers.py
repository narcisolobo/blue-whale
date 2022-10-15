from app.models.subscriber import Subscriber
from app import app, request, redirect

@app.post('/subscribers')
def create_subscriber():
    Subscriber.save(request.form)
    return redirect('/magazines')