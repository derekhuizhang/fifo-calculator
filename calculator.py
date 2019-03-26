import pandas as pd
from collections import deque

def get_portfolio_data(file_name):
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
	current_profit_loss = {}
	current_prices = {}

	for index, row in df.iterrows():
		if row['ASSET'] not in transactions:
			if row['AMOUNT'] < 0:
				return {
					'error': 'Error: detected sale before purchase (short selling is not supported)'
				}

			current_prices[row['ASSET']] = row['PRICE']

			transactions[row['ASSET']] = deque()
			transactions[row['ASSET']].append([row['AMOUNT'], row['PRICE']])

			current_profit_loss[row['ASSET']] = 0
		else:
			current_prices[row['ASSET']] = row['PRICE']
			
			if row['AMOUNT'] > 0:
				transactions[row['ASSET']].append([row['AMOUNT'], row['PRICE']])
			else:
				amount_left = -row['AMOUNT']
				while amount_left > 0:
					try:
						earliest_transaction = transactions[row['ASSET']].popleft()
						if amount_left > earliest_transaction[0]:
							amount_left -= earliest_transactions[row['ASSET']][0]
							current_profit_loss[row['ASSET']] += earliest_transaction[0] * (row['PRICE'] - earliest_transaction[1])
						else:
							earliest_transaction[0] -= amount_left
							current_profit_loss[row['ASSET']] += amount_left * (row['PRICE'] - earliest_transaction[1])
							transactions[row['ASSET']].appendleft(earliest_transaction)
							break
					except IndexError:
						return {
							'error': 'Error: detected sale before purchase (short selling is not supported)'
						}
	final_holdings = {}
	total_value = 0
	total_profit_loss = 0
	nonzero_assets = 0

	for asset in transactions:
		if len(transactions[asset]) > 0: 
			final_amount = sum([item[0] for item in transactions[asset]])
			final_holdings[asset] = {
				'amount': final_amount, 
				'value': final_prices[asset] * final_amount,
				'profit_loss': current_profit_loss[asset]
			}
			total_value += final_amount * final_prices[asset]
			total_profit_loss += current_profit_loss[asset]
			nonzero_assets += 1
		else:
			final_holdings[asset] = {
				'profit_loss': current_profit_loss[asset]
			}
	
	return {
		'final_holdings': final_holdings,
		'nonzero_assets': nonzero_assets,
		'total_value': total_value,
		'total_profit_loss': total_profit_loss
	}

