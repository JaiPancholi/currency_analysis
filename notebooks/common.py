import datetime
import pandas as pd

def treat_data(df):
    """
    Clean Dataframe to rename values, format columns, and drop unnecessary columns.
    """
    # drop columns
    df.drop(columns=['id', 'url', 'created_at', 'updated_at'], inplace=True)

    # date manipulation
    df['date'] = df.apply(lambda x: datetime.date(x['year'], x['month'], x['day']), axis=1)
    df['date'] = pd.to_datetime(df['date'])
    df['week'] = df['date'].dt.week

    # rename values to ISO format
    currency_dict = {'Japanese Yen': 'JPY','Malaysian ringgit': 'MYR','New Zealand Dollar': 'NZD','Norwegian Krone': 'NOK','Polish Zloty': 'PLN','Russian Ruble': 'RUB','Saudi Riyal': 'SAR','Singapore Dollar': 'SGD','South African Rand': 'ZAR','South Korean Won': 'KRW','Swedish Krona': 'SEK','Swiss Franc': 'CHF','Taiwan Dollar': 'TWD','Thai Baht': 'THB','Turkish Lira': 'TRY','US Dollar': 'USD','Australian Dollar': 'AUD','Canadian Dollar': 'CAD','Chinese Yuan': 'Yuan','Cyprus Pound': 'CYP','Czech Koruna': 'CZK','Danish Krone': 'DKK','Estonian Kroon': 'EEK','Euro': 'EUR','Hong Kong Dollar': 'HKD','Hungarian Forint': 'HUF','Indian Rupee': 'INR','Israeli Shekel': 'ILS','Latvian Lats': 'LVL','Lithuanian Litas': 'LTL','Maltese Lira': 'MTL','Slovak Koruna': 'SKK','Slovenian Tolar': 'SIT','Sterling': 'GBP','Swedish Krona ': 'SEK','Brazilian Real': 'BRL','Austrian Schilling': 'ATS','Belgian Franc': 'BEF','Deutschemark': 'DEM','Finnish Markka': 'FIM','French Franc': 'FRF','Greek Drachma': 'GRD','Irish Punt': 'IEP','Italian Lire': 'ITL','Netherlands Guilder': 'NLG','Portuguese Escudo': 'PTE','Spanish Peseta': 'ESP'}
    df['target_currency'].replace('Latvian Lats\r\nCurrency joined the Euro on 01/01/2014', 'Latvian Lats', inplace=True)
    df['target_currency_symbol'] = df['target_currency'].apply(lambda x: currency_dict[x])
    df.drop(columns=['target_currency'], inplace=True)

    # reorder columns, mostly aesthetic
    df = df[['date', 'year', 'month', 'week', 'day', 'base_currency', 'target_currency_symbol', 'target_spot_rate']]

    return df

# def extract_period_returns(currency_df):
#     """
#     input should be a dataframe that that has spot rates from multiple currencies against a single currency.
#     """

#     # TODO FIX the problem of day return on Monday is always null, so we should spill over from Friday.


#     currency_pivot_df = currency_df.pivot(index='date', columns='target_currency_symbol', values='target_spot_rate')
    
#     # get relative change in prices of currencies
#     currency_pivot_d_change = currency_pivot_df/currency_pivot_df.shift(1, freq=pd.to_timedelta(1, 'D')) - 1
#     currency_pivot_d_change = currency_pivot_d_change.unstack().reset_index().rename({0: '1d_return'}, axis=1)

#     currency_pivot_w_change = currency_pivot_df/currency_pivot_df.shift(7, freq=pd.to_timedelta(1, 'D')) - 1
#     currency_pivot_w_change = currency_pivot_w_change.unstack().reset_index().rename({0: '1w_return'}, axis=1)

#     currency_pivot_m_change = currency_pivot_df/currency_pivot_df.shift(30, freq=pd.to_timedelta(1, 'D')) - 1
#     currency_pivot_m_change = currency_pivot_m_change.unstack().reset_index().rename({0: '1m_return'}, axis=1)

#     currency_pivot_y_change = currency_pivot_df/currency_pivot_df.shift(365, freq=pd.to_timedelta(1, 'D')) - 1
#     currency_pivot_y_change = currency_pivot_y_change.unstack().reset_index().rename({0: '1y_return'}, axis=1)

#     currency_df = currency_df.merge(currency_pivot_d_change, how='left', on=['date', 'target_currency_symbol'])
#     currency_df = currency_df.merge(currency_pivot_w_change, how='left', on=['date', 'target_currency_symbol'])
#     currency_df = currency_df.merge(currency_pivot_m_change, how='left', on=['date', 'target_currency_symbol'])
#     currency_df = currency_df.merge(currency_pivot_y_change, how='left', on=['date', 'target_currency_symbol'])
#     currency_df = currency_df[~currency_df['base_currency'].isnull()]
    
#     return currency_df

def extract_period_returns(currency_df):
    frames = []
    for target_currency in currency_df['target_currency_symbol'].unique():
        temp_df = currency_df[currency_df['target_currency_symbol']==target_currency]
        temp_df = extract_period_returns_single_currency(temp_df)
        temp_df['target_currency_symbol'] = target_currency

        frames.append(temp_df)

    df = pd.concat(frames)
    df['day'] = df['date'].dt.day
    df['week'] = df['date'].dt.week
    df['month'] = df['date'].dt.month
    df['year'] = df['date'].dt.year

    return df

def extract_period_returns_single_currency(currency_df):
    # extract a single target currency and drop unneeded columns
    currency_df.drop(columns=['target_currency_symbol', 'base_currency'], inplace=True)
    currency_df.drop(columns=['year', 'month', 'week', 'day'], inplace=True)

    # add in data for missing dates
    currency_df = currency_df.sort_values(['date'])
    currency_df.set_index('date',inplace=True)
    currency_df = currency_df.resample('D', axis=0).pad()
    currency_df = currency_df.reset_index()

    # find shifts in period dates
    currency_df['date_last_day'] = currency_df['date'] - pd.to_timedelta(1, 'D')
    currency_df['date_last_week'] = currency_df['date'] - pd.to_timedelta(1, 'W')
    currency_df['date_last_month'] = currency_df['date'] - pd.to_timedelta(1, 'M')
    currency_df['date_last_year'] = currency_df['date'] - pd.to_timedelta(1, 'Y')
    currency_df['date_last_day'] = currency_df['date_last_day'].dt.floor(freq='D')
    currency_df['date_last_week'] = currency_df['date_last_week'].dt.floor(freq='D')
    currency_df['date_last_month'] = currency_df['date_last_month'].dt.floor(freq='D')
    currency_df['date_last_year'] = currency_df['date_last_year'].dt.floor(freq='D')

    
    # extract the price on the shifted dates
    rename_dict = {
        'date_x': 'date',
        'date_last_day_x': 'date_last_day',
        'date_last_week_x': 'date_last_week',
        'date_last_month_x': 'date_last_month',
        'date_last_year_x': 'date_last_year',
        'target_spot_rate_x': 'target_spot_rate'
    }

    currency_df = currency_df.merge(currency_df[['date_last_day','target_spot_rate']], left_on='date', right_on='date_last_day')
    currency_df.drop(columns='date_last_day_y', inplace=True)
    rename_dict['target_spot_rate_y'] = 'one_day_future_price'
    currency_df = currency_df.rename(rename_dict, axis=1)

    currency_df = currency_df.merge(currency_df[['date_last_week','target_spot_rate']], left_on='date', right_on='date_last_week')
    currency_df.drop(columns='date_last_week_y', inplace=True)
    rename_dict['target_spot_rate_y'] = 'one_week_future_price'
    currency_df = currency_df.rename(rename_dict, axis=1)

    currency_df = currency_df.merge(currency_df[['date_last_month','target_spot_rate']], left_on='date', right_on='date_last_month')
    currency_df.drop(columns='date_last_month_y', inplace=True)
    rename_dict['target_spot_rate_y'] = 'one_month_future_price'
    currency_df = currency_df.rename(rename_dict, axis=1)

    currency_df = currency_df.merge(currency_df[['date_last_year','target_spot_rate']], left_on='date', right_on='date_last_year')
    currency_df.drop(columns='date_last_year_y', inplace=True)
    rename_dict['target_spot_rate_y'] = 'one_year_future_price'
    currency_df = currency_df.rename(rename_dict, axis=1)

    # caluclate returns based on shifted prices
    currency_df['one_day_future_return'] = (currency_df['one_day_future_price'] - currency_df['target_spot_rate'])/currency_df['target_spot_rate']
    currency_df['one_week_future_return'] = (currency_df['one_week_future_price'] - currency_df['target_spot_rate'])/currency_df['target_spot_rate']
    currency_df['one_month_future_return'] = (currency_df['one_month_future_price'] - currency_df['target_spot_rate'])/currency_df['target_spot_rate']
    currency_df['one_year_future_return'] = (currency_df['one_year_future_price'] - currency_df['target_spot_rate'])/currency_df['target_spot_rate']
    currency_df.drop(columns=['one_day_future_price', 'one_week_future_price', 'one_month_future_price', 'one_year_future_price'], inplace=True)

    currency_df = currency_df.merge(currency_df[['date','target_spot_rate']], left_on='date_last_day', right_on='date')
    currency_df.drop(columns='date_y', inplace=True)
    rename_dict['target_spot_rate_y'] = 'one_day_past_price'
    currency_df = currency_df.rename(rename_dict, axis=1)

    currency_df = currency_df.merge(currency_df[['date','target_spot_rate']], left_on='date_last_week', right_on='date')
    currency_df.drop(columns='date_y', inplace=True)
    rename_dict['target_spot_rate_y'] = 'one_week_past_price'
    currency_df = currency_df.rename(rename_dict, axis=1)

    currency_df = currency_df.merge(currency_df[['date','target_spot_rate']], left_on='date_last_month', right_on='date')
    currency_df.drop(columns='date_y', inplace=True)
    rename_dict['target_spot_rate_y'] = 'one_month_past_price'
    currency_df = currency_df.rename(rename_dict, axis=1)

    currency_df = currency_df.merge(currency_df[['date','target_spot_rate']], left_on='date_last_year', right_on='date')
    currency_df.drop(columns='date_y', inplace=True)
    rename_dict['target_spot_rate_y'] = 'one_year_past_price'
    currency_df = currency_df.rename(rename_dict, axis=1)

    # caluclate returns based on shifted prices
    currency_df['one_day_past_return'] = (currency_df['target_spot_rate'] - currency_df['one_day_past_price'])/currency_df['one_day_past_price']
    currency_df['one_week_past_return'] = (currency_df['target_spot_rate'] - currency_df['one_week_past_price'])/currency_df['one_week_past_price']
    currency_df['one_month_past_return'] = (currency_df['target_spot_rate'] - currency_df['one_month_past_price'])/currency_df['one_month_past_price']
    currency_df['one_year_past_return'] = (currency_df['target_spot_rate'] - currency_df['one_year_past_price'])/currency_df['one_year_past_price']
    
    currency_df.drop(columns=['date_last_day', 'date_last_week', 'date_last_month', 'date_last_year'], inplace=True)

    return currency_df


def extract_volatility_of_prices(currency_df):
    week_vol = currency_df.groupby(['week', 'month', 'year', 'target_currency_symbol'])['target_spot_rate'].std()
    week_vol = week_vol.reset_index().rename({'target_spot_rate': '1w_vol'}, axis=1)

    month_vol = currency_df.groupby(['month', 'year', 'target_currency_symbol'])['target_spot_rate'].std()
    month_vol = month_vol.reset_index().rename({'target_spot_rate': '1m_vol'}, axis=1)

    year_vol = currency_df.groupby(['year', 'target_currency_symbol'])['target_spot_rate'].std()
    year_vol = year_vol.reset_index().rename({'target_spot_rate': '1y_vol'}, axis=1)

    currency_df = currency_df.merge(week_vol, how='left', on=['week', 'month', 'year', 'target_currency_symbol'])
    currency_df = currency_df.merge(month_vol, how='left', on=['month', 'year', 'target_currency_symbol'])
    currency_df = currency_df.merge(year_vol, how='left', on=['year', 'target_currency_symbol'])

    return currency_df


def reshape_df(currency_df, target_currencies=['AUD', 'CAD', 'USD', 'EUR', 'JPY']):
    """
    Input is with period returns and price volatilities.
    """
    # reshape dataframe to use returns from other currencies as features.
    cols = ['target_spot_rate', '1d_return', '1w_return', '1m_return', '1y_return', '1w_vol', '1m_vol', '1y_vol']
    cols = ['target_spot_rate', '1w_vol', '1m_vol', '1y_vol', 'one_day_future_return', 'one_week_future_return', 'one_month_future_return', 'one_year_future_return', 'one_day_past_return', 'one_week_past_return', 'one_month_past_return', 'one_year_past_return']
    
    test_df = currency_df

    for cur in target_currencies:
        temp_df = currency_df[currency_df['target_currency_symbol']==cur][['date']+cols]
        temp_df = temp_df.reset_index().rename({col: cur+'_'+col for col in cols}, axis=1)
        temp_df.drop(columns=['index'], inplace=True, axis=1)

        test_df = test_df.merge(temp_df, how='left', on=['date'])


    test_df.drop(columns=['target_currency_symbol']+cols, axis=1, inplace=True)
    test_df.drop_duplicates(inplace=True)
    test_df.reset_index().drop('index', inplace=True, axis=1)

    return test_df