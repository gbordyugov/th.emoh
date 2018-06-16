from time import time
from numpy.random import choice
from datetime import timedelta, datetime

def generate_attributions(no_attributions=10,
        filename='csv/attributions.csv'):
    """ creates a csv file representing the attribution tables,
    returns a list of valid anonymous_user_ids"""

    rows = []
    user_ids = []
    campaigns = ['Campaign A', 'Campaign B', 'Campaign C']
    no_campaigns = len(campaigns)
    
    now = datetime.now()
    
    for attr in range(no_attributions):
        timestamp = now + timedelta(minutes=attr)
        campaign = campaigns[attr % no_campaigns]
        user_id = attr # just for simplicity
        user_ids.append(user_id) # for the records
        row = ','.join(s for s in [str(attr), str(timestamp),
            campaign, str(user_id)])
        rows.append(row)

    print('write %s'%(filename))
    with open(filename, 'w') as f:
        f.write('\n'.join(rows))
    
    return user_ids


def generate_button_events(user_ids, no_events=10,
        filename='csv/button_events.csv'):
    """ given a list of valid user_ids, randomly generates no_events
    entries for the button events table
    returns the list of users ids with button events"""
    rows = []
    now = datetime.now() + timedelta(hours=1)

    # this one is with replacement, i.e. allowing repeating users
    user_ids = choice(user_ids, no_events)
    
    for id, user_id in enumerate(user_ids):
        timestamp = now + timedelta(minutes=id)
        user_email = str(user_id) + 'foo@bar.com'
        row = ','.join(s for s in [str(id), str(timestamp),
            user_email, str(user_id)])
        rows.append(row)

    print('write %s'%(filename))
    with open(filename, 'w') as f:
        f.write('\n'.join(rows))

    return user_ids

def generate_bank_events(user_ids, no_events=10,
        filename='csv/bank_events.csv'):
    """ given a list of valid user_ids, randomly generates no_events
    entries for the bank details events table
    returns the list of users ids with bank details events"""
    rows = []
    now = datetime.now() + timedelta(hours=2)

    # this one is with replacement, i.e. allowing repeating users
    user_ids = choice(user_ids, no_events)
    
    for id, user_id in enumerate(user_ids):
        timestamp = now + timedelta(minutes=id)
        bank_name = str(user_id) + "'s bank"
        row = ','.join(s for s in [str(id), str(timestamp),
            bank_name, str(user_id)])
        rows.append(row)

    print('write %s'%(filename))
    with open(filename, 'w') as f:
        f.write('\n'.join(rows))

    return user_ids


no_attributions = 10000
no_button_events = int(no_attributions/2)
no_bank_events   = int(no_button_events/5)

if '__main__' == __name__:
    all_user_ids = generate_attributions(no_attributions)
    clicked_button_user_ids = generate_button_events(all_user_ids,
            no_button_events)
    generate_bank_events(clicked_button_user_ids, no_bank_events)
