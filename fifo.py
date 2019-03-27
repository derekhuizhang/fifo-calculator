import pandas as pd
from collections import deque
import argparse

def get_output(file_name):
    calculated_portfolio = get_portfolio_data(file_name)

    if 'error' in calculated_portfolio:
        output = calculated_portfolio['error']
        output_file_name = file_name[:-4] + '.out'
        print(output)
        with open(output_file_name, 'w+') as f:
            f.write(output)
        print('\nSuccessfully saved output to file: %s' % (output_file_name))
        return
    output = ''    
    final_holdings = calculated_portfolio['final_holdings']
    
    if calculated_portfolio['nonzero_assets'] == 1:
        asset_string = 'asset'
    else:
        asset_string = 'assets'
    output += 'Portfolio (%d %s) \n' % (calculated_portfolio['nonzero_assets'], asset_string)
    
    for asset in final_holdings:
        if 'amount' in final_holdings[asset]:
            output += '%s: %d %s \n' % (asset, final_holdings[asset]['amount'], format_dollars(final_holdings[asset]['value']))
    output += 'Total value: %s \n' % (format_dollars(calculated_portfolio['total_value']))

    if len(final_holdings.keys()) == 1:
        asset_string = 'asset'
    else:
        asset_string = 'assets'
    output += 'Portfolio P&L (%d %s): \n' % (len(final_holdings.keys()), asset_string)
    
    for asset in final_holdings:
        output += '%s: %s \n' % (asset, format_dollars(final_holdings[asset]['realized_pl']))
    output += 'Total P&L: %s \n' % (format_dollars(calculated_portfolio['total_realized_pl']))
    
    print(output)
    output_file_name = file_name[:-4] + '.out'
    with open(output_file_name, 'w+') as f:
        f.write(output)
    print('\nSuccessfully saved output to file: %s' % (output_file_name))

def get_portfolio_data(file_name):
    # read file
    try:
        df = pd.read_csv(file_name)
    except IOError:
        return {
            'error': 'Error: Invalid file name! Check your file name and try again'
        }

    # edge case: return error if no transactions exist in ledger
    if (pd.isna(df.iloc[0]['ASSET'])):
        return {
            'error': 'Error: No transactions found in ledger.'
        }

    transactions = {}
    current_realized_pl = {}
    current_prices = {}

    for index, row in df.iterrows():
        if row['ASSET'] not in transactions:
            if row['AMOUNT'] < 0:
                return {
                    'error': 'Error: detected sale before purchase (short selling is not supported). ' +
                        'Error occurred on index %d: %d %s' % (index, row['AMOUNT'], row['ASSET'])
                }

            current_prices[row['ASSET']] = row['PRICE']
            transactions[row['ASSET']] = deque()
            transactions[row['ASSET']].append([row['AMOUNT'], row['PRICE']])

            current_realized_pl[row['ASSET']] = 0
        else:
            current_prices[row['ASSET']] = row['PRICE']

            if row['AMOUNT'] > 0:
                transactions[row['ASSET']].append([row['AMOUNT'], row['PRICE']])
            else:
                amount_left = -row['AMOUNT']
                while amount_left > 0:
                    try:
                        # FIFO: remove the first added transaction
                        earliest_transaction = transactions[row['ASSET']].popleft()
                        
                        # remove entire transaction if removing more than amount left
                        if amount_left >= earliest_transaction[0]:
                            amount_left -= earliest_transaction[0]
                            current_realized_pl[row['ASSET']] += earliest_transaction[0] \
                                * (row['PRICE'] - earliest_transaction[1])
                        
                        # add back part of transaction if left over after removing amount left
                        else:
                            earliest_transaction[0] -= amount_left
                            current_realized_pl[row['ASSET']] += amount_left \
                                * (row['PRICE'] - earliest_transaction[1])
                            transactions[row['ASSET']].appendleft(earliest_transaction)
                            break
                    except IndexError:
                        return {
                            'error': 'Error: detected sale before purchase (short selling is not supported). ' +
                                'Error occurred on index %d: %d %s' % (index, row['AMOUNT'], row['ASSET'])
                        }
    final_holdings = {}
    total_value = 0
    total_realized_pl = 0
    nonzero_assets = 0
    for asset in transactions:
        if len(transactions[asset]) > 0: 
            # include 'amount' and 'value' for transactions with nonzero amounts in portfolio
            final_amount = sum([item[0] for item in transactions[asset]])
            final_holdings[asset] = {
                'amount': final_amount, 
                'value': current_prices[asset] * final_amount,
                'realized_pl': current_realized_pl[asset]
            }
            total_value += final_amount * current_prices[asset]
            total_realized_pl += current_realized_pl[asset]
            nonzero_assets += 1
        else:
            # only include 'realized profit/loss' for transactions with zero amount in portfolio
            final_holdings[asset] = {
                'realized_pl': current_realized_pl[asset]
            }
            total_realized_pl += current_realized_pl[asset]
            
    return {
        'final_holdings': final_holdings,
        'nonzero_assets': nonzero_assets,
        'total_value': total_value,
        'total_realized_pl': total_realized_pl
    }

def format_dollars(value):
    if value < 0:
        return '-${:,.2f}'.format(-value)
    else:
        return '${:,.2f}'.format(value)
    
def parse_file_name():
    parser = argparse.ArgumentParser(description='Implementation of FIFO calculator.')
    parser.add_argument('file_name', help='Path to CSV file of ledger', default='empty_string')
    args = parser.parse_args()

    if args.file_name == 'empty_string':
        print('Error: Missing path to CSV file!')
        return
    if len(args.file_name) < 5 or args.file_name[-4:] != '.csv':
        print('Error: Invalid path! Check to make sure you are including a valid path to a CSV file.')
        return
    return args.file_name

if __name__ == '__main__':
    file_name = parse_file_name()
    if file_name is not None:
        get_output(file_name)