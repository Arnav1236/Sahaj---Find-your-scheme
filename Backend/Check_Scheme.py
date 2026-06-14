import firebase_admin
from firebase_admin import credentials, firestore

# ── CONNECT TO FIREBASE ──
# Make sure serviceAccountKey.json is in the same folder
# Download it from: Firebase Console → Project Settings → Service Accounts → Generate New Private Key
if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()


# ── MATCHING LOGIC ──
def match_schemes(gender,age, income, location, occupation):
    # for doc in schemes_ref:
    #     print(doc.to_dict())
    """
    Fetches all schemes from Firebase and filters them
    based on the user's answers.

    Returns a list of matching scheme dictionaries.
    """

    # Fetch all schemes from Firestore
    schemes_ref = db.collection("SchemeMultilingual").get()

    matched = []

    for doc in schemes_ref:
        scheme = doc.to_dict()
        scheme["id"] = doc.id  # Add document ID to the scheme

        if is_eligible(scheme, gender, age, income, location, occupation):
            matched.append(scheme)

    return matched



def is_eligible(scheme,gender, age, income, location, occupation):
    """
    Checks if a single scheme matches the user's profile.
    A scheme is eligible only if ALL present criteria match.
    If a scheme has no criteria for a field, it matches everyone.
    """

    # Check gender
    if "gender" in scheme and scheme["gender"]:
        if gender not in scheme["gender"]:
            return False
    # Check age
    if "age" in scheme and scheme["age"]:
        if age not in scheme["age"]:
            return False

    # Check income
    if "income" in scheme and scheme["income"]:
        if income not in scheme["income"]:
            return False

    # Check location
    # Check location
    if "location" in scheme and scheme["location"] and scheme["location"] != ['']:
        if location not in scheme["location"]:
            return False

    # Check occupation
    if "occupation" in scheme and scheme["occupation"]:
        if occupation not in scheme["occupation"]:
            return False

    # All checks passed
    return True