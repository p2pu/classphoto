from bio import db

import datetime
import string
import random

def _bio2dict( bio_db ):
    bio_dict = { 
        'email': bio_db.email,
        'secret': bio_db.secret,
        'sequence': bio_db.sequence,
        'name': bio_db.name,
        'bio': bio_db.bio,
        'avatar': bio_db.avatar,
    }
    if bio_db.twitter:
        bio_dict['twitter'] = bio_db.twitter
    if bio_db.gplus:
        bio_dict['gplus'] = bio_db.gplus
    return bio_dict


def save_bio( email, sequence, name, bio, avatar, twitter=None, gplus=None):
    
    now = datetime.datetime.utcnow()

    # delete any previous bios
    if db.UserBio.objects.filter(email=email, sequence=sequence, date_deleted__isnull=True).exists():
        pending_bio = db.UserBio.objects.get(email=email, sequence=sequence, date_deleted__isnull=True)
        pending_bio.date_deleted = now
        pending_bio.save()

    bio_db = db.UserBio()
    bio_db.secret = ''.join([
        random.choice(string.letters+string.digits) for i in range(32)
    ])

    bio_db.email = email
    bio_db.sequence = sequence
    bio_db.name = name
    bio_db.bio = bio
    bio_db.avatar = avatar
    bio_db.twitter = twitter
    bio_db.gplus = gplus
    bio_db.date_added = now
    bio_db.date_updated = now
    bio_db.save()
    return _bio2dict(bio_db)


def has_bio( email, sequence ):
    bios_db = db.UserBio.objects.filter(
        email=email,
        sequence=sequence,
        date_deleted__isnull=True
    )
    return bios_db.exists()


def get_bio( email, sequence ):
    bios_db = db.UserBio.objects.get(
        email=email,
        date_deleted__isnull=True
    )
    return _bio2dict(bios_db)


def get_bios( sequence, limit=100 ):
    bios_db = db.UserBio.objects.filter(
        sequence=sequence,
        date_deleted__isnull=True
    )
    if limit > 0:
        bios_db = bios_db[:limit]
    return [ _bio2dict(bio) for bio in bios_db ]


def get_bios_by_email( sequence, emails ):
    bios_db = db.UserBio.objects.filter(
        sequence=sequence,
        email__in=emails,
        date_deleted__isnull=True
    )
    return [ _bio2dict(bio) for bio in bios_db ]


def get_bio_by_secret( secret ):
    bios_db = db.UserBio.objects.get(secret=secret)
    return _bio2dict(bios_db)
