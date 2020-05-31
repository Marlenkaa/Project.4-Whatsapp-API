import pandas as pd

df = pd.read_fwf('../INPUT/whatsapp.txt')

def cleaning(df):
    '''Cleans and sorts the hole dataset'''
    # Drop all useless columns
    df = df.drop(columns=list(df.columns[1:]))
    # Rename the column to simplify the usage at the beginning
    df = df.rename(columns={df.columns[0]: 'beginning'})
    df = df.dropna()
    # First filter to drop rows with missing info
    df['todrop'] = df['beginning'].apply(lambda x: 'no' if '/' in x else 'yes')
    noInfo = df[df['todrop'] == 'yes'].index
    df = df.drop(noInfo)
    df = df.drop(columns='todrop')
    # Expand all the data and drop all useless info
    df2 = df.beginning.str.split(expand=True)
    df2 = df2.drop(columns=list(df2.columns[4:]))
    # Bring back column with the hole info
    df2['raw'] = df['beginning']
    df2 = df2.drop(columns=2)
    # Create new column with cleaned users
    df2[3] = df2[3].astype('str')
    df2['users'] = df2[3].apply(lambda x: x.replace(":", ""))
    chat_users = list(df2['users'].value_counts()[:15].keys())
    df2['todrop'] = df2['users'].apply(lambda x: 'yes' if x not in chat_users else 'no')
    no_users = df2[df2['todrop'] == 'yes'].index
    df2 = df2.drop(no_users)
    df2 = df2.drop(columns='todrop')
    df2 = df2.drop(columns=3)
    # Extract only the messages by user
    df2['messages'] = df2['raw'].apply(lambda x: x.split(":")[-1].strip())
    df2 = df2.drop(columns='raw')
    # Change date format
    df2['date'] = df2[0].apply(lambda x: x.replace("/", "-"))
    df2 = df2.drop(columns=0)
    # Rename final columns
    df2 = df2.rename(columns={1:'hour'})
    df2.to_csv('../OUTPUT/whatsapp.csv')
    return df2

