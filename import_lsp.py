#!/usr/bin/env python

"""
This is a WIP script for importing data from the old LSP.
It expects a MySQL server without password and with the db being named 'lsp'
running on localhost.
"""
# TODO: How to properly import time data?
# TODO: Import subcategories (tags)

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'lsp2.settings'
import django
django.setup()

from django.db import transaction
transaction.set_autocommit(False)

from lsp2.submissions.models import *

import pymysql

###############################################################################


print("Connecting to database… ", end="")
con = pymysql.connect(host='localhost', user='root', passwd=None, db='lsp')
cur = con.cursor()
print("Done")


###############################################################################


def print_status(cursor, name):
    print(
        "\rImported %d of %d %s" % (cursor.rownumber, cursor.rowcount, name),
        end=''
    )


###############################################################################


cur.execute(
    'SELECT id, login, password, realname, is_admin FROM users GROUP BY login')

for row in cur:
    id, login, password, realname, is_admin = row

    u = User(
        pk=id,
        username=login,
        first_name=realname.split()[0] if realname else "",
        last_name=realname[realname.rfind(' '):] if realname else "",
        password='sha1$$' + password,
        is_staff=is_admin
    )

    u.save()
    print_status(cur, "users")
print()

User(username="admin", password="pbkdf2_sha256$12000$FAyIyGH6tztt$ttgkL2UapbnKsZMJiB06dfUt7r19oELU2jCmIMMydXk=",is_superuser=1, is_staff=1).save()


###############################################################################


licenses = (
    (1, 'Artistic License 2.0', 'http://opensource.org/licenses/Artistic-2.0'),
    (2, 'BSD', 'http://opensource.org/licenses/bsd-license.php'),
    (3, 'Common Public License', 'http://opensource.org/licenses/cpl1.0.php'),
    (4, 'GNU Free Documentation License', 'http://www.gnu.org/copyleft/fdl.html'),
    (5, 'Green openmusic', 'http://openmusic.linuxtag.org/green.html'),
    (6, 'Yellow openmusic', 'http://openmusic.linuxtag.org/yellow.html'),
    (7, 'Red openmusic', 'http://openmusic.linuxtag.org/red.html'),
    (8, 'Creative Commons (by)', 'http://creativecommons.org/licenses/by/4.0/'),
    (9, 'Creative Commons (by-nc)', 'http://creativecommons.org/licenses/by-nc/4.0/'),
    (10, 'Creative Commons (by-nd)', 'http://creativecommons.org/licenses/by-nd/4.0/'),
    (11, 'Creative Commons (by-sa)', 'http://creativecommons.org/licenses/by-sa/4.0/'),
    (13, 'Creative Commons (by-nc-sa)', 'http://creativecommons.org/licenses/by-nc-sa/4.0/'),
    (12, 'Creative Commons (by-nc-nd)', 'http://creativecommons.org/licenses/by-nc-nd/4.0/'),
)

for l in licenses:
    License(
        id=l[0],
        name=l[1],
        url=l[2]
    ).save()
print("Imported licenses")


###############################################################################


categories = {}
cur.execute('SELECT id, name FROM categories')

for row in cur:
    categories[row[0]] = row[1]
    print_status(cur, "categories")
print()


###############################################################################


cur.execute('SELECT id, user_id, filename, license_id, category, subcategory, \
description, insert_date, update_date, rate, size, hash, downloads FROM files')

for row in cur:
    id, user_id, filename, license_id, category, subcategory, description, \
        insert_date, update_date, rate, size, hash, downloads = row

    if category < 1 or category > 6:
        print("Fatal: Unknown category %d" % category)
        continue

    cat = categories[category]
    if cat == "Projects":
        # TODO: Get length of project in seconds
        s = ProjectSubmission(
            seconds=None
        )
    elif cat == "Samples":
        # TODO: Get length of sample in milliseconds
        s = SampleSubmission(
            milliseconds=None
        )
    elif cat == "UI themes":
        s = ThemeSubmission()
    elif cat == "Presets":
        pass
    elif cat == "Tutorials":
        pass
    elif cat == "Screenshots":
        pass

    s.id = id
    s.uploader = User.objects.get(pk=user_id)
    s.name = filename[0:filename.rfind('.')]
    s.license = None if license_id==0 else License.objects.get(pk=license_id)
    s.description = description
    s.submitDate = insert_date
    s.updateDate = update_date

    s.save()

    f = File(submission=s, filename=filename, version=1, size=size, downloadCount=downloads, sha1hash=hash, date=insert_date)
    f.save()

    print_status(cur, "files")
print()


###############################################################################


cur.execute('SELECT id, user_id, file_id, `date`, `text` FROM comments')

skipped = 0
for row in cur:
    id, user_id, file_id, date, text = row

    if Submission.objects.filter(pk=file_id).count() == 0:
        skipped += 1
        continue

    comment = Comment(
        pk=id,
        user=User.objects.get(pk=user_id),
        submission=Submission.objects.get(pk=file_id),
        date=date,
        text=text
    )

    comment.save()
    print_status(cur, "comments")
print(" (%d skipped because of missing submission)" % skipped)

###############################################################################


cur.execute('SELECT id, file_id, user_id, stars FROM ratings')

skipped = 0
for row in cur:
    id, file_id, user_id, stars = row

    if Submission.objects.filter(pk=file_id).count() == 0:
        skipped += 1
        continue

    # 3 stars ratings will not be counted
    if stars == 3:
        continue

    vote = Vote(
        user=User.objects.get(pk=user_id),
        submission=Submission.objects.get(pk=file_id),
        date=None,
        upvote=1 if stars > 3 else 0
    )

    vote.save()
    print_status(cur, "ratings")
print(" (%d skipped because of missing submission)" % skipped)


###############################################################################

transaction.commit()
