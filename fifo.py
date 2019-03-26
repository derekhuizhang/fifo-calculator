import argparse 
from calculator import get_portfolio_data

def get_output(file_name):
    calculated_portfolio = get_portfolio_data(file_name)
    
    if 'error' in calculated_portfolio:
        return calculated_portfolio['error']
    
    output = ''    
    final_holdings = calculated_portfolio['final_holdings']
    
    if calculated_portfolio['nonzero_assets'] == 1:
        asset_string = 'asset'
    else:
        asset_string = 'assets'
    output += 'Portfolio (%d %s) \n' % (calculated_portfolio['nonzero_assets'], asset_string)
    
    for asset in final_holdings:
        if 'amount' in final_holdings[asset]:
            output += '%s: %d $%d \n' % (asset, final_holdings[asset]['amount'], final_holdings[asset]['value'])
    output += 'Total value: $%d \n' % (calculated_portfolio['total_value'])

    if len(final_holdings.keys()) == 1:
        asset_string = 'asset'
    else:
        asset_string = 'assets'
    output += 'Portfolio P&L (%d %s): \n' % (len(final_holdings.keys()), asset_string)
    
    for asset in final_holdings:
        output += '%s: $%d \n' % (asset, final_holdings[asset]['profit_loss'])
    
    output += 'Total P&L: $%d \n' % (calculated_portfolio['total_profit_loss'])
    
    output_file_name = file_name[:-4] + '.out'
    with open(output_file_name, 'w+') as f:
        f.write(output)
    print('Successfully saved output to file: %s' % (output_file_name))

def parse_file_name():
    parser = argparse.ArgumentParser()
    parser.add_argument('file_name', help='Path to CSV file of ledger', default='empty_string')
    args = parser.parse_args()

    if args.file_name == 'empty_string':
        print('Error: Missing path to CSV file!')
        return

    return args.file_name

if __name__ == '__main__':
    file_name = parse_file_name()
    if file_name is not None:
        get_output(file_name)