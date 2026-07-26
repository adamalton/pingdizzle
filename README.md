pingdizzle
==========

A simple App Engine application to ping your websites and notify you if they're down.

# Local Development

* `python3.12 -m venv .venv`
* `source .venv/bin/activate`
* `pip install -r requirements-dev.txt`
* `python manage.py runserver`


# Set Up

1. Add the URLs that you want to check into `settings.PINGCONF`.
2. Add your email address(es) into `settings.SEND_DOWNTIME_NOTIFICATIONS_T0`.
3. Create an App Engine project in Google Cloud Platform and set your app ID in `bin/deploy.py`.
    - Enable the Cloud Tasks API, the Datastore (Firestore) API, and the Cloud Scheduler API.
    - Assign the permissions to use those APIs to the App Engine default service account.
4. Run `bin/deploy.,py`
5. Relax.

